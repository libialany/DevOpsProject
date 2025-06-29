
output "demo_pub_vpc_tg" {
  value = aws_ec2_transit_gateway.demo_pub_tgw.id
}

output "private_subnet_ids" {
  description = "The IDs of the private subnets"
  value       = [aws_subnet.demo_pub_private_1.id, aws_subnet.demo_pub_private_2.id]
}
# Internet Gateway Outputs
output "internet_gateway_id" {
  description = "The ID of the Internet Gateway"
  value       = aws_internet_gateway.demo_pub_igw.id
}

# NAT Gateway Outputs
output "nat_gateway_id" {
  description = "The ID of the NAT Gateway"
  value       = aws_nat_gateway.demo_pub_nat.id
}

output "nat_gateway_eip" {
  description = "The Elastic IP address of the NAT Gateway"
  value       = aws_eip.demo_pub_nat_eip.public_ip
}