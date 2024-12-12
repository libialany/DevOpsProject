"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# Step 1: Create a VPC
vpc = aws.ec2.Vpc('my-vpc-1',
    cidr_block='10.0.0.0/16',
    enable_dns_support=True,
    enable_dns_hostnames=True
)

# Step 2: Create subnets in two different availability zones for Multi-AZ support
subnet_1 = aws.ec2.Subnet('my-subnet-1b',
    vpc_id=vpc.id,
    cidr_block='10.0.1.0/24',
    availability_zone='us-east-1a',  # Specify Availability Zone 1
    map_public_ip_on_launch=True
)

subnet_2 = aws.ec2.Subnet('my-subnet-1b',
    vpc_id=vpc.id,
    cidr_block='10.0.2.0/24',
    availability_zone='us-east-1b',  # Specify Availability Zone 2
    map_public_ip_on_launch=True
)

# Step 3: Create a security group for the Aurora cluster
aurora_security_group = aws.ec2.SecurityGroup('aurora-sg',
    vpc_id=vpc.id,
    egress=[aws.ec2.SecurityGroupEgressArgs(
        cidr_blocks=['0.0.0.0/0'],
        protocol='-1',
    )],
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        cidr_blocks=['0.0.0.0/0'],
        from_port=3306,  # MySQL default port
        to_port=3306,
        protocol='tcp',
    )]
)

# Step 4: Create a DB Subnet Group for the Aurora Cluster
db_subnet_group = aws.rds.SubnetGroup('aurora-subnet-group01',
    subnet_ids=[subnet_1.id, subnet_2.id]
)

# Step 5: Create the Aurora DB Cluster (Multi-AZ)
aurora_cluster = aws.rds.Cluster('aurora-cluster-1',
    engine='aurora-mysql',  # Aurora MySQL compatible engine
    engine_version='5.7.mysql_aurora.2.10.2',
    master_username='admin',
    master_password='password123',  # Replace with a more secure password
    db_subnet_group_name=db_subnet_group.name,
    vpc_security_group_ids=[aurora_security_group.id],
    skip_final_snapshot=True,  # Skip the final snapshot on deletion (for demo purposes)
    backup_retention_period=7,  # Keep backups for 7 days
    multi_az=True,  # Enable Multi-AZ for high availability
    storage_encrypted=True,  # Enable storage encryption
    tags={
        'Name': 'Aurora-MultiAZ-Cluster'
    }
)

# Step 6: Create Aurora DB Instances (one for each AZ)
aurora_instance_1 = aws.rds.ClusterInstance('aurora-instance-1',
    cluster_identifier=aurora_cluster.id,
    instance_class='db.t3.small',  # Choose the instance class based on your needs
    engine='aurora-mysql',
    availability_zone='us-east-1a',  # The AZ of the first instance
    db_subnet_group_name=db_subnet_group.name,
    vpc_security_group_ids=[aurora_security_group.id],
    publicly_accessible=False  # Set to True if you want public access
)

aurora_instance_2 = aws.rds.ClusterInstance('aurora-instance-2',
    cluster_identifier=aurora_cluster.id,
    instance_class='db.t3.small',
    engine='aurora-mysql',
    availability_zone='us-east-1b',  # The AZ of the second instance
    db_subnet_group_name=db_subnet_group.name,
    vpc_security_group_ids=[aurora_security_group.id],
    publicly_accessible=False
)

# Step 7: Export the Cluster Endpoint and Instance Endpoints
pulumi.export('cluster_endpoint_01', aurora_cluster.endpoint)
pulumi.export('reader_endpoint_01', aurora_cluster.reader_endpoint)
pulumi.export('instance_1_endpoint_01', aurora_instance_1.endpoint)
pulumi.export('instance_2_endpoint_01', aurora_instance_2.endpoint)
