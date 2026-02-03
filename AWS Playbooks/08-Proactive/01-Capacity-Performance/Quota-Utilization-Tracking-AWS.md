# Quota Utilization Tracking

## Meaning

Quota utilization tracking indicates that AWS service quota utilization cannot be accurately tracked or quota limit warnings are not generated (triggering alarms like QuotaTrackingUnavailable or QuotaLimitWarningFailed) because quota utilization metrics are unavailable, quota limit warnings are not generated, quota utilization trends cannot be analyzed, quota tracking tools fail, or quota utilization data is inaccurate. Quota utilization metrics show unavailable data, quota limit warnings are not generated, quota utilization trends show anomalies, and quota tracking fails. This affects the capacity planning layer and quota management, typically caused by quota monitoring failures, quota tracking tool unavailability, quota data collection issues, or quota warning automation failures; if quota tracking affects container workloads, container quota limits may be exceeded unexpectedly and applications may experience quota constraint failures.

## Impact

QuotaTrackingUnavailable alarms fire; QuotaLimitWarningFailed alarms fire; quota utilization cannot be tracked; quota limit warnings are not generated; quota limits may be exceeded unexpectedly; resource provisioning may fail due to quota constraints. Quota utilization tracking is unavailable; if quota tracking affects container workloads, container quota limits may be exceeded unexpectedly, pod quota constraints may be hit, and container applications may experience quota constraint failures; applications may experience quota exhaustion or unexpected quota limit errors.

## Playbook

1. Retrieve service quota utilization data for EC2 instances in region `<region>` including vCPU quota, instance count quota, and Elastic IP quota to identify approaching quota limits.
2. Retrieve service quota utilization data for RDS DB instances in region `<region>` including DB instance quota and storage quota to identify approaching database quota limits.
3. Retrieve service quota utilization data for VPC resources in region `<region>` including VPC quota, subnet quota, and security group quota to identify approaching networking quota limits.
4. Query CloudWatch Logs for log groups containing service quota events and filter for quota limit warnings or quota constraint errors within the last 7 days.
5. Retrieve CloudWatch metrics for service quota utilization including quota usage percentage and quota limit proximity over the last 30 days to identify quota utilization trends.
6. Compare quota utilization trend data with quota limit warning generation results and verify whether warnings are generated when quotas approach limits, using service quota data as supporting evidence.
7. Retrieve service quota increase request history for account `<account-id>` in region `<region>` and verify whether quota increases are requested proactively, checking quota management practices.
8. Analyze quota utilization growth patterns over the last 90 days to identify approaching quota limits and predict when quotas will be exhausted.

## Diagnosis

1. **Analyze quota utilization from Step 1, Step 2, and Step 3**: If any quota exceeds 80% utilization, proactive action is needed. If vCPU quota is approaching limits, instance launches may fail. If VPC or subnet quotas are near limits, network expansion is blocked.

2. **Evaluate warning generation from Step 4 and Step 6**: If quota warnings are not being generated when utilization exceeds thresholds, monitoring configuration needs review. If warnings are generated but not acted upon, process improvements are needed.

3. **Review quota trends from Step 5 and Step 8**: If utilization is growing steadily, project when limits will be reached. If utilization is stable, current quotas are adequate. If utilization spiked recently, investigate the cause.

4. **Cross-reference with increase requests from Step 7**: If quota increases were recently requested, verify they were approved and applied. If increases are frequently requested, consider larger increases or architectural changes.

5. **Assess service-specific quotas**: If specific services consistently hit quotas, evaluate architectural alternatives. If quotas are hit during peak periods, consider Reserved Capacity or pre-provisioning.

If the above analysis is inconclusive: Review Service Quotas console for comprehensive quota visibility. Check for soft vs. hard limits and request increases where possible. Consider multi-region deployment to distribute quota usage. Evaluate AWS Organizations for quota aggregation across accounts.
