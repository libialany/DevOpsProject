## Thank you so much for your time!! 
## Problem

The application consumes more memory than expected , which can effect other workloads on the node or cause the container to be terminated





<img width="603" height="229" alt="image" src="https://github.com/user-attachments/assets/27fa3bc6-74f3-46ea-b227-fddbed9d78ea" />


<img width="712" height="235" alt="image" src="https://github.com/user-attachments/assets/0b01ab33-d783-467c-859c-d683a760f025" />


## Solution
 

configure appropiate memory request than expected and limits so kubernetes can reserve workloads memory for the application and prevent it from consuming unlimiting resource .  I can execute these comand 

i use logs to theck the last logs 

```
k logs demo-75486f954-hwfq2  --previous 
```
describe the resources of the pod 
with this we loook for OOM killed error .
```
k describe pod demo-75486f954-hwfq2
k describe pod demo-75486f954-hwfq2
k describe deployment demo | grep Environment
```

describe the atributes of the service:

```
k describe deployment demo | grep Mounts:
k describe deployment demo | grep Liveness:
k describe deployment demo | grep Readiness:
k top pods
```

finally  i  fix the problem . i redeploy the app  and watch the  logs and the deployment is working again.