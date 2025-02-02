import pulumi
import pulumi_aws as aws
# 2. Crear VPC
vpc = aws.ec2.Vpc("myVpc",
                  cidr_block="10.0.0.0/16",
                  enable_dns_support=True,
                  enable_dns_hostnames=True)

# Crear un Security Group para el ELB
elb_sg = aws.ec2.SecurityGroup('elb-sg',
vpc_id=vpc.id,
    description='Security group for ELB',
    ingress=[
        {'protocol': 'tcp', 'from_port': 80, 'to_port': 80, 'cidr_blocks': ['0.0.0.0/0']},
        {'protocol': 'tcp', 'from_port': 443, 'to_port': 443, 'cidr_blocks': ['0.0.0.0/0']}
    ],
    egress=[
        {'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0']}
    ]
)

# Crear el ELB
elb = aws.elb.LoadBalancer('my-elb',
    availability_zones=aws.get_availability_zones().names,
    listeners=[
        {'instance_port': 80, 'instance_protocol': 'HTTP', 'lb_port': 80, 'lb_protocol': 'HTTP'}
    ],
    health_check={
        'target': 'HTTP:80/',
        'interval': 30,
        'timeout': 5,
        'healthy_threshold': 2,
        'unhealthy_threshold': 2
    },
    security_groups=[elb_sg.id]
)

# # Crear una zona hospedada en Route 53
# zone = aws.route53.Zone('my-zone',
#     name='example.com'
# )

# # Crear un registro DNS que apunte al ELB
# record = aws.route53.Record('my-record',
#     zone_id=zone.id,
#     name='www.example.com',
#     type='A',
#     aliases=[{
#         'name': elb.dns_name,
#         'zone_id': elb.zone_id,
#         'evaluate_target_health': True
#     }]
# )
