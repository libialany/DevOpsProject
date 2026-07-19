# OOM Pod Kill Experiment

## Environment

- [simple eks](https://github.com/libialany/DevOpsProject/tree/feat/k8s-hello-wordl)

## State of the app

- Custom Log Groups (Using Fluent Bit Annotations)
By default, the AWS add-on dumps all app logs into one massive log group (usually `/aws/eks/<cluster-name>/workloads`). If you want to separate logs into **custom log groups** (e.g., `/my-app/frontend`, `/my-app/backend`), you can use Kubernetes annotations on your Pods/Deployments.

Add these annotations to your Pod template metadata:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    metadata:
      annotations:
        # Tells Fluent Bit to send this pod's logs to a specific log group
        fluentbit.io/log-group-name: "/my-custom-app-group"
        # Optional: Specify a specific log stream name
        fluentbit.io/log-stream-name: "frontend-pods"
    spec:
      containers: ...
```
*(Note: For custom annotations to work, you may need to modify the Fluent Bit ConfigMap included in the add-on to enable the `kubernetes` filter to parse these annotations).*


*   **Application Logs:** `/aws/eks/<cluster-name>/workloads` (or `/aws/containerinsights/<cluster-name>/application`)

## Experiment

```
resource "aws_fis_experiment_template" "pod_memory_stress" {
  description = "Memory stress test against EKS application pods"

  role_arn = aws_iam_role.fis_role.arn

  stop_condition {
    source = "none"
  }

  target {
    name           = "target-pods"
    resource_type  = "aws:eks:pod"
    selection_mode = "COUNT(1)"

    parameters = {
      clusterIdentifier = aws_eks_cluster.main.name
      namespace         = "production"

      # Choose ONE targeting method:

      # Option 1 - Label selector
      selectorType  = "labelSelector"
      labelSelector = "app=my-api"

      # Option 2 - Deployment
      # selectorType = "deploymentName"
      # selectorValue = "my-api"

      # Option 3 - Pod name
      # selectorType = "podName"
      # selectorValue = "my-api-7bdbb86f95-xxxxx"
    }
  }

  action {
    name      = "memory-stress"
    action_id = "aws:eks:pod-memory-stress"

    target {
      key   = "Pods"
      value = "target-pods"
    }

    parameters = {
      duration = "PT5M"

      # Percent of available memory to consume
      percent = "80"

      # Number of stress workers
      workers = "2"
    }
  }

  tags = {
    Name        = "pod-memory-stress"
    Environment = "prod"
    Chaos       = "true"
  }
}

```
Update by increasing the count(number of replicas).

**Objetive*  show how much our infraestructure can resist.

*What could happen* 2 pods can died and the app is still responding.

## Result

Cloddwatch log groups 

```
aws fis get-experiment \
  --id EXPERIMENT_ID \
  --query "experiment.startTime" \
  --output text
# result START=$(date -d "2026-07-19T14:31:10Z" +%s000)
```

and the use aws cli:

```
aws logs filter-log-events \
  --log-group-name "/aws/fis/experiments" \
  --start-time $START \
  --query "events[].message" \
  --output text > fis-experiment-report.txt

```

### How to Query the Logs (CloudWatch Logs Insights)
Because EKS logs are unstructured by default, the best way to search them is using **CloudWatch Logs Insights**.

1. Go to **CloudWatch -> Logs -> Logs Insights**.
2. Select your EKS application log group (e.g., `/aws/eks/my-cluster/workloads`).
3. Use the following query examples:

**Find all ERROR logs across the cluster:**
```sql
fields @timestamp, @message, kubernetes.pod_name, kubernetes.namespace_name
| filter @message like /error/i or @message like /exception/i
| sort @timestamp desc
| limit 100
```

**Find logs for a specific Kubernetes Namespace:**
```sql
fields @timestamp, @message, kubernetes.pod_name
| filter kubernetes.namespace_name = "production"
| sort @timestamp desc
```

**Find logs for a specific Pod:**
```sql
fields @timestamp, @message
| filter kubernetes.pod_name like /my-app-deployment-abc123/
| sort @timestamp desc
```

**IAM Permissions:** 

Ensure the IAM Role attached to your EKS Node Group (or IRSA role if using Fargate) has the `CloudWatchAgentServerPolicy` attached, otherwise the agent will fail to push logs.

## Inform 

[Chaos daily report](https://www.cncf.io/blog/2022/03/01/develop-a-daily-reporting-system-for-chaos-mesh-to-improve-system-resilience/)