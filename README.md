
Prometheus:

```
kubectl get svc
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts


helm repo update

kubectl create namespace monitoring

helm install monitoring \
prometheus-community/kube-prometheus-stack \
--namespace monitoring

kubectl get pods -n monitoring
```

Check these resources:

 - prometheus
 - grafana
 - alertmanager
 - node-exporter
 - kube-state-metrics
 - prometheus-operator

Service Monitoring:

[integrate prometheus index](./k8s/app-servicemonitor.yaml)

Check the services: 

```
 kubectl get svc -n monitoring
 kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090
 kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
 kubectl get secret \
 -n monitoring \
 monitoring-grafana \
 -o jsonpath="{.data.admin-password}" | base64 --decode
```