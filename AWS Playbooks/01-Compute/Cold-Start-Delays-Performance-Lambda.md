# Lambda Cold Start Delays Performance

## Meaning

Lambda cold start delays cause performance degradation (triggering latency alarms like LambdaDuration or LambdaColdStart) because function initialization takes too long, package size is large increasing startup time, runtime initialization is slow, provisioned concurrency is not configured, function code has heavy initialization logic, or Lambda VPC configuration adds latency. Lambda function invocations experience high latency, cold start delays increase response times, and first requests after idle periods are slow. This affects the serverless compute layer and impacts application performance, typically caused by initialization overhead, package size, or missing concurrency configuration; if using Lambda container images, cold start times may be longer and applications may experience inconsistent performance.

## Impact

Lambda function invocations experience high latency; cold start delays increase response times; user-facing latency degrades; first request after idle period is slow; Lambda function performance is inconsistent; LambdaDuration or LambdaColdStart alarms fire; application user experience is impacted; function startup time exceeds acceptable thresholds. Lambda function performance is inconsistent between cold and warm invocations; if using Lambda container images, cold starts may take significantly longer; applications may experience errors or performance degradation due to inconsistent latency; user-facing services experience spikes in response times.

## Playbook

1. Verify Lambda function `<function-name>` exists and AWS service health for Lambda in region `<region>` is normal.
2. Retrieve CloudWatch metrics for Lambda function `<function-name>` including Duration, InitDuration, and ColdStartDuration over the last 1 hour to identify cold start patterns, analyzing cold start frequency and duration.
3. Retrieve the Lambda Function `<function-name>` in region `<region>` and inspect its package size, runtime configuration, provisioned concurrency settings, memory allocation, and deployment package type (ZIP vs container image).
4. Query CloudWatch Logs for log group `/aws/lambda/<function-name>` and filter for initialization logs, cold start indicators, or startup time patterns, including InitDuration metrics.
5. Retrieve CloudWatch alarms associated with Lambda function `<function-name>` with metric Duration and check for alarms in ALARM state related to latency, verifying alarm threshold configurations.
6. Retrieve CloudWatch metrics for Lambda function `<function-name>` including Invocations and ConcurrentExecutions to identify invocation frequency and analyze invocation patterns to identify idle periods causing cold starts.
7. Retrieve the Lambda Function `<function-name>` VPC configuration and verify if function is configured in VPC, checking if VPC configuration adds initialization latency.
8. Retrieve the Lambda Function `<function-name>` deployment package type and verify package type (ZIP vs container image), checking if container image deployments have longer cold start times.
9. Compare CloudWatch metrics for Lambda function `<function-name>` including InitDuration across different memory allocations if memory changes occurred, analyzing correlation between memory and cold start duration.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when LambdaDuration or LambdaColdStart thresholds were first breached. This alarm timestamp serves as the correlation baseline for all subsequent analysis.

2. If CloudWatch metrics (from Playbook step 2) show elevated InitDuration values around the alarm time, examine the function configuration (from Playbook step 3) for recent package size increases or runtime changes that extended initialization.

3. If InitDuration is normal but cold start frequency is high, check invocation patterns (from Playbook step 6). If ConcurrentExecutions show sparse traffic with gaps exceeding function idle timeout, infrequent invocations are causing cold starts.

4. If invocation patterns are consistent, check VPC configuration (from Playbook step 7). If function is VPC-attached and cold starts increased after VPC configuration, ENI creation latency is the likely cause.

5. If no VPC is configured, examine deployment package type (from Playbook step 8). If using container images, compare InitDuration with ZIP deployments - container images typically have longer cold starts due to image layer loading.

6. If cold starts correlate with provisioned concurrency changes (from Playbook step 3), verify whether provisioned concurrency was reduced or removed, causing the function to rely on on-demand initialization.

7. If cold start duration varies by memory allocation (from Playbook step 9), insufficient memory may be throttling CPU during initialization - Lambda allocates CPU proportionally to memory.

If no correlation is found: extend analysis to 24 hours, review CloudWatch Logs (from Playbook step 4) for initialization errors or slow dependency loading, check for Lambda SnapStart eligibility for Java runtimes, and verify container image layer caching configuration. Cold start delays may result from large packages, heavy initialization logic, VPC ENI delays, or container image overhead.
