variable "vpc_cidr" {
  description = "The CIDR block for the VPC network."
  type        = string
}

variable "cluster_name" {
  description = "The name of the Kubernetes cluster."
  type        = string
}

variable "kubernetes_version" {
  description = "The Kubernetes version to use for the cluster."
  type        = string
}
