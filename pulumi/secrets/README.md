# Pulumi - Secrets Management

## Resources

Here is a list of resources that provide further explanation and context:

1. **Pulumi Documentation**
   - [Pulumi Official Documentation](https://www.pulumi.com/docs/): Comprehensive guide to using Pulumi for infrastructure as code.

2. **Pulumi Secrets Management**
   - [Managing Configuration](https://www.sanjaybhagia.com/2021/01/26/pulumi-secrets-management): Understand how to securely manage secrets in Pulumi.

3. **Vault**

    - [Set up Vault](https://developer.hashicorp.com/vault/tutorials/get-started/setup): First steps


4. **Vault Encriptation**
   - [Encrypt data in transit with Vault](https://developer.hashicorp.com/vault/tutorials/encryption-as-a-service/eaas-transit): This relieves the burden of data encryption and decryption from the application developers and moves the burden to Vault.



5. **creating the secret in vault**

*Note:* Ensure that environment variables like `VAULT_TOKEN` and `VAULT_ADDR` are correctly set.

  ```bash
  vault token lookup #Check Token Permissions
  ```

  ```hcl
  path "my-secret/*" {
      capabilities = ["read", "list"]
  }  // Verify Policy Configuration
  ```

  ```bash
  vault token create -policy="your-policy-name" # Apply the policy
  ```

  ```bash
  vault secrets list # List Secrets Engine
  ```

  ```bash
  vault secrets enable -path=my-secret kv #Enable and Configure Secrets Engine
  ```

