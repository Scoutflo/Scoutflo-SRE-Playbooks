# API Gateway CORS Issues

## Meaning

API Gateway CORS (Cross-Origin Resource Sharing) issues occur (triggering CORS errors or APIGatewayCORS errors) because CORS headers are not configured, allowed origins are incorrect, preflight OPTIONS requests fail, CORS configuration is missing or misconfigured, response headers do not include required CORS headers, or API Gateway deployment removes CORS settings. Cross-origin requests fail, browser CORS errors occur, and web applications cannot access APIs from different origins. This affects the API layer and blocks cross-origin access, typically caused by CORS configuration issues, missing OPTIONS methods, or deployment problems; if using API Gateway HTTP APIs vs REST APIs, CORS behavior differs and applications may experience cross-origin request failures.

## Impact

Cross-origin requests fail; browser CORS errors occur; web applications cannot access APIs; preflight requests are rejected; API responses lack CORS headers; frontend applications cannot communicate with backend APIs; user-facing errors increase; API integration fails. APIGatewayCORS errors fire; if using API Gateway HTTP APIs vs REST APIs, CORS configuration differs; applications may experience errors or performance degradation due to blocked cross-origin requests; frontend-backend integration breaks.

## Playbook

1. Verify API Gateway API `<api-id>` exists and is deployed, and AWS service health for API Gateway in region `<region>` is normal.
2. Retrieve the API Gateway REST API `<api-id>` or HTTP API `<api-id>` in region `<region>` and inspect its CORS configuration, allowed origins, allowed methods, and allowed headers settings, verifying CORS is enabled.
3. Query CloudWatch Logs for log groups containing API Gateway access logs and filter for CORS-related error patterns or preflight request failures, including OPTIONS request failures.
4. Retrieve CloudWatch metrics for API Gateway API `<api-id>` including 4XXError and 5XXError over the last 1 hour to identify CORS-related error patterns, analyzing error frequency.
5. Retrieve the API Gateway `<api-id>` API type (REST API vs HTTP API) and verify API type configuration, checking type-specific CORS behavior differences.
6. Retrieve the API Gateway `<api-id>` method configurations and check OPTIONS method configuration and CORS header settings, verifying OPTIONS method exists for preflight requests.
7. Query CloudWatch Logs for log groups containing application logs and filter for CORS error messages or cross-origin request failures, including browser console error patterns.
8. Retrieve the API Gateway `<api-id>` deployment configuration and verify CORS settings are included in deployment, checking if deployments removed CORS configuration.
9. Query CloudWatch Logs for log groups containing API Gateway execution logs and filter for CORS header response patterns, verifying CORS headers in responses.

## Diagnosis

1. Analyze CloudWatch metrics (from Playbook step 4) to identify when 4XXError rates increased. Cross-reference with access logs (from Playbook step 3) to confirm CORS-related 403 or preflight failures occurred at this timestamp.

2. If API type check (from Playbook step 5) shows HTTP API, verify CORS configuration is set at API level. If REST API, check that OPTIONS method exists for each resource (from Playbook step 6). Missing OPTIONS methods cause preflight request failures.

3. If CloudTrail events (from Playbook step 9) show API Gateway deployment around the error timestamp, compare pre and post-deployment CORS settings. Deployments may have inadvertently removed or overwritten CORS configuration.

4. If CORS configuration exists (from Playbook step 2) but errors persist, examine allowed origins settings. If the requesting origin does not exactly match configured origins (including protocol and port), CORS rejections will occur.

5. If access logs (from Playbook step 3) show preflight OPTIONS requests returning 4XX errors, check OPTIONS method configuration (from Playbook step 6). The OPTIONS response must include Access-Control-Allow-Origin, Access-Control-Allow-Methods, and Access-Control-Allow-Headers.

6. If CORS errors are method-specific (from Playbook step 3 analysis), integration response headers (from Playbook step 9) may be missing CORS headers for that specific method while other methods work correctly.

7. If browser console errors (from Playbook step 7) indicate credential-related CORS failures, Access-Control-Allow-Credentials header may be missing or misconfigured for authenticated requests.

If no correlation is found: extend analysis to 2 hours, verify frontend application origin matches configured allowed origins exactly, check HTTP API vs REST API CORS behavior differences, and examine authorizer CORS handling for authenticated endpoints.
