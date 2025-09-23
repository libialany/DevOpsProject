provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "example" {
  bucket = "my-unique-s3-bucket-1234567890"
  tags = {
    Environment = "Dev"
  }
}
