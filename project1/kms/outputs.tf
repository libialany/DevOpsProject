output "key_arn" {
  description = "The ARN of the KMS key"
  value       = var.key_type == "service" ? join("", aws_kms_key.service_key.*.arn) : join("", aws_kms_key.direct_key.*.arn)
}

output "key_id" {
  description = "The ID of the KMS key"
  value       = var.key_type == "service" ? join("", aws_kms_key.service_key.*.key_id) : join("", aws_kms_key.direct_key.*.key_id)
}
