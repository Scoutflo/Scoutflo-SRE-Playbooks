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

1. Describe the Ingress `<ingress-name>` in namespace `<namespace>` using `kubectl describe ingress <ingress-name> -n <namespace>` and inspect its status, rules, annotations, and backend service references to verify configuration.

2. List events in namespace `<namespace>` using `kubectl get events -n <namespace> --field-selector involvedObject.name=<ingress-name> --sort-by='.lastTimestamp'` and filter for ingress-related events, focusing on events with reasons such as `Failed`, `Sync`, or messages indicating routing or backend errors.

3. List IngressController pods in the ingress controller namespace (typically `ingress-nginx` or `kube-system`) and check their status and readiness to confirm the controller is running.

4. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for errors related to the ingress resource, backend services, or routing failures.

5. Retrieve the Service `<service-name>` referenced as a backend in the ingress and verify it exists, has endpoints, and is accessible.

6. From a test pod, execute `curl` or `wget` to the ingress hostname or IP address using Pod Exec tool to test connectivity and verify routing behavior.

## Diagnosis

Begin by analyzing the Ingress describe output and events collected in the Playbook section. The Ingress status, controller pod state, and backend service availability provide the primary diagnostic signals.

**If ingress controller pods are not Running or show CrashLoopBackOff:**
- The ingress controller is down. This is the root cause. Investigate controller pod failures using the IngressControllerPodsCrashLooping playbook before continuing.

**If Ingress status shows no address assigned:**
- The ingress controller has not processed this Ingress resource. Check if the IngressClass matches the controller's class. Verify the controller is watching the correct namespace.

**If backend service has no endpoints (shown in Ingress describe):**
- No pods are available to serve traffic. Verify pods matching the service selector exist and are Ready. Check if the service selector labels match pod labels exactly.

**If curl test returns 502 Bad Gateway:**
- The controller reaches the service but backend pods are not responding. Follow the IngressReturning502BadGateway playbook for detailed diagnosis.

**If curl test returns 404 Not Found:**
- No Ingress rule matches the request. Check that the hostname and path in the request match the Ingress rules. Follow the IngressShows404 playbook if needed.

**If DNS resolution for the ingress hostname fails:**
- DNS is not configured for the Ingress hostname. Verify DNS records point to the ingress controller's external IP or load balancer. This is external to Kubernetes.

**If events are inconclusive, correlate timestamps:**
1. Check if routing failures began after Ingress modifications by examining the Ingress resource version changes.
2. Check if failures align with backend Deployment changes by comparing with Deployment rollout timestamps.
3. Check if NetworkPolicies were added that block controller-to-backend traffic.

**If no clear cause is identified:** Test the backend service directly from within the cluster using a debug pod to bypass the ingress controller and isolate whether the issue is in routing or the backend itself.

