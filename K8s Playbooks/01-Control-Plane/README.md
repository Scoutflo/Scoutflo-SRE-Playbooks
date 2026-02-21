# Control Plane Playbooks

This folder contains **24 playbooks** for troubleshooting Kubernetes control plane component issues.

## What is the Control Plane?

The control plane is the brain of your Kubernetes cluster. It manages the cluster's state, schedules pods, and coordinates all cluster activities. Key components include:

- **API Server**: The front-end for the Kubernetes control plane
- **Scheduler**: Assigns pods to nodes
- **Controller Manager**: Runs controller processes
- **etcd**: Consistent and highly-available key-value store

## Common Issues Covered

- API Server high latency or downtime
- Scheduler failures
- Controller Manager problems
- Certificate expiration and management (cert-manager)
- Version mismatches
- Upgrade failures
- Client connection errors

## Playbooks in This Folder

1. `APIServerHighLatency-control-plane.md` - API Server responding slowly
2. `CannotAccessAPI-control-plane.md` - Cannot access Kubernetes API
3. `CertificateExpired-control-plane.md` - Control plane certificates expired
4. `ConnectionRefused-control-plane.md` - Connection refused to control plane
5. `ContextDeadlineExceeded-control-plane.md` - API requests timing out
6. `ControlPlaneComponentsNotStarting-control-plane.md` - Control plane components failing to start
7. `KubeAggregatedAPIDown-control-plane.md` - Aggregated API server down
8. `KubeAggregatedAPIErrors-control-plane.md` - Aggregated API server errors
9. `KubeAPIDown-control-plane.md` - Kubernetes API server down
10. `KubeAPIErrorBudgetBurn-control-plane.md` - API error rate too high
11. `KubeAPITerminatedRequests-control-plane.md` - API requests being terminated
12. `KubeClientCertificateExpiration-control-plane.md` - Client certificates expiring
13. `KubeClientErrors-control-plane.md` - Client connection errors
14. `KubeControllerManagerDown-control-plane.md` - Controller Manager down
15. `KubeSchedulerDown-control-plane.md` - Scheduler down
16. `KubeVersionMismatch-control-plane.md` - Component version mismatches
17. `Timeout-control-plane.md` - Control plane timeouts
18. `UpgradeFails-control-plane.md` - Cluster upgrade failures
19. `CertificateExpiringCritical-cert.md` - Certificate expiring critically soon
20. `CertificateExpiringSoon-cert.md` - Certificate expiring soon warning
21. `CertificateNotReady-cert.md` - Certificate not ready
22. `CertManagerACMEOrderFailed-cert.md` - Cert-manager ACME order failed
23. `CertManagerControllerHighError-cert.md` - Cert-manager controller high error rate
24. `CertManagerDown-cert.md` - Cert-manager down

## Quick Start

If you're experiencing control plane issues:

1. **Check API Server**: Start with `KubeAPIDown-control-plane.md` or `APIServerHighLatency-control-plane.md`
2. **Certificate Issues**: See `CertificateExpired-control-plane.md`
3. **Component Failures**: Check `KubeSchedulerDown-control-plane.md` or `KubeControllerManagerDown-control-plane.md`
4. **Upgrade Problems**: See `UpgradeFails-control-plane.md`

## Related Categories

- **02-Nodes/**: Node-level issues that might affect control plane communication
- **07-RBAC/**: Authorization issues that might appear as API problems

## Understanding Playbook Steps

**Important**: These playbooks are designed for **AI agents** using natural language processing. The playbook steps use natural language instructions like:

- "Retrieve the Pod `<pod-name>` in namespace `kube-system` with label `component=kube-apiserver` and inspect its status"
- "Retrieve logs from the Pod `<pod-name>` in namespace `kube-system` and filter for error patterns"

AI agents interpret these instructions and execute the appropriate actions using available tools (like Kubernetes MCP tools or kubectl).

### Manual Verification Commands

If you need to manually verify or troubleshoot (outside of AI agent usage), here are equivalent kubectl commands:

**Basic Status Checks:**
```bash
# Check API Server status
kubectl get componentstatuses

# Check control plane pods
kubectl get pods -n kube-system

# Check all control plane components
kubectl get pods -n kube-system -l component=kube-apiserver
kubectl get pods -n kube-system -l component=kube-scheduler
kubectl get pods -n kube-system -l component=kube-controller-manager

# Check API Server health
kubectl get --raw /healthz
kubectl get --raw /readyz
```

**Logs and Debugging:**
```bash
# Check API Server logs
kubectl logs -n kube-system kube-apiserver-<node-name>

# Check Scheduler logs
kubectl logs -n kube-system kube-scheduler-<node-name>

# Check Controller Manager logs
kubectl logs -n kube-system kube-controller-manager-<node-name>

# Check etcd status and logs
kubectl get pods -n kube-system | grep etcd
kubectl logs -n kube-system etcd-<node-name>
```

**API Server Information:**
```bash
# Check API Server version
kubectl version --short

# Check API resources
kubectl api-resources

# Test API connectivity
kubectl cluster-info
```

## Best Practices

### Control Plane Health
- **Monitor API Server**: Set up alerts for API Server latency and error rates
- **Certificate Management**: Implement automated certificate rotation
- **Version Consistency**: Keep all control plane components on the same version
- **Resource Limits**: Set appropriate resource requests/limits for control plane pods
- **High Availability**: Run multiple API Server instances for HA

### Troubleshooting Tips
- **Start with API Server**: Most issues manifest as API Server problems
- **Check Logs First**: Control plane logs provide detailed error information
- **Verify Network**: Ensure control plane components can communicate
- **Check Certificates**: Expired certificates are a common cause of issues
- **Review Events**: Use `kubectl get events` to see recent control plane events

### Performance Optimization
- **API Server**: Monitor request rates and adjust `--max-requests-inflight` if needed
- **etcd**: Monitor etcd performance and consider tuning for large clusters
- **Scheduler**: Review scheduling latency metrics
- **Controller Manager**: Monitor controller reconciliation times

## Additional Resources

### Official Documentation
- [Kubernetes Control Plane Components](https://kubernetes.io/docs/concepts/overview/components/) - Component overview
- [API Server Troubleshooting](https://kubernetes.io/docs/tasks/debug/) - Debugging guide
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/) - Complete API docs
- [Control Plane Security](https://kubernetes.io/docs/concepts/security/controlling-access/) - Security best practices

### Learning Resources
- [Kubernetes Control Plane Deep Dive](https://kubernetes.io/docs/concepts/overview/components/#control-plane-components) - Component details
- [etcd Documentation](https://etcd.io/docs/) - etcd cluster management
- [API Server Configuration](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/) - Configuration options

### Tools & Utilities
- [kube-apiserver Metrics](https://kubernetes.io/docs/reference/instrumentation/metrics/) - Available metrics
- [kubectl debug](https://kubernetes.io/docs/tasks/debug/) - Debugging tools
- [kubeadm Troubleshooting](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/) - kubeadm issues

### Community Resources
- [Kubernetes Slack #sig-api-machinery](https://slack.k8s.io/) - API machinery discussions
- [Stack Overflow - Kubernetes Control Plane](https://stackoverflow.com/questions/tagged/kubernetes+control-plane) - Q&A

[Back to Main K8s Playbooks](../README.md)
