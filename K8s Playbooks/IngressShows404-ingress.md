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

1. Retrieve the Ingress `<ingress-name>` in namespace `<namespace>` and inspect its rules, paths, and backend service references to verify routing configuration.

2. Retrieve logs from the ingress controller pod `<controller-pod-name>` in namespace `<namespace>` and filter for 404 errors, no matching rules, or routing failure messages related to the ingress.

3. Verify that the request path matches the ingress rule paths and that path matching rules (exact, prefix) are correctly configured.

4. Retrieve the Service `<service-name>` referenced as a backend in the ingress and verify it exists and is accessible.

5. From a test pod, execute `curl` or `wget` to the ingress hostname and path using Pod Exec tool to test routing behavior and verify which paths are accessible.

6. Check if multiple ingress resources have conflicting rules or if ingress class annotations are correctly configured.

## Diagnosis

1. Compare the ingress 404 error timestamps with ingress rule modification timestamps, and check whether routing rules were changed within 30 minutes before 404 errors began.

2. Compare the ingress 404 error timestamps with ingress path modification timestamps, and check whether path configurations were modified within 30 minutes before 404 errors.

3. Compare the ingress 404 error timestamps with backend service deletion or modification timestamps, and check whether backend services were removed or changed within 30 minutes before 404 errors.

4. Compare the ingress 404 error timestamps with ingress controller restart or configuration reload timestamps, and check whether controller issues occurred within 5 minutes before 404 errors.

5. Compare the ingress 404 error timestamps with ingress class or annotation modification timestamps, and check whether ingress class changes occurred within 30 minutes before routing failures.

6. Compare the ingress 404 error timestamps with deployment rollout or application path change timestamps, and check whether application changes occurred within 1 hour before 404 errors, indicating the new version may have different path requirements.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review ingress controller logs for gradual routing rule processing issues, check for intermittent path matching problems, examine if ingress rules accumulated conflicts over time, verify if ingress controller configuration drifted gradually, and check for DNS or hostname resolution issues affecting routing. 404 errors may result from gradual ingress configuration drift rather than immediate changes.

