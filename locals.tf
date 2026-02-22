###############################################################################
# Locals
###############################################################################

locals {
  s3_origin_id = "gallery-s3-origin"

  tags = {
    Project     = var.project_name
    ManagedBy   = "Terraform"
    Environment = "production"
  }
}
