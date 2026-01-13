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

1. Retrieve the Ingress `<ingress-name>` in namespace `<namespace>` and inspect its configuration and backend service references to verify routing rules.

2. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for 502 errors, backend connection failures, or service unreachable messages related to the ingress.

3. Retrieve the Service `<service-name>` referenced as a backend in the ingress and verify it exists, has endpoints, and check its port configuration.

4. List Endpoints for the Service `<service-name>` in namespace `<namespace>` and verify that pods are registered as endpoints and are ready.

5. Retrieve pods associated with the backend service and check their Ready condition and status to verify if pods are running and ready to receive traffic.

6. From a test pod, execute `curl` or `wget` to the backend service endpoint directly using Pod Exec tool to test connectivity and verify if the service is accessible internally.

## Diagnosis

1. Compare the ingress 502 error timestamps with backend service endpoint change timestamps, and check whether endpoints became unavailable within 5 minutes before 502 errors began.

2. Compare the ingress 502 error timestamps with pod Ready condition transition times for backend pods, and check whether pods became NotReady within 5 minutes before 502 errors.

3. Compare the ingress 502 error timestamps with service port configuration modification timestamps, and check whether port changes occurred within 30 minutes before 502 errors.

4. Compare the ingress 502 error timestamps with backend pod restart or crash timestamps, and check whether pod failures occurred within 5 minutes before 502 errors.

5. Compare the ingress 502 error timestamps with NetworkPolicy modification timestamps that may affect backend service traffic, and check whether policy changes occurred within 10 minutes before 502 errors.

6. Compare the ingress 502 error timestamps with deployment rollout or image update timestamps for backend pods, and check whether application changes occurred within 1 hour before 502 errors, indicating the new version may have different port or health check behavior.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review backend service logs for gradual performance degradation, check for intermittent pod readiness issues, examine if service port configurations drifted over time, verify if network path issues developed gradually, and check for DNS or service discovery issues affecting backend connectivity. 502 errors may result from gradual backend service degradation rather than immediate configuration changes.

