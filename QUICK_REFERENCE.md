# Quick Reference Card

One-page cheat sheet for SRE Playbooks.

## 🚀 Quick Start

```
1. Identify Issue → AWS or Kubernetes?
2. Find Playbook → Match symptoms to title
3. Follow Steps → Replace placeholders
4. Use Diagnosis → Correlate events
5. Apply Fix → Document findings
```

## 📁 Repository Structure

```
scoutflo-SRE-Playbooks/
├── AWS Playbooks/          (158 playbooks in 8 folders)
│   ├── 01-Compute/         (27) - EC2, Lambda, ECS, EKS
│   ├── 02-Database/        (8)  - RDS, DynamoDB
│   ├── 03-Storage/         (7)  - S3
│   ├── 04-Networking/      (17) - VPC, ELB, Route53
│   ├── 05-Security/        (16) - IAM, KMS, GuardDuty
│   ├── 06-Monitoring/      (8)  - CloudTrail, CloudWatch
│   ├── 07-CI-CD/           (9)  - CodePipeline
│   └── 08-Proactive/       (66) - Proactive monitoring
├── K8s Playbooks/          (233 playbooks in 13 folders)
│   ├── 01-Control-Plane/   (18)
│   ├── 02-Nodes/           (12)
│   ├── 03-Pods/            (31) ⭐ Most common
│   ├── 04-Workloads/       (23)
│   ├── 05-Networking/      (19)
│   ├── 06-Storage/         (9)
│   ├── 07-RBAC/            (6)
│   ├── 08-Configuration/   (6)
│   ├── 09-Resource-Management/ (8)
│   ├── 10-Monitoring-Autoscaling/ (3)
│   ├── 11-Installation-Setup/ (1)
│   ├── 12-Namespaces/      (2)
│   └── 13-Proactive/       (56) - Proactive monitoring
└── Sentry Playbooks/       (25 playbooks in 3 folders)
    ├── 01-Error-Tracking/  (19)
    ├── 02-Performance/     (6)
    └── 03-Release-Health/  (placeholder)
```

## 🔍 Finding the Right Playbook

| Issue Type | Category | Example Playbook |
|------------|----------|-----------------|
| Pod crashing | `03-Pods/` | `CrashLoopBackOff-pod.md` |
| Pod not starting | `03-Pods/` | `PendingPods-pod.md` |
| Service not working | `05-Networking/` | `ServiceNotAccessible-service.md` |
| Permission denied | `07-RBAC/` | `RBACPermissionDeniedError-rbac.md` |
| Volume mount failed | `06-Storage/` | `PVCPendingDueToStorageClassIssues-storage.md` |
| Deployment not scaling | `04-Workloads/` | `DeploymentNotScalingProperly-deployment.md` |
| Node not ready | `02-Nodes/` | `KubeNodeNotReady-node.md` |
| API Server down | `01-Control-Plane/` | `KubeAPIDown-control-plane.md` |
| EC2 SSH timeout | `AWS Playbooks/` | `Connection-Timeout-SSH-Issues-EC2.md` |
| RDS connection failed | `AWS Playbooks/` | `Connection-Timeout-from-Lambda-RDS.md` |
| Sentry error | `01-Error-Tracking/` | `UnhandledException-Error-application.md` |
| API timeout | `02-Performance/` | `TimeoutError-RequestTimeout-API-Error-application.md` |
| AWS cost issue | `08-Proactive/04-Cost-Optimization/` | `Cost-Anomaly-Detection-AWS.md` |
| K8s capacity | `13-Proactive/01-Capacity-Performance/` | `Capacity-Trend-Analysis-K8s.md` |

## 🔧 Common Commands

### Kubernetes

```bash
# Pods
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous

# Services
kubectl get services -n <namespace>
kubectl describe service <service-name> -n <namespace>

# Nodes
kubectl get nodes
kubectl describe node <node-name>

# Events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Resource usage
kubectl top pods -n <namespace>
kubectl top nodes
```

### AWS

```bash
# EC2
aws ec2 describe-instances --instance-ids <instance-id>
aws ec2 describe-security-groups --group-ids <sg-id>

# RDS
aws rds describe-db-instances --db-instance-identifier <id>

# Lambda
aws lambda get-function-configuration --function-name <name>

# CloudWatch Logs
aws logs tail <log-group-name> --follow
```

## 📝 Placeholder Reference

### AWS
- `<instance-id>` - EC2 instance ID
- `<bucket-name>` - S3 bucket name
- `<region>` - AWS region (e.g., us-east-1)
- `<function-name>` - Lambda function name
- `<vpc-id>` - VPC identifier

### Kubernetes
- `<pod-name>` - Pod name
- `<namespace>` - Kubernetes namespace
- `<deployment-name>` - Deployment name
- `<node-name>` - Node name
- `<service-name>` - Service name

## 🎯 Playbook Structure

Every playbook has:
1. **Title** - Issue identification
2. **Meaning** - What the issue means
3. **Impact** - Business/technical impact
4. **Playbook** - 8-10 diagnostic steps
5. **Diagnosis** - Correlation analysis

## ⚡ Quick Troubleshooting

### Pod Issues
```
Pod crashing? → 03-Pods/CrashLoopBackOff-pod.md
Pod pending? → 03-Pods/PendingPods-pod.md
Image pull failed? → 03-Pods/ImagePullBackOff-registry.md
```

### Network Issues
```
Service not accessible? → 05-Networking/ServiceNotAccessible-service.md
DNS not resolving? → 05-Networking/ServiceNotResolvingDNS-dns.md
Ingress not working? → 05-Networking/IngressNotWorking-ingress.md
```

### Resource Issues
```
Quota exceeded? → 09-Resource-Management/KubeQuotaExceeded-namespace.md
Node disk full? → 02-Nodes/NodeDiskPressure-storage.md
High CPU? → 09-Resource-Management/HighCPUUsage-compute.md
```

## 🔗 Essential Links

- **Main README**: [README.md](README.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **FAQ**: [FAQ.md](FAQ.md)
- **Examples**: [EXAMPLES.md](EXAMPLES.md)
- **Support**: [.github/SUPPORT.md](.github/SUPPORT.md)

## 📚 Resources

- **Kubernetes Docs**: https://kubernetes.io/docs/
- **AWS Docs**: https://docs.aws.amazon.com/
- **Scoutflo Docs**: https://scoutflo-documentation.gitbook.io/scoutflo-documentation
- **YouTube**: https://www.youtube.com/@scoutflo6727

## 🆘 Getting Help

- **GitHub Discussions**: Ask questions
- **GitHub Issues**: Report bugs
- **Slack**: Join community
- **Email**: security@scoutflo.com (security issues)

## 💡 Pro Tips

1. **Bookmark** frequently used playbooks
2. **Clone locally** for offline access
3. **Customize** for your environment
4. **Contribute** improvements back
5. **Share** with your team

---

**Print this page** and keep it handy! 📄
