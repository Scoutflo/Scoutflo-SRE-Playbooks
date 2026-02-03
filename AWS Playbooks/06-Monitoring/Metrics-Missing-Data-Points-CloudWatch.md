# CloudWatch Metrics Missing Data Points

## Meaning

CloudWatch metrics are missing data points (triggering monitoring gaps or CloudWatchMetricsMissing alarms) because metric namespace is incorrect, metric dimensions do not match, metric publishing fails, metric retention period expires, CloudWatch Metrics service encounters errors during data ingestion, or metric publishing application errors prevent data submission. CloudWatch metrics have missing data points, monitoring data is incomplete, and metric-based alarms cannot evaluate. This affects the monitoring and observability layer and reduces monitoring visibility, typically caused by metric publishing issues, dimension mismatches, or service problems; if using custom metrics, publishing patterns may differ and applications may experience metric data gaps.

## Impact

CloudWatch metrics have missing data points; monitoring data is incomplete; metric-based alarms cannot evaluate; metric graphs show gaps; monitoring visibility is reduced; metric retention causes data loss; metric publishing fails; observability is compromised. CloudWatchMetricsMissing alarms may fire; if using custom metrics, publishing patterns may differ; applications may experience errors or performance degradation due to missing monitoring data; alarm evaluation may be ineffective.

## Playbook

1. Verify metric namespace `<namespace>` exists and AWS service health for CloudWatch Metrics in region `<region>` is normal.
2. Retrieve CloudWatch metrics for metric namespace `<namespace>` and metric name `<metric-name>` over the last 24 hours to identify missing data point patterns and gaps, analyzing data point frequency.
3. Query CloudWatch Logs for log groups containing application logs and filter for CloudWatch metric publishing errors or PutMetricData API call failures, including error message details.
4. Retrieve CloudWatch metric metadata for metric namespace `<namespace>` and metric name `<metric-name>` and inspect available dimensions, metric properties, and metric statistics, verifying dimension configuration.
5. List CloudWatch metrics in namespace `<namespace>` and compare data point availability across different metrics to determine if the issue is metric-specific, analyzing metric availability.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CloudWatch PutMetricData API call failures or metric publishing errors, including API error details.
7. Retrieve CloudWatch metrics for CloudWatch Metrics service including PutMetricData errors if available and verify service health, checking if service issues affect publishing.
8. Retrieve CloudWatch metric retention settings for metric namespace `<namespace>` and verify retention period, checking if retention expiration causes data loss.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for metric namespace or dimension modification events within the last 7 days, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch metrics data (from Playbook step 2) to identify the pattern of missing data points over the last 24 hours. If data points are consistently missing at regular intervals, the metric publishing application may have stopped or is failing periodically. If data points are sporadically missing, there may be transient publishing failures or network issues.

2. Review CloudWatch Logs for metric publishing errors (from Playbook steps 3 and 6) to identify any PutMetricData API call failures. If logs show "AccessDenied" errors, verify IAM permissions for the publishing application. If logs show "InvalidParameterValue" errors, the metric dimensions or values are incorrectly formatted.

3. Examine metric metadata and dimensions (from Playbook step 4) to verify dimension configuration matches expected values. If metric dimensions have changed or are inconsistent, data points may be published to different metric combinations, causing apparent data gaps in the expected metric.

4. Compare metric availability across different metrics in the same namespace (from Playbook step 5). If all metrics in the namespace are missing data, the publishing application or service has stopped. If only specific metrics are affected, dimension configuration or metric-specific publishing logic is the issue.

5. Check metric retention settings (from Playbook step 8) to determine if older data points have been aged out according to retention policies. High-resolution metrics (1-second) are retained for 3 hours, 60-second metrics for 15 days, and lower resolutions for longer periods.

6. Verify CloudWatch custom metric quota limits by examining if the account is approaching or has exceeded PutMetricData API request limits. If quota limits are reached, new data points may be rejected.

7. Correlate CloudTrail events (from Playbook step 9) with missing data point timestamps within 5 minutes to identify any metric namespace or dimension modification events. If configuration changes coincide with when data points started missing, those changes are the likely cause.

8. Review metric resolution configuration to verify the expected publishing frequency matches the metric resolution. If the application publishes metrics less frequently than the expected resolution, data points appear to be missing.

If no correlation is found within the specified time windows: extend timeframes to 30 days, review alternative evidence sources including metric publishing application code and CloudWatch service health, check for gradual issues like metric dimension changes or publishing application failures, verify external dependencies like CloudWatch Metrics service availability or network connectivity, examine historical patterns of missing data points, check for CloudWatch custom metric quota limits, verify CloudWatch metric resolution configuration. Missing data points may result from metric publishing application errors, CloudWatch Metrics service issues, metric dimension mismatches, CloudWatch custom metric quota limits, or CloudWatch metric resolution configuration rather than immediate metric configuration changes.
