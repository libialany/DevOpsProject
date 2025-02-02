# import pulumi
# import pulumi_aws as aws

# config = pulumi.Config()
# stage_name = config.get("stageName")
# if stage_name is None:
#     stage_name = "example"
# example = aws.apigateway.RestApi("example")
# example_log_group = aws.cloudwatch.LogGroup("example",
#     name=example.id.apply(lambda id: f"API-Gateway-Execution-Logs_{id}/{stage_name}"),
#     retention_in_days=7)
# example_stage = aws.apigateway.Stage("example", stage_name=stage_name,opts = pulumi.ResourceOptions(depends_on=[example_log_group]))

import pulumi
import pulumi_aws as aws

# Configuración del nombre de la etapa
config = pulumi.Config()
stage_name = config.get("stageName") or "example"

# Creación de la API REST en API Gateway
example_api = aws.apigateway.RestApi(
    "exampleApi",
    name="example-api",
    description="API de ejemplo creada con Pulumi"
)

# Creación del grupo de logs en CloudWatch para la API Gateway
example_log_group = aws.cloudwatch.LogGroup(
    "exampleLogGroup",
    name=example_api.id.apply(lambda id: f"API-Gateway-Execution-Logs_{id}/{stage_name}"),
    retention_in_days=7
)

# Creación de la etapa de despliegue en API Gateway
example_deployment = aws.apigateway.Deployment(
    "exampleDeployment",
    rest_api=example_api.id,
    description="Despliegue inicial de la API de ejemplo",
    opts=pulumi.ResourceOptions(depends_on=[example_log_group])
)

# Configuración de la etapa de la API Gateway
example_stage = aws.apigateway.Stage(
    "exampleStage",
    rest_api=example_api.id,
    deployment=example_deployment.id,
    stage_name=stage_name,
    access_log_settings=aws.apigateway.StageAccessLogSettingsArgs(
        destination_arn=example_log_group.arn,
        format='{"requestId":"$context.requestId","ip":"$context.identity.sourceIp","caller":"$context.identity.caller","user":"$context.identity.user","requestTime":"$context.requestTime","httpMethod":"$context.httpMethod","resourcePath":"$context.resourcePath","status":"$context.status","protocol":"$context.protocol","responseLength":"$context.responseLength"}'
    ),
    opts=pulumi.ResourceOptions(depends_on=[example_deployment])
)

# Exportar la URL de invocación de la API
pulumi.export("invoke_url", example_stage.invoke_url)
