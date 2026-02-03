---
title: Ingress Returning 502 Bad Gateway - Ingress
weight: 245
categories:
  - kubernetes
  - ingress
---

# IngressReturning502BadGateway-ingress

## Meaning

Ingress resources are returning 502 Bad Gateway errors (triggering KubeIngressNotReady or KubeServiceNotReady alerts) because the backend service referenced in ingress rules has no endpoints, pods matching the service selector are not ready, the service port configuration does not match pod container ports, or the backend service is unreachable due to network policies or pod failures. Ingress endpoints return 502 Bad Gateway errors, backend services show no endpoints in kubectl, and ingress controller logs show backend connection failures or upstream errors. This affects the network plane and prevents external traffic from reaching applications, typically caused by backend service unavailability or pod readiness failures; applications become unavailable to users and may show errors.

## Impact

Ingress endpoints return 502 Bad Gateway errors; external traffic cannot reach applications; users see Bad Gateway errors; services appear unavailable; ingress controller logs show backend connection failures and upstream errors; KubeIngressNotReady alerts fire when ingress cannot route to backend services; KubeServiceNotReady alerts fire when backend services have no ready endpoints; backend service has no ready endpoints; application traffic is blocked; ingress status shows backend service errors. Ingress endpoints return 502 Bad Gateway errors indefinitely; backend services show no endpoints; applications become unavailable to users and may experience errors or performance degradation; user-facing services are blocked.

## Playbook

1. Describe the Ingress `<ingress-name>` in namespace `<namespace>` using `kubectl describe ingress <ingress-name> -n <namespace>` and inspect its configuration, backend service references, and annotations to verify routing rules.

2. List events in namespace `<namespace>` using `kubectl get events -n <namespace> --field-selector involvedObject.name=<ingress-name> --sort-by='.lastTimestamp'` and filter for ingress-related events, focusing on events with reasons such as `Failed`, `Sync`, or messages indicating backend connection or routing errors.

3. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for 502 errors, backend connection failures, or service unreachable messages related to the ingress.

4. Retrieve the Service `<service-name>` referenced as a backend in the ingress and verify it exists, has endpoints, and check its port configuration.

5. List Endpoints for the Service `<service-name>` in namespace `<namespace>` and verify that pods are registered as endpoints and are ready.

6. From a test pod, execute `curl` or `wget` to the backend service endpoint directly using Pod Exec tool to test connectivity and verify if the service is accessible internally.

## Diagnosis

Begin by analyzing the Ingress describe output and backend service status collected in the Playbook section. The service endpoints, backend pod readiness, and controller error logs provide the primary diagnostic signals.

**If the backend service shows no endpoints:**
- No healthy pods are available. Check if pods matching the service selector exist. If pods exist, verify they pass readiness probes. Fix pod health issues before the ingress can route traffic.

**If endpoints exist but pods are in NotReady state:**
- Pods are running but failing readiness probes. Check pod logs for application startup errors. Verify readiness probe configuration matches the application's actual health endpoint.

**If the service port does not match the container port:**
- Port mismatch prevents traffic from reaching the application. Verify the service `targetPort` matches the container port where the application listens. Check Ingress `backend.service.port` matches the service port.

**If curl directly to the backend service ClusterIP fails:**
- The backend service itself is unreachable. Check if NetworkPolicies block traffic to the service. Verify the application is listening on the expected port.

**If curl to backend succeeds but ingress returns 502:**
- The ingress controller cannot reach the backend. Check if NetworkPolicies block traffic from the ingress controller namespace to the backend namespace. Verify the controller can resolve the service DNS name.

**If controller logs show upstream connection timeout:**
- The backend is too slow to respond. Check backend pod resource usage for CPU or memory pressure. Increase ingress proxy timeout annotations if the backend legitimately needs more time.

**If events are inconclusive, correlate timestamps:**
1. Check if 502 errors began after a Deployment rollout by comparing error onset with pod creation timestamps.
2. Check if errors align with pod restarts or OOM kills in the backend.
3. Check if service or endpoint resources were modified.

**If no clear cause is identified:** Exec into a debug pod in the ingress controller namespace and curl the backend service directly to test network connectivity from the controller's perspective.

