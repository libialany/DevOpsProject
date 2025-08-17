module "kms_key_sns_sqs" {
  source               = "./kms"
  alias_name           = var.alias_name
  description          = var.description
  key_type             = var.key_type
  append_random_suffix = var.append_random_suffix
  direct_key_principal = {
    Service = ["sqs.amazonaws.com", "sns.amazonaws.com"]
  }
  tags = {
    "Env"      = "dev",
    "AssetId"  = "sqs-demo",
    "Resource" = "kms",
    "Name"     = "kms-sqs-demo"
  }
  kms_policy_json            = var.kms_policy_json
  principals_identifiers_arn = var.principals_identifiers_arn
  providers = {
    aws = aws.spoke
  }
}

