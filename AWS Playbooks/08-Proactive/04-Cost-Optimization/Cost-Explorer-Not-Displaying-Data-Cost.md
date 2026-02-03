# AWS Cost Explorer Not Displaying Data

## Meaning

AWS Cost Explorer is not displaying data (triggering cost visibility gaps or CostExplorerDataMissing alarms) because cost data is not available, date range selection is incorrect, cost data processing is delayed, IAM permissions are insufficient for Cost Explorer access, Cost Explorer service encounters errors during data retrieval, or Cost Explorer query filters exclude all data. AWS Cost Explorer data is not visible, cost analysis is unavailable, and cost reporting fails. This affects the cost management and visibility layer and reduces cost visibility, typically caused by data processing delays, permission issues, or query configuration problems; if using Cost Explorer with different granularities or filters, data display behavior may differ and applications may experience cost visibility gaps.

## Impact

AWS Cost Explorer data is not visible; cost analysis is unavailable; cost reporting fails; cost visibility is compromised; Cost Explorer queries fail; cost-based decision making is limited; cost data processing is delayed; financial analysis is interrupted. CostExplorerDataMissing alarms may fire; if using Cost Explorer with different granularities or filters, data display behavior may differ; applications may experience reduced cost visibility; cost management decisions may be limited.

## Playbook

1. Verify AWS Cost Explorer access and AWS service health for Cost Explorer and Billing in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Cost Explorer API call failures or data retrieval errors, including API error details.
3. Retrieve CloudWatch metrics for AWS Cost Explorer including API call success rates over the last 7 days to identify data retrieval patterns, analyzing API call patterns.
4. Retrieve the IAM user `<user-name>` or IAM role `<role-name>` accessing Cost Explorer and inspect its policy permissions for Cost Explorer operations, verifying IAM permissions.
5. List AWS billing data availability for the selected date range and check cost data processing status and data availability timestamps, verifying data availability.
6. Query CloudWatch Logs for log groups containing application logs and filter for Cost Explorer query errors or data display failures, including query error details.
7. Retrieve the AWS Cost Explorer query configuration including date range and filters and verify query parameters, checking if query filters exclude all data.
8. Retrieve CloudWatch metrics for AWS billing data processing including billing data availability and verify billing data processing status, checking if data processing delays affect Cost Explorer.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for IAM policy modification events related to Cost Explorer access within the last 7 days, checking for permission changes.

## Diagnosis

1. **Check IAM Permissions from Step 4 First**: If Cost Explorer access requires IAM permissions, verify the IAM role or user from Step 4 has `ce:GetCostAndUsage`, `ce:GetCostForecast`, and related permissions. If CloudTrail events from Step 2 show "AccessDenied" errors for Cost Explorer API calls, then insufficient IAM permissions are blocking data access. If permissions appear correct, continue to step 2.

2. **Analyze CloudWatch Metrics and API Patterns from Step 3**: If CloudWatch metrics show Cost Explorer API call success rates dropping or failing, then service-level issues exist. If API calls succeed but return empty data, continue to step 3 for data availability issues. If API calls are failing with errors, check the specific error patterns in CloudTrail logs from Step 2.

3. **Verify Billing Data Availability from Steps 5 and 8**: If billing data availability from Step 5 shows data is not yet processed for the selected date range, then data processing delays are the cause. Cost and usage data typically has a 24-48 hour delay. If CloudWatch metrics from Step 8 indicate billing data processing is delayed, wait for processing to complete. If data should be available, continue to step 4.

4. **Review Query Configuration from Step 7**: If query parameters from Step 7 include filters that exclude all data (wrong account, service, region, or tag filters), then query configuration is returning empty results. Verify date range is within valid bounds - Cost Explorer supports data from the last 14 months. If query configuration appears correct, continue to step 5.

5. **Correlate with IAM Policy Changes from Step 9**: If CloudTrail events from Step 9 show IAM policy modifications affecting Cost Explorer access within 5 minutes of data disappearing, then recent permission changes revoked access. Review the specific policy changes to identify removed permissions.

**If no correlation is found**: Extend analysis to 90 days using query results patterns. Verify Cost Explorer is enabled for the account (requires activation for new accounts). Check for consolidated billing effects if this is a member account. Review billing data processing status for the specific date range and verify Cost Explorer service health from Step 1.
