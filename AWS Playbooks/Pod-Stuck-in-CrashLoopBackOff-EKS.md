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

1. Compare pod creation or configuration change timestamps with crash loop start timestamps within 5 minutes and verify whether crash loops began after pod configuration changes, using EKS pod events as supporting evidence.
2. Correlate application error timestamps with pod restart timestamps and verify whether application errors caused repeated pod crashes, using pod logs as supporting evidence.
3. Compare resource limit modification timestamps with pod crash timestamps within 5 minutes and verify whether resource limit changes caused pod crashes, using pod resource metrics as supporting evidence.
4. Compare EKS node group health change timestamps with pod crash timestamps and verify whether node group issues caused pod failures, using EKS node group events as supporting evidence.
5. Analyze crash loop frequency over the last 15 minutes to determine if crashes are constant (application bug) or intermittent (resource constraints).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including node-level logs and cluster events, check for gradual issues like node resource exhaustion, verify external dependencies like external service availability, examine historical patterns of pod crashes, check for EKS managed node groups vs self-managed differences, verify EKS Windows node scenarios. Crash loops may result from node-level issues, image pull failures, persistent volume mount problems, EKS cluster version incompatibilities, or EKS add-on issues rather than immediate pod configuration changes.
