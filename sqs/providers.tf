provider "aws" {
  alias = "logging"
  region = "us-east-1"
}

provider "aws" {
  alias = "spoke"
  region = "us-east-1"
}

