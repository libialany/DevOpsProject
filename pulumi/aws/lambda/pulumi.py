import pulumi
import pulumi_archive as archive
import pulumi_aws as aws

assume_role = aws.iam.get_policy_document(statements=[{
    "effect": "Allow",
    "principals": [{
        "type": "Service",
        "identifiers": ["lambda.amazonaws.com"],
    }],
    "actions": ["sts:AssumeRole"],
}])
iam_for_lambda = aws.iam.Role("iam_for_lambda",
    name="iam_for_lambda",
    assume_role_policy=assume_role.json)
lambda_ = archive.get_file(type="zip",
    source_file="lambda.js",
    output_path="lambda_function_payload.zip")
test_lambda = aws.lambda_.Function("test_lambda",
    code=pulumi.FileArchive("lambda_function_payload.zip"),
    name="lambda_function_name",
    role=iam_for_lambda.arn,
    handler="index.test",
    source_code_hash=lambda_.output_base64sha256,
    runtime=aws.lambda_.Runtime.NODE_JS18D_X,
    environment={
        "variables": {
            "foo": "bar",
        },
    })
