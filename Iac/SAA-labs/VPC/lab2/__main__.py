import pulumi
from pulumi_aws import ec2, s3, iam

# Crear una VPC
vpc = ec2.Vpc('mi-vpc',
    cidr_block='10.0.0.0/16',
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={'Name': 'mi-vpc'}
)

# Crear una subred pública
subnet = ec2.Subnet('subnet-publica',
    vpc_id=vpc.id,
    cidr_block='10.0.1.0/24',
    map_public_ip_on_launch=True,
    tags={'Name': 'subnet-publica'}
)

# Crear una gateway de Internet
igw = ec2.InternetGateway('internet-gateway',
    vpc_id=vpc.id,
    tags={'Name': 'internet-gateway'}
)

# Crear una tabla de rutas para la subred pública
route_table = ec2.RouteTable('tabla-rutas',
    vpc_id=vpc.id,
    routes=[{
        'cidr_block': '0.0.0.0/0',
        'gateway_id': igw.id,
    }],
    tags={'Name': 'tabla-rutas'}
)

# Asociar la tabla de rutas con la subred pública
route_table_association = ec2.RouteTableAssociation('asociacion-tabla-rutas',
    subnet_id=subnet.id,
    route_table_id=route_table.id
)

# Crear un bucket de S3 para almacenar los VPC Flow Logs
flow_logs_bucket = s3.Bucket('bucket-flow-logs',
    acl='private',
    tags={'Name': 'bucket-flow-logs'}
)

security_group = ec2.SecurityGroup('grupo-seguridad',
    vpc_id=vpc.id,
    description='permitir trafico SSH y HTTP',
    ingress=[
        {
            'protocol': 'tcp',
            'from_port': 22,
            'to_port': 22,
            'cidr_blocks': ['0.0.0.0/0'],
        },
        {
            'protocol': 'tcp',
            'from_port': 80,
            'to_port': 80,
            'cidr_blocks': ['0.0.0.0/0'],
        },
    ],
    egress=[
        {
            'protocol': '-1',
            'from_port': 0,
            'to_port': 0,
            'cidr_blocks': ['0.0.0.0/0'],
        },
    ],
    tags={'Name': 'grupo-seguridad'}
)

# Crear una instancia EC2
ami = ec2.get_ami(most_recent=True,
    owners=['amazon'],
    filters=[{'name': 'name', 'values': ['amzn2-ami-hvm-*-x86_64-gp2']}]
)

instance = ec2.Instance('mi-instancia',
    instance_type='t2.micro',
    vpc_security_group_ids=[security_group.id],
    subnet_id=subnet.id,
    ami=ami.id,
    key_name='test3',
    tags={'Name': 'mi-instancia'}
)

# Crear una Network ACL
network_acl = ec2.NetworkAcl('network-acl',
    vpc_id=vpc.id,
    tags={'Name': 'network-acl'}
)

# Reglas de entrada para la Network ACL
network_acl_ingress = ec2.NetworkAclRule('regla-ingreso',
    network_acl_id=network_acl.id,
    rule_number=100,
    egress=False,
    protocol='-1',
    rule_action='allow',
    cidr_block='0.0.0.0/0',
    from_port=0,
    to_port=0
)

# Reglas de salida para la Network ACL
network_acl_egress = ec2.NetworkAclRule('regla-salida',
    network_acl_id=network_acl.id,
    rule_number=100,
    egress=True,
    protocol='-1',
    rule_action='allow',
    cidr_block='0.0.0.0/0',
    from_port=0,
    to_port=0
)


# Asociar la Network ACL con la subred
subnet_network_acl_association = ec2.NetworkAclAssociation('asociacion-network-acl',
    subnet_id=subnet.id,
    network_acl_id=network_acl.id
)

# Crear un rol de IAM para los VPC Flow Logs
flow_logs_role = iam.Role('rol-flow-logs',
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "vpc-flow-logs.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    }"""
)

# Adjuntar la política necesaria al rol de IAM
flow_logs_policy_attachment = iam.RolePolicyAttachment('adjunto-politica-flow-logs',
    role=flow_logs_role.name,
    policy_arn='arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs'
)

# Crear los VPC Flow Logs
flow_log = ec2.FlowLog('vpc-flow-log',
    vpc_id=vpc.id,
    traffic_type='ALL',
    log_destination=flow_logs_bucket.arn,
    iam_role_arn=flow_logs_role.arn
)

# Exportar las salidas necesarias
pulumi.export('vpc_id', vpc.id)
pulumi.export('subnet_id', subnet.id)
pulumi.export('instance_id', instance.id)
pulumi.export('flow_logs_bucket', flow_logs_bucket.bucket)
