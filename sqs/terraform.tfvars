
# ================================ SQS ================================
tag_topic = {
  "Env"      = "dev",
  "AssetId"  =  "demo-sqs",
  "Resource" = "sqs",
  "Name"     = "demosqs"
}

list_topics = [{
  listsqs    = ["demosqs_publish_consumer"]
  }
]

topic_name = "sqs-demosqs-topic"

# ================================ kms ================================
alias_name           = "alias/aws/sqs/demosqs"
description          = "Master key for Sqs"
key_type             = "direct"
append_random_suffix = false
kms_policy_json = [
  "kms:CancelKeyDeletion",
  "kms:GenerateDataKey*",
  "kms:GenerateDataKey",
  "kms:Encrypt",
  "kms:Decrypt",
  "kms:ReEncrypt*",
  "kms:CreateGrant",
  "kms:DescribeKey"
]
principals_identifiers_arn = ["arn:aws:iam::123"]

