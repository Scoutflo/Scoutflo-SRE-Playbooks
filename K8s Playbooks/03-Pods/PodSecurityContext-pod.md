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

1. Describe pod <pod-name> in namespace <namespace> to inspect pod security context and container security context to verify security context configuration.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify pod-related events, focusing on events with reasons such as FailedCreate or messages indicating security context validation failures.

3. Check the pod <pod-name> status and inspect container waiting state reason and message fields to identify security context errors.

4. Retrieve PodSecurityPolicy or verify PodSecurityStandards enforcement in the cluster to understand security requirements.

5. Retrieve the Deployment <deployment-name> in namespace <namespace> and review security context configuration in the pod template.

6. Check if security context settings conflict with cluster security policies or if required settings are missing.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify the security context violation. Events showing "FailedCreate" with security-related messages indicate which security setting is causing the failure.

2. If events indicate "forbidden: unable to validate against any pod security policy" (legacy PSP), check PodSecurityPolicy configuration (Playbook step 4) and verify the pod's service account has access to a suitable PSP.

3. If events indicate Pod Security Standards violations (Kubernetes 1.23+), check the namespace labels for enforcement level:
   - "pod-security.kubernetes.io/enforce: restricted" requires strict security settings
   - "pod-security.kubernetes.io/enforce: baseline" allows common workloads
   - "pod-security.kubernetes.io/enforce: privileged" allows all pods

4. If container waiting state shows security context errors (from Playbook step 3), common violations include:
   - Running as root when runAsNonRoot is required
   - Requesting privileged containers in restricted namespaces
   - Using hostPath volumes when forbidden
   - Requesting capabilities that are not allowed
   - Using hostNetwork, hostPID, or hostIPC when forbidden

5. If deployment security context (from Playbook step 5) conflicts with namespace security policies, update the pod template to comply:
   - Set runAsNonRoot: true and specify a non-root runAsUser
   - Remove privileged: true from container security context
   - Use allowPrivilegeEscalation: false
   - Drop all capabilities and add only required ones

6. If security context settings appear correct but pod still fails, check if admission controllers or OPA/Gatekeeper policies are blocking pod creation with additional constraints.

**To resolve security context issues**: Align pod security context with the most restrictive policy in the namespace. For legitimate privileged workloads, consider using a dedicated namespace with relaxed security policies or explicit policy exceptions.

