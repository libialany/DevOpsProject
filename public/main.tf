provider "aws" {
    region = "us-east-1"
  }
  
  resource "aws_vpc" "demo_pub_main" {
    cidr_block           = "172.0.0.0/16"
    enable_dns_support   = true
    enable_dns_hostnames = true
  
    tags = {
      Name = "DemoPubMainVPC"
    }
  }
  
  # 2. Public Subnet
  resource "aws_subnet" "demo_pub_public" {
    vpc_id                  = aws_vpc.demo_pub_main.id
    cidr_block              = "172.0.1.0/24"
    map_public_ip_on_launch = true
    availability_zone       = "${var.aws_region}b"
  
    tags = {
      Name = "DemoPubPublicSubnet"
    }
  }
  
  # 3. Private Subnets
  resource "aws_subnet" "demo_pub_private_1" {
    vpc_id            = aws_vpc.demo_pub_main.id
    cidr_block        = "172.0.2.0/24"
    availability_zone = "${var.aws_region}a"

    tags = {
      Name = "DemoPubPrivateSubnet1"
    }
  }

  resource "aws_subnet" "demo_pub_private_2" {
    vpc_id            = aws_vpc.demo_pub_main.id
    cidr_block        = "172.0.3.0/24"
    availability_zone = "${var.aws_region}c"

    tags = {
      Name = "DemoPubPrivateSubnet2"
    }
  }

  # 4. NAT Gateway for Private Subnets
  resource "aws_eip" "demo_pub_nat_eip" {
    domain = "vpc"
    depends_on = [aws_internet_gateway.demo_pub_igw]

    tags = {
      Name = "DemoPubNATEIP"
    }
  }

  resource "aws_nat_gateway" "demo_pub_nat" {
    allocation_id = aws_eip.demo_pub_nat_eip.id
    subnet_id     = aws_subnet.demo_pub_public.id

    tags = {
      Name = "DemoPubMainNAT"
    }

    depends_on = [aws_internet_gateway.demo_pub_igw]
  }

  # 5. Private Route Table
  resource "aws_route_table" "demo_pub_private" {
    vpc_id = aws_vpc.demo_pub_main.id

    route {
      cidr_block     = "0.0.0.0/0"
      nat_gateway_id = aws_nat_gateway.demo_pub_nat.id
    }

    tags = {
      Name = "DemoPubPrivateRouteTable"
    }
  }

  # 6. Private Route Table Associations
  resource "aws_route_table_association" "demo_pub_private_1_assoc" {
    subnet_id      = aws_subnet.demo_pub_private_1.id
    route_table_id = aws_route_table.demo_pub_private.id
  }

  resource "aws_route_table_association" "demo_pub_private_2_assoc" {
    subnet_id      = aws_subnet.demo_pub_private_2.id
    route_table_id = aws_route_table.demo_pub_private.id
  }

  # 7. Internet Gateway
  resource "aws_internet_gateway" "demo_pub_igw" {
    vpc_id = aws_vpc.demo_pub_main.id
  
    tags = {
      Name = "DemoPubMainIGW"
    }
  }
  
  resource "aws_route_table" "demo_pub_public" {
    vpc_id = aws_vpc.demo_pub_main.id
  
    tags = {
      Name = "DemoPubPublicRouteTable"
    }
  }
  
  resource "aws_route_table_association" "demo_pub_public_assoc" {
    subnet_id      = aws_subnet.demo_pub_public.id
    route_table_id = aws_route_table.demo_pub_public.id
  }
  
  resource "aws_route" "demo_pub_igw" {
    route_table_id         = aws_route_table.demo_pub_public.id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id             = aws_internet_gateway.demo_pub_igw.id
  }
  
  resource "aws_ec2_transit_gateway" "demo_pub_tgw" {
    description = "MyTransitGateway for cloud"
  
    tags = {
      Name = "DemoPubMainTGW"
    }
  }
  
  resource "aws_ec2_transit_gateway_vpc_attachment" "demo_pub_df_rt_tg" {
    transit_gateway_id = aws_ec2_transit_gateway.demo_pub_tgw.id
    subnet_ids = [
        aws_subnet.demo_pub_public.id
    ]
    vpc_id = aws_vpc.demo_pub_main.id
    tags = {
      Name = "DemoPubWeb App VPC Attachment"
    }
  }

resource "aws_vpn_gateway" "demo_pub_vgw" {
  vpc_id = aws_vpc.demo_pub_main.id
  amazon_side_asn = 64513

  tags = {
    Name = "DemoPubMainVGW"
  }
}

resource "aws_customer_gateway" "demo_pub_cgw" {
  bgp_asn    = 65000
  ip_address = var.public_ec2_ip
  type       = "ipsec.1"

  tags = {
    Name = "DemoPubMyCustomerGateway"
  }
}


resource "aws_vpn_connection" "demo_pub_vpn" {
  customer_gateway_id = aws_customer_gateway.demo_pub_cgw.id
  vpn_gateway_id      = aws_vpn_gateway.demo_pub_vgw.id
  type                = "ipsec.1"
  static_routes_only  = true

  tags = {
    Name = "DemoPubMyVPNConnection"
  }
}

resource "aws_vpn_connection_route" "demo_pub_vpn_route" {
  vpn_connection_id = aws_vpn_connection.demo_pub_vpn.id
  destination_cidr_block = "10.0.0.0/16"
}