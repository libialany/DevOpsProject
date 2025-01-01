
## Project

### Projec 1
    Infrastructuere:
        - 1 VPC (10.10.0.0/16)
        - 1 public(10.10.10/24)
        - 2 private subnet (10.10.2.0/24)[Ec2]- (10.10.3.0/24)[RDS MySQL database].
    Sumary: fix the routes.
    importantes notes:
        - RDS security group inbound rule is incorrectly configured with 10.10.1.0/24 instead of 10.10.2.0/24.
        - 10.10.3.0/24 subnet's NACL denies inbound on port 3306 from subnet 10.10.2.0/24
    [lab1](./lab1)

### Projec 2

    AWS Services used: EC2, S3, VPC
    Summary: Set up VPC Flow Logs, analyze traffic, and manage inbound traffic using network access control lists.
    [lab2](./lab2) 



sources:
[vpc](https://tutorialsdojo.com/amazon-vpc/)
[bastion](https://jayendrapatil.com/aws-bastion-host/)