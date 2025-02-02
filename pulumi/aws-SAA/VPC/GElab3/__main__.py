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
# 

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
###
# Create an S3 bucket
my_s3_bucket = aws.s3.Bucket("my-test-s3",
    acl="private"  # Set ACL as needed
)

s3_gateway_endpoint = aws.ec2.VpcEndpoint("s3-gateway-endpoint",
    vpc_id=vpc.id,
    service_name="com.amazonaws.us-east-1.s3",  # Change region as needed
    route_table_ids=[route_table.id]
)
# -----------------------------------------------------------------------------
# 12. Exports (valores útiles)
# -----------------------------------------------------------------------------
pulumi.export("vpcId", vpc.id)
pulumi.export("publicSubnetId", public_subnet.id)
pulumi.export("ec2InstanceId", ec2_instance.id)
pulumi.export("ec2InstancePublicIp", ec2_instance.public_ip)
pulumi.export("s3bucketName", my_s3_bucket.id)













