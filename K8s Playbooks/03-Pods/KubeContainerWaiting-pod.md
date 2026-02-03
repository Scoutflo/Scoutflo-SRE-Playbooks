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

1. Describe pod <pod-name> in namespace <namespace> to inspect its container waiting state and reason to identify why containers cannot start.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp and filter for waiting-related error patterns including ImagePullBackOff, ErrImagePull, CreateContainerConfigError, CreateContainerError to identify startup blockers.

3. Retrieve ConfigMap, Secret, and PersistentVolumeClaim resources referenced by pod <pod-name> in namespace <namespace> and check for missing dependencies that prevent container initialization.

4. Retrieve the Pod <pod-name> in namespace <namespace> and verify container image availability and image pull configuration including image pull secrets to identify image pull issues.

5. Retrieve the Pod <pod-name> in namespace <namespace> and check pod resource requests especially for special resources such as GPU and verify the Node <node-name> availability for those resources to identify resource constraints.

6. Retrieve the Node <node-name> and check node taints and tolerations to verify compatibility with pod requirements and identify scheduling issues.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify the container waiting reason. Events clearly indicate why the container cannot start. Order diagnosis by most common causes:

2. If events show "ImagePullBackOff" or "ErrImagePull" (from Playbook step 2):
   - Verify image name and tag are correct
   - Check if image exists in the registry
   - Verify imagePullSecrets are configured for private registries
   - Check network connectivity to the container registry
   - Verify registry authentication credentials are valid

3. If events show "CreateContainerConfigError" (from Playbook step 2), check for missing dependencies (Playbook step 3):
   - ConfigMap referenced in envFrom or volumeMounts does not exist
   - Secret referenced in envFrom, volumeMounts, or imagePullSecrets does not exist
   - PersistentVolumeClaim is not bound or does not exist

4. If events show "CreateContainerError", check container runtime logs for specific errors. Common causes include:
   - Invalid container configuration (malformed command/args)
   - Container image incompatible with the runtime
   - Security context preventing container creation

5. If container waiting is due to resource constraints (from Playbook steps 5-6), the scheduler placed the pod but resources are unavailable:
   - GPU or other extended resources not available on the node
   - Volume cannot be attached to the node

6. If node has taints that the pod does not tolerate (from Playbook step 6), the pod was scheduled but the node is not suitable. This usually indicates a scheduling race condition.

**To resolve container waiting**: Address the specific issue identified in the events. For ImagePullBackOff, fix image references or registry access. For CreateContainerConfigError, create missing ConfigMaps, Secrets, or PVCs. For resource issues, adjust resource requests or node configuration.
