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
  region = var.region
    profile = var.aws_profile
}

data "aws_iam_policy_document" "developer_trust" {

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

resource "aws_iam_role" "developer" {

  name = "FastAPIDeveloperRole"

  description = "Developer role for SQS management"

  assume_role_policy = data.aws_iam_policy_document.developer_trust.json

  max_session_duration = 3600

  tags = {
    Role    = "Developer"
    Project = "FastAPI"
  }
}

data "aws_iam_policy_document" "developer_policy" {

  statement {
    sid    = "CreateQueue"
    effect = "Allow"

    actions = [
      "sqs:CreateQueue",
      "sqs:GetQueueUrl",
      "sqs:GetQueueAttributes",
      "sqs:ListQueues"
    ]

    resources = "*"
  }

  statement {
    sid    = "ManageMessages"
    effect = "Allow"

    actions = [
      "sqs:SendMessage",
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:ChangeMessageVisibility"
    ]

    resources = "*"
  }
}

resource "aws_iam_policy" "developer" {

  name = "FastAPIDeveloperSQSPolicy"

  description = "Developer permissions for SQS"

  policy = data.aws_iam_policy_document.developer_policy.json
}

resource "aws_iam_role_policy_attachment" "developer" {

  role = aws_iam_role.developer.name

  policy_arn = aws_iam_policy.developer.arn
}