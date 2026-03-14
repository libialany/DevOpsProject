output "alb_dns_name" {
  value = aws_lb.alb.dns_name
}
output "instance_ids" {
  value = [for instance in aws_instance.web : instance.public_ip]
}