"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc('my-vpc',
    cidr_block='10.0.0.0/16',
    enable_dns_support=True,
    enable_dns_hostnames=True
)

# Create a subnet within the VPC
subnet = aws.ec2.Subnet('my-subnet',
    vpc_id=vpc.id,
    cidr_block='10.0.1.0/24',
    availability_zone='us-east-1a',  # Specify the Availability Zone
    map_public_ip_on_launch=True
)

# Create another subnet in a different AZ (to make it a Multi-AZ setup)
subnet_2 = aws.ec2.Subnet('my-subnet-2',
    vpc_id=vpc.id,
    cidr_block='10.0.2.0/24',
    availability_zone='us-east-1b',  # Another AZ for high availability
    map_public_ip_on_launch=True
)

# Create a security group for the RDS instance
rds_security_group = aws.ec2.SecurityGroup('rds-sg',
    vpc_id=vpc.id,
    egress=[aws.ec2.SecurityGroupEgressArgs(
        cidr_blocks=['0.0.0.0/0'],
        protocol='-1',
        from_port=0,
        to_port=0
    )],
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        cidr_blocks=['0.0.0.0/0'],
        from_port=3306,  # MySQL port
        to_port=3306,
        protocol='tcp',
    )]
)

# Create an RDS DB Subnet Group (to be used by the RDS instance)
db_subnet_group = aws.rds.SubnetGroup('db-subnet-group',
    subnet_ids=[subnet.id, subnet_2.id]
)

# Create the Multi-AZ RDS Instance
rds_instance = aws.rds.Instance('multi-az-db',
    instance_class='db.t3.micro',  # Choose instance type based on your needs
    allocated_storage=20,  # Storage in GB
    engine='mysql',  # MySQL database engine (can change to others like postgres)
    engine_version="8.0",
    db_subnet_group_name=db_subnet_group.name,
    vpc_security_group_ids=[rds_security_group.id],
    multi_az=True,  # Enable Multi-AZ for high availability
    publicly_accessible=False,  # Change to True if the DB should be publicly accessible
    username='admin',
    password='password123',  # Replace with a stronger password
    db_name='mydatabase',
    storage_encrypted=True,  # Enable encryption for the storage
    tags={
        'Name': 'MultiAZ-RDS-Instance'
    }
)

# Export the RDS instance endpoint
pulumi.export('db_endpoint', rds_instance.endpoint)
pulumi.export('db_instance_id', rds_instance.id)
