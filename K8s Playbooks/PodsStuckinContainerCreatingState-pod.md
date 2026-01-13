---
title: Pods Stuck in ContainerCreating State - Pod
weight: 222
categories:
  - kubernetes
  - pod
---

# PodsStuckinContainerCreatingState-pod

## Meaning

Pods remain stuck in ContainerCreating state (triggering KubePodPending alerts) because container image pull is failing, volumes cannot be mounted, container runtime is experiencing issues, or resource constraints prevent container creation. Pods show ContainerCreating state in kubectl, container waiting state reason shows ImagePullBackOff, ErrImagePull, or CreateContainerConfigError, and pod events show Failed, ErrImagePull, or FailedMount errors. This affects the workload plane and prevents pods from transitioning to Running state, typically caused by image pull failures, PersistentVolumeClaim binding failures, or container runtime issues; missing ConfigMap, Secret, or PersistentVolumeClaim dependencies may block container creation.

## Impact

Pods cannot start; containers never begin running; deployments remain at 0 ready replicas; services have no endpoints; applications are unavailable; pods remain in ContainerCreating state indefinitely; KubePodPending alerts fire; pod status shows container creation failures; application startup is blocked. Pods show ContainerCreating state indefinitely; container waiting state reason shows ImagePullBackOff, ErrImagePull, or CreateContainerConfigError; missing ConfigMap, Secret, or PersistentVolumeClaim dependencies may prevent container creation; applications cannot start and may show errors.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect container waiting state reason and message fields to identify the specific container creation failure reason.

2. List events in namespace `<namespace>` and filter for container creation errors associated with the pod, focusing on events with reasons such as `Failed`, `ErrImagePull`, or volume mount failures.

3. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and verify container image references, volume mounts, and resource requests to ensure they are valid and available.

4. Check the pod `<pod-name>` for volume mount issues by inspecting pod volume configuration and verifying that referenced PersistentVolumeClaims, ConfigMaps, or Secrets exist and are accessible.

5. Verify container image pull status by checking if the image exists in the registry and if image pull secrets are configured correctly.

6. Check the node where the pod is scheduled for container runtime health, disk space availability, and resource availability that may prevent container creation.

## Diagnosis

1. Compare the container creation failure timestamps with image pull failure event timestamps, and check whether image pull errors occurred within 5 minutes before container creation failures.

2. Compare the container creation failure timestamps with volume mount failure event timestamps, and check whether volume mount errors occurred within 5 minutes before container creation failures.

3. Compare the container creation failure timestamps with PersistentVolumeClaim binding or availability timestamps, and check whether PVC issues occurred within 5 minutes before container creation failures.

4. Compare the container creation failure timestamps with node disk space or resource availability timestamps, and check whether node resource constraints occurred within 5 minutes before container creation failures.

5. Compare the container creation failure timestamps with container runtime restart or failure timestamps on the node, and check whether runtime issues occurred within 5 minutes before container creation failures.

6. Compare the container creation failure timestamps with deployment rollout or configuration change timestamps, and check whether changes occurred within 30 minutes before container creation failures, indicating new volume mounts, images, or resource requirements may be causing issues.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review node-level container runtime logs for gradual performance degradation, check for intermittent image registry connectivity issues, examine volume provider problems that may have developed over time, verify if node disk space gradually exhausted, and check for container runtime resource constraints that accumulated over time. Container creation failures may result from gradual infrastructure degradation rather than immediate configuration changes.

