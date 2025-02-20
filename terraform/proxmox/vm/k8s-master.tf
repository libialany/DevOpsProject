resource "proxmox_vm_qemu" "k8s-master" {
  count       = 3
  name        = "k8s0${count.index + 1}.mydomain.intra"
  target_node = var.proxmox_host
  vmid        = "101${count.index + 1}"
  clone       = var.template_name
  os_type     = "cloud-init"
  cpu         = "kvm64"
  cores       = 2
  sockets     = 1
  memory      = 6144
  storage     = "local-lvm"

  network {
    model     = "virtio"
    bridge    = "vmbr0"
    tag       = 101
    firewall  = false
    link_down = false
  }

  ipconfig0 = "ip=192.168.10.1${count.index + 1}/22,gw=192.168.10.1"
  ciuser    = "terraform"
  sshkeys   = <<EOF
  ${var.ssh_key}
  EOF
}