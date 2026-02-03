# API Gateway Route Not Matching Requests

## Meaning

API Gateway route is not matching requests (triggering routing failures or APIGatewayRouteMismatch alarms) because route configuration is incorrect, route path patterns do not match request paths, HTTP method mappings are wrong, route priority conflicts exist, route integration is misconfigured, or API Gateway route path parameters are incorrectly configured. API Gateway routes do not match requests, requests return 404 Not Found errors, and route routing fails. This affects the API layer and blocks endpoint access, typically caused by route configuration issues, path pattern problems, or integration errors; if using API Gateway HTTP APIs vs REST APIs, route configuration may differ and applications may experience routing failures.

## Impact

API Gateway routes do not match requests; requests return 404 Not Found errors; route routing fails; API endpoints are unreachable; route configuration is ineffective; request routing is incorrect; API integration fails; user-facing routing errors occur. APIGatewayRouteMismatch alarms may fire; if using API Gateway HTTP APIs vs REST APIs, route configuration may differ; applications may experience errors or performance degradation due to failed routing; API endpoints may be completely unreachable.

## Playbook

1. Verify API Gateway API `<api-id>` exists and AWS service health for API Gateway in region `<region>` is normal.
2. Retrieve the API Gateway REST API `<api-id>` or HTTP API `<api-id>` in region `<region>` and inspect its route configurations, path patterns, HTTP method mappings, and route priorities, verifying route configuration.
3. Query CloudWatch Logs for log groups containing API Gateway access logs and filter for 404 error patterns or route mismatch events related to API `<api-id>`, including request path details.
4. Retrieve CloudWatch metrics for API Gateway API `<api-id>` including 4XXError and Count over the last 1 hour to identify routing error patterns, analyzing error frequency.
5. List API Gateway routes for API `<api-id>` and check route path patterns, method configurations, and route integration settings, verifying route matching logic.
6. Query CloudWatch Logs for log groups containing API Gateway execution logs and filter for route matching failures or routing decision patterns, including routing decision details.
7. Retrieve the API Gateway API `<api-id>` route path parameter configuration and verify path parameters are correctly configured, checking if path parameters affect matching.
8. Retrieve the API Gateway API `<api-id>` route integration configuration and verify integration settings, checking if integration configuration affects routing.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for API Gateway route or path pattern modification events related to API `<api-id>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch Logs containing API Gateway access logs (from Playbook step 3) to identify specific 404 error patterns and the request paths that failed. If access logs show requests to paths that should exist, the route path patterns may not match the request format. Compare actual request paths with configured route patterns.

2. Review CloudWatch metrics for API Gateway (from Playbook step 4) including 4XXError and Count over the last hour to identify routing error patterns. If 4XX errors suddenly increased, correlate the timestamp with recent route configuration changes. If errors are constant, the route configuration has a persistent issue.

3. Examine API Gateway route configuration (from Playbook step 2) to verify route path patterns, HTTP methods, and route priorities. If path patterns use incorrect syntax (especially for path parameters in HTTP APIs vs REST APIs), requests will not match routes.

4. Review API Gateway execution logs (from Playbook step 6) to understand routing decision logic for failed requests. Execution logs show which routes were evaluated and why requests did not match any route.

5. Verify route path parameter configuration (from Playbook step 7) to ensure path parameters are correctly defined. HTTP APIs use {proxy+} syntax while REST APIs may use different formats. If path parameter syntax is incorrect, routes with dynamic segments will not match.

6. Check route integration configuration (from Playbook step 8) to verify integrations are properly configured. Even if routes match, misconfigured integrations can cause request failures.

7. Correlate CloudTrail events (from Playbook step 9) with route mismatch timestamps within 5 minutes to identify any route or path pattern modifications. If configuration changes coincide with when requests started failing, those changes are the likely cause.

8. Compare route mismatch patterns across different routes within 1 hour. If mismatches are route-specific, focus on that route's path pattern syntax. If mismatches affect all routes, check API-wide configuration like stage settings or base path mappings.

9. For HTTP APIs, verify the route format follows the {method} {path} syntax (e.g., "GET /users/{userId}"). For REST APIs, verify resource paths and method configurations match expected request patterns.

If no correlation is found within the specified time windows: extend timeframes to 24 hours, review alternative evidence sources including route integration configuration and API Gateway stage settings, check for gradual issues like route path pattern changes or HTTP method mapping modifications, verify external dependencies like request path formatting or route integration availability, examine historical patterns of route mismatches, check for API Gateway HTTP API route format differences, verify API Gateway route path parameter syntax. Route mismatches may result from route path pattern syntax errors, route priority conflicts, route integration configuration issues, API Gateway HTTP API route format differences, or API Gateway route path parameter syntax rather than immediate route configuration changes.
