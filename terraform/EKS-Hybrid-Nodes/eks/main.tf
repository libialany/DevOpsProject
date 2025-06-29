locals {
  # RFC 1918 IP ranges supported
  remote_network_cidr = var.remote_cidr
  remote_node_cidr    = cidrsubnet(local.remote_network_cidr, 2, 0)
}

module "eks_hybrid_node_role" {
  source  = "terraform-aws-modules/eks/aws//modules/hybrid-node-role"
  version = "~> 20.31"

  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.31"

  cluster_name    = "DemoPubHN"
  cluster_version = "1.31"

  cluster_addons = {
    coredns                = {}
    eks-pod-identity-agent = {}
    kube-proxy             = {}
  }

  cluster_endpoint_public_access = true
  enable_cluster_creator_admin_permissions = true

  create_node_security_group = false
  cluster_security_group_additional_rules = {
    hybrid-all = {
      cidr_blocks = [var.remote_cidr]
      description = "Allow all traffic from remote node/pod network"
      from_port   = 0
      to_port     = 0
      protocol    = "all"
      type        = "ingress"
    }
  }

  cluster_compute_config = {
    enabled    = true
    node_pools = ["system"]
  }

  access_entries = {
    hybrid-node-role = {
      principal_arn = module.eks_hybrid_node_role.arn
      type          = "HYBRID_LINUX"
    }
  }

  vpc_id     = var.vpc_pub
  subnet_ids = var.ids_subnets

  cluster_remote_network_config = {
    remote_node_networks = {
      cidrs = [var.remote_cidr]
    }
  }

  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}