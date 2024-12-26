import pulumi
import pulumi_aws as aws

# Define the Security Group for EC2 instance
security_group = aws.ec2.SecurityGroup("ec2-sg",
    description="Allow HTTP and SSH",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],  # SSH from anywhere
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],  # HTTP from anywhere
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",  # Allow all outbound traffic
            cidr_blocks=["0.0.0.0/0"],
        ),
    ]
)

# Create the EC2 instance
ec2_instance = aws.ec2.Instance("my-web-server",
    ami="ami-0c55b159cbfafe1f0",  # Replace with your desired AMI ID
    instance_type="t2.micro",  # Change instance type if needed
    security_groups=[security_group.name],
    tags={"Name": "MyWebServer"},
)

# Create an S3 Bucket
bucket = aws.s3.Bucket("my-bucket",
    website={
        "index_document": "index.html",
        "not_found_document": "404.html",
    },
    tags={
        "Name": "MyBucket",
        "Environment": "Dev",
    }
)

# Export the S3 bucket name and website URL
pulumi.export("bucket_name", bucket.bucket)
pulumi.export("website_url", bucket.website_endpoint)
pulumi.export("public_ip", ec2_instance.public_ip)
