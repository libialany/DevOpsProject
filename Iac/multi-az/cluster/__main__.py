import pulumi
import pulumi_aws as aws
import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": "My Custom VPC"
    }
)

# Create Subnets in different Availability Zones
subnet1 = aws.ec2.Subnet("c-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",  # Specify your region's AZ
    map_public_ip_on_launch=True
)

subnet2 = aws.ec2.Subnet("c-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="us-east-1b",  # Different AZ
    map_public_ip_on_launch=True
)

security_group = aws.ec2.SecurityGroup("c-my-security-group",
    vpc_id=vpc.id,  # Important: associate with VPC
    description="Allow database access",
    
    # Ingress rules (incoming traffic)
    ingress=[{
        "from_port": 3306,  # MySQL port
        "to_port": 3306,
        "protocol": "tcp",
        "cidr_blocks": ["0.0.0.0/0"]  # Be more restrictive in production
    }],
    
    # Egress rules (outgoing traffic)
    egress=[{
        "from_port": 0,
        "to_port": 0,
        "protocol": "-1",  # All protocols
        "cidr_blocks": ["0.0.0.0/0"]
    }]
)
# Create a DB Subnet Group
subnet_group = aws.rds.SubnetGroup("my-c-subnet-group",
    subnet_ids=[subnet1.id, subnet2.id]
)
default = aws.rds.Cluster("default",
    cluster_identifier="aurora-cluster-demo",
    availability_zones=[
        "us-west-2a",
        "us-west-2b",
        "us-west-2c",
    ],
    database_name="mydb",
    master_username="foo",
    engine="mysql",  # Specify the exact engine
    engine_version="8.0", 
    vpc_security_group_ids=[security_group.id],
    db_subnet_group_name=subnet_group.name,
    master_password="barbut8chars")
cluster_instances = []
for range in [{"value": i} for i in range(0, 2)]:
    cluster_instances.append(aws.rds.ClusterInstance(f"cluster_instances-{range['value']}",
        identifier=f"aurora-cluster-demo-{range['value']}",
        cluster_identifier=default.id,
        instance_class=aws.rds.InstanceType.R4_LARGE,
        engine=default.engine,
        engine_version=default.engine_version))