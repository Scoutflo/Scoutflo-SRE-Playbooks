---
title: Kube Container Waiting
weight: 20
---

# KubeContainerWaiting

## Meaning

Container in pod is in Waiting state for too long (triggering KubeContainerWaiting alerts) because the container cannot start due to missing dependencies, resource constraints, image pull issues, or configuration problems. Containers show Waiting state in kubectl, pod events show ImagePullBackOff, ErrImagePull, CreateContainerConfigError, or CreateContainerError, and container status indicates waiting reasons. This affects the workload plane and indicates that containers are blocked from starting, preventing pods from becoming ready, typically caused by image pull failures, missing ConfigMaps or Secrets, resource unavailability, or node taint/toleration mismatches; missing ConfigMap, Secret, or PersistentVolumeClaim dependencies may block container initialization.

## Impact

KubeContainerWaiting alerts fire; service degradation or unavailability; containers cannot start; pods remain in Waiting state; applications cannot run; container startup is blocked; pod readiness is prevented; workloads cannot achieve desired state. Containers show Waiting state indefinitely; pod events show ImagePullBackOff, ErrImagePull, or CreateContainerConfigError errors; applications cannot start and may show errors; missing ConfigMap, Secret, or PersistentVolumeClaim dependencies may cause initialization failures.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and inspect its container waiting state and reason to identify why containers cannot start.

2. Retrieve events for the Pod `<pod-name>` in namespace `<namespace>` and filter for waiting-related error patterns including 'ImagePullBackOff', 'ErrImagePull', 'CreateContainerConfigError', 'CreateContainerError' to identify startup blockers.

3. Retrieve ConfigMap, Secret, and PersistentVolumeClaim resources referenced by pod `<pod-name>` in namespace `<namespace>` and check for missing dependencies that prevent container initialization.

4. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and verify container image availability and image pull configuration including image pull secrets to identify image pull issues.

5. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and check pod resource requests especially for special resources such as GPU and verify the Node `<node-name>` availability for those resources to identify resource constraints.

6. Retrieve the Node `<node-name>` and check node taints and tolerations to verify compatibility with pod requirements and identify scheduling issues.

## Diagnosis

Compare container waiting detection timestamps with pod creation or update timestamps within 5 minutes and verify whether waiting state began when pod was created or updated, using pod events and container status as supporting evidence.

Correlate container waiting with image pull failure timestamps within 5 minutes and verify whether image pull issues caused containers to wait, using pod events and image pull error logs as supporting evidence.

Compare container waiting with missing ConfigMap or Secret detection timestamps within 5 minutes and verify whether missing dependencies caused containers to wait, using pod events and resource availability as supporting evidence.

Analyze container waiting patterns over the last 15 minutes to determine if waiting is due to image pull issues, missing dependencies, or resource constraints, using pod events and container status as supporting evidence.

Correlate container waiting with node resource pressure or taint change timestamps within 5 minutes and verify whether node conditions prevented container startup, using node conditions and pod scheduling events as supporting evidence.

Compare container waiting with pod resource request and node available resource mismatches to verify whether resource constraints caused waiting, using pod resource specifications and node metrics as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 30 minutes for image pull and dependency resolution, review container image configurations, check for registry connectivity issues, verify ConfigMap and Secret configurations, examine historical container startup patterns. Container waiting may result from image registry issues, missing dependencies, or persistent resource constraints rather than immediate changes.
