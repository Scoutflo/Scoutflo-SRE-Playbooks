# Trace Coverage Issues

## Meaning

Trace coverage issues indicate that distributed tracing coverage is incomplete or trace coverage gaps are detected (triggering alerts like TraceCoverageIncomplete or TraceCollectionGapDetected) because distributed tracing is not enabled for pods, trace sampling rates are too low, trace collection agents are not installed, trace coverage analysis tools fail, or trace coverage monitoring indicates gaps. Trace coverage gaps are detected, distributed tracing is not enabled, trace sampling rates are low, and trace coverage analysis fails. This affects the observability layer and distributed tracing coverage, typically caused by trace configuration failures, trace collection agent installation issues, trace coverage analysis tool failures, or trace coverage monitoring gaps; if trace coverage affects container workloads, container traces may not be collected and applications may experience trace monitoring blind spots.

## Impact

TraceCoverageIncomplete alerts fire; TraceCollectionGapDetected alerts fire; distributed tracing coverage is incomplete; trace coverage gaps are detected; trace monitoring may be insufficient; distributed system analysis may be difficult. Trace coverage gaps are detected; if trace coverage affects container workloads, container traces may not be collected, pod traces may be missing, and container applications may experience trace monitoring blind spots; applications may experience trace coverage gaps or trace collection failures.

## Playbook

1. List all pods in namespace <namespace> with wide output to retrieve their status, including sidecar containers for tracing agents.
2. List recent events in namespace <namespace> sorted by timestamp to identify tracing agent failures, sidecar injection issues, or trace collection errors.
3. Describe pod <pod-name> in namespace <namespace> to inspect the pod configuration and verify distributed tracing sidecar injection and trace sampling configuration.
4. List deployments in namespace `<namespace>` and verify deployment tracing configuration and trace collection settings, checking deployment trace coverage.
5. Retrieve distributed tracing sampling configuration for services in namespace `<namespace>` and verify sampling rates are appropriate for trace coverage, checking trace sampling coverage.
6. Retrieve distributed tracing trace data for service `<service-name>` and verify trace availability over the last 7 days to identify missing traces or trace collection failures, checking trace collection health.
7. Compare trace coverage analysis results with pod deployment timestamps and verify whether new pods have distributed tracing enabled upon deployment, using pod configuration data as supporting evidence.
8. Retrieve distributed tracing agent status for pods in namespace `<namespace>` and verify agent health and trace collection status, checking trace agent coverage.
9. List distributed tracing trace groups and verify trace group coverage for services to identify services without trace groups, checking trace group coverage gaps.

## Diagnosis

1. Review the pod sidecar configurations from Steps 1 and 3. If pods lack tracing agent sidecars, this is the primary coverage gap. Determine whether sidecar injection is disabled or misconfigured.

2. Analyze the trace sampling configuration from Step 5. If sampling rates are too low (e.g., below 1%), then traces may be collected but rarely captured. If sampling is appropriate but traces are missing, then collection issues exist.

3. If Step 6 trace data shows gaps in trace availability, identify whether gaps are time-based (suggesting collection downtime) or service-based (suggesting service-specific configuration issues).

4. Review the trace agent status from Step 8. If agents show unhealthy status, then existing tracing infrastructure is failing. If agents are healthy, then trace propagation or collection configuration is the issue.

5. If Step 7 shows new pods without tracing enabled upon deployment, then deployment templates and admission webhooks need updating to automatically inject tracing configuration.

If analysis is inconclusive: Examine events from Step 2 for tracing agent failures or sidecar injection issues. Review trace group coverage from Step 9 to identify services without trace groups. Determine whether coverage gaps are concentrated in specific namespaces or service types (suggesting deployment pipeline issues) or distributed randomly (suggesting ad-hoc deployment practices).
