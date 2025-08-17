resource "aws_kms_key" "direct_key" {
  description             = var.description
  enable_key_rotation     = true
  deletion_window_in_days = var.deletion_window

  policy = data.aws_iam_policy_document.kms_key_policy_direct[0].json

  tags = merge({
    Alias = var.alias_name
  }, var.tags)

  count = 1 - local.service_key_count
}

resource "aws_kms_alias" "direct_key" {
  name          = "alias/${local.alias_name}"
  target_key_id = aws_kms_key.direct_key[0].key_id
  count         = 1 - local.service_key_count
}

data "aws_iam_policy_document" "kms_key_policy_direct" {

  statement {
    sid = "Allow Admin" # Root user will have permissions to manage the CMK, but do not have permissions to use the CMK in cryptographic operations. - https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations
    actions = concat([
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
    ],var.kms_policy_json)
    resources = ["*"]

    principals {
      type        = "AWS"
      identifiers = concat(["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"],var.principals_identifiers_arn)
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

    dynamic "principals" {
      for_each = var.direct_key_principal
      content {
        type        = principals.key
        identifiers = principals.value
      }
    }
  }

  count = 1 - local.service_key_count
}

