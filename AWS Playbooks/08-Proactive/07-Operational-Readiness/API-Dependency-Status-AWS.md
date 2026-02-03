# API Dependency Status

## Meaning

API dependency status indicates that API dependencies are unavailable or API dependency health issues are detected (triggering alarms like APIDependencyUnavailable or APIDependencyHealthFailed) because API dependency health checks fail, API dependency connectivity is impaired, API dependency response times exceed thresholds, API dependency error rates are high, or API dependency monitoring indicates problems. API dependency health checks show failures, API dependency connectivity is impaired, API dependency response times are high, and API dependency monitoring indicates problems. This affects the dependency management layer and API reliability, typically caused by API dependency service unavailability, API dependency connectivity issues, API dependency performance problems, or API dependency monitoring failures; if API dependencies affect container workloads, container API calls may fail and applications may experience API dependency-related failures.

## Impact

APIDependencyUnavailable alarms fire; APIDependencyHealthFailed alarms fire; API dependency health cannot be verified; API dependency connectivity issues are detected; API reliability is compromised; API calls may fail. API dependency health checks show failures; if API dependencies affect container workloads, container API calls may fail, pod API dependencies may be unavailable, and container applications may experience API dependency-related failures; applications may experience API call failures or API dependency health issues.

## Playbook

1. Retrieve the API Gateway API `<api-id>` configuration and inspect API endpoint health status and backend service connectivity, verifying API dependency accessibility.
2. Retrieve CloudWatch metrics for API Gateway API including 4xxErrorRate, 5xxErrorRate, and Latency over the last 24 hours to identify API dependency health issues.
3. Query CloudWatch Logs for log groups containing API Gateway access logs and filter for API dependency error patterns or timeout patterns within the last 24 hours.
4. Retrieve X-Ray trace data for API calls and analyze trace segments to identify API dependency response times and error rates, checking trace-level API dependency health.
5. Retrieve the Application Load Balancer `<alb-arn>` target group health status for API backend services and verify target health indicates API dependency availability, checking load balancer-level API dependency health.
6. Compare API dependency health check failure timestamps with API dependency service error timestamps within 5 minutes and verify whether service errors cause health check failures, using API Gateway API configuration data as supporting evidence.
7. Retrieve CloudWatch metrics for API Gateway API including IntegrationLatency and BackendLatency over the last 24 hours to identify API dependency performance issues.
8. List CloudWatch alarms with state 'ALARM' for API Gateway APIs and verify alarm status indicates API dependency health issues, checking alarm-based API dependency health monitoring.

## Diagnosis

1. **Analyze API Gateway metrics from Step 2**: If 5xxErrorRate is elevated, backend services are failing. If 4xxErrorRate is high, client requests are malformed or authentication is failing. If Latency is high but error rates are normal, performance degradation exists without failures.

2. **Evaluate backend integration from Step 7**: If IntegrationLatency is high, the API Gateway to backend connection is slow. If BackendLatency is high, the backend service itself is slow. If both are high, network or backend overload is the cause.

3. **Review X-Ray traces from Step 4**: If traces show specific downstream services with high error rates, those services are the root cause. If traces show timeouts, dependencies are overloaded or unresponsive.

4. **Cross-reference with target health from Step 5**: If ALB targets are unhealthy, the backend services are not responding to health checks. If some targets are healthy and others are not, partial availability exists.

5. **Assess alarm status from Step 8**: If API alarms are in ALARM state, the issue is confirmed. If alarms are not firing but issues exist, alarm thresholds need review. If multiple API alarms fire together, a common dependency is failing.

If the above analysis is inconclusive: Test API endpoints directly with curl or Postman. Review API Gateway execution logs for specific errors. Check VPC connectivity if API integrates with private resources. Verify API stage deployment is current.
