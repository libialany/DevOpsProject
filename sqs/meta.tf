
data "aws_caller_identity" "current" {
  provider = aws.spoke
}

data "aws_region" "spoke" {
  provider = aws.spoke
}
