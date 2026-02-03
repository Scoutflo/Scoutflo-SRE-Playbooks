# AWS Free Tier Unexpectedly Exceeded

## Meaning

AWS Free Tier is unexpectedly exceeded (triggering cost anomalies or FreeTierExceeded alarms) because free tier usage limits are reached, free tier eligible services are used beyond limits, free tier period has expired, service usage exceeds free tier thresholds, free tier tracking is inaccurate, or free tier eligible resource configuration does not match free tier requirements. AWS Free Tier limits are exceeded, unexpected charges occur, and free tier benefits are lost. This affects the cost management and free tier monitoring layer and causes unexpected charges, typically caused by usage growth, period expiration, or tracking inaccuracies; if using AWS Free Tier across multiple services, limit calculations may differ and applications may experience unexpected free tier exceedances.

## Impact

AWS Free Tier limits are exceeded; unexpected charges occur; free tier benefits are lost; cost tracking is inaccurate; free tier usage monitoring fails; billing charges appear unexpectedly; free tier automation is ineffective; cost management objectives are not met. FreeTierExceeded alarms may fire; if using AWS Free Tier across multiple services, limit calculations may differ; applications may experience unexpected charges; free tier benefits may not be realized.

## Playbook

1. Verify AWS Free Tier eligibility and AWS service health for Billing in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing CloudTrail events and filter for service usage events that may contribute to free tier consumption, checking for usage events.
3. Retrieve CloudWatch metrics for AWS service usage including service-specific usage metrics over the last 30 days to identify free tier consumption patterns, analyzing usage trends.
4. List AWS service resource usage for free tier eligible services and check resource counts, usage volumes, and free tier limit comparisons, analyzing free tier usage.
5. Query CloudWatch Logs for log groups containing billing events and filter for free tier limit exceeded events or unexpected charge patterns, checking billing details.
6. Retrieve AWS service usage data for free tier eligible services and analyze usage patterns against free tier limits, verifying limit comparisons.
7. Retrieve the AWS Free Tier period start date and expiration date and verify free tier period status, checking if period expiration affects charges.
8. Retrieve CloudWatch metrics for AWS service resource creation including resource counts and verify resource creation patterns, checking if resource creation exceeds free tier limits.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for free tier eligible service resource creation events within the last 30 days, checking for resource creation.

## Diagnosis

1. **Analyze CloudWatch Metrics from Step 3**: Review service usage metrics for free tier consumption patterns. If CloudWatch metrics show EC2 hours exceeding 750 per month, S3 requests exceeding 2,000 PUT or 20,000 GET, or Lambda invocations exceeding 1 million, then usage has exceeded free tier limits. Compare usage growth rate to identify when limits were exceeded. If usage is within limits, continue to step 2.

2. **Check Free Tier Period Status from Step 7**: If free tier period from Step 7 shows the 12-month introductory period has expired, then time-limited free tier benefits have ended. Some services (EC2 t2.micro/t3.micro, S3 5GB) are only free for 12 months after account creation. If period has expired for specific services, that explains the charges. If period is still valid, continue to step 3.

3. **Review Resource Usage Patterns from Steps 4 and 6**: If resource usage from Step 4 shows resources that do not qualify for free tier (wrong instance types, wrong regions, or wrong configurations), then ineligible usage is being charged. Verify EC2 instances are t2.micro or t3.micro, EBS volumes are within 30GB, and other resources meet free tier specifications. If resources appear eligible, continue to step 4.

4. **Evaluate Billing Events from Step 5**: If billing events from Step 5 show specific services exceeding free tier limits, identify which services and usage types caused charges. Check for data transfer costs, which often exceed free tier unexpectedly. If billing shows charges but usage appears within limits, continue to step 5.

5. **Correlate with Resource Creation from Step 9**: If CloudTrail events from Step 9 show new resource creation within 30 days before charges appeared, then new resources pushed usage over free tier limits. Calculate cumulative usage across all resources to identify the threshold breach.

**If no correlation is found**: Extend analysis to 90 days using billing data from Step 5. Verify account creation date to confirm free tier eligibility period. Check for resources in multiple regions that cumulatively exceed limits. Review data transfer patterns - outbound data transfer is often overlooked. Check for AWS Marketplace charges that are not covered by free tier.
