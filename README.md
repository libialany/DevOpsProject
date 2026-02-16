🔐 **Authenticate GitHub Actions with AWS Using OIDC — Stop Storing AWS Keys in Secrets**

By using OpenID Connect (OIDC), your GitHub workflow can request **short-lived credentials directly from AWS STS** — no static secrets, no key rotation headaches, and significantly reduced blast radius.

With OIDC:

* ✅ No stored AWS access keys in GitHub
* ✅ Temporary, short-lived credentials
* ✅ Fine-grained IAM trust policies
* ✅ Branch and repo restrictions enforced in AWS

step: 

```
wget https://gist.github.com/libialany/f8a84c3bc22bae78d636527e7b6d7c40
bash GH-2-AWS_OIDC.sh GhRole RepoX BranchX
```
