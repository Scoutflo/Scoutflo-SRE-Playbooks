# Dependency Health Check

## Meaning

Dependency health check indicates that service dependency health cannot be verified or dependency health issues are detected (triggering alarms like DependencyHealthCheckFailed or DependencyUnhealthy) because dependency health checks fail, dependency health status is unavailable, dependency health monitoring indicates problems, dependency connectivity checks fail, or dependency health check tools are unavailable. Dependency health checks show failures, dependency health status is unavailable, dependency health monitoring indicates problems, and dependency health check tools fail. This affects the dependency management layer and service reliability, typically caused by dependency service unavailability, dependency connectivity issues, dependency health check tool failures, or dependency health monitoring issues; if dependency health affects container workloads, container service dependencies may be unhealthy and applications may experience dependency-related failures.

## Impact

DependencyHealthCheckFailed alarms fire; DependencyUnhealthy alarms fire; dependency health cannot be verified; dependency health issues are detected; service reliability is compromised; dependency-related failures may occur. Dependency health checks show failures; if dependency health affects container workloads, container service dependencies may be unhealthy, pod dependencies may be unavailable, and container applications may experience dependency-related failures; applications may experience service dependency failures or health check failures.

## Playbook

1. Retrieve the Application Load Balancer `<alb-arn>` target group health check status and verify target health status and dependency service availability, checking load balancer dependency health.
2. Retrieve CloudWatch metrics for service health including HealthyHostCount and UnhealthyHostCount over the last 24 hours to identify dependency health issues.
3. Query CloudWatch Logs for log groups containing service health check events and filter for dependency health check failures or unhealthy dependency patterns within the last 24 hours.
4. Retrieve Route 53 Health Check `<health-check-id>` status for dependency service endpoints and verify health check results and dependency availability, checking DNS-level dependency health.
5. Retrieve CloudWatch metrics for API Gateway API health including 4xxErrorRate and 5xxErrorRate over the last 24 hours to identify API dependency health issues.
6. Compare dependency health check failure timestamps with dependency service error timestamps within 5 minutes and verify whether service errors cause health check failures, using dependency health check results as supporting evidence.
7. Retrieve X-Ray trace data for service `<service-name>` and analyze trace error rates to identify unhealthy downstream dependencies, checking trace-level dependency health.
8. List CloudWatch alarms with state 'ALARM' for dependency services and verify alarm status indicates dependency health issues, checking alarm-based dependency health monitoring.

## Diagnosis

1. **Analyze target health from Step 1 and Step 2**: If UnhealthyHostCount is elevated, identify which targets are failing health checks. If HealthyHostCount is zero, the dependency is completely unavailable. If health fluctuates, intermittent issues exist.

2. **Evaluate Route 53 health from Step 4**: If DNS health checks show unhealthy status, the dependency endpoint is not responding. If health check failure reason indicates timeout, network or overload issues exist. If response validation fails, the dependency returns incorrect data.

3. **Review API Gateway metrics from Step 5**: If 5xxErrorRate is elevated, dependencies behind API Gateway are failing. If 4xxErrorRate is high, client-side issues or misconfigurations exist. If both rates are elevated, broader issues affect the dependency.

4. **Cross-reference with trace data from Step 7**: If traces show high error rates to specific downstream services, those are the unhealthy dependencies. If latency is elevated before errors, dependencies are degraded before failing.

5. **Assess alarm status from Step 8**: If dependency alarms are in ALARM state, investigate those specific services. If multiple dependency alarms fire together, a common cause exists. If alarms are not firing but health checks fail, alarm thresholds need review.

If the above analysis is inconclusive: Test dependency endpoints directly with health check tools. Review dependency service logs for specific errors. Check network connectivity between services. Implement circuit breakers to prevent cascading failures during dependency issues.
