# Quick Reference

> Fast lookup for common issues and their playbooks.

## Kubernetes Quick Reference

### Pod Issues

| Symptom | Playbook | CLI Check |
|---------|----------|-----------|
| Pod stuck in `Pending` | [PendingPods](/k8s/03-pods?id=pendingpods) | `kubectl describe pod <name>` |
| Pod in `CrashLoopBackOff` | [CrashLoopBackOff](/k8s/03-pods?id=crashloopbackoff) | `kubectl logs <pod> --previous` |
| Pod in `ImagePullBackOff` | [ImagePullBackOff](/k8s/03-pods?id=imagepullbackoff) | `kubectl describe pod <name>` |
| Pod `OOMKilled` | [OOMKilled](/k8s/03-pods?id=oomkilled) | `kubectl describe pod <name>` |
| Pod stuck `Terminating` | [Terminating](/k8s/03-pods?id=terminating) | `kubectl delete pod <name> --force` |

### Node Issues

| Symptom | Playbook | CLI Check |
|---------|----------|-----------|
| Node `NotReady` | [NodeNotReady](/k8s/02-nodes?id=nodenotready) | `kubectl describe node <name>` |
| Node disk pressure | [DiskPressure](/k8s/02-nodes?id=diskpressure) | `kubectl describe node <name>` |
| Node memory pressure | [MemoryPressure](/k8s/02-nodes?id=memorypressure) | `kubectl top node` |
| Node unreachable | [NodeUnreachable](/k8s/02-nodes?id=unreachable) | `kubectl get nodes` |

### Networking Issues

| Symptom | Playbook | CLI Check |
|---------|----------|-----------|
| Service not accessible | [ServiceNotAccessible](/k8s/05-networking?id=servicenotaccessible) | `kubectl get endpoints <svc>` |
| DNS not resolving | [DNSResolution](/k8s/05-networking?id=dnsresolution) | `kubectl run test --image=busybox -- nslookup <svc>` |
| Ingress returning 502 | [Ingress502](/k8s/05-networking?id=ingress502) | `kubectl describe ingress <name>` |
| CoreDNS down | [CoreDNSDown](/k8s/05-networking?id=corednsdown) | `kubectl get pods -n kube-system -l k8s-app=kube-dns` |

### Workload Issues

| Symptom | Playbook | CLI Check |
|---------|----------|-----------|
| Deployment not updating | [DeploymentNotUpdating](/k8s/04-workloads?id=deploymentnotupdating) | `kubectl rollout status deployment/<name>` |
| HPA not scaling | [HPANotScaling](/k8s/04-workloads?id=hpanotscaling) | `kubectl describe hpa <name>` |
| Job failing | [JobFailing](/k8s/04-workloads?id=jobfailing) | `kubectl describe job <name>` |
| DaemonSet not running on all nodes | [DaemonSetNotRunning](/k8s/04-workloads?id=daemonsetnotrunning) | `kubectl get ds <name> -o wide` |

### Storage Issues

| Symptom | Playbook | CLI Check |
|---------|----------|-----------|
| PVC stuck `Pending` | [PVCPending](/k8s/06-storage?id=pvcpending) | `kubectl describe pvc <name>` |
| Volume mount failed | [VolumeMountFailed](/k8s/06-storage?id=volumemountfailed) | `kubectl describe pod <name>` |

---

## AWS Quick Reference

### Compute

| Symptom | Playbook | CLI Check |
|---------|----------|-----------|
| EC2 unreachable | [ConnectionTimeout](/aws/01-compute?id=connectiontimeout) | `aws ec2 describe-instance-status` |
| Lambda timeout | [LambdaTimeout](/aws/01-compute?id=lambdatimeout) | `aws logs filter-log-events` |
| ECS task failing | [ECSTaskFailing](/aws/01-compute?id=ecstaskfailing) | `aws ecs describe-tasks` |
| Auto Scaling not working | [AutoScalingNotWorking](/aws/01-compute?id=autoscalingnotworking) | `aws autoscaling describe-scaling-activities` |

### Database

| Symptom | Playbook | CLI Check |
|---------|----------|-----------|
| RDS connection failed | [RDSConnectionFailed](/aws/02-database?id=rdsconnectionfailed) | `aws rds describe-db-instances` |
| DynamoDB throttling | [DynamoDBThrottling](/aws/02-database?id=dynamodbthrottling) | `aws cloudwatch get-metric-statistics` |

### Storage

| Symptom | Playbook | CLI Check |
|---------|----------|-----------|
| S3 access denied | [S3AccessDenied](/aws/03-storage?id=s3accessdenied) | `aws s3api get-bucket-policy` |
| S3 slow performance | [S3SlowPerformance](/aws/03-storage?id=s3slowperformance) | `aws s3api head-object` |

### Security

| Symptom | Playbook | CLI Check |
|---------|----------|-----------|
| IAM permission denied | [IAMPermissionDenied](/aws/05-security?id=iampermissiondenied) | `aws iam simulate-principal-policy` |
| KMS key access denied | [KMSAccessDenied](/aws/05-security?id=kmsaccessdenied) | `aws kms describe-key` |
| GuardDuty finding | [GuardDutyFinding](/aws/05-security?id=guarddutyfinding) | `aws guardduty list-findings` |

---

## Sentry Quick Reference

### Error Tracking

| Error Type | Playbook | Sentry Action |
|------------|----------|---------------|
| Unhandled exception | [UnhandledException](/sentry/01-error-tracking) | Check stack trace |
| Null pointer | [NullPointerException](/sentry/01-error-tracking) | Review variable state |
| Type error | [TypeError](/sentry/01-error-tracking) | Check input validation |

### Performance

| Issue | Playbook | Sentry Action |
|-------|----------|---------------|
| Slow transaction | [SlowTransaction](/sentry/02-performance) | Check spans |
| Timeout | [TimeoutError](/sentry/02-performance) | Review performance tab |
| High latency | [HighLatency](/sentry/02-performance) | Check database queries |

---

## Common kubectl Commands

```bash
# Get all pods in all namespaces
kubectl get pods -A

# Describe a resource
kubectl describe <resource> <name> -n <namespace>

# Get logs
kubectl logs <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --previous  # Previous container

# Get events sorted by time
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Execute into a pod
kubectl exec -it <pod> -n <namespace> -- /bin/sh

# Check resource usage
kubectl top pods -n <namespace>
kubectl top nodes

# Force delete stuck pod
kubectl delete pod <name> -n <namespace> --force --grace-period=0
```

## Common AWS CLI Commands

```bash
# EC2
aws ec2 describe-instances --instance-ids <id>
aws ec2 describe-instance-status --instance-ids <id>

# RDS
aws rds describe-db-instances --db-instance-identifier <id>

# Lambda
aws lambda get-function --function-name <name>
aws logs filter-log-events --log-group-name /aws/lambda/<name>

# S3
aws s3 ls s3://<bucket>
aws s3api get-bucket-policy --bucket <bucket>

# IAM
aws iam get-user
aws iam simulate-principal-policy --policy-source-arn <arn> --action-names <action>
```
