resource "aws_iam_role" "fis_role" {
  name = "fis-ec2-stop-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "fis.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "fis_policy" {
  role = aws_iam_role.fis_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:StopInstances",
        "ec2:StartInstances",
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

