import aws_cdk as core
import aws_cdk.assertions as assertions

from hello_lambda.hello_lambda_stack import HelloLambdaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in hello_lambda/hello_lambda_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HelloLambdaStack(app, "hello-lambda")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
