## Comand to debug an app

```
k logs demo-75486f954-hwfq2  --previous 
k describe pod demo-75486f954-hwfq2
k describe pod demo-75486f954-hwfq2
k describe pod ingress-nginx-controller-7d65c586d6-r74vl  -n ingress-nginx  | grep -i liveness 
k describe deployment demo | grep Environment
k describe deployment demo | grep Mounts:
k describe deployment demo | grep Liveness:
k describe deployment demo | grep Readiness:
k top pods
```

<img width="603" height="229" alt="image" src="https://github.com/user-attachments/assets/27fa3bc6-74f3-46ea-b227-fddbed9d78ea" />
