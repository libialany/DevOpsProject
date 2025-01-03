import json
import pulumi
from pulumi import ResourceOptions, export
import pulumi_aws as aws

# Crear VPC
vpc = aws.ec2.Vpc("myVpc",
                  cidr_block="10.0.0.0/16",
                  enable_dns_support=True,
                  enable_dns_hostnames=True,
                  tags={"Name": "myVpc", "Environment": "Development"})

# Crear subnets públicas en diferentes zonas de disponibilidad
public_subnet1 = aws.ec2.Subnet("publicSubnet1",
                                vpc_id=vpc.id,
                                cidr_block="10.0.0.0/24",
                                availability_zone="us-east-1a",
                                tags={"Name": "publicSubnet1", "Zone": "us-east-1a"})

public_subnet2 = aws.ec2.Subnet("publicSubnet2",
                                vpc_id=vpc.id,
                                cidr_block="10.0.1.0/24",
                                availability_zone="us-east-1b",
                                tags={"Name": "publicSubnet2", "Zone": "us-east-1b"})

# Crear una gateway de internet y asociarla con la VPC
internet_gateway = aws.ec2.InternetGateway("internetGateway",
                                           vpc_id=vpc.id,
                                           tags={"Name": "internetGateway"})

# Crear una tabla de rutas para las subnets públicas
route_table = aws.ec2.RouteTable("routeTable",
                                 vpc_id=vpc.id,
                                 routes=[{
                                     "cidr_block": "0.0.0.0/0",
                                     "gateway_id": internet_gateway.id,
                                 }],
                                 tags={"Name": "publicRouteTable"})

# Asociar la tabla de rutas con las subnets públicas
route_table_association1 = aws.ec2.RouteTableAssociation("routeTableAssociation1",
                                                         subnet_id=public_subnet1.id,
                                                         route_table_id=route_table.id)

route_table_association2 = aws.ec2.RouteTableAssociation("routeTableAssociation2",
                                                         subnet_id=public_subnet2.id,
                                                         route_table_id=route_table.id)

# Crear un grupo de seguridad para permitir tráfico HTTP
security_group = aws.ec2.SecurityGroup("webSecurityGroup",
                                       vpc_id=vpc.id,
                                       description="Enable HTTP access",
                                       ingress=[{
                                           "protocol": "tcp",
                                           "from_port": 80,
                                           "to_port": 80,
                                           "cidr_blocks": ["0.0.0.0/0"],
                                       }],
                                       egress=[{
                                           "protocol": "-1",
                                           "from_port": 0,
                                           "to_port": 0,
                                           "cidr_blocks": ["0.0.0.0/0"],
                                       }],
                                       tags={"Name": "webSecurityGroup", "Purpose": "HTTP Access"})

# Crear un balanceador de carga (ALB)
alb = aws.lb.LoadBalancer("appLoadBalancer",
                          security_groups=[security_group.id],
                          subnets=[public_subnet1.id, public_subnet2.id],
                          tags={"Name": "appLoadBalancer", "Environment": "Development"})

# Crear un grupo de destino para el ALB
target_group = aws.lb.TargetGroup("appTargetGroup",
                                  port=80,
                                  protocol="HTTP",
                                  target_type="ip",
                                  vpc_id=vpc.id,
                                  health_check={
                                      "path": "/health",
                                      "port": "80",
                                      "protocol": "HTTP"
                                  },
                                  tags={"Name": "appTargetGroup"})

# Crear un listener para el ALB
listener = aws.lb.Listener("appListener",
                           load_balancer_arn=alb.arn,
                           port=80,
                           default_actions=[{
                               "type": "forward",
                               "target_group_arn": target_group.arn,
                           }],
                           tags={"Name": "appListener"})

# Crear un rol de IAM para la ejecución de tareas de ECS
task_execution_role = aws.iam.Role("taskExecutionRole",
                                   assume_role_policy=json.dumps({
                                       "Version": "2012-10-17",
                                       "Statement": [{
                                           "Effect": "Allow",
                                           "Principal": {
                                               "Service": "ecs-tasks.amazonaws.com"
                                           },
                                           "Action": "sts:AssumeRole"
                                       }]
                                   }),
                                   tags={"Name": "taskExecutionRole", "Environment": "Development"})

# Adjuntar la política necesaria al rol de ejecución
task_execution_role_policy_attachment = aws.iam.RolePolicyAttachment("taskExecutionRolePolicyAttachment",
                                                                     role=task_execution_role.name,
                                                                     policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy")

# Crear una definición de tarea para ECS
task_definition = aws.ecs.TaskDefinition("appTaskDefinition",
                                         family="fargate-task-definition",
                                         cpu="256",
                                         memory="512",
                                         network_mode="awsvpc",
                                         requires_compatibilities=["FARGATE"],
                                         execution_role_arn=task_execution_role.arn,
                                         container_definitions=json.dumps([{
                                             "name": "myAppContainer",
                                             "image": "nginx",
                                             "portMappings": [{
                                                 "containerPort": 80,
                                                 "protocol": "tcp"
                                             }]
                                         }]),
                                         tags={"Name": "appTaskDefinition"})

# Crear un clúster de ECS
ecs_cluster = aws.ecs.Cluster("appEcsCluster",
                              tags={"Name": "appEcsCluster", "Environment": "Development"})

# Crear un servicio de ECS para ejecutar las tareas
ecs_service = aws.ecs.Service("appEcsService",
                              cluster=ecs_cluster.arn,
                              desired_count=3,
                              launch_type="FARGATE",
                              task_definition=task_definition.arn,
                              network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
                                  assign_public_ip=True,
                                  subnets=[public_subnet1.id, public_subnet2.id],
                                  security_groups=[security_group.id]
                              ),
                              load_balancers=[aws.ecs.ServiceLoadBalancerArgs(
                                  target_group_arn=target_group.arn,
                                  container_name="myAppContainer",
                                  container_port=80
                              )],
                              opts=ResourceOptions(depends_on=[listener]),
                              tags={"Name": "appEcsService"})

# Exportar la URL del balanceador de carga y detalles adicionales
export("alb_url", alb.dns_name)
export("subnet1_id", public_subnet1.id)
export("subnet2_id", public_subnet2.id)
