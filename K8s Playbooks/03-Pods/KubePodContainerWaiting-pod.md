---
title: Kube Pod Container Waiting
weight: 29
categories: [kubernetes, pod]
---

# KubePodContainerWaiting

## Meaning

Pod container is stuck in Waiting state (triggering KubePodContainerWaiting alerts) because the container cannot start due to image pull issues, resource provisioning delays, or configuration problems. Container status shows Waiting with a specific reason (ImagePullBackOff, CreateContainerConfigError, PodInitializing), and the container is not running. This affects the workload plane and indicates blocking issues preventing container startup; pod cannot serve traffic; deployment is incomplete; service capacity is reduced.

## Impact

KubePodContainerWaiting alerts fire; container cannot start; pod is not ready; deployment shows incomplete replicas; service endpoints are missing; scaling operations are blocked; HPA effectiveness is reduced; jobs cannot execute; dependent services may fail if waiting for this pod; deployment progress deadline may be exceeded.

## Playbook

1. Retrieve the Pod `<pod-name>` in namespace `<namespace>` and identify which container is in Waiting state and the specific waiting reason.

2. Retrieve events for the Pod and filter for the specific waiting reason to get detailed error information.

3. If reason is ImagePullBackOff or ErrImagePull: verify image name, tag, and registry credentials are correct.

4. If reason is CreateContainerConfigError: check ConfigMap and Secret references in pod spec exist and are correctly formatted.

5. If reason is PodInitializing: check init container status and logs to identify why initialization is not completing.

6. Verify all volume mounts reference existing PersistentVolumeClaims that are bound and available.

7. Check if resource requests can be satisfied by available node capacity.

## Diagnosis

Analyze waiting reason and correlate with specific subsystem: ImagePull* indicates registry issues, CreateContainer* indicates configuration issues, PodInitializing indicates init container issues, using pod status and events as supporting evidence.

Compare container configuration with existing cluster resources and verify all referenced ConfigMaps, Secrets, and PVCs exist in the namespace, using resource inventory and pod spec as supporting evidence.

Check if the container uses a sidecar injection pattern (Istio, Vault) and verify the injection webhook is functioning correctly, using webhook logs and injection status as supporting evidence.

Correlate waiting start time with recent changes and verify whether deployment, ConfigMap, or Secret changes triggered the waiting state, using resource modification timestamps as supporting evidence.

Verify init containers complete successfully if present, as main containers wait for all init containers to finish, using init container logs and status as supporting evidence.

If no correlation is found within the specified time windows: check container runtime logs (containerd/docker), verify node has sufficient disk space for container layers, check for container creation timeout issues, examine security context and capabilities for container start failures.
