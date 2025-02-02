
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