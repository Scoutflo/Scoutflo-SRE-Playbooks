# API Gateway Throttling Requests

## Meaning

API Gateway throttles requests (returning 429 Too Many Requests errors or triggering APIGatewayThrottling alarms) because rate limits or burst limits are exceeded, throttling configuration is too restrictive, Lambda concurrency limits are reached, sudden traffic spikes exceed configured throttling thresholds, or API Gateway usage plan throttling limits are reached. API requests are throttled, 429 Too Many Requests errors occur, and application requests fail. This affects the API layer and reduces service availability, typically caused by throttling configuration issues, traffic spikes, or Lambda concurrency constraints; if using API Gateway HTTP APIs vs REST APIs, throttling behavior differs and applications may experience request throttling failures.

## Impact

API requests are throttled; 429 Too Many Requests errors occur; API availability degrades; user-facing errors increase; API rate limits are exceeded; burst capacity is exhausted; application requests fail; service reliability is impacted. APIGatewayThrottling alarms fire; if using API Gateway HTTP APIs vs REST APIs, throttling limits differ; applications may experience errors or performance degradation due to throttled requests; user-facing services experience request failures.

## Playbook

1. Verify API Gateway API `<api-id>` exists and is deployed, and AWS service health for API Gateway in region `<region>` is normal.
2. Retrieve CloudWatch metrics for API Gateway API `<api-id>` including 4XXError, Count, and ThrottleCount over the last 1 hour to identify throttling patterns, analyzing throttling frequency.
3. Retrieve the API Gateway REST API `<api-id>` or HTTP API `<api-id>` in region `<region>` and inspect its throttling configuration, rate limits, and burst limits, verifying throttling settings.
4. Query CloudWatch Logs for log groups containing API Gateway access logs and filter for 429 error patterns or throttling-related log entries, including throttling exception details.
5. Retrieve CloudWatch alarms associated with API Gateway API `<api-id>` with metric 4XXError or ThrottleCount and check for alarms in ALARM state, verifying alarm threshold configurations.
6. Retrieve the API Gateway `<api-id>` API type (REST API vs HTTP API) and verify API type configuration, checking type-specific throttling behavior differences.
7. Retrieve the API Gateway `<api-id>` usage plan configuration and verify usage plan throttling settings, checking if usage plan throttling limits are contributing to throttling.
8. List Lambda function concurrency metrics for functions integrated with API Gateway API `<api-id>` and check if Lambda throttling contributes to API throttling, analyzing Lambda concurrency patterns.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for API Gateway throttling configuration changes related to API `<api-id>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when APIGatewayThrottling or 4XXError alarms first triggered. This timestamp establishes when throttling began and serves as the correlation baseline.

2. If CloudWatch metrics (from Playbook step 2) show Count exceeding rate limits around the alarm time, compare with throttling configuration (from Playbook step 3). If configured rate/burst limits are lower than peak traffic, insufficient limits are the root cause.

3. If throttling occurred after CloudTrail shows configuration changes (from Playbook step 9), verify whether rate limit reductions or usage plan modifications caused the throttling to begin.

4. If access logs (from Playbook step 4) show 429 errors concentrated on specific API keys or stages, examine usage plan configuration (from Playbook step 7). Usage plan throttling may be more restrictive than API-level throttling.

5. If API type (from Playbook step 6) is HTTP API and throttling patterns differ from REST API expectations, note that HTTP APIs have different default throttling behavior and burst capacity calculations.

6. If Lambda concurrency metrics (from Playbook step 8) show throttling around the same timestamp as API throttling, Lambda concurrency limits are causing backend throttling that propagates to the API layer.

7. If throttling is intermittent rather than constant (from Playbook step 2 trend), burst capacity is being exhausted during peak periods. Burst limits may need adjustment or traffic should be smoothed at the client level.

If no correlation is found: extend analysis to 24 hours, review API key-specific throttling limits, check account-level API Gateway throttling quotas, verify WebSocket API throttling behavior if applicable, and examine client request patterns for burst traffic.
