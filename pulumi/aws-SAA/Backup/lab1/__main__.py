import pulumi
import pulumi_aws as aws

# -----------------------------------------------------------------------------
# 1. Crear la VPC personalizada
# -----------------------------------------------------------------------------
vpc = aws.ec2.Vpc(
    resource_name="myCustomVpc",
    cidr_block="10.0.0.0/16",
    tags={
        "Name": "myCustomVpc",
        "Environment": "Production"
    }
)

# -----------------------------------------------------------------------------
# 2. Crear el Internet Gateway
# -----------------------------------------------------------------------------
igw = aws.ec2.InternetGateway(
    resource_name="myInternetGateway",
    vpc_id=vpc.id,
    tags={
        "Name": "myInternetGateway"
    }
)

# -----------------------------------------------------------------------------
# 3. Crear la Subnet pública
# -----------------------------------------------------------------------------
public_subnet = aws.ec2.Subnet(
    resource_name="myPublicSubnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,  # Permite IP pública a las instancias
    tags={
        "Name": "myPublicSubnet"
    }
)

# -----------------------------------------------------------------------------
# 4. Crear la Route Table y asociarla a la Subnet pública
# -----------------------------------------------------------------------------
route_table = aws.ec2.RouteTable(
    resource_name="myRouteTable",
    vpc_id=vpc.id,
    tags={
        "Name": "myPublicRouteTable"
    }
)

# Ruta por defecto hacia Internet
public_route = aws.ec2.Route(
    resource_name="myDefaultRoute",
    route_table_id=route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw.id
)

# Asociar la ruta a la Subnet pública
route_table_assoc = aws.ec2.RouteTableAssociation(
    resource_name="myRouteTableAssociation",
    subnet_id=public_subnet.id,
    route_table_id=route_table.id
)

# -----------------------------------------------------------------------------
# 5. Crear un Security Group que permita SSH y HTTP
# -----------------------------------------------------------------------------
security_group = aws.ec2.SecurityGroup(
    resource_name="mySecurityGroup",
    vpc_id=vpc.id,
    description="SG para acceso SSH y HTTP",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]  # SSH abierto a Internet (¡ajusta para mayor seguridad!)
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"]  # HTTP abierto a Internet
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"]
        )
    ],
    tags={
        "Name": "mySecurityGroup"
    }
)
ami = aws.ec2.get_ami(most_recent=True,
                      owners=["amazon"],
                      filters=[{"name": "name", "values": ["amzn2-ami-hvm-*-x86_64-gp2"]}])

# -----------------------------------------------------------------------------
# 6. Crear la instancia EC2
# -----------------------------------------------------------------------------
ec2_instance = aws.ec2.Instance(
    resource_name="myEC2Instance",
    ami=ami.id,
    key_name="test3",
    instance_type="t2.micro",
    subnet_id=public_subnet.id,
    vpc_security_group_ids=[security_group.id],
    associate_public_ip_address=True,  # Asigna IP pública
    tags={
        "Name": "myEC2Instance",
        "Backup": "Daily",  # Etiqueta usada en el Backup Selection
        "Environment": "Production"
    }
)

# -----------------------------------------------------------------------------
# 7. Crear el Backup Vault
# -----------------------------------------------------------------------------
backup_vault = aws.backup.Vault(
    resource_name="myBackupVault",
    name="my-backup-vault",
    tags={
        "Environment": "Production"
    }
)

# -----------------------------------------------------------------------------
# 8. Definir la regla para el Backup Plan (respaldo diario a la 1 AM UTC)
# -----------------------------------------------------------------------------
backup_rule = {
    "ruleName": "daily-ebs-backups",
    "targetVaultName": backup_vault.name,
    "schedule": "cron(49 11 * * ? *)", 
    "lifecycle": {
        "deleteAfterDays": 7  # Retención de 7 días
    },
    "completionWindow": 120,  # ventana de finalización en minutos
    "startWindow": 60,        # ventana de inicio en minutos
    # copyActions, etc. si deseas respaldos cross-region
}

# -----------------------------------------------------------------------------
# 9. Crear el Backup Plan
# -----------------------------------------------------------------------------
backup_plan = aws.backup.Plan("myBackupPlan",
    name="my-backup-plan",
    # rules=[backup_rule]
    rules=[{
     "rule_name": "daily-ebs-backups",
    "target_vault_name": backup_vault.name,
    "schedule": "cron(0 1 * * ? *)",  # 1:00 AM UTC
    "lifecycle": {
        "delete_after": 7  # Retención de 7 días
    },
    }]
)

# -----------------------------------------------------------------------------
# 10. Crear la IAM Role para AWS Backup
# -----------------------------------------------------------------------------
backup_role = aws.iam.Role(
    resource_name="myBackupRole",
    assume_role_policy="""{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "backup.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }"""
)

# Política asociada que permite a AWS Backup manejar snapshots EBS
backup_policy = aws.iam.RolePolicy(
    resource_name="myBackupPolicy",
    role=backup_role.id,
    policy=pulumi.Output.all().apply(
        lambda _: """{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "ec2:DescribeVolumes",
                        "ec2:CreateSnapshot",
                        "ec2:DescribeVolumes",
                        "ec2:CreateSnapshot",
                        "ec2:DeleteSnapshot",
                        "ec2:DescribeSnapshots",
                        "ec2:CreateTags",
                        "ec2:DeleteTags",
                        "iam:PassRole",
                        "tag:GetResources",
                        "backup:DescribeBackupVault",
                        "backup:CopyIntoBackupVault"
                    ],
                    "Resource": "*"
                }
            ]
        }"""
    )
)

# -----------------------------------------------------------------------------
# 11. Seleccionar los volúmenes a respaldar mediante etiquetas
# -----------------------------------------------------------------------------
backup_selection = aws.backup.Selection(
    resource_name="myBackupSelection",
    name="my-backup-selection",
    plan_id=backup_plan.id,
    iam_role_arn=backup_role.arn,
    selection_tags=[
        {
            "type": "STRINGEQUALS",
            "key": "Backup",
            "value": "Daily"
        }
    ]
)

# -----------------------------------------------------------------------------
# 12. Exports (valores útiles)
# -----------------------------------------------------------------------------
pulumi.export("vpcId", vpc.id)
pulumi.export("publicSubnetId", public_subnet.id)
pulumi.export("ec2InstanceId", ec2_instance.id)
pulumi.export("ec2InstancePublicIp", ec2_instance.public_ip)
pulumi.export("backupVaultName", backup_vault.name)
pulumi.export("backupPlanName", backup_plan.name)














