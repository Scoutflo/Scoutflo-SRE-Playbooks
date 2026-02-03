# AWS Lambda Timeout Error

## Meaning

Lambda function executions timeout before completion (triggering alarms like LambdaFunctionError or LambdaDuration) because function timeout settings are too low, function code has performance bottlenecks, CloudWatch logs show execution delays, external API calls exceed timeout limits, function memory allocation is insufficient, or Lambda VPC configuration adds latency. Lambda functions fail to complete execution, function invocations timeout, and CloudWatch Logs show timeout errors. This affects the serverless compute layer and blocks function execution, typically caused by timeout configuration issues, code performance problems, or VPC networking delays; if using Lambda container images, cold start times may be longer and applications may experience function execution failures.

## Impact

Lambda functions fail to complete execution; function invocations timeout; LambdaFunctionError alarms fire; downstream services do not receive responses; function duration exceeds limits; timeout errors appear in CloudWatch logs; application workflows fail; data processing is incomplete; user-facing features timeout. Lambda function execution fails; if using Lambda container images, cold start times may be longer causing additional timeouts; applications may experience errors or performance degradation due to incomplete function execution; downstream services may not receive expected data.

## Playbook

1. Verify Lambda function `<function-name>` exists and AWS service health for Lambda in region `<region>` is normal.
2. Retrieve the Lambda Function `<function-name>` in region `<region>` and check the function's timeout settings in configuration, verifying timeout value against expected execution time.
3. Query CloudWatch Logs for log group `/aws/lambda/<function-name>` and filter for timeout errors, performance bottlenecks, execution delays, or external API call patterns, including duration metrics.
4. Retrieve CloudWatch metrics for Lambda function `<function-name>` including duration, memory usage, and error count to identify performance issues, analyzing duration trends.
5. Retrieve the Lambda Function `<function-name>` VPC configuration and verify if function is configured in VPC, checking VPC subnet and security group configuration that may add latency.
6. Retrieve the Lambda Function `<function-name>` configuration and inspect memory allocation settings that may affect execution time, verifying memory vs CPU allocation relationship.
7. Retrieve the Lambda Function `<function-name>` reserved concurrency settings and verify reserved concurrency is not causing throttling that appears as timeouts, checking concurrency limits.
8. Retrieve the Lambda Function `<function-name>` deployment package type (ZIP vs container image) and dead letter queue configuration and verify package type and DLQ configuration, checking if container image deployments have longer cold start times and DLQ is configured for timeout handling.
9. Query CloudWatch Logs for log group `/aws/lambda/<function-name>` and filter for VPC ENI creation delays or VPC networking issues that may cause timeouts.

## Diagnosis

1. Analyze CloudWatch metrics from Playbook step 4 to identify when duration exceeded timeout thresholds. The metric timestamps showing duration approaching or exceeding limits provide the baseline for correlation with configuration changes.

2. If AWS service health check from Playbook step 1 indicates Lambda service issues in the region, this is likely an AWS-side issue requiring monitoring rather than configuration remediation.

3. If CloudWatch Logs from Playbook step 3 show timeout errors correlating with specific external API call patterns, examine the logs for slow response times from downstream services. Events showing "Task timed out" after external calls indicate dependency delays.

4. If function configuration from Playbook step 2 shows timeout value is less than observed execution duration from Playbook step 4, the timeout setting is insufficient for the function workload.

5. If VPC configuration from Playbook step 5 shows the function is VPC-enabled, check CloudWatch Logs from Playbook step 9 for ENI creation delays. Events showing prolonged cold starts indicate VPC networking latency.

6. If memory allocation from Playbook step 6 is low relative to function requirements, correlate memory usage metrics from Playbook step 4 with timeout occurrences. Low memory reduces CPU allocation, slowing execution.

7. If reserved concurrency from Playbook step 7 shows throttling, check if apparent timeouts are actually throttled invocations being misinterpreted as timeout failures.

8. If deployment package type from Playbook step 8 shows container image deployment, verify cold start times are accounted for in timeout settings. Container images typically have longer initialization times.

If no correlation is found from the collected data: extend CloudWatch Logs query timeframes to 1 hour, review function code for performance bottlenecks, check database query execution times, and examine external API response latency patterns. Timeout errors may result from code-level inefficiencies, database query optimization needs, external service degradation, or Lambda SnapStart configuration issues for Java functions.

