# Cost Anomaly Detection

## Meaning

Cost anomaly detection indicates that AWS costs show unexpected spikes or unusual patterns that deviate from normal spending baselines (triggering alarms like CostAnomalyDetected or UnexpectedCostIncrease) because cost metrics exceed historical baselines, cost trends show sudden increases, cost allocation shows unexpected service usage, budget thresholds are exceeded, or cost patterns indicate unusual resource consumption. Cost metrics show spikes or anomalies, budget alerts fire unexpectedly, cost trends deviate from historical patterns, and cost allocation indicates unexpected service usage. This affects the cost management layer and financial monitoring, typically caused by resource provisioning spikes, service usage increases, pricing changes, or cost allocation issues; if cost anomalies affect container workloads, container resource consumption may have increased unexpectedly and applications may experience cost overruns.

## Impact

CostAnomalyDetected alarms fire; UnexpectedCostIncrease alarms fire; budget thresholds are exceeded; unexpected costs accumulate; cost trends deviate from historical patterns; financial planning is disrupted. Cost metrics show sudden spikes or anomalies; if cost anomalies affect container workloads, container resource consumption may have increased unexpectedly, pod resource usage may have spiked, and container applications may experience cost overruns; applications may experience unexpected cost increases or budget overruns.

## Playbook

1. Retrieve Cost Explorer data for total costs in region `<region>` over the last 30 days and compare with historical cost baselines to identify cost anomalies or spikes.
2. List AWS Budgets in account `<account-id>` and retrieve budget status for budgets with status 'ALARM' or 'FORECASTED' to identify budget threshold violations.
3. Retrieve Cost Explorer data by service in region `<region>` over the last 7 days and identify services with unexpected cost increases compared to historical averages.
4. Query CloudWatch Logs for log groups containing Cost Explorer or billing events and filter for patterns indicating cost anomalies or unexpected charges within the last 7 days.
5. Retrieve CloudWatch metrics for AWS service usage including service-specific cost metrics over the last 7 days to identify services with usage spikes.
6. Compare cost allocation tag data with resource usage metrics over the last 7 days to identify cost centers or projects with unexpected cost increases.
7. Retrieve Cost Anomaly Detection findings from AWS Cost Anomaly Detection service and verify anomaly details including affected services and cost impact.
8. Compare cost spike timestamps with resource provisioning timestamps and verify whether cost increases correlate with resource creation events, using Cost Explorer data as supporting evidence.

## Diagnosis

1. **Analyze Cost Anomaly Detection findings from Step 7**: If anomaly findings identify specific services, focus investigation on those services. If anomaly shows high confidence score, the deviation is significant. If multiple services show anomalies simultaneously, a common cause like increased traffic or deployment is likely.

2. **Evaluate service-level costs from Step 3**: If EC2 costs spiked, check for new instance launches or instance type changes. If data transfer costs spiked, check for increased outbound traffic or cross-region transfers. If storage costs spiked, check for new EBS volumes or S3 data growth.

3. **Cross-reference with resource events from Step 8**: If cost spikes correlate with CloudTrail resource creation events, the cost increase is due to new provisioning. If no resource changes correlate, usage patterns changed on existing resources.

4. **Review budget status from Step 2**: If budget is in ALARM state, immediate attention is needed. If budget is FORECASTED to exceed, proactive action can prevent overrun. If multiple budgets are affected, the anomaly is widespread.

5. **Assess cost allocation from Step 6**: If specific cost centers show increases, isolate the investigation to those teams or projects. If untagged resources show cost increases, improve tagging for future visibility.

If the above analysis is inconclusive: Review CloudTrail for any automation or scripts that may have provisioned resources. Check for Reserved Instance or Savings Plans expirations causing on-demand pricing. Examine marketplace charges or third-party service integrations. Verify pricing changes in AWS announcements.
