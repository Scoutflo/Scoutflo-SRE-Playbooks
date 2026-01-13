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

1. Compare Lambda function timeout configuration change timestamps with timeout error timestamps within 5 minutes and verify whether timeout errors began after timeout setting changes, using Lambda configuration events as supporting evidence.
2. Correlate function code deployment timestamps with timeout error timestamps and verify whether timeout errors occurred after code changes that introduced performance bottlenecks, using Lambda deployment events as supporting evidence.
3. Compare Lambda VPC configuration change timestamps with timeout error timestamps within 5 minutes and verify whether VPC configuration changes added latency causing timeouts, using Lambda VPC configuration events as supporting evidence.
4. Compare function memory allocation change timestamps with timeout error timestamps within 5 minutes and verify whether memory constraints caused execution delays leading to timeouts, using Lambda metrics as supporting evidence.
5. Analyze timeout error frequency over the last 15 minutes to determine if timeouts are constant (configuration issue) or intermittent (external dependency delays).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including function code complexity and database query performance, check for gradual issues like external API degradation, verify external dependencies like database connection times, examine historical patterns of function execution, check for Lambda container image deployment issues, verify Lambda SnapStart configuration for Java functions. Timeout errors may result from code-level performance issues, database query optimization needs, external service degradation, Lambda VPC ENI creation delays, or Lambda container image cold start times rather than immediate timeout configuration changes.
