# Service Dependency Mapping

## Meaning

Service dependency mapping indicates that service dependencies cannot be mapped or dependency relationships are not identified (triggering alerts like DependencyMappingFailed or ServiceDependencyUnavailable) because service dependency mapping tools fail, dependency relationships are not discovered, service dependency graphs are unavailable, dependency mapping data is missing, or service dependency analysis cannot be performed. Service dependency mapping shows failures, dependency relationships are not identified, service dependency graphs are unavailable, and service dependency analysis fails. This affects the dependency management layer and service architecture understanding, typically caused by dependency mapping tool failures, service discovery issues, dependency relationship tracking failures, or dependency mapping data collection issues; if dependency mapping affects container workloads, container service dependencies may be unknown and applications may experience dependency-related failures.

## Impact

DependencyMappingFailed alerts fire; ServiceDependencyUnavailable alerts fire; service dependencies cannot be mapped; dependency relationships are not identified; service architecture understanding is limited; dependency-related failures may occur unexpectedly. Service dependency mapping is unavailable; if dependency mapping affects container workloads, container service dependencies may be unknown, pod dependencies may be unmapped, and container applications may experience dependency-related failures; applications may experience service dependency failures or architecture understanding gaps.

## Playbook

1. List all services in namespace <namespace> with wide output to retrieve their endpoint configurations, selectors, and cluster IPs.
2. List recent events in namespace <namespace> sorted by timestamp to identify service connectivity issues, endpoint changes, or dependency-related errors.
3. Describe service <service-name> in namespace <namespace> to inspect the service configuration including endpoints, target ports, and backend pod selectors.
4. Retrieve Prometheus metrics for service-to-service communication including service_call_count and service_latency metrics over the last 7 days to identify service dependency patterns.
5. Retrieve service mesh trace data for service `<service-name>` and analyze trace segments to identify downstream service dependencies and dependency relationships.
6. Compare service dependency mapping results with service call pattern timestamps and verify whether dependencies are accurately mapped, using application pod logs as supporting evidence.
7. Retrieve service mesh service map data for namespace `<namespace>` and verify service dependency graph availability, checking service mesh configuration.
8. Retrieve logs from network policy controller pods and filter for inter-service communication patterns to identify network-level service dependencies.

## Diagnosis

1. Review the service-to-service communication metrics from Step 4. If service call patterns show dependencies not reflected in the service map, then mapping is incomplete. If call patterns match the map, then mapping is accurate for active dependencies.

2. Analyze the service mesh trace data from Step 5. If trace segments reveal downstream service calls, these represent actual runtime dependencies that should be in the dependency map. If traces show unexpected dependencies, investigate whether these are intentional.

3. If Step 7 service mesh service map shows unavailable data, then mapping infrastructure is failing. If the map is available but incomplete, then specific services may not be instrumented for dependency detection.

4. Review the network-level dependencies from Step 8. If network policy logs show inter-service communication not reflected in application-level mapping, then lower-level dependencies exist that may not be captured by application tracing.

5. If Step 6 comparison shows dependency mapping results diverging from actual call patterns, then mapping accuracy has degraded. Focus on services with the largest discrepancies.

If analysis is inconclusive: Examine events from Step 2 for service connectivity issues or endpoint changes that may indicate dependency relationship changes. Determine whether mapping failures affect all services (suggesting infrastructure issues) or specific services (suggesting service-level configuration gaps). Verify that service discovery and service mesh components are functioning correctly.
