resource "aws_sns_topic" "demo-sqs_publish_consumer" {
  name              = var.topic_name
  kms_master_key_id = var.kms_master_key
  tags = {
    "Env"      = "dev",
    "Resource" = "sns",
    "Name"     = "sqs-demo-sqs-topic"
  }
  provider = aws.spoke
}

resource "aws_sqs_queue" "demo-sqs_verification" {
  depends_on                = [aws_sqs_queue.demo-sqs_verification_DLQ]
  name                      = var.list_topics[0].listsqs[0]
  kms_master_key_id         = var.kms_master_key
  message_retention_seconds = 345600
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.demo-sqs_verification_DLQ.arn
    maxReceiveCount     = 10
  })

  tags = {
    "Env"      = "dev",
    "Resource" = "sqs",
    "Name"     = "demo-sqs"
  }
  provider = aws.spoke
}
resource "aws_sqs_queue" "demo-sqs_verification_DLQ" {
  name                      = "${var.list_topics[0].listsqs[0]}_error"
  kms_master_key_id         = var.kms_master_key
  message_retention_seconds = 345600
  tags = {
    "Env"      = "dev",
    "Resource" = "sqs",
    "Name"     = "demo-sqs"
  }
  provider = aws.spoke
}
resource "aws_sqs_queue_policy" "demo-sqs_verification_DLQ_Policy" {
  queue_url  = aws_sqs_queue.demo-sqs_verification.id
  depends_on = [aws_sqs_queue.demo-sqs_verification]

  provider = aws.spoke

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "read-message",
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.demo-sqs_verification.arn}",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "${aws_sns_topic.demo-sqs_publish_consumer.arn}"
        }
      }
    }
  ]
}
POLICY
}


resource "aws_sns_topic_subscription" "demo-sqs_verification_Sqs_Target" {
  topic_arn = aws_sns_topic.demo-sqs_publish_consumer.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.demo-sqs_verification.arn

  provider = aws.spoke
}
