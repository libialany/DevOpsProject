#!/bin/bash
echo "<h1>123</h1>" | sudo tee /tmp/index.html

sudo apt-get update -y && sudo apt-get install -y apt-transport-https curl ca-certificates gpg

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" -o /tmp 
sudo chmod +x kubectl
sudo mv kubectl /usr/local/bin/kubectl

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update -y 
sudo apt-get install -y kubelet kubeadm
sudo apt-mark hold kubelet kubeadm
