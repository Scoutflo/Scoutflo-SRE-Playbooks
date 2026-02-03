# Multi-cluster Failover

## Meaning

Multi-cluster failover indicates that cross-cluster failover procedures cannot be executed or failover operations fail during disaster recovery scenarios (triggering alerts like FailoverFailed or MultiClusterFailoverFailed) because failover operations timeout, DNS failover does not occur, cross-cluster replication is not synchronized, failover health checks fail, or failover automation triggers do not activate. Failover operations show failed status, DNS records do not update to secondary cluster, cross-cluster replication shows lag or errors, and failover health checks indicate unhealthy state in secondary cluster. This affects the networking layer and disaster recovery infrastructure, typically caused by DNS propagation issues, replication lag problems, health check failures, or failover automation misconfiguration; if failover protects container workloads, container services may remain unavailable and applications may experience extended downtime.

## Impact

MultiClusterFailoverFailed alerts fire; FailoverFailed alerts fire; disaster recovery procedures cannot be executed; RTO targets cannot be met; services remain unavailable in primary cluster; DNS failover does not occur; cross-cluster replication is not synchronized; failover health checks fail. Failover operations remain in pending or failed state; DNS records do not update to secondary cluster endpoints; if failover protects container workloads, container services may remain unavailable, pod scheduling may fail in secondary cluster, and container applications may experience extended downtime; applications may experience extended service unavailability or data loss.

## Playbook

1. List ingress, services, and endpoints in namespace <namespace> with wide output and describe ingress <ingress-name> in namespace <namespace> to understand the failover configuration and current cluster routing state.

2. List recent events in namespace <namespace> sorted by timestamp and list events in kube-system namespace filtered by involved object kind Ingress to identify any recent failover triggers or DNS update issues.

3. Retrieve ingress health check configuration for ingress `<ingress-name>` in namespace `<namespace>` and inspect its status, endpoint configuration, and failure threshold settings, verifying health check accessibility.

4. List services in namespace `<namespace>` and retrieve service endpoint configurations to verify failover endpoint configuration and current active cluster endpoints.

5. Retrieve Prometheus metrics for ingress health checks including ingress_health_status and ingress_health_failure_reason over the last 1 hour to identify health check failure patterns.

6. Retrieve logs from ingress controller pod in namespace `<namespace>` and filter for failover record change patterns or DNS update failures within the last 1 hour.

7. Retrieve cross-cluster replication status for resource `<resource-name>` and verify replication lag metrics, checking replication synchronization between primary and secondary clusters.

8. List active Prometheus alerts with state 'firing' in primary cluster `<primary-cluster>` and secondary cluster `<secondary-cluster>` to identify cluster service health differences.

9. Retrieve deployment `<deployment-name>` configuration in secondary cluster `<secondary-cluster>` and verify its replica count and pod health status, checking secondary cluster readiness.

10. Compare DNS record update timestamps with failover trigger timestamps within 5 minutes and verify whether DNS failover occurs within expected time windows, using ingress controller logs as supporting evidence.

## Diagnosis

1. Review the ingress health check configuration from Step 3. If health checks show failures or incorrect threshold settings, this is the most likely cause of failover issues. Verify health check endpoints are accessible and failure thresholds are appropriate.

2. Analyze the cross-cluster replication status from Step 7. If replication lag exceeds acceptable thresholds, then data consistency risks exist during failover. If replication is synchronized, proceed to secondary cluster readiness analysis.

3. If Step 5 health check metrics show failures, examine whether failures are in the primary cluster (should trigger failover) or secondary cluster (would prevent failover completion). If primary is failing but failover is not triggering, then automation configuration needs review.

4. Review secondary cluster deployment status from Step 9. If replica count is zero or pods are unhealthy, then the secondary cluster cannot accept traffic during failover. If secondary is ready but failover still fails, then DNS or routing configuration is the issue.

5. If Step 6 ingress controller logs show DNS update failures, then DNS propagation or permissions are preventing failover completion. If logs show no failover attempts, then failover triggers are not activating.

If analysis is inconclusive: Compare cluster health alerts from Step 8 to identify differences between primary and secondary cluster states. Review the failover trigger configuration and verify that health check failure thresholds are correctly calibrated to avoid false positives or missed failovers.
