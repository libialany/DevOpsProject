provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "demo_onprem_main_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "Demo-HN-onprem-MainVPC"
  }
}

resource "aws_internet_gateway" "demo_onprem_igw" {
  vpc_id = aws_vpc.demo_onprem_main_vpc.id
  tags = {
    Name = "Demo-HN-onprem-MainIGW"
  }
}

resource "aws_subnet" "demo_onprem_subnet_a" {
  vpc_id                  = aws_vpc.demo_onprem_main_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "Demo-HN-onprem-SubnetA"
  }
}

resource "aws_subnet" "demo_onprem_subnet_b" {
  vpc_id                  = aws_vpc.demo_onprem_main_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true

  tags = {
    Name = "Demo-HN-onprem-SubnetB"
  }
}

resource "aws_route_table" "demo_onprem_public_rt" {
  vpc_id = aws_vpc.demo_onprem_main_vpc.id
  tags = {
    Name = "Demo-HN-onprem-PublicRouteTable"
  }
}

resource "aws_route" "default_route" {
  route_table_id         = aws_route_table.demo_onprem_public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.demo_onprem_igw.id
}

resource "aws_route_table_association" "demo_onprem_subnet_a_assoc" {
  subnet_id      = aws_subnet.demo_onprem_subnet_a.id
  route_table_id = aws_route_table.demo_onprem_public_rt.id
}

resource "aws_route_table_association" "demo_onprem_subnet_b_assoc" {
  subnet_id      = aws_subnet.demo_onprem_subnet_b.id
  route_table_id = aws_route_table.demo_onprem_public_rt.id
}
resource "aws_security_group" "demo_onprem_allow_ssh" {
  name        = "Demo-HN-onprem-allow_ssh"
  description = "Allow SSH inbound traffic"
  vpc_id      = aws_vpc.demo_onprem_main_vpc.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
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
resource "aws_security_group" "demo_onprem_allow_external_vpc" {
  name        = "Demo-HN-onprem-allow_external_vpc"
  description = "Allow VPC inbound traffic"
  vpc_id      = aws_vpc.demo_onprem_main_vpc.id

ingress {
  description = "Allow all TCP"
  from_port   = 0
  to_port     = 65535
  protocol    = "tcp"
  cidr_blocks = ["172.0.0.0/16"]
}

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_instance" "demo_onprem_web" {
  ami                         = var.ami_id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.demo_onprem_subnet_a.id
  associate_public_ip_address = true
  key_name                    = var.key_name

  tags = {
    Name = "Demo-HN-onprem-PublicEC2"
  }

  vpc_security_group_ids = [aws_security_group.demo_onprem_allow_ssh.id , aws_security_group.demo_onprem_allow_external_vpc.id]
}

resource "aws_eip" "demo_onprem_ec2_eip" {
  instance = aws_instance.demo_onprem_web.id
  domain   = "vpc"
  depends_on = [aws_internet_gateway.demo_onprem_igw]
}