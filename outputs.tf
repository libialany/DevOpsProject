###############################################################################
# Outputs
###############################################################################

output "s3_bucket_name" {
  description = "Name of the S3 images bucket"
  value       = module.gallery_bucket.s3_bucket_id
}

output "cloudfront_domain" {
  description = "CloudFront distribution domain – use this as base URL for images"
  value       = module.cloudfront.cloudfront_distribution_domain_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = module.cloudfront.cloudfront_distribution_id
}

output "api_gateway_endpoint" {
  description = "API Gateway endpoint to retrieve the image list"
  value       = "${module.api_gateway.api_endpoint}/images"
}

output "lambda_function_name" {
  description = "Name of the gallery Lambda function"
  value       = module.lambda_function.lambda_function_name
}

output "lambda_role_arn" {
  description = "IAM role ARN attached to the Lambda function"
  value       = module.lambda_function.lambda_role_arn
}

output "waf_web_acl_arn" {
  description = "ARN of the WAF Web ACL protecting the API Gateway stage"
  value       = aws_wafv2_web_acl.gallery_api.arn
}

output "waf_web_acl_id" {
  description = "ID of the WAF Web ACL"
  value       = aws_wafv2_web_acl.gallery_api.id
}
