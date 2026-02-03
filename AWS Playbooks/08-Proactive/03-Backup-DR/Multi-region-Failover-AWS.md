# Multi-region Failover

## Meaning

Multi-region failover indicates that cross-region failover procedures cannot be executed or failover operations fail during disaster recovery scenarios (triggering alarms like FailoverFailed or MultiRegionFailoverFailed) because failover operations timeout, DNS failover does not occur, cross-region replication is not synchronized, failover health checks fail, or failover automation triggers do not activate. Failover operations show failed status, DNS records do not update to secondary region, cross-region replication shows lag or errors, and failover health checks indicate unhealthy state in secondary region. This affects the networking layer and disaster recovery infrastructure, typically caused by DNS propagation issues, replication lag problems, health check failures, or failover automation misconfiguration; if failover protects container workloads, container services may remain unavailable and applications may experience extended downtime.

## Impact

MultiRegionFailoverFailed alarms fire; disaster recovery procedures cannot be executed; RTO targets cannot be met; services remain unavailable in primary region; DNS failover does not occur; cross-region replication is not synchronized; failover health checks fail. Failover operations remain in pending or failed state; DNS records do not update to secondary region endpoints; if failover protects container workloads, container services may remain unavailable, pod scheduling may fail in secondary region, and container applications may experience extended downtime; applications may experience extended service unavailability or data loss.

## Playbook

1. Retrieve the Route 53 Health Check `<health-check-id>` configuration and inspect its status, endpoint configuration, and failure threshold settings, verifying health check accessibility.
2. List Route 53 hosted zones in region `<region>` and retrieve DNS record sets for domain `<domain-name>` to verify failover record configuration and current active region endpoints.
3. Retrieve CloudWatch metrics for Route 53 health checks including HealthCheckStatus and HealthCheckFailureReason over the last 1 hour to identify health check failure patterns.
4. Query CloudWatch Logs for log groups containing Route 53 events and filter for failover record change patterns or DNS update failures within the last 1 hour.
5. Retrieve cross-region replication status for resource `<resource-arn>` and verify replication lag metrics, checking replication synchronization between primary and secondary regions.
6. List active alarms in region `<primary-region>` and region `<secondary-region>` with state 'ALARM' to identify regional service health differences.
7. Retrieve the Auto Scaling Group `<asg-name>` configuration in secondary region `<secondary-region>` and verify its desired capacity and instance health status, checking secondary region readiness.
8. Compare DNS record update timestamps with failover trigger timestamps within 5 minutes and verify whether DNS failover occurs within expected time windows, using Route 53 record change history as supporting evidence.

## Diagnosis

1. **Analyze health check status from Step 1 and Step 3**: If HealthCheckStatus shows 'Unhealthy' for primary region endpoints, DNS failover should trigger automatically. If primary is unhealthy but DNS has not updated (Step 2), check failover routing policy configuration. If health check configuration shows incorrect endpoints, this is the root cause.

2. **Evaluate DNS record configuration from Step 2**: If failover records are not configured or routing policy is not set to 'Failover', DNS will not redirect traffic. If active region still points to primary despite primary being unhealthy, the failover TTL may not have expired yet or health check thresholds are not met.

3. **Review secondary region readiness from Step 7**: If secondary region ASG shows zero healthy instances or desired capacity is zero, failover will succeed but traffic will fail. If secondary instances are unhealthy, the issue is with secondary region infrastructure, not failover mechanism.

4. **Cross-reference replication status from Step 5**: If replication lag is high, failover may result in data loss. If replication shows errors, data in secondary region may be inconsistent. This does not prevent failover but affects recovery point objective.

5. **Assess DNS propagation timing from Step 8**: If DNS records updated but traffic still routes to primary, DNS cache TTL is the cause. If DNS records have not updated within expected time, Route 53 service issues or configuration errors exist.

If the above analysis is inconclusive: Verify Route 53 health check protocol matches endpoint protocol. Check for Route 53 service limits on health checks. Examine secondary region resource quotas. Test DNS resolution from multiple geographic locations. Review CloudWatch alarms from Step 6 for additional failure indicators.
