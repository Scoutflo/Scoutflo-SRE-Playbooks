# DynamoDB Throttling Errors

## Meaning

DynamoDB throttling errors occur (ProvisionedThroughputExceededException) because provisioned read or write capacity is exceeded, hot partitions cause uneven capacity distribution, burst capacity is exhausted, on-demand mode encounters account-level limits, sudden traffic spikes exceed capacity, or DynamoDB table capacity settings are insufficient. DynamoDB requests return throttling exceptions, application requests fail, and CloudWatch metrics show throttled events. This affects the database layer and blocks data access, typically caused by capacity planning issues, hot partition problems, or traffic pattern changes; if using DynamoDB with Lambda or application services, throttling errors may cascade to upstream services and applications may experience data access failures.

## Impact

DynamoDB requests are throttled; ProvisionedThroughputExceededException errors occur; application requests fail; read and write operations are rejected; user-facing errors increase; application performance degrades; database operations cannot complete; service availability is impacted. DynamoDB throttling errors appear in application logs; if using DynamoDB with Lambda or application services, upstream services may experience errors or performance degradation; data access operations fail; user-facing features that depend on DynamoDB become unavailable.

## Playbook

1. Verify DynamoDB table `<table-name>` exists and is in "ACTIVE" state, and AWS service health for DynamoDB in region `<region>` is normal.
2. Retrieve CloudWatch metrics for DynamoDB table `<table-name>` including ReadThrottledEvents, WriteThrottledEvents, ConsumedReadCapacityUnits, and ConsumedWriteCapacityUnits over the last 1 hour to identify throttling patterns, analyzing throttling frequency and capacity consumption.
3. Retrieve the DynamoDB Table `<table-name>` in region `<region>` and inspect its provisioned read and write capacity settings, on-demand mode configuration, table status, and capacity mode (provisioned vs on-demand).
4. Query CloudWatch Logs for log groups containing application logs and filter for ProvisionedThroughputExceededException error patterns related to table `<table-name>`, including throttling exception timestamps.
5. Retrieve CloudWatch alarms associated with DynamoDB table `<table-name>` with metrics ReadThrottledEvents or WriteThrottledEvents and check for alarms in ALARM state, verifying alarm threshold configurations.
6. Retrieve CloudWatch metrics for DynamoDB table `<table-name>` including UserErrors and SystemErrors to identify error patterns associated with throttling, analyzing error correlation with throttling events.
7. Retrieve the DynamoDB Table `<table-name>` partition key configuration and analyze capacity consumption patterns to identify hot partitions or uneven distribution, checking partition key design.
8. Retrieve CloudWatch metrics for DynamoDB table `<table-name>` including ConsumedReadCapacityUnits and ConsumedWriteCapacityUnits by partition key to identify hot partition patterns, analyzing per-partition capacity consumption.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for DynamoDB table capacity modification events related to table `<table-name>` within the last 24 hours, checking for capacity changes.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when ReadThrottledEvents or WriteThrottledEvents alarms first triggered. This timestamp establishes the baseline for correlating throttling with capacity or traffic patterns.

2. If CloudWatch metrics (from Playbook step 2) show ConsumedReadCapacityUnits or ConsumedWriteCapacityUnits exceeded provisioned capacity around the alarm time, simple capacity exhaustion is the root cause.

3. If consumed capacity metrics show uneven distribution, examine per-partition capacity consumption (from Playbook step 8). If specific partitions show disproportionately high consumption, hot partition issues due to partition key design are causing localized throttling.

4. If table configuration (from Playbook step 3) shows on-demand mode and throttling still occurs, account-level throughput limits may be reached. If provisioned mode shows recent capacity reductions in CloudTrail (from Playbook step 9), those reductions caused the throttling.

5. If application logs (from Playbook step 4) show ProvisionedThroughputExceededException correlating with specific operations or time windows, analyze request patterns. Sudden traffic bursts exceeding burst capacity allocation are the likely cause.

6. If UserErrors and SystemErrors metrics (from Playbook step 6) correlate with throttling events, downstream effects of throttling are cascading into application-level errors.

7. If throttling is intermittent rather than constant (from Playbook step 2 trend analysis), burst capacity is being exhausted during peak periods - consider on-demand mode or capacity auto-scaling.

If no correlation is found: extend analysis to 24 hours, review partition key distribution for hot key patterns, check DynamoDB Global Tables replication capacity overhead, verify DynamoDB Streams capacity consumption, and examine burst capacity utilization patterns.
