import pulumi
import pulumi_aws as aws

# Step 1: Create an EFS File System
file_system = aws.efs.FileSystem("efs-file-system", 
    lifecycle_policies=[{
        "transition_to_ia": "AFTER_30_DAYS",
    }],
    tags={
        "Name": "MyEFSFileSystem",
    }
)

# Step 2: Create an EFS Access Point
access_point = aws.efs.AccessPoint("efs-access-point", 
    file_system_id=file_system.id,
    root_directory={
        "path": "/lambda",  # Path under which the Lambda will store data
        "creation_info": {
            "owner_uid": 1001,
            "owner_gid": 1001,
            "permissions": "750",
        },
    }
)

# Step 3: Create an IAM Role for Lambda
lambda_role = aws.iam.Role("lambda-role", 
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            }
        }]
    }"""
)

# Attach the AmazonElasticFileSystemClientFullAccess policy to the Lambda role
aws.iam.RolePolicyAttachment("lambda-efs-policy",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/AmazonElasticFileSystemClientFullAccess"
)

# Step 4: Create Lambda Function with EFS Access
lambda_function = aws.lambda_.Function("lambda-efs",
    runtime="python3.8",  # Python runtime for Lambda
    role=lambda_role.arn,
    handler="index.get_text",
    code=pulumi.FileArchive("lambda_function.zip"),
    file_system_configs=[{
        "arn": access_point.arn,
        "local_mount_path": "/mnt/text"  # Mount path to Lambda's local file system
    }]
)

# Step 5: Create the API Gateway HTTP API
api = aws.apigatewayv2.Api("lambda-api", 
    protocol_type="HTTP",
    description="API Gateway for Lambda function"
)

# Step 6: Create the route and integration
route = aws.apigatewayv2.Route("lambda-route", 
    api_id=api.id,
    route_key="GET /invoke",
    target=f"integrations/{lambda_function.name}"
)

# Step 7: Create the Lambda integration for API Gateway
integration = aws.apigatewayv2.Integration("lambda-integration",
    api_id=api.id,
    integration_type="AWS_PROXY",
    integration_uri=lambda_function.arn,
    payload_format_version="2.0"
)

# Step 8: Grant permission for API Gateway to invoke Lambda
aws.lambda_.Permission("api-gateway-invoke",
    action="lambda:InvokeFunction",
    function=lambda_function.name,
    principal="apigateway.amazonaws.com"
)

# Step 9: Output the API Gateway URL
pulumi.export("api_url", api.api_endpoint)
