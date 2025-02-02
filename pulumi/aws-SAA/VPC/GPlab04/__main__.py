import pulumi
import pulumi_aws as aws
import json

# 1. Crear VPC
vpc = aws.ec2.Vpc(
    "my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={"Name": "my-vpc"}
)

# 2. Crear Internet Gateway (IGW) para permitir tráfico entrante/saliente en la subred pública
igw = aws.ec2.InternetGateway(
    "my-igw",
    vpc_id=vpc.id,
    tags={"Name": "my-igw"}
)

# 3. Crear tabla de rutas y asociarle una ruta a 0.0.0.0/0
public_route_table = aws.ec2.RouteTable(
    "myPublicRouteTable",
    vpc_id=vpc.id,
    tags={"Name": "my-public-route-table"},
)

public_route = aws.ec2.Route(
    "myPublicRoute",
    route_table_id=public_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw.id
)

# 4. Crear subred pública y privada
public_subnet = aws.ec2.Subnet(
    "public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    availability_zone="us-east-1a",
    tags={"Name": "public-subnet"}
)

private_subnet = aws.ec2.Subnet(
    "private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    map_public_ip_on_launch=False,
    availability_zone="us-east-1b",
    tags={"Name": "private-subnet"}
)

# Asociar la subred pública a la tabla de rutas pública
public_subnet_rta = aws.ec2.RouteTableAssociation(
    "myPublicSubnetRouteAssoc",
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id
)

# 5. Crear tabla DynamoDB
dynamodb_table = aws.dynamodb.Table(
    "my-table",
    attributes=[{"name": "id", "type": "S"}],
    hash_key="id",
    billing_mode="PAY_PER_REQUEST",
    tags={"Name": "my-table"}
)

# 6. Crear endpoint de VPC para DynamoDB (Gateway endpoint)
dynamodb_vpc_endpoint = aws.ec2.VpcEndpoint(
    "dynamodb-vpc-endpoint",
    vpc_id=vpc.id,
    service_name="com.amazonaws.us-east-1.dynamodb",
    vpc_endpoint_type="Gateway",
    route_table_ids=[public_route_table.id],  # Se puede asignar también a otras RouteTables
    tags={"Name": "dynamodb-vpc-endpoint"}
)

# 7. Crear IAM Role y Policies para Lambda
lambda_role = aws.iam.Role(
    "lambda-exec-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Effect": "Allow"
        }]
    }),
    tags={"Name": "lambda-exec-role"}
)

# Adjuntar políticas
aws.iam.RolePolicyAttachment(
    "lambda-dynamodb-access",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
)

aws.iam.RolePolicyAttachment(
    "lambda-vpc-access",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
)

# 8. Crear Lambda (dentro de la subred privada para acceder a DynamoDB por Endpoint)
lambda_function = aws.lambda_.Function(
    "my-function",
    role=lambda_role.arn,
    runtime="python3.8",
    handler="lambda_function.lambda_handler",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda_code")  # Carpeta local con tu código
    }),
    vpc_config={
        # Nota: si tu Lambda necesita Internet, deberías crear un NAT y enrutar aquí.
        # Si solo necesita DynamoDB, basta con el VPC Endpoint.
        "subnet_ids": [private_subnet.id],
        # Usamos el security group por defecto de la VPC. 
        # En producción conviene crear uno específico para Lambda.
        "security_group_ids": [vpc.default_security_group_id]
    },
    environment={
        "variables": {
            "TABLE_NAME": dynamodb_table.name
        }
    },
    tags={"Name": "my-function"}
)

# 9. Crear API Gateway
api = aws.apigateway.RestApi(
    "my-api",
    description="API Gateway con Lambda y DynamoDB",
    tags={"Name": "my-api"}
)

# Crear recurso, por ejemplo /items
resource = aws.apigateway.Resource(
    "my-resource",
    rest_api=api.id,
    parent_id=api.root_resource_id,
    path_part="items"
)

# Crear método GET
method = aws.apigateway.Method(
    "my-method",
    rest_api=api.id,
    resource_id=resource.id,
    http_method="GET",
    authorization="NONE"
)

# Integración proxy con Lambda
integration = aws.apigateway.Integration(
    "my-integration",
    rest_api=api.id,
    resource_id=resource.id,
    http_method=method.http_method,
    integration_http_method="POST",
    type="AWS_PROXY",
    uri=lambda_function.invoke_arn
)

# 10. Crear Deployment y Stage
deployment = aws.apigateway.Deployment(
    "my-deployment",
    rest_api=api.id,
    opts=pulumi.ResourceOptions(depends_on=[integration])
)

stage = aws.apigateway.Stage(
    "my-stage",
    rest_api=api.id,
    deployment=deployment.id,
    stage_name="prod"
)

# 11. Dar permisos de invocación a API Gateway
lambda_permission = aws.lambda_.Permission(
    "apiGatewayPermission",
    action="lambda:InvokeFunction",
    function=lambda_function.arn,  # Mejor usar ARN que nombre
    principal="apigateway.amazonaws.com",
    source_arn=api.execution_arn.apply(lambda arn: f"{arn}/*/*")
    # O también podrías usar stage.invoke_url (convertido a ARN), etc.
)

# 12. Exportar la URL de la API
pulumi.export("api_url", stage.invoke_url.apply(
    lambda url: f"{url}/items"
))
