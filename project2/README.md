# STEPS

```
docker build -t order-processor:latest . --no-cache
minikube image load order-processor:latest
k apply -f .
bash test.sh
```