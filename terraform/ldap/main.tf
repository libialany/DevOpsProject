terraform {
  required_providers {
    ldap = {
      source  = "elastic-infra/ldap"
      version = "~> 2.0"
    }
  }
}

provider "ldap" {
  ldap_host     = "localhost"
  ldap_port     = 389
  bind_user     = "cn=admin,dc=libia,dc=xyz"
  bind_password = "admin"
}