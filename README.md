## AWS 

```
tt init
tt plan --profile p1
tt apply --profile p1
```

### Improvements

create a module for the creation

## K8s

```

helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm repo update

helm install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver \
  --namespace kube-system \
  --set syncSecret.enabled=true

helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

helm install vault hashicorp/vault \
  --namespace vault --create-namespace \
  --set "server.dev.enabled=true" \
  --set "injector.enabled=false"

kubectl get pods -n kube-system -l app=secrets-store-csi-driver | kubectl get pods -n vault

helm install vault-csi-provider hashicorp/vault-csi-provider \
  --namespace vault

```


## set up inside container

```
export VAULT_ADDR='http://127.0.0.1:8200'
vault login root

vault auth enable kubernetes

vault write auth/kubernetes/config \
  kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443"

vault policy write fastapi-app-policy - <<EOF
path "secret/data/fastapi-app" {
  capabilities = ["read"]
}
EOF

vault write auth/kubernetes/role/fastapi-app \
  bound_service_account_names=fastapi-app-sa \
  bound_service_account_namespaces=default \
  policies=fastapi-app-policy \
  ttl=24h

exit

export VAULT_ADDR='http://127.0.0.1:8200'
vault login root

vault secrets enable -path=secret kv-v2

vault kv put secret/fastapi-app db_password="s3cr3t-p@ss" api_key="abc123"

exit

```

## how to applly it

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fastapi-app-sa
  namespace: default
---
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: fastapi-app-vault-secrets
  namespace: default
spec:
  provider: vault
  parameters:
    vaultAddress: "http://vault.vault:8200"
    roleName: "fastapi-app"
    objects: |
      - objectName: "db_password"
        secretPath: "secret/data/fastapi-app"
        secretKey: "db_password"
      - objectName: "api_key"
        secretPath: "secret/data/fastapi-app"
        secretKey: "api_key"
  secretObjects:
    - secretName: fastapi-app-secret
      type: Opaque
      data:
        - objectName: db_password
          key: db_password
        - objectName: api_key
          key: api_key
```

## how use it

```
kubectl exec -it <fastapi-pod-name> -- env | grep -E "db_password|api_key"
```