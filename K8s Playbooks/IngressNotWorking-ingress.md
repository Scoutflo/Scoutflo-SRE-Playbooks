---
title: Ingress Not Working - Ingress
weight: 208
categories:
  - kubernetes
  - ingress
---

# IngressNotWorking-ingress

## Meaning

Ingress resources are not routing traffic to backend services (triggering alerts like KubeIngressNotReady or KubeIngressDown) because the ingress controller pods are not running in the ingress controller namespace (typically ingress-nginx or kube-system), ingress rules are misconfigured with invalid paths or hostnames, backend services referenced in ingress rules are unavailable or have no endpoints, DNS is not configured correctly for ingress hostnames, or network policies are blocking traffic between ingress controller and backend services. Ingress controller pods show CrashLoopBackOff or Failed state in kubectl, ingress endpoints return 502 Bad Gateway or 503 Service Unavailable errors, and ingress controller logs show routing failures or backend connection errors. This affects the network plane and prevents external traffic from reaching applications, typically caused by ingress controller failures, misconfigured ingress rules, or backend service unavailability; applications become unavailable to users and may show errors.

## Impact

KubeIngressNotReady or KubeIngressDown alerts fire; external traffic cannot reach applications through ingress endpoints; ingress endpoints return 502 Bad Gateway or 503 Service Unavailable errors; services are unreachable from outside the cluster; applications become unavailable to users; ingress controller logs show routing failures and backend connection errors; backend services receive no traffic; DNS resolution fails for ingress hosts; ingress status shows no address or backend service errors; user-facing services are completely unavailable. Ingress controller pods remain in CrashLoopBackOff or Failed state; ingress endpoints return errors indefinitely; applications become unavailable to users and may experience errors or performance degradation.

## Playbook

1. Retrieve the Ingress `<ingress-name>` in namespace `<namespace>` and inspect its status, rules, and backend service references to verify configuration.

2. List IngressController pods in the ingress controller namespace (typically `ingress-nginx` or `kube-system`) and check their status and readiness to confirm the controller is running.

3. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for errors related to the ingress resource, backend services, or routing failures.

4. Retrieve the Service `<service-name>` referenced as a backend in the ingress and verify it exists, has endpoints, and is accessible.

5. List Endpoints for the Service `<service-name>` in namespace `<namespace>` and verify that pods are registered as endpoints and are ready.

6. From a test pod, execute `curl` or `wget` to the ingress hostname or IP address using Pod Exec tool to test connectivity and verify routing behavior.

## Diagnosis

1. Compare the ingress routing failure timestamps with ingress controller pod restart or crash timestamps, and check whether controller failures occurred within 5 minutes before routing issues began.

2. Compare the ingress routing failure timestamps with ingress resource modification timestamps, and check whether configuration changes were made within 30 minutes before routing failures.

3. Compare the ingress routing failure timestamps with backend service endpoint change timestamps, and check whether endpoints became unavailable within 5 minutes before routing issues.

4. Compare the ingress routing failure timestamps with NetworkPolicy modification timestamps that may affect ingress controller or backend service traffic, and check whether policy changes occurred within 10 minutes before routing failures.

5. Compare the ingress routing failure timestamps with DNS configuration change timestamps or ingress hostname updates, and check whether DNS changes occurred within 30 minutes before routing issues.

6. Compare the ingress routing failure timestamps with cluster network changes, node maintenance, or ingress controller deployment updates, and check whether infrastructure changes occurred within 1 hour before routing failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review ingress controller logs for gradual performance degradation, check for DNS propagation delays, examine backend service health trends, verify if ingress controller resource constraints developed over time, and check for network path issues that may have accumulated. Ingress routing issues may result from gradual system degradation rather than immediate configuration changes.

