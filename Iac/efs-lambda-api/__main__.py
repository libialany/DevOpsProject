# import pulumi
# import pulumi_aws as aws

# # Step 1: Create an EFS File System
# file_system = aws.efs.FileSystem("efs-file-system", 
#     lifecycle_policies=[{
#         "transition_to_ia": "AFTER_30_DAYS",
#     }],
#     tags={
#         "Name": "MyEFSFileSystem",
#     }
# )

# # Step 2: Create an EFS Access Point
# access_point = aws.efs.AccessPoint("efs-access-point", 
#     file_system_id=file_system.id,
#     root_directory={
#         "path": "/lambda",  # Path under which the Lambda will store data
#         "creation_info": {
#             "owner_uid": 1001,
#             "owner_gid": 1001,
#             "permissions": "750",
#         },
#     }
# )

# # Step 3: Create an IAM Role for Lambda
# lambda_role = aws.iam.Role("lambda-role", 
#     assume_role_policy="""{
#         "Version": "2012-10-17",
#         "Statement": [{
#             "Action": "sts:AssumeRole",
#             "Effect": "Allow",
#             "Principal": {
#                 "Service": "lambda.amazonaws.com"
#             }
#         }]
#     }"""
# )

# # Attach the AmazonElasticFileSystemClientFullAccess policy to the Lambda role
# aws.iam.RolePolicyAttachment("lambda-efs-policy",
#     role=lambda_role.name,
#     policy_arn="arn:aws:iam::aws:policy/AmazonElasticFileSystemClientFullAccess"
# )

# # Step 4: Create Lambda Function with EFS Access
# lambda_function = aws.lambda_.Function("lambda-efs",
#     runtime="python3.8",  # Python runtime for Lambda
#     role=lambda_role.arn,
#     handler="index.get_text",
#     code=pulumi.FileArchive("lambda_function.zip"),
#     file_system_config={
#         "arn": access_point.arn,
#         "local_mount_path": "/mnt/text"  # Mount path to Lambda's local file system
#     }
# )

# # Step 5: Create the API Gateway HTTP API
# api = aws.apigatewayv2.Api("lambda-api", 
#     protocol_type="HTTP",
#     description="API Gateway for Lambda function"
# )

# # Step 6: Create the route and integration
# route = aws.apigatewayv2.Route("lambda-route", 
#     api_id=api.id,
#     route_key="GET /invoke",
#     target=lambda_function.name.apply(lambda name: f"integrations/{name}")  #
# )

# # Step 7: Create the Lambda integration for API Gateway
# integration = aws.apigatewayv2.Integration("lambda-integration",
#     api_id=api.id,
#     integration_type="AWS_PROXY",
#     integration_uri=lambda_function.arn,
#     payload_format_version="2.0"
# )

# # Step 8: Grant permission for API Gateway to invoke Lambda
# aws.lambda_.Permission("api-gateway-invoke",
#     action="lambda:InvokeFunction",
#     function=lambda_function.name,
#     principal="apigateway.amazonaws.com"
# )

# # Step 9: Output the API Gateway URL
# pulumi.export("api_url", api.api_endpoint)


import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx
import os

# Create a VPC
vpc = awsx.ec2.Vpc("vpc", subnets=[{"type": "private"}, {"type": "public"}])
subnet_ids = vpc.public_subnet_ids

# Create an EFS filesystem
filesystem = aws.efs.FileSystem("filesystem")
targets = []

# Create mount targets for each public subnet
for i in range(len(subnet_ids)):
    targets.append(aws.efs.MountTarget(f"fs-mount-{i}", 
        file_system_id=filesystem.id,
        subnet_id=subnet_ids[i],
        security_groups=[vpc.vpc.default_security_group_id],
    ))

# Create an EFS access point
ap = aws.efs.AccessPoint("ap", 
    file_system_id=filesystem.id,
    posix_user={"uid": 1000, "gid": 1000},
    root_directory={"path": "/www", "creation_info": {"owner_gid": 1000, "owner_uid": 1000, "permissions": "755"}},
    opts=pulumi.ResourceOptions(depends_on=targets)
)

# Define the Lambda function callback
def efsvpc_callback(name: str, f: aws.lambda_.Callback) -> aws.lambda_.CallbackFunction:
    return aws.lambda_.CallbackFunction(name,
        policies=[
            aws.iam.ManagedPolicy.AWS_LAMBDA_VPC_ACCESS_EXECUTION_ROLE,
            aws.iam.ManagedPolicy.LAMBDA_FULL_ACCESS,
        ],
        vpc_config={
            "subnet_ids": vpc.private_subnet_ids,
            "security_group_ids": [vpc.vpc.default_security_group_id],
        },
        file_system_config={"arn": ap.arn, "local_mount_path": "/mnt/storage"},
        callback=f,
    )

# Create the API Gateway
api = awsx.apigateway.API("api", routes=[
    {
        "method": "GET",
        "path": "/files/{filename+}",
        "event_handler": efsvpc_callback("getHandler", 
            lambda ev, ctx: {
                "statusCode": 200,
                "body": open(f"/mnt/storage/{ev['pathParameters']['filename']}", "r").read(),
            } if os.path.exists(f"/mnt/storage/{ev['pathParameters']['filename']}") else {
                "statusCode": 500,
                "body": ""
            }
        ),
    },
    {
        "method": "POST",
        "path": "/files/{filename+}",
        "event_handler": efsvpc_callback("uploadHandler", 
            lambda ev, ctx: {
                "statusCode": 200,
                "body": "",
            } if (open(f"/mnt/storage/{ev['pathParameters']['filename']}", "wb").write(base64.b64decode(ev['body']))) else {
                "statusCode": 500,
                "body": ""
            }
        ),
    },
])