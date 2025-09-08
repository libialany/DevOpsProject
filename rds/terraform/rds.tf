provider "aws" {
  region = "us-east-1"
}


resource "aws_db_parameter_group" "mysql_logging" {
  name   = "mysql-logging-pg"
  family = "mysql8.0"  
  description = "MySQL parameter group with logging enabled"

  parameter {
    name  = "slow_query_log"
    value = "1"
  }

  parameter {
    name  = "general_log"
    value = "1"
  }

  parameter {
    name  = "log_output"
    value = "TABLE"
  }

  parameter {
    name  = "long_query_time"
    value = "2"
  }
}

resource "aws_db_subnet_group" "default" {
  name       = "example-subnet-group"
  subnet_ids = ["subnet-12345678", "subnet-abcdef12"]

  tags = {
    Name = "My DB subnet group"
  }
}

resource "aws_db_instance" "mysql" {
  identifier             = "my-mysql-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  storage_type           = "gp2"
  username               = "admin"
  password               = "securepassword123"
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = ["sg-0123456789abcdef0"]
  multi_az               = false
  publicly_accessible    = false
  skip_final_snapshot    = true

  parameter_group_name = aws_db_parameter_group.mysql_logging.name
  enabled_cloudwatch_logs_exports = ["general", "error", "slowquery", "audit"]

  tags = {
    Name = "MySQLWithLogging"
  }
}