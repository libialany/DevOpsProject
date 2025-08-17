resource "aws_kms_key" "service_key" {
  description             = var.description
  enable_key_rotation     = true
  deletion_window_in_days = var.deletion_window

  policy = data.aws_iam_policy_document.combined_policy[0].json

  tags = merge({
    Alias = var.alias_name
  }, var.tags)

  count = local.service_key_count
}

resource "aws_kms_alias" "service_key" {
  name          = "alias/${local.alias_name}"
  target_key_id = aws_kms_key.service_key[0].key_id
  count         = local.service_key_count
}

data "aws_iam_policy_document" "combined_policy" {
  override_policy_documents = [
    data.aws_iam_policy_document.kms_key_policy_via_service[0].json,
    var.add_kms_policy_json
  ]
  
  count = local.service_key_count
}

data "aws_iam_policy_document" "kms_key_policy_via_service" {
  statement {
    sid = "Allow Admin" # Root user will have permissions to manage the CMK, but do not have permissions to use the CMK in cryptographic operations. - https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations
    actions = [
      "kms:Create*",
      "kms:Describe*",
      "kms:Enable*",
      "kms:List*",
      "kms:Put*",
      "kms:Update*",
      "kms:Revoke*",
      "kms:Disable*",
      "kms:Get*",
      "kms:Delete*",
      "kms:TagResource",
      "kms:UntagResource",
      "kms:ScheduleKeyDeletion",
      "kms:CancelKeyDeletion"
    ]
    resources = ["*"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
  }
  
  statement {
    sid = "Allow Cryptography"

    actions = [
      "kms:Encrypt",
      "kms:Decrypt",
      "kms:ReEncrypt*",
      "kms:GenerateDataKey*",
      "kms:CreateGrant",
      "kms:DescribeKey",
    ]

    resources = ["*"]

    principals {
      type        = "AWS"
      identifiers = var.principals_service_arn
    }

    condition {
      test     = "StringEquals"
      variable = "kms:ViaService"
      values   = var.service_key_info.aws_service_names
    }

    dynamic "condition" {
      for_each = local.kms_conditions

      content {
        test     = condition.value.test
        variable = condition.value.variable
        values   = condition.value.values
      }
    }
  }

  count = local.service_key_count
}
