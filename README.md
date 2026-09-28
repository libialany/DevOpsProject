
## Thank you so much for your time!!
## Problem

Both Blue-Green and Canary deployment solve the same broad production problem:

```
How can we release a new version without puttin all production users at risk?
```

Both deployments give you safer ways to introduce the new version.

### BG 
advanatges of BG is the rollback is fast because you have the old environment.
disadvantage it require additional infrastructure.

### Canary

if a deploy the v2 to 10% of users the errror rates increades from 0.2 to 5. I will stop the  or pause the rollout. 

## Rollouts 

gradually replace old pods with new pods

implementation is an ingress -> svc -> pods

## Solution

_for canary_

i would deploy the new version alonsige  the stable version route a small percentage of prod traffic to the new version, , monitor metrics such as error rate and latency with Prometheus, and progressively increase traffic if the metrics remain healthy. if the metric of error invrease  i will stop

_for BG_

i would deploy the version as separate enviromnet test it while the old version continues serving traffic , then switch the svc or traffic router to the new environment. If there is a problem, I can quickly swithc traffic back to the old environment.
