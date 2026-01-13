---
title: Pods Stuck in Init State - Pod
weight: 229
categories:
  - kubernetes
  - pod
---

# PodsStuckinInitState-pod

## Meaning

Pods remain stuck in Init state (triggering KubePodPending alerts) because init containers are failing to complete, hanging, or experiencing errors. Pods show Init container status indicating failures or hanging, init container logs show errors or timeout messages, and pod events show init container failure events. This affects the workload plane and prevents pods from transitioning from Init to Running state, typically caused by init container command failures, missing dependencies, or timeout issues; applications cannot start.

## Impact

Pods cannot start; main application containers never begin; deployments remain at 0 ready replicas; services have no endpoints; applications are unavailable; pods remain in Init state indefinitely; KubePodPending alerts fire; pod status shows init container failures; application startup is blocked. Pods show Init container status indicating failures indefinitely; init container logs show errors or timeout messages; applications cannot start and may show errors; deployments remain at 0 ready replicas.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect init container status to identify which init container is failing and check its state, reason, and message.

2. Retrieve logs from the init container in pod `<pod-name>` in namespace `<namespace>` and filter for errors, failures, or hang indicators that explain why the init container cannot complete.

3. List events in namespace `<namespace>` and filter for events related to the pod's init containers, focusing on failure events or error messages.

4. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review the init container configuration including commands, arguments, image, and resource constraints.

5. From a test pod, execute the init container command manually using Pod Exec tool to verify if the command completes successfully and test init container behavior.

6. Check if the init container depends on external resources (databases, services, volumes) and verify those dependencies are available and accessible.

## Diagnosis

1. Compare the init container failure timestamps with init container command or image modification timestamps in the deployment, and check whether init container configuration changes occurred within 30 minutes before failures.

2. Compare the init container failure timestamps with dependency service availability timestamps (databases, APIs, external services), and check whether dependencies became unavailable within 5 minutes before init container failures.

3. Compare the init container failure timestamps with volume mount or PersistentVolumeClaim binding timestamps, and check whether volume issues occurred within 5 minutes before init container failures.

4. Compare the init container failure timestamps with network policy or security policy modification timestamps that may affect init container network access, and check whether policy changes occurred within 10 minutes before failures.

5. Compare the init container failure timestamps with deployment rollout or image update timestamps, and check whether application changes occurred within 1 hour before init container failures, indicating the new version may have different init requirements.

6. Compare the init container failure timestamps with node resource pressure condition timestamps, and check whether node-level resource constraints occurred within 5 minutes before init container failures.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review init container logs for gradual timeout or performance issues, check for intermittent dependency failures, examine network connectivity issues that may have developed over time, verify if init container resource constraints became insufficient, and check for external service degradation that may affect init container execution. Init container failures may result from gradual dependency or infrastructure issues rather than immediate configuration changes.

