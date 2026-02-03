# Sudden Unexpected Increase in AWS Bill

## Meaning

AWS bill shows sudden unexpected increase (triggering cost anomalies or UnexpectedBillIncrease alarms) because new resources were provisioned, existing resource usage increased, service pricing changed, data transfer costs spiked, cost allocation is incorrect, or AWS service usage patterns changed unexpectedly. AWS costs increase unexpectedly, budget thresholds are exceeded, and unexpected charges appear. This affects the cost management and financial planning layer and disrupts budgets, typically caused by resource provisioning spikes, usage increases, or pricing changes; if using AWS with multiple accounts or cost allocation tags, cost attribution may differ and applications may experience unexpected cost increases.

## Impact

AWS costs increase unexpectedly; budget thresholds are exceeded; cost anomalies occur; unexpected charges appear; cost tracking is inaccurate; cost management objectives are not met; billing alerts fire; financial planning is disrupted. UnexpectedBillIncrease alarms may fire; if using AWS with multiple accounts or cost allocation tags, cost attribution may differ; applications may experience unexpected costs; financial planning may be disrupted.

## Playbook

1. Verify AWS billing access and AWS service health for Billing in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing CloudTrail events and filter for resource creation events, service usage spikes, or cost-related API calls over the billing period, checking for resource provisioning.
3. Retrieve CloudWatch metrics for AWS service usage including service-specific usage metrics and data transfer metrics over the last 30 days to identify usage patterns, analyzing usage trends.
4. List AWS service resources created or modified during the billing period and check resource counts, usage volumes, and cost implications, analyzing resource provisioning.
5. Query CloudWatch Logs for log groups containing billing events and filter for cost spike patterns or unexpected charge events, checking billing details.
6. Retrieve AWS service usage data for high-cost services and analyze usage patterns against historical baselines, identifying high-cost services.
7. Retrieve CloudWatch metrics for AWS data transfer including DataTransferOut and verify data transfer patterns, checking if data transfer spikes affect costs.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for service pricing or cost allocation tag modification events within the last 30 days, checking for pricing or tag changes.
9. Retrieve AWS cost allocation tag data and verify cost allocation tag accuracy, checking if tag misconfiguration affects cost attribution.

## Diagnosis

1. **Analyze CloudWatch Metrics from Steps 3 and 7**: Review service usage and data transfer metrics for anomalies. If CloudWatch metrics show significant spikes in EC2 hours, Lambda invocations, S3 requests, or data transfer, then increased usage is driving costs. Identify which services show the largest increase relative to baseline. If usage patterns appear normal, continue to step 2.

2. **Review Resource Provisioning from Steps 2 and 4**: If CloudTrail events from Step 2 show new resource creation (EC2 instances, RDS databases, large EBS volumes), then new resources are adding costs. If resource inventory from Step 4 shows unexpected resources, investigate who created them and whether they are needed. If no new resources, continue to step 3.

3. **Check Data Transfer Costs from Step 7**: If CloudWatch metrics show DataTransferOut spikes, then data egress is a significant cost driver. Cross-region transfer, internet egress, and NAT Gateway data processing are common unexpected cost sources. If data transfer correlates with cost increase, investigate data movement patterns. If data transfer is normal, continue to step 4.

4. **Evaluate Billing Details from Step 5**: If billing events from Step 5 show specific service line items with unusual charges, focus investigation on those services. Check for AWS Marketplace subscriptions, support plan changes, or service-specific pricing changes. Compare current billing to previous periods to identify the variance source.

5. **Correlate with Configuration Changes from Step 8**: If CloudTrail events from Step 8 show cost allocation tag modifications, then cost attribution may have changed without actual spending increase. If pricing changes or new service tiers were applied, then AWS pricing updates may explain the increase.

**If no correlation is found**: Extend analysis to 180 days using billing data from Step 5. Check for resources in unexpected regions that may have been provisioned accidentally. Review linked accounts for cost increases. Check for AWS Marketplace charges, support plan upgrades, or premium features enabled. Verify no compromised credentials are creating resources.
