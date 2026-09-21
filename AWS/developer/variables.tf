variable "region" {
    description = "aws region"
    type = string
    default = "us-east-1"
}
variable "trusted_principal_arn" {
  description = "Principal allowed to assume the developer role"
  type = string
}
variable "aws_profile" {
    description = "value"
    type = string

}