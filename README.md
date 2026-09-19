## Comand to debug an app

```
k apply -f k8s
k describe pod demo-75486f954-hwfq2
k logs demo-75486f954-hwfq2 
k logs demo-75486f954-hwfq2  --previous 
k logs -p demo-75486f954-hwfq2 
k get deployment 
k describe deployment demo
k describe deployment demo | grep Environment
k describe deployment demo | grep Mounts:
k describe deployment demo | grep Liveness:
k describe deployment demo | grep Readiness:
k describe deployment demo | grep Startup:
k describe get deployment demo -o yaml 
k get deployment demo -o yaml 
k get secrets
k get configmaps
k describe configmap argocd-cm
k get configmaps
k get secretKeyRef
k get secret 
k get po
k describe pod demo-75486f954-hwfq2
k describe configmap demo-config
kubectl describe po Startup
kubectl describe po | grep Live*
k top pods
```
