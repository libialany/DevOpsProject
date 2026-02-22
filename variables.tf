###############################################################################
# Variables
###############################################################################

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix used for resource naming"
  type        = string
  default     = "gallery-app"
}

variable "bucket_name" {
  description = "Name of the S3 bucket that stores gallery images"
  type        = string
  # Override in terraform.tfvars – bucket names must be globally unique
}
