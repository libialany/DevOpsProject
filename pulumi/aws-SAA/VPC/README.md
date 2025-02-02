
## Project

### Projec 1 - Bastion Mysql Ec2
    Infrastructuere:
        - 1 VPC (10.10.0.0/16)
        - 1 public(10.10.10/24)
        - 2 private subnet (10.10.2.0/24)[Ec2]- (10.10.3.0/24)[RDS MySQL database].
    Sumary: fix the routes.
    importantes notes:
        - RDS security group inbound rule is incorrectly configured with 10.10.1.0/24 instead of 10.10.2.0/24.
        - 10.10.3.0/24 subnet's NACL denies inbound on port 3306 from subnet 10.10.2.0/24
[lab1-Bastion](./lab1)

[example](https://github.com/tapanhegde26/pulumi-aws-infra-bastion-host/blob/main/__main__.py)


    ```
    ssh -i <private-key.pem> -L 3306:<db-endpoint>:3306 ec2-user@<bastion-host-public-ip>
    ssh -i test3.pem -L 3306:my-db-instancef5e204a.cblmbbid3my4.us-east-1.rds.amazonaws.com:3306 ec2-user@3.228.10.252
    ```


### Projec 2 - VPC Flow Logs

    AWS Services used: EC2, S3, VPC
    Summary: Set up VPC Flow Logs, analyze traffic, and manage inbound traffic using network access control lists.

[lab2](./lab2) 

### Project 3 - VPC Endpoints 

[VPC Endpoints - Gateways - S3](./GElab3)

### sources:

[vpc](https://tutorialsdojo.com/amazon-vpc/)
[bastion](https://jayendrapatil.com/aws-bastion-host/)
[Gateways](https://medium.com/@cse.20bcsd64/vpc-endpoint-setup-for-s3-bucket-b366a9ec0ec0)
[Gateways Part2](https://blog.scottlowe.org/2020/01/25/creating-aws-vpc-endpoint-with-pulumi/)