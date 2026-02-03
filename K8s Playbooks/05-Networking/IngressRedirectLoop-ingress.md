---
title: Ingress Redirect Loop - Ingress
weight: 298
categories:
  - kubernetes
  - ingress
---

# IngressRedirectLoop-ingress

## Meaning

Ingress resources are causing redirect loops (triggering KubeIngressNotReady alerts) because misconfigured ingress rules redirect traffic back to the same path, backend services redirect to paths that match other ingress rules, or SSL/TLS redirect annotations (nginx.ingress.kubernetes.io/ssl-redirect) create circular redirects. Ingress endpoints cause infinite redirects, ingress controller logs show redirect loops and circular redirect patterns, and browsers show redirect loop errors. This affects the network plane and prevents external traffic from reaching applications, typically caused by misconfigured ingress redirect rules or SSL/TLS redirect conflicts; applications become unavailable to users and may show errors.

## Impact

Ingress endpoints cause infinite redirects; browsers show redirect loop errors; requests never complete; applications are unreachable; ingress controller logs show redirect loops and circular redirect patterns; KubeIngressNotReady alerts fire when ingress cannot route traffic successfully; user traffic is blocked; SSL/TLS redirects create loops; ingress status shows routing failures; external access to applications fails completely. Ingress endpoints cause infinite redirects indefinitely; ingress controller logs show redirect loops; applications become unavailable to users and may experience errors or performance degradation; external access to applications fails completely.

## Playbook

1. Describe the Ingress `<ingress-name>` in namespace `<namespace>` using `kubectl describe ingress <ingress-name> -n <namespace>` and inspect its rules, annotations, and redirect configurations to identify potential loop sources.

2. List events in namespace `<namespace>` using `kubectl get events -n <namespace> --field-selector involvedObject.name=<ingress-name> --sort-by='.lastTimestamp'` and filter for ingress-related events, focusing on events with reasons such as `Sync`, `Failed`, or messages indicating redirect or routing issues.

3. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for redirect loop errors, circular redirect messages, or routing conflicts.

4. Check ingress annotations for SSL/TLS redirect configurations (e.g., `nginx.ingress.kubernetes.io/ssl-redirect`, `cert-manager.io/issuer`) and verify if redirects are creating loops.

5. Retrieve all Ingress resources in namespace `<namespace>` and check for conflicting rules or overlapping paths that may cause redirect loops.

6. From a test pod, execute `curl` with redirect following disabled using Pod Exec tool to trace redirect paths and identify where loops occur.

## Diagnosis

Begin by analyzing the Ingress describe output and curl trace results collected in the Playbook section. The Ingress annotations, TLS configuration, and redirect path trace provide the primary diagnostic signals.

**If Ingress has `nginx.ingress.kubernetes.io/ssl-redirect: "true"` and backend also redirects to HTTPS:**
- Both ingress and application are forcing HTTPS, creating a loop. Set `nginx.ingress.kubernetes.io/ssl-redirect: "false"` on the Ingress since TLS termination happens at the ingress controller.

**If curl trace shows HTTP to HTTPS redirect followed by HTTPS to HTTP redirect:**
- The backend application is redirecting to HTTP while the ingress forces HTTPS. Configure the backend to use HTTPS URLs in its redirects, or set appropriate headers like `X-Forwarded-Proto` to inform the backend it's behind TLS termination.

**If multiple Ingress resources match the same hostname with different redirect rules:**
- Conflicting Ingress resources are causing the loop. List all Ingress resources matching the hostname and consolidate redirect rules into a single Ingress or ensure paths do not overlap.

**If curl trace shows redirects between paths that match different Ingress rules:**
- Path-based routing is creating a redirect cycle. Review all Ingress path rules for the hostname. Ensure application redirects target paths handled by the same backend or adjust Ingress path matching.

**If the backend application implements its own redirect logic:**
- The application's redirect URL conflicts with ingress routing. Check application configuration for redirect URLs. Ensure redirects use the correct protocol and hostname that the ingress expects.

**If events are inconclusive, correlate timestamps:**
1. Check if the loop started after adding TLS configuration or ssl-redirect annotation by examining Ingress modification history.
2. Check if the loop began after creating a new Ingress for the same hostname.
3. Check if backend Deployment changes introduced application-level redirects.

**If no clear cause is identified:** Temporarily disable ssl-redirect and test with HTTP only to isolate whether the issue is TLS-related. Capture the full redirect chain using `curl -L -v --max-redirs 10` to trace the exact loop pattern.

