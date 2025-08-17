resource "random_string" "random_suffix" {
  length  = 5
  upper   = false
  lower   = true
  numeric = false
  special = false
}
