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

1. Retrieve the Ingress `<ingress-name>` in namespace `<namespace>` and inspect its rules, annotations, and redirect configurations to identify potential loop sources.

2. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for redirect loop errors, circular redirect messages, or routing conflicts.

3. Check ingress annotations for SSL/TLS redirect configurations (e.g., `nginx.ingress.kubernetes.io/ssl-redirect`, `cert-manager.io/issuer`) and verify if redirects are creating loops.

4. Retrieve all Ingress resources in namespace `<namespace>` and check for conflicting rules or overlapping paths that may cause redirect loops.

5. Retrieve the backend Service `<service-name>` and check if the application itself is redirecting traffic, which may combine with ingress redirects to create loops.

6. From a test pod, execute `curl` with redirect following disabled using Pod Exec tool to trace redirect paths and identify where loops occur.

## Diagnosis

1. Compare the ingress redirect loop timestamps with ingress rule modification timestamps, and check whether routing rules were changed within 30 minutes before redirect loops began.

2. Compare the ingress redirect loop timestamps with ingress SSL/TLS redirect annotation modification timestamps, and check whether redirect configurations were added or modified within 30 minutes before loops.

3. Compare the ingress redirect loop timestamps with conflicting ingress resource creation timestamps, and check whether overlapping ingress rules were added within 30 minutes before redirect loops.

4. Compare the ingress redirect loop timestamps with backend service redirect configuration modification timestamps, and check whether application redirects were introduced within 30 minutes before loops.

5. Compare the ingress redirect loop timestamps with ingress controller configuration or annotation modification timestamps, and check whether controller redirect settings were changed within 30 minutes before loops.

6. Compare the ingress redirect loop timestamps with certificate or TLS configuration change timestamps, and check whether SSL/TLS changes occurred within 1 hour before redirect loops, indicating certificate redirects may be causing issues.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review ingress controller logs for gradual redirect rule processing issues, check for intermittent redirect conflicts, examine if ingress rules accumulated redirect configurations over time, verify if backend service redirect behavior changed gradually, and check for certificate renewal or TLS configuration drift that may have introduced redirect loops. Redirect loops may result from cumulative configuration changes rather than immediate modifications.

