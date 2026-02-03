# API Dependency Status

## Meaning

API dependency status indicates that API dependencies are unavailable or API dependency health issues are detected (triggering alerts like APIDependencyUnavailable or APIDependencyHealthFailed) because API dependency health checks fail, API dependency connectivity is impaired, API dependency response times exceed thresholds, API dependency error rates are high, or API dependency monitoring indicates problems. API dependency health checks show failures, API dependency connectivity is impaired, API dependency response times are high, and API dependency monitoring indicates problems. This affects the dependency management layer and API reliability, typically caused by API dependency service unavailability, API dependency connectivity issues, API dependency performance problems, or API dependency monitoring failures; if API dependencies affect container workloads, container API calls may fail and applications may experience API dependency-related failures.

## Impact

APIDependencyUnavailable alerts fire; APIDependencyHealthFailed alerts fire; API dependency health cannot be verified; API dependency connectivity issues are detected; API reliability is compromised; API calls may fail. API dependency health checks show failures; if API dependencies affect container workloads, container API calls may fail, pod API dependencies may be unavailable, and container applications may experience API dependency-related failures; applications may experience API call failures or API dependency health issues.

## Playbook

1. Describe service <service-name> in namespace <namespace> to inspect service endpoint health status and backend service connectivity.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent API dependency issues or service changes.

3. Retrieve endpoints <service-name> in namespace <namespace> with YAML output to verify backend pod connectivity and health status.

4. Retrieve logs from application pods with label app=<app-name> in namespace <namespace> and filter for API dependency error patterns or timeout patterns.

5. Retrieve Prometheus metrics for service API including 4xx_error_rate, 5xx_error_rate, and latency over the last 24 hours to identify API dependency health issues.

6. Retrieve service mesh trace data for API calls and analyze trace segments to identify API dependency response times and error rates, checking trace-level API dependency health.

7. Retrieve Prometheus metrics for service API including integration_latency and backend_latency over the last 24 hours to identify API dependency performance issues.

8. List active Prometheus alerts with state 'firing' for service APIs and verify alert status indicates API dependency health issues, checking alert-based API dependency health monitoring.

## Diagnosis

1. Review the endpoint health status from Steps 1 and 3. If endpoints show unhealthy backends or missing addresses, then API dependency connectivity is broken. Verify backend pod health and network policies.

2. Analyze the API error rate metrics from Step 5. If 4xx errors are high, then client-side request issues exist. If 5xx errors are high, then backend service failures are occurring. Focus remediation based on error type.

3. If Step 4 application logs show timeout patterns, then API dependency response times exceed client timeouts. Review the latency metrics from Step 7 to identify whether backend or integration latency is the issue.

4. Review the trace data from Step 6. If trace analysis shows specific API endpoints with high error rates or latency, focus investigation on those endpoints. If all endpoints are affected, then the issue is service-wide.

5. If Step 8 alerts show firing for API services, then alerting is correctly detecting issues. If alerts are not firing despite health issues, then alert thresholds need adjustment.

If analysis is inconclusive: Examine events from Step 2 for API service changes or endpoint updates. Determine whether health issues affect all API consumers (suggesting server-side issues) or specific consumers (suggesting client-side or network issues). Verify that API dependency health checks have appropriate timeouts and thresholds.
