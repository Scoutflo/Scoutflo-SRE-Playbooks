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

1. Describe pod <pod-name> in namespace <namespace> to see the container waiting reason in the Status section and check Events for FailedMount, ErrImagePull, or CreateContainerConfigError with specific details.

2. Retrieve events for pod <pod-name> in namespace <namespace> sorted by timestamp to see the sequence of failures (image pull, volume mount, config errors).

3. Retrieve the container waiting state for pod <pod-name> in namespace <namespace> to see exactly why container creation is stuck.

4. If volume mount issue, list PersistentVolumeClaims in namespace <namespace> and describe PVC <pvc-name> to see if PVC is bound and volume is available.

5. If ConfigMap/Secret issue, verify they exist: check ConfigMap <name> and Secret <name> in namespace <namespace>.

6. Describe Deployment <deployment-name> in namespace <namespace> to check image references, volume mounts, and imagePullSecrets configuration.

7. Describe node <node-name> where pod is scheduled to look for disk pressure, container runtime issues, or resource constraints.

8. Check container runtime on the node (SSH required) to see container creation attempts and runtime logs for errors.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify why container creation is stuck. Events showing the container waiting reason provide the specific blocker. Order diagnosis by most common causes:

2. If events show "ImagePullBackOff" or "ErrImagePull" (from Playbook step 2):
   - Image does not exist or tag is incorrect
   - Private registry requires imagePullSecrets not configured
   - Network connectivity to registry failed
   - Registry rate limiting or authentication issues
   - Check deployment image configuration (Playbook step 6)

3. If events show "FailedMount" for volumes (from Playbook step 2):
   - PVC is not bound (Playbook step 4) - check storage class and provisioner
   - PV cannot attach to node - check cloud provider volume limits
   - Volume already attached to another node - multi-attach not supported
   - NFS or network storage unreachable

4. If events show "CreateContainerConfigError" (from Playbook step 3):
   - ConfigMap or Secret does not exist (Playbook step 5)
   - Key referenced in envFrom or volumeMount missing
   - Syntax error in container command or args

5. If node shows resource issues (from Playbook step 7):
   - DiskPressure: Node disk full, cannot pull images
   - Container runtime overloaded or unresponsive
   - Too many containers on node

6. If container runtime logs show errors (from Playbook step 8):
   - Runtime cannot create container sandbox
   - Image format incompatible with runtime
   - Security policy blocking container creation

**To resolve ContainerCreating issues**: Fix image references for pull errors, create missing ConfigMaps/Secrets, ensure PVCs are bound and volumes can attach, free node disk space if needed, and verify container runtime is healthy.

