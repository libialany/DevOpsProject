terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}
provider "aws" {
  region = "us-east-1" 
}

# Define the source S3 bucket (the one you want to back up)
resource "aws_s3_bucket" "source_bucket" {
  bucket = "s3-june-events-resume"  # Replace with your source bucket name
  acl    = "private"

  versioning {
    enabled = true
  }
}

# Define the destination S3 bucket (where backups will be stored)
resource "aws_s3_bucket" "backup_bucket" {
  bucket = "s3-events-resumes"  # Replace with your backup bucket name
  acl    = "private"

  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket_object" "replication_role_policy" {
  bucket = aws_s3_bucket.backup_bucket.bucket
  key    = "replication-policy.json"
  content = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/ReplicationRole"
      },
      "Action": ["s3:ReplicateObject", "s3:ReplicateDelete"],
      "Resource": "arn:aws:s3:::${aws_s3_bucket.backup_bucket.bucket}/*"
    }
  ]
}
POLICY
}

# Create an IAM Role for replication
resource "aws_iam_role" "replication_role" {
  name = "ReplicationRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# Attach policy to allow replication actions
resource "aws_iam_role_policy" "replication_policy" {
  role = aws_iam_role.replication_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "s3:*"
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.source_bucket.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.source_bucket.bucket}/*"
        ]
      }
    ]
  })
}
# Set up the S3 bucket replication configuration
resource "aws_s3_bucket_replication_configuration" "replication" {
  role = aws_iam_role.replication_role.arn
  bucket = aws_s3_bucket.source_bucket.id

  rule {
    id     = "replication-rule"
    status = "Enabled"

    filter {
      prefix = ""
    }

    destination {
      bucket = "arn:aws:s3:::${aws_s3_bucket.backup_bucket.bucket}"
      storage_class = "STANDARD"  # Change if you want to use another storage class
    }
    delete_marker_replication {
                status= "Disabled"
    }
  }

  depends_on = [aws_iam_role_policy.replication_policy]
}
data "aws_caller_identity" "current" {}