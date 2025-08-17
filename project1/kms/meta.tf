data "aws_caller_identity" "current" {}

locals {
  service_key_count = var.key_type == "service" ? 1 : 0
  alias_name        = "${var.alias_name}${var.append_random_suffix ? "-${random_string.random_suffix.result}" : ""}"

  caller_account_condition = {
    test     = "StringEquals"
    variable = "kms:CallerAccount"
    values   = var.service_key_info.caller_account_ids
  }
  kms_conditions = length(var.service_key_info.caller_account_ids) > 0 ? setunion(var.kms_key_conditions, [local.caller_account_condition]) : var.kms_key_conditions
}
