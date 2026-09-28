## Thank you so much for your time!!

## Problem

manually configuring the number of replicas. Considering the traffic isn't constant keeping all the pods running long hours and also reduce your billing cost.

## Solution

HPA  automatically changes the number of pod replicas based on observed metrcis such us CPU, memory, or custom/applicatin metrics. Yo configure the min and max number of pods HPA wil maintain. one important point is the tarjet. for example you setup averageUtilization: 70. It means HPA tries to maintainapproximately 70% average CPU utilization.

```
desired replicas =
current replicas × current metric / desired metric  ## 2 × 140 / 70 = 4
```
in the other hand vpa increase the resources allocated to a pod.

## Random


autoscaling/v2 es la versión estable y nativa actual de la API de Kubernetes para configurar el Horizontal Pod Autoscaler (HPA)