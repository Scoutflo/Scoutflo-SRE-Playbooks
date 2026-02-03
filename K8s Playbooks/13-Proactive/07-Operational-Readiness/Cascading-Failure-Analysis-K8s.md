# Cascading Failure Analysis

## Meaning

Cascading failure analysis indicates that cascading failure risks cannot be analyzed or cascading failure patterns are detected (triggering alerts like CascadingFailureDetected or FailureCascadeAnalysisFailed) because cascading failure analysis tools fail, cascading failure patterns are not detected, failure propagation paths are not identified, cascading failure risk assessment is unavailable, or cascading failure monitoring indicates problems. Cascading failure analysis shows failures, cascading failure patterns are detected, failure propagation paths are not identified, and cascading failure risk assessment fails. This affects the dependency management layer and service resilience, typically caused by service dependency failures, failure propagation tracking issues, cascading failure analysis tool failures, or cascading failure monitoring issues; if cascading failures affect container workloads, container service failures may propagate and applications may experience widespread service outages.

## Impact

CascadingFailureDetected alerts fire; FailureCascadeAnalysisFailed alerts fire; cascading failure risks cannot be analyzed; cascading failure patterns are detected; service resilience is compromised; widespread service outages may occur. Cascading failure analysis shows failures; if cascading failures affect container workloads, container service failures may propagate, pod failures may cascade, and container applications may experience widespread service outages; applications may experience service-wide failures or cascading failure propagation.

## Playbook

1. List pods and services in namespace <namespace> with wide output to identify current state of all workloads and potential failure points.

2. List recent events in namespace <namespace> sorted by timestamp to identify cascading failure patterns and failure propagation timeline.

3. Describe pod <pod-name> in namespace <namespace> to understand failure causes and dependencies.

4. Retrieve logs from pod <pod-name> in namespace <namespace> and filter for cascading failure patterns or failure propagation patterns.

5. Retrieve Prometheus metrics for service error rates including error_rate and failure_rate over the last 24 hours to identify failure propagation patterns across services.

6. Retrieve service mesh trace data for service `<service-name>` and analyze trace error propagation to identify cascading failure paths and downstream service impact.

7. Retrieve service mesh service map data for namespace `<namespace>` and analyze service dependency paths to identify potential cascading failure propagation routes.

8. Retrieve logs from network policy controller pods and filter for service-to-service communication failures to identify network-level cascading failures.

## Diagnosis

1. Review the pod and service status from Step 1 and events from Step 2. If multiple services failed within a short timeframe, this suggests cascading failure. Identify the first service to fail as the likely root cause.

2. Analyze the service error rate metrics from Step 5. If error rates increased sequentially across services in dependency order, then failures propagated through the dependency chain. If error rates increased simultaneously, then a shared dependency may be the root cause.

3. If Step 6 trace data shows error propagation patterns, identify the service where errors originated. If trace data is incomplete, then tracing coverage gaps are preventing failure analysis.

4. Review the service dependency map from Step 7. If dependency paths exist between failed services, then cascading failure through those paths is confirmed. If failed services are not connected, then shared infrastructure (network, storage) may be the common failure point.

5. If Step 4 pod logs show failure patterns, identify whether failures are timeout-related (suggesting downstream unavailability) or error-related (suggesting upstream data/request issues).

If analysis is inconclusive: Examine network policy logs from Step 8 for service-to-service communication failures. Determine whether cascading failures follow the expected dependency graph or reveal unexpected dependencies. Verify that circuit breakers and other resilience mechanisms are configured to prevent failure propagation.
