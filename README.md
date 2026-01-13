# SRE Playbooks Repository

This repository contains comprehensive incident response playbooks for **AWS** and **Kubernetes (K8s)** environments. These playbooks are designed to help Site Reliability Engineers (SREs) systematically diagnose and resolve common infrastructure and application issues.

## Repository Structure

```
scoutflo-SRE-Playbooks/
├── AWS Playbooks/          # 25 AWS service playbooks
│   └── README.md          # AWS playbooks documentation
├── K8s Playbooks/         # 138 Kubernetes playbooks
│   └── README.md          # Kubernetes playbooks documentation
└── README.md              # This file
```

## Contents

### AWS Playbooks (`AWS Playbooks/`)
**25 playbooks** covering critical AWS services and common issues:
- **Compute Services**: EC2, Lambda, ECS, EKS
- **Networking**: VPC, ELB, Route 53, NAT Gateway
- **Storage**: S3, EBS, RDS
- **Security**: IAM, KMS, GuardDuty, CloudTrail
- **Integration**: API Gateway, CodePipeline

**Key Topics:**
- Connection timeouts and network issues
- Access denied and permission problems
- Resource unavailability and capacity issues
- Security breaches and threat detection
- Service integration failures

See [AWS Playbooks/README.md](AWS%20Playbooks/README.md) for complete documentation.

### Kubernetes Playbooks (`K8s Playbooks/`)
**138 playbooks** covering Kubernetes cluster and workload issues:
- **Control Plane**: API Server, Scheduler, Controller Manager
- **Nodes**: Node readiness, kubelet issues, resource constraints
- **Pods**: Scheduling, lifecycle, health checks, resource limits
- **Workloads**: Deployments, StatefulSets, DaemonSets, Jobs
- **Networking**: Services, Ingress, DNS, Network Policies
- **Storage**: PersistentVolumes, PersistentVolumeClaims
- **RBAC**: ServiceAccounts, Roles, RoleBindings
- **Monitoring**: Metrics Server, HPA, resource quotas
- **Autoscaling**: Cluster Autoscaler, HPA scaling

**Key Topics:**
- Pod lifecycle issues (CrashLoopBackOff, Pending, Terminating)
- Control plane component failures
- Network connectivity and DNS resolution
- Storage and volume mounting problems
- RBAC and permission errors
- Resource quota and capacity constraints

See [K8s Playbooks/README.md](K8s%20Playbooks/README.md) for complete documentation.

## Common Playbook Structure

Both AWS and K8s playbooks follow a consistent structure:

### 1. **Title**
Clear, descriptive title identifying the issue

### 2. **Meaning**
Comprehensive explanation of:
- What the issue means
- Common symptoms and error messages
- Which service/component is affected
- Typical root causes

### 3. **Impact**
Description of:
- Service availability implications
- User-facing effects
- Related alarms or alerts
- Cascading effects on dependent services

### 4. **Playbook**
Numbered, actionable diagnostic steps:
- Ordered from most common to specific causes
- Includes resource identifiers (placeholders like `<instance-id>`, `<pod-name>`)
- References specific AWS services or Kubernetes resources
- Provides clear commands and checks

### 5. **Diagnosis**
Correlation analysis framework:
- Time-based correlation between events and symptoms
- Comparison of configuration changes with failure timestamps
- Patterns to determine constant vs. intermittent issues
- Guidance for extending time windows
- Alternative evidence sources

## Quick Start

### For AWS Issues:
1. Navigate to `AWS Playbooks/`
2. Find the playbook matching your issue
3. Follow the numbered steps, replacing placeholders with your actual resource identifiers
4. Use the Diagnosis section for root cause analysis

### For Kubernetes Issues:
1. Navigate to `K8s Playbooks/`
2. Find the playbook matching your issue (search by resource type suffix)
3. Follow the numbered steps, replacing placeholders with your actual resource names
4. Use the Diagnosis section for correlation analysis

## Usage Guidelines

### General Best Practices:
1. **Start Early**: Begin with the most common causes (earlier steps in Playbook section)
2. **Replace Placeholders**: All playbooks use placeholders (e.g., `<instance-id>`, `<pod-name>`) that must be replaced with actual values
3. **Follow Order**: Execute steps sequentially unless you have strong evidence pointing to a specific step
4. **Correlate Timestamps**: Use the Diagnosis section to correlate events with failures
5. **Extend Windows**: If initial correlations don't reveal causes, extend time windows as suggested
6. **Document Findings**: Keep notes of what you've checked and what you found

### AWS-Specific:
- Use CloudWatch Logs Insights for efficient log analysis
- Check AWS service health dashboards
- Review CloudTrail events for configuration changes
- Verify IAM permissions and resource policies

### Kubernetes-Specific:
- Use `kubectl describe` for detailed resource information
- Check `kubectl get events` for recent events
- Review pod logs with `kubectl logs`
- Inspect node conditions and resource availability
- Check scheduler logs for scheduling issues

## Placeholder Reference

### AWS Playbooks:
- `<instance-id>` - EC2 instance identifier
- `<bucket-name>` - S3 bucket name
- `<region>` - AWS region
- `<function-name>` - Lambda function name
- `<role-name>` - IAM role name
- `<user-name>` - IAM user name
- `<security-group-id>` - Security group identifier
- `<vpc-id>` - VPC identifier
- `<rds-instance-id>` - RDS instance identifier
- `<load-balancer-name>` - Load balancer name

### Kubernetes Playbooks:
- `<pod-name>` - Pod name
- `<namespace>` - Kubernetes namespace
- `<deployment-name>` - Deployment name
- `<node-name>` - Node name
- `<service-name>` - Service name
- `<ingress-name>` - Ingress name

## Contributing

When adding new playbooks:
1. Follow the established structure (Title, Meaning, Impact, Playbook, Diagnosis)
2. Use consistent placeholder naming
3. Order steps from most common to specific
4. Include time-based correlation guidance in Diagnosis section
5. Provide alternative evidence sources if initial correlations fail

## Statistics

- **Total Playbooks**: 163
  - AWS: 25 playbooks
  - Kubernetes: 138 playbooks
- **Coverage**: Major AWS services and Kubernetes components
- **Format**: Markdown with structured sections
- **Language**: English

## Related Resources

### AWS
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Troubleshooting Guides](https://docs.aws.amazon.com/general/latest/gr/aws_troubleshooting.html)

### Kubernetes
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Troubleshooting](https://kubernetes.io/docs/tasks/debug/)

## License

This repository contains operational playbooks for internal use. Please refer to your organization's documentation policies for usage and distribution guidelines.
