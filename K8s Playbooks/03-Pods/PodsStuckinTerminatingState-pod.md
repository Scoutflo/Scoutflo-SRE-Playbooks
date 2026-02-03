---
title: Pods Stuck in Terminating State - Pod
weight: 293
categories:
  - kubernetes
  - pod
---

# PodsStuckinTerminatingState-pod

## Meaning

Pods remain stuck in Terminating state (triggering KubePodNotReady alerts) because finalizers cannot complete, persistent volumes cannot be unmounted, the kubelet on the node cannot communicate with the control plane, or the node itself is unreachable. Pods show Terminating state indefinitely in kubectl, pod finalizers prevent deletion, and PersistentVolumeClaim resources may show stuck binding. This affects the workload plane and blocks resource cleanup, typically caused by finalizer processing failures, PersistentVolume unmount issues, or node communication problems; PersistentVolumeClaim binding failures may prevent pod termination.

## Impact

Pods cannot be deleted; namespace cleanup is blocked; resources remain allocated; new pods may fail to schedule due to resource constraints; finalizers prevent resource deletion; volumes remain attached; pod IPs remain allocated; KubePodNotReady alerts fire; pod status shows Terminating indefinitely; cluster resource management is impaired. Pods show Terminating state indefinitely; pod finalizers prevent deletion; PersistentVolumeClaim binding failures may prevent pod termination; applications may experience resource allocation issues.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to inspect pod deletion timestamp and finalizers to confirm the pod is in Terminating state and identify which finalizers are present.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify events related to volume unmount failures, finalizer errors, or node communication issues.

3. Check the node where the pod was scheduled and verify its Ready condition and communication status with the control plane by checking node status conditions to determine if the node is reachable.

4. Verify node-to-control-plane connectivity by checking if kubelet on the node can communicate with the API server.

5. Retrieve the PersistentVolumeClaim objects referenced by the pod and check their status to verify if volumes are stuck in use or cannot be released.

6. Retrieve the pod <pod-name> and inspect pod volume configuration to identify all volume types and their mount points, then verify if any volumes have unmount issues.

7. List all finalizers on the pod and check if any custom resource controllers or operators are responsible for those finalizers and verify their status by checking controller pod logs.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify why termination is blocked. Events showing volume unmount failures, finalizer errors, or node communication issues indicate the specific blocker preventing pod deletion.

2. If pod metadata shows finalizers (from Playbook step 1), identify which finalizer is blocking deletion:
   - "kubernetes.io/pvc-protection": PersistentVolumeClaim cannot be released
   - "foregroundDeletion": Dependent resources still exist
   - Custom finalizers: Operator or controller responsible for cleanup is failing

3. If node status shows NotReady condition (from Playbook step 3), the kubelet cannot complete pod cleanup. The pod will remain Terminating until the node recovers or is removed from the cluster.

4. If events indicate volume unmount failures (from Playbook step 2), check PersistentVolumeClaim status (Playbook step 5). Common causes include:
   - Storage provider issues preventing volume detachment
   - Volume still in use by another pod
   - Node cannot communicate with storage backend

5. If kubelet connectivity check fails (from Playbook step 4), the node cannot report pod termination completion to the API server. Verify network connectivity between the node and control plane.

6. If finalizer controller pods are failing or restarting (from Playbook step 7), the finalizer cannot be processed. Check controller logs for errors and restart the controller if necessary.

7. If no specific blocker is identified in events, check if the terminationGracePeriodSeconds has been exceeded. Kubernetes will force-kill the pod after this period, but cleanup may still be blocked by finalizers or volumes.

**If pod remains stuck after investigation**: Consider force-deleting the pod with `kubectl delete pod --force --grace-period=0` (use with caution as this may leave orphaned resources). For stuck finalizers, manually remove them only after verifying the underlying resource is cleaned up.

