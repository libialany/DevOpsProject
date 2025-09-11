# Create cluster
`eksctl create cluster -f cluster/cluster-config.yaml`

# Delete cluster
`eksctl delete cluster --name my-multi-nodegroup-cluster --region us-east-1`

# Create lambda
```
terraform init
terraform apply
terraform destroy
```