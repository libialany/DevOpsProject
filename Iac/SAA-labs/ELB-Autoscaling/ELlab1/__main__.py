
from pulumi import export, Output
import pulumi_aws as aws
import json, hashlib

h = hashlib.new('sha1')

# Create the EKS Service Role and the correct role attachments
service_role = aws.iam.Role("eks-service-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "eks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    })
)

service_role_managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy",
    "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
]

for policy in service_role_managed_policy_arns:
    h.update(policy.encode('utf-8'))
    role_policy_attachment = aws.iam.RolePolicyAttachment(f"eks-service-role-{h.hexdigest()[0:8]}",
        policy_arn=policy,
        role=service_role.name
    )

# Create the EKS NodeGroup Role and the correct role attachments
node_group_role = aws.iam.Role("eks-nodegroup-role",
    assume_role_policy=json.dumps({
       "Version": "2012-10-17",
       "Statement": [{
           "Sid": "",
           "Effect": "Allow",
           "Principal": {
               "Service": "ec2.amazonaws.com"
           },
           "Action": "sts:AssumeRole"
       }]
    })
)

nodegroup_role_managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
]

for policy in nodegroup_role_managed_policy_arns:
    h.update(policy.encode('utf-8'))
    role_policy_attachment = aws.iam.RolePolicyAttachment(f"eks-nodegroup-role-{h.hexdigest()[0:8]}",
        policy_arn=policy,
        role=node_group_role.name
    )
#####
vpc = aws.ec2.Vpc(
    resource_name="myCustomVpc",
    cidr_block="10.0.0.0/16",
    tags={
        "Name": "myCustomVpc",
        "Environment": "Production"
    }
)
private_subnet = aws.ec2.Subnet("private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="us-east-1a",
)
# -----------------------------------------------------------------------------
# 2. Crear el Internet Gateway
# -----------------------------------------------------------------------------
igw = aws.ec2.InternetGateway(
    resource_name="myInternetGateway",
    vpc_id=vpc.id,
    tags={
        "Name": "myInternetGateway"
    }
)

# -----------------------------------------------------------------------------
# 3. Crear la Subnet pública
# -----------------------------------------------------------------------------
public_subnet = aws.ec2.Subnet(
    resource_name="myPublicSubnet",
    vpc_id=vpc.id,
    availability_zone="us-east-1b", 
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,  # Permite IP pública a las instancias
    tags={
        "Name": "myPublicSubnet"
    }
)

# -----------------------------------------------------------------------------
# 4. Crear la Route Table y asociarla a la Subnet pública
# -----------------------------------------------------------------------------
route_table = aws.ec2.RouteTable(
    resource_name="myRouteTable",
    vpc_id=vpc.id,
    tags={
        "Name": "myPublicRouteTable"
    }
)

# Ruta por defecto hacia Internet
public_route = aws.ec2.Route(
    resource_name="myDefaultRoute",
    route_table_id=route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw.id
)

# Asociar la ruta a la Subnet pública
route_table_assoc = aws.ec2.RouteTableAssociation(
    resource_name="myRouteTableAssociation",
    subnet_id=public_subnet.id,
    route_table_id=route_table.id
)
#######################################################
sg = aws.ec2.SecurityGroup("eks-cluster-security-group",
    vpc_id=vpc.id,
    revoke_rules_on_delete="true",
    ingress=[{
       'cidr_blocks' : ["0.0.0.0/0"],
       'from_port' : '80',
       'to_port' : '80',
       'protocol' : 'tcp',
    }]
)

sg_rule = aws.ec2.SecurityGroupRule("eks-cluster-security-group-egress-rule",
    type="egress",
    from_port=0,
    to_port=0,
    protocol="-1",
    cidr_blocks=["0.0.0.0/0"],
    security_group_id=sg.id
)

# Create EKS Cluster
cluster = aws.eks.Cluster("eks-cluster",
    role_arn=service_role.arn,
    vpc_config={
      "security_group_ids": [sg.id],
      "subnet_ids": [private_subnet.id, public_subnet.id],
      "endpointPrivateAccess": "false",
      "endpointPublicAccess": "true",
      "publicAccessCidrs": ["0.0.0.0/0"],
    },
)

# Create Cluster NodeGroup
node_group = aws.eks.NodeGroup("eks-node-group",
    cluster_name=cluster.name,
    node_role_arn=node_group_role.arn,
    subnet_ids=[private_subnet.id, public_subnet.id],
    scaling_config = {
       "desired_size": 1,
       "max_size": 2,
       "min_size": 1,
    },
)

def generateKubeconfig(endpoint, cert_data, cluster_name):
    return {
        "apiVersion": "v1",
        "clusters": [{
            "cluster": {
                "server": f"{endpoint}",
                "certificate-authority-data": f"{cert_data}"
            },
            "name": "kubernetes",
        }],
        "contexts": [{
            "context": {
                "cluster": "kubernetes",
                "user": "aws",
            },
            "name": "aws",
        }],
        "current-context": "aws",
        "kind": "Config",
        "users": [{
            "name": "aws",
            "user": {
                "exec": {
                    "apiVersion": "client.authentication.k8s.io/v1alpha1",
                    "command": "aws-iam-authenticator",
                    "args": [
                        "token",
                        "-i",
                        f"{cluster_name}",
                    ],
                },
            },
        }],
    }

# Create the KubeConfig Structure as per https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html
kubeconfig = Output.all(cluster.endpoint, cluster.certificate_authority["data"], cluster.name).apply(lambda args: generateKubeconfig(args[0], args[1], args[2]))

export("kubeconfig", kubeconfig)
