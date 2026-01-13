---
title: Secrets Not Accessible - Secret
weight: 210
categories:
  - kubernetes
  - secret
---

# SecretsNotAccessible-secret

## Meaning

Secrets are not accessible to pods (triggering pod-related alerts) because Secrets are not mounted correctly, RBAC permissions prevent access, the Secret reference is incorrect, or the pod's service account lacks permissions. Pods show CrashLoopBackOff or Pending state, pod events show FailedMount errors, and container waiting state reason may indicate Secret access failures. This affects the workload plane and prevents pods from reading Secret data, typically caused by RBAC permission issues or incorrect mount configurations; missing Secret dependencies may block container initialization.

## Impact

Pods cannot access secrets; applications fail to read sensitive data; Secret mount failures occur; environment variables are not populated; pods enter CrashLoopBackOff or Pending state; KubePodPending alerts may fire; authentication credentials are missing; services cannot start without required secrets; image pull secrets fail. Pods show CrashLoopBackOff or Pending state indefinitely; pod events show FailedMount errors; missing Secret dependencies may block container initialization; applications cannot start and may show errors.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod volume configuration, container volume mounts, environment variable sources, or image pull secrets to identify which Secret is referenced and how it should be accessed.

2. Retrieve the Secret `<secret-name>` in namespace `<namespace>` and verify it exists and contains the expected data.

3. Check the pod `<pod-name>` status and inspect container waiting state reason and message fields to identify Secret access errors.

4. Verify RBAC permissions by checking if the pod's service account has permissions to access Secrets in the namespace.

5. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review Secret references and mount configurations in the pod template.

6. List events in namespace `<namespace>` and filter for Secret-related events, focusing on events with reasons such as `FailedMount` or messages indicating Secret access or permission failures.

## Diagnosis

1. Compare the pod Secret access failure timestamps with Secret mount configuration modification timestamps in the deployment, and check whether mount changes occurred within 30 minutes before access failures.

2. Compare the pod Secret access failure timestamps with RBAC Role or RoleBinding modification timestamps, and check whether permission changes occurred within 30 minutes before access failures.

3. Compare the pod Secret access failure timestamps with service account modification timestamps, and check whether service account changes occurred within 30 minutes before access failures.

4. Compare the pod Secret access failure timestamps with deployment rollout or pod template update timestamps, and check whether Secret reference or mount changes occurred within 1 hour before access failures.

5. Compare the pod Secret access failure timestamps with Secret deletion or modification timestamps, and check whether Secrets were removed or changed within 30 minutes before access failures.

6. Compare the pod Secret access failure timestamps with namespace creation or pod namespace change timestamps, and check whether namespace mismatches occurred within 30 minutes before access failures.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review pod logs for gradual Secret access issues, check for intermittent RBAC permission problems, examine if Secret mount configurations drifted over time, verify if service account permissions were gradually restricted, and check for API server or etcd issues affecting Secret retrieval. Secret accessibility issues may result from gradual permission or configuration drift rather than immediate changes.

