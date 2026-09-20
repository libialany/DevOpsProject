## helm rollbach simple steps


```
port-forward svc/demo 8000:8000
docker build -t demo:v2 .
kind load docker-image demo:v2 --name speedtest-cluster
helm upgrade demo ./helm/demo
k port-forward svc/demo 8000:8000
helm history demo
helm rollback demo 1
```
