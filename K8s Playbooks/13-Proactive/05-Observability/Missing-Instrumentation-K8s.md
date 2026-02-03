# Missing Instrumentation

## Meaning

Missing instrumentation indicates that pods or services are not properly instrumented for observability or instrumentation gaps are detected (triggering alerts like InstrumentationMissing or ObservabilityGapDetected) because Prometheus metrics are not collected, pod logs are not configured, distributed tracing is not enabled, custom metrics are missing, or instrumentation coverage is incomplete. Instrumentation gaps are detected, Prometheus metrics are missing, pod logs are not configured, and instrumentation coverage is incomplete. This affects the observability layer and monitoring coverage, typically caused by instrumentation configuration failures, monitoring tool unavailability, instrumentation deployment issues, or instrumentation coverage gaps; if missing instrumentation affects container workloads, container observability may be incomplete and applications may experience monitoring blind spots.

## Impact

InstrumentationMissing alerts fire; ObservabilityGapDetected alerts fire; pods are not properly instrumented; monitoring coverage is incomplete; observability gaps exist; troubleshooting may be difficult. Instrumentation gaps are detected; if missing instrumentation affects container workloads, container observability may be incomplete, pod metrics may be missing, and container applications may experience monitoring blind spots; applications may experience observability gaps or monitoring failures.

## Playbook

1. List pods, deployments, and services in namespace <namespace> with wide output and describe deployment <deployment-name> in namespace <namespace> to understand the instrumentation configuration and identify pods without proper observability setup.

2. List recent events in namespace <namespace> sorted by timestamp to identify any instrumentation-related failures or configuration issues during pod startup.

3. List pods in namespace `<namespace>` and verify Prometheus metrics collection status and metrics exporter configuration, checking pod-level instrumentation.

4. List deployments in namespace `<namespace>` and verify pod log configuration and distributed tracing enablement status, checking deployment instrumentation.

5. List services in namespace `<namespace>` and verify service monitoring configuration and metrics collection settings, checking service instrumentation.

6. Retrieve Prometheus metrics namespace coverage for services in namespace `<namespace>` and verify metric collection coverage to identify services without metrics, checking metric instrumentation gaps.

7. Retrieve Prometheus metrics for pod metrics including pod_metrics_available and pod_logs_configured over the last 7 days to identify missing metrics or metric collection failures, checking metric collection health.

8. Compare instrumentation coverage analysis results with pod deployment timestamps and verify whether new pods are instrumented upon deployment, using pod configuration data as supporting evidence.

9. Retrieve Prometheus exporter status for pods in namespace `<namespace>` and verify exporter health and metric collection status, checking metrics exporter coverage.

10. List Prometheus service monitors and verify service monitor coverage for services to identify services without service monitors, checking service monitor coverage gaps.

## Diagnosis

1. Review the pod-level instrumentation status from Steps 3-5. If pods lack Prometheus metrics collection, log configuration, or distributed tracing enablement, prioritize addressing each gap based on operational criticality.

2. Analyze the metric instrumentation from Steps 6-7. If services show no metrics in Prometheus or metric collection health shows failures, then metric observability is compromised. Focus on exporter installation and ServiceMonitor configuration.

3. If Step 9 exporter status shows unhealthy exporters, then existing instrumentation is failing. If exporters are healthy but Step 10 ServiceMonitor coverage shows gaps, then collection configuration is the issue.

4. Review the deployment instrumentation from Step 4. If deployments lack log configuration or distributed tracing, then application-level observability for debugging and performance analysis will be limited.

5. If Step 8 shows new pods without instrumentation upon deployment, then deployment templates and automation pipelines need updating to include observability configuration as standard practice.

If analysis is inconclusive: Examine events from Step 2 for instrumentation-related failures during pod startup. Determine whether instrumentation gaps affect all observability pillars (metrics, logs, traces) or specific ones. Prioritize based on operational needs and verify that instrumentation automation is integrated into CI/CD pipelines.
