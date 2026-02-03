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

1. Analyze AWS service health from Playbook step 1 to verify API Gateway service availability in the region. If service health indicates issues, 500 errors may be AWS-side requiring monitoring rather than configuration changes.

2. If API Gateway logs from Playbook step 8 show specific error messages, use these to identify the failure point. Examine execution logs for timestamps and error context (integration timeout, Lambda error, mapping template failure).

3. If resource policies from Playbook step 2 contain Deny statements or do not Allow the requesting source, API Gateway returns 500 for policy violations. Verify resource policy permits the caller.

4. If API type from Playbook step 3 is REST API, examine execution logs for detailed error traces. HTTP APIs have simpler error handling but may return generic 500s for Lambda integration failures.

5. If Lambda integration (Playbook step 4) shows the execution role lacks lambda:InvokeFunction permission or Lambda resource policy does not allow API Gateway, invocation fails with 500. Verify both IAM policy and Lambda resource-based policy.

6. If integration timeout from Playbook step 6 is shorter than Lambda execution time, API Gateway times out and returns 504 (gateway timeout) which may appear as 500 in some client contexts. Increase timeout if Lambda requires more time.

7. If integration type from Playbook step 7 shows HTTP integration with an unreachable or failing backend, API Gateway returns 500. Verify backend service health and network connectivity.

8. If mapping templates from Playbook step 9 contain syntax errors or reference non-existent request/response fields, transformation fails with 500. Validate VTL template syntax.

9. If WAF logs from Playbook step 10 show blocked requests, WAF rules may be rejecting traffic before it reaches API Gateway integration, causing error responses.

If no correlation is found from the collected data: extend API Gateway log query timeframes to 30 minutes, verify Lambda function CloudWatch logs for execution errors, check for API Gateway authorizer failures (Lambda or Cognito), and examine stage variables for misconfigurations. 500 errors may result from Lambda cold start failures, VPC connectivity issues for Lambda integrations, or API Gateway canary deployment misconfigurations.

