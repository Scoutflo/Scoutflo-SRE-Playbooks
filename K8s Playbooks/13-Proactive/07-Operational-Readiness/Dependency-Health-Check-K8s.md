# Dependency Health Check

## Meaning

Dependency health check indicates that service dependency health cannot be verified or dependency health issues are detected (triggering alerts like DependencyHealthCheckFailed or DependencyUnhealthy) because dependency health checks fail, dependency health status is unavailable, dependency health monitoring indicates problems, dependency connectivity checks fail, or dependency health check tools are unavailable. Dependency health checks show failures, dependency health status is unavailable, dependency health monitoring indicates problems, and dependency health check tools fail. This affects the dependency management layer and service reliability, typically caused by dependency service unavailability, dependency connectivity issues, dependency health check tool failures, or dependency health monitoring issues; if dependency health affects container workloads, container service dependencies may be unhealthy and applications may experience dependency-related failures.

## Impact

DependencyHealthCheckFailed alerts fire; DependencyUnhealthy alerts fire; dependency health cannot be verified; dependency health issues are detected; service reliability is compromised; dependency-related failures may occur. Dependency health checks show failures; if dependency health affects container workloads, container service dependencies may be unhealthy, pod dependencies may be unavailable, and container applications may experience dependency-related failures; applications may experience service dependency failures or health check failures.

## Playbook

1. Describe service <service-name> in namespace <namespace> to inspect endpoint health status and dependency service availability.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent dependency health issues or service failures.

3. Retrieve endpoints <service-name> in namespace <namespace> with YAML output to verify backend pod connectivity and health status.

4. Retrieve logs from service health check pods with label app=health-check in namespace <namespace> and filter for dependency health check failures.

5. Retrieve Prometheus metrics for service health including healthy_endpoint_count and unhealthy_endpoint_count over the last 24 hours to identify dependency health issues.

6. Describe ingress in namespace <namespace> for dependency service endpoints and verify health check results.

7. Retrieve service mesh trace data for service `<service-name>` and analyze trace error rates to identify unhealthy downstream dependencies, checking trace-level dependency health.

8. List active Prometheus alerts with state 'firing' for dependency services and verify alert status indicates dependency health issues, checking alert-based dependency health monitoring.

## Diagnosis

1. Review the service endpoint health from Steps 1 and 3. If endpoints show unhealthy backends or missing addresses, then dependency services are unavailable. Verify backend pod health and network policies.

2. Analyze the health check logs from Step 4. If logs show health check failure patterns, identify whether failures are timeout-related (suggesting performance issues) or error-related (suggesting service issues).

3. If Step 5 health metrics show high unhealthy endpoint counts, then multiple dependencies are failing. Prioritize investigation based on dependency criticality.

4. Review the trace-level dependency health from Step 7. If trace analysis shows specific downstream services with high error rates, focus investigation on those services.

5. If Step 8 alerts show firing for dependency services, then alerting is correctly detecting issues. If issues exist but alerts are not firing, then alert thresholds need adjustment.

If analysis is inconclusive: Examine events from Step 2 for dependency health issues or service failures. Review the ingress health from Step 6 to verify external endpoint health. Determine whether health issues affect all dependencies (suggesting network or infrastructure issues) or specific dependencies (suggesting service-specific problems).
