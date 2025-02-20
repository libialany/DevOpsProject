provider.tfprovider "proxmox" {
  pm_api_url = "https://192.168.1.74:8006/api2/json"
  # api token id is in the form of: <username>@pam!<tokenId>
  pm_api_token_id = "xfg@pam!k3sadmin"
  # this is the full secret wrapped in quotes.
  pm_api_token_secret = var.PROXMOX_API_SECRET
  pm_tls_insecure     = true

  # debug log
  #  pm_log_enable = true
  #  pm_log_file   = "terraform-plugin-proxmox.log"
  #  pm_debug      = true
  #  pm_log_levels = {
  #    _default    = "debug"
  #    _capturelog = ""
  #  }
}