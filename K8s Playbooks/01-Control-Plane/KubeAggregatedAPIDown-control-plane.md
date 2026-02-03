---
title: Kube Aggregated API Down
weight: 20
---

# KubeAggregatedAPIDown

## Meaning

Kubernetes aggregated API server is unavailable (triggering KubeAggregatedAPIDown alerts) because the aggregated API server has failed, lost network connectivity, or cannot be reached by the API server aggregation layer. Aggregated API server pods show CrashLoopBackOff or Failed state in kubectl, aggregated API server logs show fatal errors, panic messages, or connection timeout errors, and aggregated API endpoints return connection refused or timeout errors. This affects the control plane and prevents custom resources, metrics APIs, or other aggregated API functionality from working, typically caused by pod failures, network issues, configuration problems, or resource constraints; applications using custom resources may show errors.

## Impact

KubeAggregatedAPIDown alerts fire; aggregated API endpoints return errors; custom resources may be unavailable; HPA may fail if using custom metrics; cluster functionality dependent on aggregated APIs is degraded; inability to see cluster metrics; unable to use custom metrics to scale; cluster operations may be severely limited; custom resource definitions cannot be accessed; metrics-based autoscaling fails. Aggregated API server pods remain in CrashLoopBackOff or Failed state; aggregated API endpoints return connection refused or timeout errors; applications using custom resources may experience errors or performance degradation; APIService registration issues may prevent aggregated API connectivity.

## Playbook

1. Describe all apiservice resources to retrieve detailed information about all aggregated API services and identify any services in unavailable or degraded states.

2. List events in namespace kube-system sorted by last timestamp to retrieve recent control plane events, filtering for aggregated API server errors or connectivity failures.

3. Retrieve the Pod `<pod-name>` in namespace `<namespace>` for aggregated API server deployments and inspect its status, restart count, and container states to verify if the aggregated API server is running.

4. Retrieve logs from the Pod `<pod-name>` in namespace `<namespace>` and filter for error patterns including 'panic', 'fatal', 'connection refused', 'timeout', 'certificate' to identify startup or runtime failures.

5. Retrieve the Service `<service-name>` for aggregated API server endpoints in namespace `<namespace>` and verify network connectivity between API server and aggregated API server endpoints.

6. Retrieve NetworkPolicy resources in namespace `<namespace>` and check if network policies block communication between API server and aggregated API servers.

7. Retrieve the Service `<service-name>` and Endpoints for aggregated API server in namespace `<namespace>` and verify aggregated API server configuration and service endpoints.

8. Retrieve APIService resources and check API server aggregation layer configuration and aggregated API server registrations.

## Diagnosis

1. Analyze aggregated API server pod events from Playbook to identify failure mode and timing. If events show CrashLoopBackOff, Failed, or pod termination, use event timestamps and error messages to determine the root cause.

2. If events indicate aggregated API server crashes or failures, examine pod logs from Playbook step 4. If logs show panic messages, fatal errors, or startup failures at event timestamps, application-level issues caused the unavailability.

3. If events indicate network connectivity issues, verify service endpoints from Playbook step 5. If service or endpoint events show unavailability at timestamps when aggregated API failed, network connectivity is the root cause.

4. If events indicate network policy changes, examine NetworkPolicy modifications from Playbook step 6. If network policy events occurred before aggregated API became unavailable, policy changes may have blocked communication between API server and aggregated API.

5. If events indicate APIService registration issues, verify APIService status from Playbook step 8. If APIService events show registration failures or condition changes at unavailability timestamps, aggregation layer configuration is the problem.

6. If events indicate resource pressure (OOMKilled, CPU throttling), verify pod resource usage at event timestamps. If resource usage exceeded limits when failures began, resource constraints caused the unavailability.

7. If events indicate configuration changes, correlate change timestamps with failure onset. If configuration modifications occurred before aggregated API became unavailable, recent changes may have introduced invalid settings.

**If no correlation is found**: Extend timeframes to 1 hour for infrastructure changes, review aggregated API server configuration, check for API server aggregation layer issues, verify network connectivity, examine historical aggregated API stability patterns. Aggregated API failures may result from network issues, configuration problems, or resource constraints rather than immediate changes.
