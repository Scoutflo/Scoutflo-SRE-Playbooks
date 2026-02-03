---
title: Error Forbidden when Running kubectl Commands - RBAC
weight: 261
categories:
  - kubernetes
  - rbac
---

# ErrorForbiddenwhenRunningkubectlCommands-rbac

## Meaning

kubectl commands return Forbidden (403) errors (triggering KubeAPIErrorsHigh alerts) because the user or service account lacks required RBAC permissions, Role or RoleBinding resources are missing or incorrect, or permissions were revoked. API requests return 403 status codes, Role or RoleBinding resources may show missing permissions, and authorization failures prevent resource management. This affects the authentication and authorization plane and prevents cluster operations, typically caused by missing RBAC permissions or incorrect Role/RoleBinding configurations; applications using Kubernetes API may show errors.

## Impact

kubectl commands fail with Forbidden errors; cluster operations are blocked; users cannot perform required actions; KubeAPIErrorsHigh alerts fire; API server returns 403 status codes; authorization failures prevent resource management; service accounts cannot access required resources; applications fail due to permission denials. API requests return 403 status codes indefinitely; Role or RoleBinding resources may show missing permissions; applications using Kubernetes API may experience errors or performance degradation; cluster operations are blocked.

## Playbook

1. Test the exact command that failed using `kubectl auth can-i <verb> <resource> -n <namespace>` to confirm which specific permission is denied - this immediately identifies the permission gap.

2. Check your current identity using `kubectl auth whoami` (K8s 1.27+) or `kubectl config current-context` and `kubectl config view --minify -o jsonpath='{.contexts[0].context.user}'` to verify which user or service account is being used.

3. List all your current permissions using `kubectl auth can-i --list -n <namespace>` to see what you CAN do, helping identify what's missing.

4. Check if a RoleBinding exists for your user using `kubectl get rolebindings -n <namespace> -o yaml | grep -A5 "<your-username-or-sa>"` or `kubectl get clusterrolebindings -o yaml | grep -A5 "<your-username-or-sa>"`.

5. If a binding exists, run `kubectl describe role <role-name> -n <namespace>` or `kubectl describe clusterrole <role-name>` to see what permissions the role grants.

6. List events related to authorization failures using `kubectl get events --all-namespaces --field-selector=reason=Forbidden` to see recent permission denials with timestamps.

7. Check API server audit logs if available using `kubectl logs -n kube-system -l component=kube-apiserver --tail=100 | grep -i "403\|forbidden"` to review authorization decisions.

## Diagnosis

1. Compare the Forbidden error timestamps with Role or ClusterRole modification timestamps, and check whether permissions were removed within 30 minutes before Forbidden errors.

2. Compare the Forbidden error timestamps with RoleBinding or ClusterRoleBinding deletion timestamps, and check whether bindings were removed within 30 minutes before Forbidden errors.

3. Compare the Forbidden error timestamps with user or service account modification timestamps, and check whether account changes occurred within 30 minutes before Forbidden errors.

4. Compare the Forbidden error timestamps with cluster upgrade or RBAC policy update timestamps, and check whether infrastructure changes occurred within 1 hour before Forbidden errors, affecting permission enforcement.

5. Compare the Forbidden error timestamps with API server configuration modification timestamps, and check whether authorization settings were changed within 30 minutes before Forbidden errors.

6. Compare the Forbidden error timestamps with resource creation or namespace creation timestamps, and check whether new resources or namespaces were created within 30 minutes before Forbidden errors, requiring new permissions.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review API server audit logs for gradual permission changes, check for intermittent RBAC policy enforcement issues, examine if Role or RoleBinding configurations drifted over time, verify if permissions were gradually restricted, and check for API server or etcd issues affecting RBAC retrieval. Forbidden errors may result from gradual permission policy changes rather than immediate revocations.

