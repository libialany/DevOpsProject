What is AWS Cognito?
AWS Cognito is a service that helps you manage user authentication and access control for your applications. AWS Cognito is a scalable and secure identity management service that allows you to add user sign-up, sign-in, and access control to your web and mobile applications. It supports user authentication through various providers, including social identity providers (like Google, Facebook, and Amazon), SAML identity providers, and even your custom identity solutions.

Key Components of AWS Cognito
User Pools: These are user directories that provide sign-up and sign-in options. They manage the user’s profile and authentication flow.
Identity Pools: These allow you to grant users access to other AWS services. They provide temporary AWS credentials to users who authenticate via a user pool or other identity providers.
AWS Cognito Sync: This is a service that enables you to synchronize user data across multiple devices.

------

What is a VPC Endpoint?
- private connection to specific AWS services and VPC endpoint services through AWS PrivateLink. 
-  information in Amazon network

VPC and the service.

VPC endpoints are virtual devices that enable communication between instances in an Amazon VPC and various services. 
Scale horizontally, ensuring redundancy and high availability within the Amazon VPC.


Interface Endpoint – a group of elastic network interfaces (ENI) created by the VPC in the subnet you specify. Each ENI is assigned a private IP address and serves as the primary entry point for traffic directed to a supported service. Although these ENIs are visible in your account, they are managed by Amazon VPC, meaning you don’t have direct control over them. Interface endpoints incur costs per hour, along with additional charges for data processing.

Gateway Endpoint – functions similarly to an Internet Gateway but is specifically designed to route traffic within an Amazon VPC to a predefined prefix list. This prefix list contains IP ranges used by Amazon DynamoDB and Amazon S3. To enable this connectivity, you simply add a route in your VPC’s route table that directs traffic to the Gateway Endpoint, targeting the prefix list for Amazon S3 or DynamoDB. Unlike an Interface Endpoint, a Gateway Endpoint does not use AWS PrivateLink, and there are no additional charges for its use.

-----

Nat Gateway
https://medium.com/@shubhamchavan4554/mastering-private-subnet-connectivity-aws-nat-gateway-guide-a35ecfd30190

-----

Transit Gateway
AWS Transit Gateway connects VPCs and on-premises networks through a central hub. This simplifies your network and puts an end to complex peering relationships. It acts as a cloud router – each new connection is only made once.

-----

AWS DataSync

AWS DataSync Cheat Sheet
An online data transfer service that simplifies, automates, and accelerates copying large amounts of data to and from AWS storage services over the internet or AWS Direct Connect. 
DataSync can copy data between:
- Network File System (NFS) or Server Message Block (SMB) file servers, 
- Amazon Simple Storage Service (Amazon S3) buckets, 
- Amazon Elastic File System (Amazon EFS) file systems, 
- Amazon FSx for Windows File Server file systems

Deploy an agent – Deploy a DataSync agent and associate it to your AWS account via the Management Console or API. The agent will be used to access your NFS server or SMB file share to read data from it or write data to it.
Create a data transfer task – Create a task by specifying the location of your data source and destination, and any options you want to use to configure the transfer, such as the desired task schedule.
Start the transfer – Start the task and monitor data movement in the console or with Amazon CloudWatch.

-------
Database Migration Service

AWS Database Migration Service (AWS DMS) is a comprehensive cloud service designed to facilitate the migration of various types of databases, including relational databases, data warehouses, and NoSQL databases. Here are some key aspects and terminology associated with AWS DMS:
Overview of AWS DMS
Purpose: AWS DMS enables users to migrate data from on-premises or cloud-based data stores to the AWS Cloud or between different cloud environments. It supports migrations between the same database engines (e.g., Oracle to Oracle) and different engines (e.g., Oracle to PostgreSQL) as long as one endpoint is on AWS15.
Key Features:
Schema Conversion: Automatically assesses and converts database schemas to be compatible with the target database engine using the AWS Schema Conversion Tool (AWS SCT)12.
Fleet Advisor: Helps discover source data infrastructure and builds an inventory for migration planning1.
Replication Tasks: Users can perform one-time migrations or set up ongoing replication to keep source and target databases synchronized1.
Components of AWS DMS
An AWS DMS migration involves five essential components:
Database Discovery: Identifying databases suitable for migration.
Automatic Schema Conversion: Converting schemas from the source to the target format.
Replication Instance: A server that runs replication software to manage data transfer.
Source and Target Endpoints: Connections that define where data is extracted from and loaded into.
Replication Task: A defined process that specifies how data will be migrated2.
Migration Process
Setup: Users create a replication instance, configure source and target endpoints, and schedule replication tasks2.
Pay-as-you-go Model: AWS DMS operates on a cost-efficient model where users only pay for resources used during migration, avoiding upfront costs typical in traditional solutions1.
Best Practices
To optimize migrations using AWS DMS, consider the following best practices:
Conduct thorough planning before migration.
Utilize data validation during the process.
Monitor tasks using metrics and logs for troubleshooting4.
Supported Targets
AWS DMS can migrate data to various targets, including:
Amazon RDS instances
Amazon EC2 instances
On-premises databases
Other services like Amazon S3, Amazon Redshift, DynamoDB, and more6.
In summary, AWS Database Migration Service provides a robust framework for migrating diverse data stores efficiently while minimizing operational overhead through automation and cloud scalability.

-------
drift detection cloudformation
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html 
-------
AWS Resource manager
https://docs.aws.amazon.com/ram/latest/userguide/shareable.html#shareable-ec2 
-------
placement group
-------
como funciona aws inspector
