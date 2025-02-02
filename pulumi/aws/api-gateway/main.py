import pulumi
import pulumi_aws as aws
from pulumi import ResourceOptions
import os

# Create an IAM role for Lambda function execution
role = aws.iam.Role("lambda-role",
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

# Create a Lambda function
lambda_function = aws.lambda_.Function("my-function",
    role=role.arn,
    runtime="python3.8",
    handler="lambda_function.handler",
    code=pulumi.FileArchive("./lambda_function.zip"),  # You can zip your function file
)

# Create an API Gateway REST API
api_gateway = aws.apigateway.RestApi("my-api",
    description="REST API for Lambda function"
)

# Create a resource (e.g., /hello)
resource = aws.apigateway.Resource("hello-resource",
    rest_api=api_gateway.id,
    parent_id=api_gateway.root_resource_id,
    path_part="hello"
)

# Create a method (e.g., GET) for the resource
method = aws.apigateway.Method("get-method",
    rest_api=api_gateway.id,
    resource_id=resource.id,
    http_method="GET",
    authorization="NONE",
)

# Integrate the Lambda function with the API method
integration = aws.apigateway.Integration("lambda-integration",
    rest_api=api_gateway.id,
    resource_id=resource.id,
    http_method=method.http_method,
    integration_http_method="POST",
    type="AWS_PROXY",
    uri=lambda_function.invoke_arn,
)

# Grant API Gateway permissions to invoke the Lambda function
lambda_permission = aws.lambda_.Permission("lambda-api-permission",
    action="lambda:InvokeFunction",
    function=lambda_function.name,
    principal="apigateway.amazonaws.com",
)

# Create a deployment for the API Gateway
deployment = aws.apigateway.Deployment("my-api-deployment",
    rest_api=api_gateway.id,
    stage_name="prod"
)

# Export the API Gateway URL
pulumi.export("api_url", deployment.invoke_url)
