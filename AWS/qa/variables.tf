variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "trusted_principal_arn" {
  description = "Principal allowed to assume the QA role"
  type        = string
}

variable "aws_profile" {
    description = "value"
    type = string

}