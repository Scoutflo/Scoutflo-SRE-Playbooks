---
title: Pod Security Context Misconfiguration - Pod
weight: 299
categories:
  - kubernetes
  - pod
---

# PodSecurityContext-pod

## Meaning

Pods fail to start due to security context misconfiguration (triggering KubePodPending or KubePodSecurityPolicyViolation alerts when PodSecurityPolicy is enabled) because security context settings (runAsUser, runAsGroup, fsGroup, capabilities) are invalid, conflict with PodSecurityPolicy (deprecated) or Pod Security Standards (Kubernetes 1.23+), or violate cluster security policies enforced via namespace labels or admission controllers. Pods show Pending state, pod events show FailedCreate errors with security context validation failures, and security context settings may conflict with security policies. This affects the workload plane and prevents pods from starting, typically caused by security context misconfiguration or security policy violations; applications cannot deploy and may show errors.

## Impact

Pods cannot start; deployments fail to create pods; pods remain in Pending state; KubePodPending alerts fire when pods cannot be created; KubePodSecurityPolicyViolation alerts fire when PodSecurityPolicy is enabled and security context violates policy; security context validation fails; pod creation is rejected by admission controllers; applications cannot deploy; security policy violations prevent pod startup; pod events show security context validation errors. Pods show Pending state indefinitely; pod events show FailedCreate errors with security context validation failures; applications cannot deploy and may experience errors or performance degradation; security policy violations prevent pod startup.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod security context and container security context to verify security context configuration.

2. List events in namespace `<namespace>` and filter for pod-related events, focusing on events with reasons such as `FailedCreate` or messages indicating security context validation failures.

3. Check the pod `<pod-name>` status and inspect container waiting state reason and message fields to identify security context errors.

4. Retrieve PodSecurityPolicy or verify PodSecurityStandards enforcement in the cluster to understand security requirements.

5. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review security context configuration in the pod template.

6. Check if security context settings conflict with cluster security policies or if required settings are missing.

## Diagnosis

1. Compare the pod security context failure timestamps with pod security context modification timestamps in the deployment, and check whether security context changes occurred within 30 minutes before pod failures.

2. Compare the pod security context failure timestamps with PodSecurityPolicy creation or modification timestamps, and check whether security policy changes occurred within 30 minutes before pod failures.

3. Compare the pod security context failure timestamps with PodSecurityStandards enforcement modification timestamps, and check whether security standard changes occurred within 30 minutes before pod failures.

4. Compare the pod security context failure timestamps with deployment rollout or pod template update timestamps, and check whether security context changes occurred within 1 hour before pod failures.

5. Compare the pod security context failure timestamps with cluster upgrade or security policy update timestamps, and check whether infrastructure changes occurred within 1 hour before pod failures, affecting security enforcement.

6. Compare the pod security context failure timestamps with namespace security label modification timestamps, and check whether namespace security settings changed within 30 minutes before pod failures.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review pod creation logs for gradual security validation issues, check for intermittent security policy enforcement problems, examine if security context configurations drifted over time, verify if security policies were gradually tightened, and check for cluster security policy updates that may have accumulated. Security context failures may result from gradual security policy changes rather than immediate modifications.

