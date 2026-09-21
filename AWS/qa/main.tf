terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
    profile = var.aws_profile
}

data "aws_iam_policy_document" "qa_trust" {

  statement {
    effect = "Allow"

    principals {
      type = "AWS"

      identifiers = [
        var.trusted_principal_arn
      ]
    }

    actions = [
      "sts:AssumeRole"
    ]
  }
}

#
# QA role
#
resource "aws_iam_role" "qa" {

  name = "FastAPIQARole"

  description = "QA role with read-only SQS message access"

  assume_role_policy = data.aws_iam_policy_document.qa_trust.json

  max_session_duration = 3600

  tags = {
    Role    = "QA"
    Project = "FastAPI"
  }
}

#
# QA permissions
#
data "aws_iam_policy_document" "qa_policy" {

  statement {
    sid    = "ReadMessages"
    effect = "Allow"

    actions = [
      "sqs:ReceiveMessage",
      "sqs:GetQueueUrl",
      "sqs:GetQueueAttributes"
    ]

    resources = "*"
  }
}

#
# IAM policy
#
resource "aws_iam_policy" "qa" {

  name = "FastAPIQASQSPolicy"

  description = "QA read-only permissions for SQS"

  policy = data.aws_iam_policy_document.qa_policy.json
}

#
# Attach policy
#
resource "aws_iam_role_policy_attachment" "qa" {

  role = aws_iam_role.qa.name

  policy_arn = aws_iam_policy.qa.arn
}

