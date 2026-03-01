## Deploy app in our cluster 

- Microk8s and containers arm64
- test our armd64 container
- enhance your deplyment with helm

### HEML DEMO

```
#!/bin/bash

set -e

CHART_NAME="calibre-web"

echo "Creating Helm chart structure..."
mkdir -p $CHART_NAME/templates

########################################
# Chart.yaml
########################################
cat <<EOF > $CHART_NAME/Chart.yaml
apiVersion: v2
name: calibre-web
description: Calibre Web ARM64 deployment
type: application
version: 0.1.0
appVersion: "latest"
EOF

########################################
# values.yaml
########################################
cat <<EOF > $CHART_NAME/values.yaml
replicaCount: 1

image:
  repository: linuxserver/calibre-web
  tag: arm64v8-0.6.26
  pullPolicy: IfNotPresent

service:
  type: NodePort
  port: 8083
  nodePort: 30083

env:
  PUID: "1000"
  PGID: "1000"
  TZ: "Europe/London"

persistence:
  config:
    hostPath: /share/magazines/config
    mountPath: /config
  books:
    hostPath: /share/magazines/library
    mountPath: /books

resources: {}
EOF

########################################
# deployment.yaml
########################################
cat <<EOF > $CHART_NAME/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
        - name: calibre-web
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: 8083
          env:
            - name: PUID
              value: "{{ .Values.env.PUID }}"
            - name: PGID
              value: "{{ .Values.env.PGID }}"
            - name: TZ
              value: "{{ .Values.env.TZ }}"
          volumeMounts:
            - name: config
              mountPath: {{ .Values.persistence.config.mountPath }}
            - name: books
              mountPath: {{ .Values.persistence.books.mountPath }}
      volumes:
        - name: config
          hostPath:
            path: {{ .Values.persistence.config.hostPath }}
        - name: books
          hostPath:
            path: {{ .Values.persistence.books.hostPath }}
EOF

########################################
# service.yaml
########################################
cat <<EOF > $CHART_NAME/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}
spec:
  type: {{ .Values.service.type }}
  selector:
    app: {{ .Release.Name }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: 8083
      nodePort: {{ .Values.service.nodePort }}
EOF

########################################
# Install Chart
########################################
echo "Installing Helm chart..."
helm install $CHART_NAME ./$CHART_NAME

echo "Deployment complete."
echo "Access via: http://<NODE_IP>:30083"
```

test it: 
```
k get pods
k get svc
```



