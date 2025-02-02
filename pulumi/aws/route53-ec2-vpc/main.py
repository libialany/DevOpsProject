import pulumi
import pulumi_aws as aws

# 1. Create a Private Hosted Zone
zone = aws.route53.Zone("my-private-zone",
    name="example.com.",  # Domain name (must end with a dot)
    vpc_ids=["vpc-xxxxxxxx"],  # VPC ID where the private hosted zone will be used
    comment="Private hosted zone for example.com"
)

# 2. Create an EC2 instance to represent the web server (optional, for demo purposes)
# Note: You may already have a web server running in your VPC

# Create a security group to allow HTTP access
sg = aws.ec2.SecurityGroup("web-sg",
    description="Allow HTTP access",
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=80,
        to_port=80,
        cidr_blocks=["0.0.0.0/0"],
    )]
)

# Launch an EC2 instance (just for demonstration purposes)
instance = aws.ec2.Instance("web-server",
    ami="ami-xxxxxxxx",  # Replace with a valid AMI ID
    instance_type="t2.micro",
    security_groups=[sg.name],
    tags={"Name": "WebServer"}
)

# 3. Create a Route 53 A record for the web server
a_record = aws.route53.Record("web-server-record",
    zone_id=zone.id,
    name="web.example.com.",  # The subdomain (e.g., web.example.com)
    type="A",
    ttl=300,
    records=[instance.public_ip],  # Point the A record to the EC2 instance's public IP
)

# Export the web server's public IP and the A record's domain name
pulumi.export("web_server_ip", instance.public_ip)
pulumi.export("web_server_url", a_record.fqdn)
