
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


Question? do not install prometheus operator or kube-prometheus-stack  both

## Thank you so much for your time

## Problem

we need to know what is hapenning in the system and why is it happening. for the 3 kubernetes and more tahn 10 pods and microservices with databases. Prometheus and grafana help you detect and investigate the problem before or while users are affected. Proemehtus collects and stores metrics. Grafana visulizes those metrics.

## Solution

<img width="859" height="427" alt="image" src="https://github.com/user-attachments/assets/9e13c7e1-a261-487b-b6d6-53a73ff71269" />

<img width="1328" height="677" alt="image" src="https://github.com/user-attachments/assets/487bff4a-aa72-43cb-968f-deffad960ce4" />
