# Monitoring & Autoscaling Playbooks

This folder contains **3 playbooks** for troubleshooting Kubernetes monitoring and autoscaling issues.

## What is Monitoring & Autoscaling?

- **Metrics Server**: Collects resource metrics (CPU, memory) from nodes and pods
- **HPA (Horizontal Pod Autoscaler)**: Automatically scales pods based on metrics
- **Cluster Autoscaler**: Automatically adjusts cluster size based on demand
- **Monitoring**: Observability tools like Prometheus, Grafana

## Common Issues Covered

- Metrics Server not providing data
- Cluster Autoscaler not adding nodes
- Autoscaler scaling too slowly
- HPA not responding to metrics

## Playbooks in This Folder

1. `AutoscalerNotAddingNodes-autoscaler.md` - Cluster Autoscaler not adding nodes
2. `AutoscalerScalingTooSlowly-autoscaler.md` - Autoscaler scaling too slowly
3. `MetricsServerShowsNoData-monitoring.md` - Metrics Server showing no data

## Quick Start

If you're experiencing monitoring/autoscaling issues:

1. **No Metrics**: Start with `MetricsServerShowsNoData-monitoring.md`
2. **Autoscaler Not Working**: See `AutoscalerNotAddingNodes-autoscaler.md`
3. **Slow Scaling**: Check `AutoscalerScalingTooSlowly-autoscaler.md`

## Related Categories

- **04-Workloads/**: HPA and workload scaling issues
- **09-Resource-Management/**: Resource quota and capacity issues
- **02-Nodes/**: Node capacity issues affecting autoscaling

## Useful Commands

### Metrics Server
```bash
# Check Metrics Server
kubectl get pods -n kube-system | grep metrics-server

# Check Metrics Server logs
kubectl logs -n kube-system -l k8s-app=metrics-server

# Check Metrics Server API
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes

# Check node metrics
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes/<node-name>

# Check pod metrics
kubectl get --raw /apis/metrics.k8s.io/v1beta1/namespaces/<namespace>/pods
```

### Horizontal Pod Autoscaler (HPA)
```bash
# Check HPA status
kubectl get hpa -n <namespace>

# Describe HPA
kubectl describe hpa <hpa-name> -n <namespace>

# Check HPA metrics
kubectl get hpa <hpa-name> -n <namespace> -o yaml

# Check HPA events
kubectl describe hpa <hpa-name> -n <namespace> | grep -A 10 "Events:"

# Watch HPA in real-time
kubectl get hpa <hpa-name> -n <namespace> -w
```

### Resource Metrics
```bash
# Check node resource metrics
kubectl top nodes

# Check pod resource metrics
kubectl top pods -n <namespace>

# Check specific pod metrics
kubectl top pod <pod-name> -n <namespace>

# Check all namespaces
kubectl top pods --all-namespaces
```

### Cluster Autoscaler
```bash
# Check Cluster Autoscaler
kubectl get pods -n kube-system | grep cluster-autoscaler

# Check autoscaler logs
kubectl logs -n kube-system -l app=cluster-autoscaler

# Check autoscaler configuration
kubectl get deployment cluster-autoscaler -n kube-system -o yaml

# Check autoscaler status (if status endpoint available)
kubectl get --raw /api/v1/namespaces/kube-system/services/cluster-autoscaler:8085/proxy/status
```

### Custom Metrics (Prometheus Adapter)
```bash
# Check Prometheus Adapter
kubectl get pods -n kube-system | grep prometheus-adapter

# Check available custom metrics
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1

# Check specific custom metric
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1/namespaces/<namespace>/pods/*/<metric-name>
```

## Best Practices

### Metrics Server
- **High Availability**: Run multiple Metrics Server replicas
- **Resource Limits**: Set appropriate resource limits
- **Network Policies**: Ensure Metrics Server can reach nodes
- **Certificate Management**: Keep Metrics Server certificates valid

### HPA Configuration
- **Min/Max Replicas**: Set appropriate min and max replica counts
- **Metrics Selection**: Start with CPU/memory before custom metrics
- **Scaling Policies**: Configure scaling policies for smooth scaling
- **Cooldown Periods**: Set appropriate scale-down delays

### Cluster Autoscaler
- **Node Groups**: Configure appropriate node group sizes
- **Scaling Policies**: Set scaling policies for different node types
- **Pod Disruption Budgets**: Use PDBs to ensure availability during scaling
- **Cost Optimization**: Balance performance needs with cost

### Monitoring Best Practices
- **Metrics Collection**: Ensure comprehensive metrics collection
- **Alerting**: Set up alerts for autoscaler failures
- **Dashboard**: Create dashboards for autoscaling metrics
- **Review Regularly**: Review autoscaling behavior regularly

### Troubleshooting Tips
- **Metrics Availability**: Verify metrics are available for HPA
- **Scaling Events**: Check HPA events to understand scaling decisions
- **Node Capacity**: Ensure nodes have capacity or autoscaler can add nodes
- **Metrics Accuracy**: Verify metrics are accurate and timely
- **Autoscaler Logs**: Review autoscaler logs for scaling decisions

## Additional Resources

### Official Documentation
- [Metrics Server](https://github.com/kubernetes-sigs/metrics-server) - Metrics Server project
- [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) - HPA guide
- [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) - Cluster Autoscaler project
- [Custom Metrics](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#autoscaling-on-multiple-metrics-and-custom-metrics) - Custom metrics guide

### Learning Resources
- [HPA Walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) - HPA tutorial
- [Advanced HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#advanced-topics) - Advanced HPA topics
- [Autoscaling Best Practices](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-configurable-scaling-behavior) - Best practices

### Tools & Utilities
- [Prometheus Adapter](https://github.com/kubernetes-sigs/prometheus-adapter) - Custom metrics adapter
- [KEDA](https://keda.sh/) - Kubernetes Event-driven Autoscaling
- [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) - VPA for right-sizing

### Monitoring Tools
- [Prometheus](https://prometheus.io/) - Metrics collection
- [Grafana](https://grafana.com/) - Visualization
- [Kubecost](https://www.kubecost.com/) - Cost and resource monitoring

### Community Resources
- [Kubernetes Slack #sig-autoscaling](https://slack.k8s.io/) - Autoscaling discussions
- [Stack Overflow - Kubernetes HPA](https://stackoverflow.com/questions/tagged/kubernetes+hpa) - Q&A

[Back to Main K8s Playbooks](../README.md)
