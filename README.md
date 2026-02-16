🔐 **Authenticate GitHub Actions with AWS Using OIDC — Stop Storing AWS Keys in Secrets**

If you're still storing long-lived AWS access keys inside GitHub Secrets for your CI/CD pipelines… it’s time to upgrade your security posture.

There’s a better (and safer) way: **OIDC federation between GitHub Actions and AWS**.

By using OpenID Connect (OIDC), your GitHub workflow can request **short-lived credentials directly from AWS STS** — no static secrets, no key rotation headaches, and significantly reduced blast radius.

### 🚨 Why This Matters (Security First)

When you use static AWS credentials:

* ❌ Long-lived access keys can leak
* ❌ Secrets must be rotated manually
* ❌ Compromised runners = exposed credentials

With OIDC:

* ✅ No stored AWS access keys in GitHub
* ✅ Temporary, short-lived credentials
* ✅ Fine-grained IAM trust policies
* ✅ Branch and repo restrictions enforced in AWS



#DevOps #CloudSecurity #AWS #GitHubActions #CICD

