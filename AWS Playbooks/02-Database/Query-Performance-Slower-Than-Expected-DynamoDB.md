# DynamoDB Query Performance Slower Than Expected

## Meaning

DynamoDB query performance is slower than expected (triggering latency alarms like DynamoDBQueryLatency or DynamoDBThrottling) because query patterns are inefficient, global secondary indexes are missing or misconfigured, provisioned throughput is insufficient, item size is large causing scan operations, hot partitions cause throttling, or DynamoDB table capacity mode affects query performance. Query response times increase, application performance degrades, and database queries take longer than expected. This affects the database layer and impacts application performance, typically caused by index configuration issues, capacity constraints, or query pattern problems; if using DynamoDB Global Tables, replication may affect performance and applications may experience query latency issues.

## Impact

Query response times increase; application performance degrades; user-facing latency increases; DynamoDB throttling may occur; read capacity is exhausted; query timeouts happen; application scalability is limited; database performance does not meet SLA requirements. DynamoDBQueryLatency alarms may fire; if using DynamoDB Global Tables, replication may affect query performance; applications may experience errors or performance degradation due to slow queries; user-facing services experience increased latency.

## Playbook

1. Verify DynamoDB table `<table-name>` exists and is in "ACTIVE" state, and AWS service health for DynamoDB in region `<region>` is normal.
2. Retrieve CloudWatch metrics for DynamoDB table `<table-name>` including ConsumedReadCapacityUnits, ReadThrottledEvents, and SuccessfulRequestLatency over the last 1 hour to identify performance patterns, analyzing latency trends.
3. Retrieve the DynamoDB Table `<table-name>` in region `<region>` and inspect its table configuration, global secondary indexes, provisioned read capacity settings, and capacity mode (provisioned vs on-demand).
4. Query CloudWatch Logs for log groups containing DynamoDB access logs and filter for slow query patterns or throttling events related to table `<table-name>`, including query execution time indicators.
5. Retrieve CloudWatch alarms associated with DynamoDB table `<table-name>` with metrics related to latency or throttling and check for alarms in ALARM state, verifying alarm threshold configurations.
6. Retrieve CloudWatch metrics for DynamoDB table `<table-name>` including ItemCount and TableSizeBytes to verify table size, checking if large table size affects query performance.
7. Retrieve the DynamoDB Table `<table-name>` partition key and sort key configuration and analyze query patterns, verifying if queries use partition key effectively.
8. List DynamoDB table metrics for table `<table-name>` and compare query performance patterns with similar tables to determine if the issue is table-specific, analyzing performance differences.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for DynamoDB index creation or modification events related to table `<table-name>` within the last 24 hours, checking for index configuration changes.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when DynamoDBQueryLatency or throttling alarms first triggered. This timestamp establishes when performance degradation began.

2. If CloudWatch metrics (from Playbook step 2) show ReadThrottledEvents around the latency increase, throttling is directly causing query slowdowns. Check consumed vs provisioned capacity to confirm.

3. If table configuration (from Playbook step 3) shows queries are using Scan operations rather than Query operations with partition keys, missing or misconfigured indexes are forcing full table scans.

4. If global secondary indexes exist (from Playbook step 3) but queries are still slow, verify query patterns are using the correct index. Queries not specifying the index or using non-indexed attributes fall back to scans.

5. If table size metrics (from Playbook step 6) show large ItemCount or TableSizeBytes, and partition key design (from Playbook step 7) shows limited cardinality, hot partitions may be causing uneven capacity distribution.

6. If CloudTrail shows capacity modifications (from Playbook step 9) around the latency increase, capacity reductions directly caused the performance degradation.

7. If latency is constant rather than intermittent (from Playbook step 2 trend), the issue is structural (index design). If intermittent, the issue is capacity-related (provisioned throughput or burst exhaustion).

8. If comparing performance across tables (from Playbook step 8) shows this table alone is slow, the issue is table-specific design or configuration.

If no correlation is found: extend analysis to 24 hours, review query patterns for optimization opportunities, check Global Tables replication overhead, verify Streams capacity consumption, and examine item size distribution for large items affecting latency.
