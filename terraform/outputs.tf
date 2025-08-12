output "master_instance_id" {
  value = module.master.id
}

output "worker_instance_ids" {
  value = module.workers.id
}

output "master_public_ip" {
  value = module.master.public_ip
}

output "worker_public_ips" {
  value = module.workers.public_ip
}

output "vpc_id" {
  value = aws_vpc.k8s_vpc.id
}

output "subnet_id_1" {
  value = aws_subnet.public_subnet_1.id
}
output "subnet_id_2" {
  value = aws_subnet.public_subnet_2.id
}

output "master_security_group_id" {
  value = aws_security_group.master_sg.id
}

output "worker_security_group_id" {
  value = aws_security_group.worker_sg.id
}