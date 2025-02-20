variable "PROXMOX_API_SECRET" {
  type = string
}

variable "ssh_key" {
  default = "ssh-rsa AAAAB3NzaC1y..."
}

variable "proxmox_host" {
  default = "proxmox"
}
variable "template_name" {
  default = "debian11.vm.shiwaforce.com"
}
