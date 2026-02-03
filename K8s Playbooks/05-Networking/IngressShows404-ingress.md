---
title: Ingress Shows 404 - Ingress
weight: 230
categories:
  - kubernetes
  - ingress
---

# IngressShows404-ingress

## Meaning

Ingress resources are returning 404 Not Found errors (triggering KubeIngressNotReady alerts) because the ingress routing rules do not match the request path or hostname, the backend service path configuration is incorrect, the ingress controller cannot find matching rules for the requested URL, or the backend service referenced in ingress rules is not configured correctly. Ingress endpoints return 404 Not Found errors, ingress controller logs show no matching rules for requested paths or hostnames, and ingress rules may show path or hostname mismatches. This affects the network plane and prevents external traffic from reaching applications, typically caused by misconfigured ingress rules or path mismatches; applications become unavailable to users and may show errors.

## Impact

Ingress endpoints return 404 Not Found errors; users see Not Found errors; traffic cannot reach applications; ingress routing fails; ingress controller logs show no matching rules for requested paths or hostnames; KubeIngressNotReady alerts fire when ingress cannot route requests successfully; application endpoints are unreachable; URL paths do not match ingress rules; ingress status shows routing configuration errors; external access to specific application paths fails. Ingress endpoints return 404 Not Found errors indefinitely; ingress controller logs show no matching rules; applications become unavailable to users and may experience errors or performance degradation; external access to specific application paths fails.

## Playbook

1. Describe the Ingress `<ingress-name>` in namespace `<namespace>` using `kubectl describe ingress <ingress-name> -n <namespace>` and inspect its rules, paths, annotations, and backend service references to verify routing configuration.

2. List events in namespace `<namespace>` using `kubectl get events -n <namespace> --field-selector involvedObject.name=<ingress-name> --sort-by='.lastTimestamp'` and filter for ingress-related events, focusing on events with reasons such as `Sync`, `Failed`, or messages indicating routing or path matching errors.

3. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for 404 errors, no matching rules, or routing failure messages related to the ingress.

4. Verify that the request path matches the ingress rule paths and that path matching rules (exact, prefix) are correctly configured.

5. Retrieve the Service `<service-name>` referenced as a backend in the ingress and verify it exists and is accessible.

6. From a test pod, execute `curl` or `wget` to the ingress hostname and path using Pod Exec tool to test routing behavior and verify which paths are accessible.

## Diagnosis

Begin by analyzing the Ingress describe output and controller logs collected in the Playbook section. The Ingress rules, path matching configuration, and request path comparison provide the primary diagnostic signals.

**If no Ingress rule matches the requested hostname:**
- The hostname in the request does not match any Ingress `host` field. Check the exact hostname used in the request. Verify the Ingress has a rule for this hostname or uses a wildcard host.

**If the Ingress has rules but none match the requested path:**
- The path in the request does not match any Ingress path rule. Compare the exact request path with Ingress path rules. Check if the Ingress uses `Exact` pathType but the request has trailing slashes or vice versa.

**If the Ingress uses `Prefix` pathType and returns 404 for subpaths:**
- The backend application may not handle the full path. Check if the ingress needs `nginx.ingress.kubernetes.io/rewrite-target` annotation to strip the path prefix before forwarding to the backend.

**If the Ingress was recently created but returns 404:**
- The ingress controller may not have processed the Ingress yet. Check Ingress status for an assigned address. Check controller logs for sync errors related to this Ingress.

**If the Ingress has an IngressClass that does not match the controller:**
- The controller is ignoring this Ingress. Verify `spec.ingressClassName` matches the IngressClass watched by the running controller. Check controller startup arguments for class filtering.

**If the backend service exists but the application returns 404:**
- Traffic reaches the application but the application has no handler for the path. This is an application issue, not an ingress issue. Verify the application routes match what the ingress is forwarding.

**If events are inconclusive, correlate timestamps:**
1. Check if 404 errors began after Ingress path changes by examining the Ingress resource version.
2. Check if the backend Deployment changed its routing configuration.
3. Check if the ingress controller was restarted and lost configuration.

**If no clear cause is identified:** Use `kubectl get ingress -A -o wide` to list all Ingress resources and their addresses. Verify the ingress controller's default backend configuration handles unmatched requests.

