# Lambda Function Exceeds Memory Limit

## Meaning

A Lambda function exceeds its memory limit (triggering out-of-memory errors or LambdaMemoryError alarms) because function memory allocation is insufficient for workload, memory leaks cause gradual memory growth, function processes large datasets exceeding memory, concurrent executions exhaust available memory, or Lambda function memory configuration is too low. Lambda function executions fail with out-of-memory errors, function invocations are terminated, and CloudWatch metrics show memory utilization exceeding limits. This affects the serverless compute layer and blocks function execution, typically caused by memory allocation issues, memory leaks, or data processing requirements; if using Lambda container images, memory behavior may differ and applications may experience function execution failures.

## Impact

Lambda function executions fail; out-of-memory errors occur; function invocations are terminated; application workflows break; Lambda function errors increase; LambdaMemoryError alarms fire; retry attempts fail; function cannot complete processing; service reliability degrades. Lambda function memory errors appear in CloudWatch Logs; if using Lambda container images, memory allocation behavior may differ; applications may experience errors or performance degradation due to incomplete function execution; downstream services may not receive expected data.

## Playbook

1. Verify Lambda function `<function-name>` exists and AWS service health for Lambda in region `<region>` is normal.
2. Retrieve CloudWatch metrics for Lambda function `<function-name>` including MemoryUtilization, Duration, and Errors over the last 1 hour to identify memory usage patterns, analyzing memory utilization trends.
3. Retrieve the Lambda Function `<function-name>` in region `<region>` and inspect its memory configuration, timeout settings, function code size, and deployment package type (ZIP vs container image).
4. Query CloudWatch Logs for log group `/aws/lambda/<function-name>` and filter for out-of-memory error patterns, memory-related exceptions, or function termination errors, including memory utilization logs.
5. Retrieve CloudWatch alarms associated with Lambda function `<function-name>` with metric Errors or MemoryUtilization and check for alarms in ALARM state, verifying alarm threshold configurations.
6. Retrieve CloudWatch metrics for Lambda function `<function-name>` including ConcurrentExecutions and verify if concurrent executions contribute to memory exhaustion, analyzing concurrency patterns.
7. Retrieve the Lambda Function `<function-name>` reserved concurrency settings and verify reserved concurrency configuration, checking if concurrency limits affect memory availability.
8. Query CloudWatch Logs for log group `/aws/lambda/<function-name>` and filter for memory allocation errors or memory-related exception patterns, checking for memory leak indicators.
9. Compare CloudWatch metrics for Lambda function `<function-name>` including MemoryUtilization across different function versions if deployments occurred, analyzing memory usage changes.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when LambdaMemoryError or Error alarms first triggered. This timestamp establishes when memory exhaustion began and serves as the correlation baseline.

2. If CloudWatch metrics (from Playbook step 2) show MemoryUtilization consistently near 100% before the alarm, compare with function memory configuration (from Playbook step 3). If configured memory is unchanged but utilization climbed to threshold, workload memory requirements have grown.

3. If MemoryUtilization shows gradual increase over function Duration (from Playbook step 2), examine CloudWatch Logs (from Playbook step 4 and step 8) for memory allocation patterns. Gradual growth within a single execution indicates memory leaks in function code.

4. If memory errors correlate with ConcurrentExecutions spikes (from Playbook step 6), check if reserved concurrency settings (from Playbook step 7) are limiting concurrent executions, causing requests to queue and timeout.

5. If memory errors began after a deployment, compare error timestamps with function version changes (from Playbook step 9). If MemoryUtilization increased after deployment, new code introduced memory-intensive operations or leaks.

6. If memory errors are intermittent rather than constant, analyze CloudWatch Logs (from Playbook step 4) for specific input patterns. Large payload processing or specific event types may trigger memory exhaustion.

7. If using container images (from Playbook step 3), container overhead may consume baseline memory - compare available memory after container initialization with ZIP-based deployments.

If no correlation is found: extend analysis to 24 hours, review CloudWatch Logs for memory profiling data, check input data size patterns, verify Lambda ephemeral storage constraints that may affect memory, and examine Lambda SnapStart memory allocation for Java functions.
