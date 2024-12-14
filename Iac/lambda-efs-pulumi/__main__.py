import pulumi
import pulumi_aws as aws
vpc_id = ""
subnet_id = ""
efs_id = ""
security_group_ids = []

# EFS access point used by lambda file system
access_point_for_lambda = aws.efs.AccessPoint("access_point_for_lambda",
    file_system_id=efs_id,
    root_directory={
        "path": "/lambda",
        "creation_info": {
            "owner_gid": 1000,
            "owner_uid": 1000,
            "permissions": "777",
        },
    },
    posix_user={
        "gid": 1000,
        "uid": 1000,
    })
# 4. Create IAM Role for Lambda with necessary permissions
lambda_role = aws.iam.Role("lambda-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    }"""
)

# Attach policy for EFS access to Lambda role
lambda_role_policy_attachment = aws.iam.RolePolicyAttachment("le-lambda-policy-attachment",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)

efs_policy_attachment = aws.iam.RolePolicyAttachment("le-efs-policy-attachment",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/AmazonElasticFileSystemFullAccess"
)

# A lambda function connected to an EFS file system
efs_lambda = aws.lambda_.Function("lambda_efs",
    runtime="python3.13",
    role=lambda_role.arn,
    handler="index.handler",  # Assuming you have index.py with a handler method
    code=pulumi.FileArchive("lambda_function_payload.zip"),
    file_system_config={
        "arn": access_point_for_lambda.arn,
        "local_mount_path": "/mnt/efs",
    },
    vpc_config={
        "subnet_ids": [subnet_id],
        "security_group_ids": security_group_ids,
    })
# Outputs
pulumi.export("access_point_id", access_point_for_lambda.arn)
pulumi.export("lambda_id", efs_lambda.id)