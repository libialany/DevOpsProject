"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# Step 1: Create a VPC
vpc = aws.ec2.Vpc("efs-demo-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={"Name": "efs-demo-vpc"}
)

# Step 2: Create 2 Public Subnets
subnet1 = aws.ec2.Subnet("efs-demo-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
    map_public_ip_on_launch=True,
    tags={"Name": "efs-demo-subnet-1"}
)

subnet2 = aws.ec2.Subnet("efs-demo-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="us-east-1b",
    map_public_ip_on_launch=True,
    tags={"Name": "efs-demo-subnet-2"}
)


# Step 4: Create a Security Group for EC2 Instance
security_group = aws.ec2.SecurityGroup("efs-demo-ec2-sg",
    vpc_id=vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            from_port=22,
            to_port=22,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],  # Allow SSH from anywhere
        ),
        aws.ec2.SecurityGroupIngressArgs(
            from_port=80,
            to_port=80,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],  # Allow HTTP from anywhere
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            from_port=0,
            to_port=0,
            protocol="-1",  # Allow all outbound traffic
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
)
efs_security_group = aws.ec2.SecurityGroup("efs-sg",
    vpc_id=vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            from_port=2049,
            to_port=2049,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],  # Allow NFS traffic from anywhere (or restrict to EC2's IP range)
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            from_port=0,
            to_port=0,
            protocol="-1",  # Allow all outbound traffic
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
)
# Step 5: Create EC2 Instance with SSH Key
key_name = "test1"  # Replace with your existing SSH key name
ami_id = "ami-0453ec754f44f9a4a"  # Replace with a valid AMI for your region (e.g., Amazon Linux 2)

# Step 6: Create Elastic File System (EFS)
efs = aws.efs.FileSystem("efs-demo-efs",
    creation_token="efs-demo-efs-token",
    performance_mode="generalPurpose",
    tags={"Name": "efs-demo-efs"}
)

# Step 7: Create Mount Target for EFS in Subnet 1
mount_target = aws.efs.MountTarget("efs-mount-target",
    file_system_id=efs.id,
    subnet_id=subnet1.id,
    security_groups=[security_group.id, efs_security_group.id]
)

# Step 8: User Data to Mount EFS on EC2 Instance
mount_efs_script = """
#!/bin/bash
sudo yum install -y amazon-efs-utils
sudo mkdir /mnt/efs
"""

# Step 9: EC2 Instance with EFS Mounting via User Data
ec2_with_efs = aws.ec2.Instance("ec2-with-efs",
    ami=ami_id,
    instance_type="t2.micro",  # Replace with desired instance type
    subnet_id=subnet1.id,  # Place instance in subnet-1 (public subnet)
    vpc_security_group_ids=[security_group.id, efs_security_group.id],
    key_name=key_name,
    associate_public_ip_address=True,
    user_data=mount_efs_script,
    tags={"Name": "ec2-with-efs"}
)

# Outputs
pulumi.export("vpc_id", vpc.id)
pulumi.export("ec2_instance_id", ec2_with_efs.id)
pulumi.export("efs_id", efs.id)