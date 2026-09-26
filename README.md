## Comand to debug an app

```
k apply -f k8s
k describe pod demo-75486f954-hwfq2
k logs demo-75486f954-hwfq2  --previous 
k get deployment
k describe pod demo-75486f954-hwfq2
k describe pod ingress-nginx-controller-7d65c586d6-r74vl  -n ingress-nginx  | grep -i liveness 
k describe deployment demo | grep Environment
k describe deployment demo | grep Mounts:
k describe deployment demo | grep Liveness:
k describe deployment demo | grep Readiness:
k top pods
```
