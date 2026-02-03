---
title: Pod Fails Readiness Probe - Pod
weight: 212
categories:
  - kubernetes
  - pod
---

# PodFailsReadinessProbe-pod

## Meaning

Pods are failing readiness probe checks (triggering KubePodNotReady alerts) because the application is not responding on the probe endpoint, the probe configuration is incorrect, the application startup time exceeds probe delays, or network issues prevent probe execution. Pods show NotReady state in kubectl, pod events show Unhealthy events with "readiness probe failed" messages, and readiness probe checks fail repeatedly. This affects the workload plane and prevents pods from transitioning to Ready state, typically caused by application startup delays, probe configuration issues, or application errors; applications may show errors in application monitoring.

## Impact

Pods remain in NotReady state; services have no endpoints; traffic cannot reach application pods; load balancers exclude pods from rotation; applications appear unavailable even if running; rolling updates fail; deployments cannot achieve desired replica count; KubePodNotReady alerts fire; pod status shows readiness probe failures. Pods show NotReady state indefinitely; pod events show Unhealthy events with "readiness probe failed" messages; applications may show errors in application monitoring; services have no endpoints and applications appear unavailable.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to see Ready condition status and Events showing "Readiness probe failed" with the specific failure (HTTP error, connection refused, timeout).

2. Retrieve events for pod <pod-name> in namespace <namespace> filtered by reason Unhealthy to see probe failure timestamps and messages.

3. Retrieve the readiness probe configuration for pod <pod-name> in namespace <namespace> to see path, port, initialDelaySeconds, periodSeconds, timeoutSeconds.

4. Execute a request to the readiness endpoint from inside pod <pod-name> to verify the endpoint is responding.

5. Retrieve logs from pod <pod-name> in namespace <namespace> to identify errors during initialization or dependency connection failures.

6. List endpoints for service <service-name> in namespace <namespace> to check if pod is registered - if pod is not listed, readiness probe is failing.

7. Describe Deployment <deployment-name> in namespace <namespace> to check if initialDelaySeconds is sufficient for application startup time.

8. Retrieve resource usage metrics for pod <pod-name> in namespace <namespace> to see if resource constraints are causing slow responses.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify readiness probe failures. Events showing "Unhealthy" with "Readiness probe failed" include the specific failure reason (HTTP status code, connection refused, timeout).

2. If events show "connection refused" for HTTP/TCP probes (from Playbook step 2):
   - Application is not listening on the configured port
   - Verify application logs (Playbook step 5) for startup errors
   - Check if application binds to correct interface (0.0.0.0 vs 127.0.0.1)
   - Verify the probe port matches application's listening port

3. If events show HTTP error codes (4xx, 5xx) for HTTP probes:
   - 404: Probe path does not exist - verify httpGet.path is correct
   - 401/403: Authentication required - probe endpoint should not require auth
   - 500/503: Application error - check application logs for errors

4. If events show "timeout" for probes:
   - Application is slow to respond - increase timeoutSeconds
   - Application startup is slow - increase initialDelaySeconds
   - Resource constraints causing slow responses - check CPU/memory usage (Playbook step 8)

5. If endpoint responds when tested manually (from Playbook step 4) but probe still fails:
   - Probe configuration mismatch (wrong port, path, or scheme)
   - Intermittent application issues under load
   - Network policy blocking kubelet probe traffic

6. If pod is not registered in service endpoints (from Playbook step 6), readiness probe is failing. The pod will not receive traffic until it passes readiness checks.

7. If initialDelaySeconds is too short (from Playbook step 7), probes fail before the application is ready. Set initialDelaySeconds to exceed typical application startup time.

**To resolve readiness probe failures**: Fix application startup issues, adjust probe timing (initialDelaySeconds, timeoutSeconds, periodSeconds), verify probe endpoint configuration matches application, and ensure the endpoint returns HTTP 2xx or 3xx for success.

