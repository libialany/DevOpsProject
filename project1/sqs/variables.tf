
# # ================================ SQS ================================
variable "list_topics" {
  description = "List of name topics"
  type = list(object({
    listsqs    = list(string)
  }))
}

variable "tag_topic" {
  type    = map(string)
  default = {}
}

variable "kms_master_key" {
  description = "The description to give to the key"
  type        = string
}

variable "topic_name" { 
  description = "SNS name"
  type        = string
}

# # ================================ KMS ================================

variable "key_type" {
  description = "Indicate which kind of key to create: 'service' for key used by services; 'direct' for other keys. Must provide service_key or direct_key maps depending on the type"
  type        = string
}

variable "description" {
  description = "The description to give to the key"
  type        = string
}

variable "alias_name" {
  description = "Name for the kms key alias. A random string will be appended depending on the 'append_random_suffix' variable"
  type        = string
}

variable "append_random_suffix" {
  description = "Append a random string to the alias name. Default: true (yes)"
  type        = bool
  default     = true
}

variable "kms_policy_json" {
  type    = list(string)
  default = []
}

variable "principals_identifiers_arn" {
  type    = list(string)
  default = []
}
