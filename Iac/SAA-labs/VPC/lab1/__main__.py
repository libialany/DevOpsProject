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

# Crear un grupo de seguridad
security_group = ec2.SecurityGroup('grupo-seguridad',
    vpc_id=vpc.id,
    description='Permitir tráfico SSH y HTTP',
    ingress=[
        {
            'protocol': 'tcp',
            'from_port': 22,
            'to_port': 22,
            'cidr_blocks': ['0.0.0.0/0'],
            'description': 'Permitir acceso SSH desde cualquier IP',
        },
        {
            'protocol': 'tcp',
            'from_port': 80,
            'to_port': 80,
            'cidr_blocks': ['0.0.0.0/0'],
            'description': 'Permitir tráfico HTTP desde cualquier IP',
        },
    ],
    egress=[
        {
            'protocol': '-1',
            'from_port': 0,
            'to_port': 0,
            'cidr_blocks': ['0.0.0.0/0'],
            'description': 'Permitir todo el tráfico de salida',
        },
    ],
    tags={'Name': 'grupo-seguridad'}
)

# Crear una clave SSH
key_pair = ec2.KeyPair('clave-ssh',
    public_key='TU_LLAVE_PUBLICA_AQUI',  # Sustituye esto con tu clave pública SSH
    tags={'Name': 'clave-ssh'}
)

# Obtener una AMI (Amazon Linux 2)
ami = ec2.get_ami(most_recent=True,
    owners=['amazon'],
    filters=[{'name': 'name', 'values': ['amzn2-ami-hvm-*-x86_64-gp2']}]
)

# Crear una instancia EC2
instance = ec2.Instance('mi-instancia',
    instance_type='t2.micro',
    vpc_security_group_ids=[security_group.id],
    subnet_id=subnet.id,
    ami=ami.id,
    key_name=key_pair.key_name,
    tags={'Name': 'mi-instancia'},
    user_data="""#!/bin/bash
    yum update -y
    yum install -y httpd
    systemctl start httpd
    systemctl enable httpd
    echo "Hola, esta es mi instancia EC2 configurada con Pulumi" > /var/www/html/index.html
    """
)

# Exportar las salidas necesarias
pulumi.export('vpc_id', vpc.id)
pulumi.export('subnet_id', subnet.id)
pulumi.export('instance_id', instance.id)
pulumi.export('security_group_id', security_group.id)
pulumi.export('key_pair_name', key_pair.key_name)
