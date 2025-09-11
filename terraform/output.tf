output "lambda_policy_arn" {
  value = aws_iam_policy.lambda_policy.arn
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}
