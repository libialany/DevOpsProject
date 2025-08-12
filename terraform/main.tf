provider "aws" {
  region = "us-east-1"  # Adjust to your region
}

resource "aws_vpc" "k8s_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.k8s_vpc.id
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.k8s_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.k8s_vpc.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1b"
}

resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.k8s_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.k8s_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public_rt_assoc_1" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_rt_assoc_2" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_security_group" "master_sg" {
  name        = "k8s-master-sg"
  description = "Security group for Kubernetes master"
  vpc_id      = aws_vpc.k8s_vpc.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # or your specific IP range for security
  }
  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 2379
    to_port     = 2380
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 10248
    to_port     = 10260
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "worker_sg" {
  name        = "k8s-worker-sg"
  description = "Security group for Kubernetes worker nodes"
  vpc_id      = aws_vpc.k8s_vpc.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # or your specific IP range for security
  }
  ingress {
    from_port   = 10248
    to_port     = 10260
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "master" {
  source = "terraform-aws-modules/ec2-instance/aws"
  version = "2.18.0"
  name   = "k8s-master"
  key_name      = "test8"
  instance_count = 1
  ami           = var.aws_ami_id
  instance_type = "t3.medium"  # 2 vCPU, 4GB RAM
  subnet_id     = aws_subnet.public_subnet_1.id
  vpc_security_group_ids = [aws_security_group.master_sg.id]
  associate_public_ip_address=true
  user_data = file("userdata.sh")
}

module "workers" {
  source = "terraform-aws-modules/ec2-instance/aws"
  version = "2.18.0"
  name   = "k8s-worker"
  key_name      = "test8"
  instance_count = 2
  ami           = var.aws_ami_id
  instance_type = "t3.small"  # 2 vCPU, but can choose t3.small (2 vCPU, 2GB) or t3.micro + RAM adjustment
  subnet_id     = aws_subnet.public_subnet_2.id
  vpc_security_group_ids = [aws_security_group.worker_sg.id]
  associate_public_ip_address=true
  user_data = file("userdata.sh")
}

