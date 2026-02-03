# EKS Pod Stuck in CrashLoopBackOff

## Meaning

EKS pods enter CrashLoopBackOff state (triggering pod restart failures or KubePodCrashLooping alerts) because pod logs show application errors, pod configuration has issues, resource limits are exceeded, application inside pod is unhealthy, pod dependencies fail, pod restart attempts fail repeatedly, or EKS node group issues prevent pod stability. Pods continuously crash and restart, applications are unavailable, and pod status shows CrashLoopBackOff indefinitely. This affects the container orchestration layer and prevents pod execution, typically caused by application errors, resource constraints, or EKS configuration issues; if using EKS managed node groups vs self-managed, troubleshooting approaches differ and container applications may experience startup failures.

## Impact

Pods continuously crash and restart; applications are unavailable; CrashLoopBackOff state persists; pod restart failures occur; application errors increase; container workloads cannot stabilize; service endpoints become unreliable; pod health checks fail; application deployments fail. KubePodCrashLooping alerts fire; if using EKS managed node groups vs self-managed, node group issues may affect pod stability; applications may experience errors or performance degradation due to pod failures; container orchestration tasks may show failures.

## Playbook

1. Verify EKS cluster exists and pod `<pod-name>` is in the cluster, and AWS service health for EKS in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing EKS pod logs or EKS events for pod `<pod-name>` and filter for error patterns, crash messages, application failures, pod events, or configuration issues, including container exit codes and pod scheduling failures.
3. Query CloudWatch Logs for log groups containing EKS pod metrics and filter for resource limit errors or resource exhaustion messages for pod `<pod-name>`, including CPU and memory limits.
4. Query CloudWatch Logs for log groups containing application logs for pod `<pod-name>` and filter for health check failures or application errors, including application startup failures.
5. Retrieve the EKS Cluster `<cluster-name>` node group configuration and verify node group health and capacity, checking if node group issues affect pod scheduling.
6. Retrieve the EKS Cluster `<cluster-name>` cluster version and verify cluster version compatibility with pod configuration, checking for version mismatches.
7. Retrieve the EKS Pod `<pod-name>` security policy configuration and verify Pod Security Standards compliance, checking if security policies block pod execution.
8. Retrieve the EKS Pod `<pod-name>` service account IAM role (IRSA) configuration and verify service account IAM role permissions, checking if IRSA issues affect pod startup.
9. Retrieve the EKS Cluster `<cluster-name>` node group type (managed vs self-managed) and verify node group configuration, checking if node group type affects troubleshooting.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify EKS service availability in the region. If service health indicates issues, pod crashes may be AWS-side requiring monitoring rather than configuration changes.

2. If pod logs from Playbook step 2 show application errors, stack traces, or crash messages, examine the exit codes and error patterns. Exit code 1 indicates application error; exit code 137 indicates OOMKilled; exit code 139 indicates segmentation fault.

3. If resource metrics from Playbook step 3 show memory usage approaching or exceeding limits before crashes, pods are being OOMKilled. Increase memory limits or optimize application memory usage.

4. If application logs from Playbook step 4 show health check failures or dependency connection errors, the application is failing readiness/liveness probes or cannot connect to required services. Verify probe configurations and dependency availability.

5. If node group configuration from Playbook step 5 shows nodes are unhealthy, NotReady, or at capacity, pod scheduling and execution are affected. Examine node group scaling and health status.

6. If cluster version from Playbook step 6 is incompatible with the pod's container images or Kubernetes API versions used in manifests, runtime failures occur. Verify compatibility between cluster version and workload requirements.

7. If Pod Security Standards from Playbook step 7 are enforced (restricted, baseline) and pod configuration violates these standards, pods cannot start. Verify securityContext, capabilities, and volume mounts comply with policies.

8. If IRSA configuration from Playbook step 8 shows the service account lacks required IAM permissions for AWS service access (S3, DynamoDB, Secrets Manager), applications fail when attempting AWS API calls.

9. If node group type from Playbook step 9 shows managed vs self-managed, troubleshooting approaches differ. Managed node groups have automated remediation; self-managed requires manual node investigation.

If no correlation is found from the collected data: extend log query timeframes to 1 hour, verify container image exists and is pullable (check for ImagePullBackOff preceding CrashLoopBackOff), examine persistent volume claims for mount failures, and check for Init container failures that prevent main container startup. Crash loops may result from ConfigMap/Secret mount failures, DNS resolution issues within the cluster, or CoreDNS problems affecting service discovery.

