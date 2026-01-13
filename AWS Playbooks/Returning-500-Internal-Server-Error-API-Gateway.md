# API Gateway Returning 500 Internal Server Error

## Meaning

API Gateway returns 500 Internal Server Error responses (triggering alarms like API Gateway 5XX errors or APIGateway500Error alarms) because API Gateway resource policies block access, IAM roles and permissions are misconfigured, Lambda function execution roles lack invoke permissions, CloudWatch logs show API Gateway errors, AWS WAF rules are blocking requests, integration timeout settings are too low, or integration endpoint failures occur. API requests fail with 500 errors, API endpoints become unavailable, and CloudWatch Logs show API Gateway errors. This affects the API layer and blocks API access, typically caused by integration configuration issues, permission problems, or timeout settings; if using API Gateway HTTP APIs vs REST APIs, error behavior may differ and applications may experience API call failures.

## Impact

API requests fail with 500 errors; API endpoints become unavailable; API Gateway 5XX error alarms fire; downstream services cannot receive requests; application integrations fail; user-facing API calls error; service-to-service communication breaks; API response times increase; error rates spike. APIGateway500Error alarms fire; if using API Gateway HTTP APIs vs REST APIs, error patterns may differ; applications may experience errors or performance degradation due to API failures; downstream services may not receive expected requests.

## Playbook

1. Verify API Gateway API `<api-id>` exists and is deployed, and AWS service health for API Gateway in region `<region>` is normal.
2. Retrieve the API Gateway `<api-id>` resource policies and verify policies allow access to the API Gateway, checking resource policy configuration.
3. Retrieve the API Gateway `<api-id>` API type (REST API vs HTTP API) and verify API type configuration, checking type-specific error behavior.
4. Retrieve the IAM role `<role-name>` and policy `<policy-name>` and check if IAM roles and permissions are set up correctly for API Gateway access, and if using Lambda integration, retrieve the Lambda function `<function-name>` execution role and verify it has lambda:InvokeFunction permissions, verifying IAM policy evaluation and Lambda resource-based policy.
6. Retrieve the API Gateway `<api-id>` integration timeout settings and verify integration timeout is sufficient for downstream services, checking timeout configuration.
7. Retrieve the API Gateway `<api-id>` integration type (Lambda vs HTTP vs AWS service) and verify integration type configuration, checking integration endpoint.
8. Query CloudWatch Logs for log group containing API Gateway logs for API `<api-id>` and filter for error patterns, 500 errors, or execution failures, including integration errors.
9. Retrieve the API Gateway `<api-id>` request/response mapping templates and verify mapping templates are correctly configured, checking template syntax errors.
10. Query CloudWatch Logs for log groups containing WAF logs if using AWS WAF and filter for blocked requests related to API Gateway `<api-id>`, checking WAF rule evaluation.

## Diagnosis

1. Compare API Gateway resource policy modification timestamps with 500 error timestamps within 5 minutes and verify whether 500 errors began shortly after resource policy changes, using API Gateway configuration data as supporting evidence.
2. Correlate IAM role permission change timestamps with API error timestamps and verify whether 500 errors occurred after IAM permission changes, using IAM role configuration data as supporting evidence.
3. Compare Lambda function execution role modification timestamps with API Gateway error timestamps within 5 minutes and verify whether permission changes prevented Lambda invocation, using Lambda permission events as supporting evidence.
4. Compare API Gateway integration timeout modification timestamps with 500 error timestamps and verify whether timeout changes caused integration failures, using API Gateway integration configuration events as supporting evidence.
5. Analyze 500 error frequency over the last 15 minutes to determine if errors are constant (configuration issue) or intermittent (downstream service failures).

If no correlation is found within the specified time windows: extend timeframes to 30 minutes, review alternative evidence sources including Lambda function errors and integration endpoint failures, check for gradual issues like downstream service degradation, verify external dependencies like Lambda function availability, examine historical patterns of API Gateway errors, check for API Gateway HTTP APIs vs REST APIs differences, verify API Gateway WebSocket API scenarios. 500 errors may result from Lambda function execution failures, integration endpoint issues, downstream service unavailability, API Gateway request/response mapping template errors, or API Gateway authorizer failures rather than immediate API Gateway configuration changes.
