output "demo_onprem_vpc_id" {
  value = aws_vpc.demo_onprem_main_vpc.id
}

output "demo_onprem_subnet_a_id" {
  value = aws_subnet.demo_onprem_subnet_a.id
}

output "demo_onprem_subnet_b_id" {
  value = aws_subnet.demo_onprem_subnet_b.id
}

output "demo_onprem_internet_gateway_id" {
  value = aws_internet_gateway.demo_onprem_igw.id
}

output "demo_onprem_ec2_public_ip" {
  value = aws_eip.demo_onprem_ec2_eip.public_ip
}
