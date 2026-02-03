---
title: Pod Stuck In Terminating State - Pod
weight: 206
categories:
  - kubernetes
  - pod
---

# PodStuckInTerminatingState-pod

## Meaning

A pod is stuck in the Terminating phase (potentially triggering KubePodNotReady alerts) because shutdown cannot complete cleanly, often due to hanging processes, blocking finalizers, or attached volumes and endpoints that cannot be detached. Pods show Terminating state indefinitely in kubectl, pod finalizers prevent deletion, and pod events may show deletion-related errors. This indicates pod deletion failures, finalizer issues, or resource dependency problems preventing graceful pod termination; PersistentVolumeClaim detachments may fail.

## Impact

Pods cannot be deleted; deployments cannot update; rolling updates hang; resources remain in terminating state; cluster state becomes inconsistent; new pods may not start if resources are blocked; KubePodNotReady alerts may fire; pods remain in Terminating state; finalizers prevent deletion; volume detachments fail. Pods show Terminating state indefinitely; pod finalizers prevent deletion; PersistentVolumeClaim detachments may fail; applications may experience resource allocation issues.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to check pod details and reason for termination delay.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify deletion-related events.

3. Retrieve pod <pod-name> in namespace <namespace> and check finalizers preventing deletion.

4. Check dependent resources like persistent volume claims, services, or other pods.

5. Retrieve deployment <deployment-name> in namespace <namespace> and verify terminationGracePeriodSeconds setting.

6. Retrieve pod <pod-name> in namespace <namespace> and check for volume mount issues.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify why the pod is stuck in Terminating state. Events showing deletion-related errors, volume detachment failures, or finalizer issues indicate the specific blocker.

2. If pod metadata shows finalizers (from Playbook step 3), identify which finalizer is preventing deletion:
   - "kubernetes.io/pvc-protection": PersistentVolumeClaim is still bound
   - "foregroundDeletion": Child resources still exist
   - Custom finalizers: Check the owning controller/operator status

3. If events indicate volume mount issues (from Playbook step 6), PersistentVolumeClaims cannot be detached. Check dependent resources (Playbook step 4) to verify PVC status and storage provider health.

4. If no events indicate the blocker, check if the node where the pod was running is healthy. A NotReady node cannot complete pod termination cleanup.

5. If terminationGracePeriodSeconds (from Playbook step 5) is very long, the pod may still be in its grace period. Kubernetes waits for containers to terminate gracefully before force-killing them.

6. If events show no errors but pod remains Terminating, check for hanging processes in the container that are not responding to SIGTERM. The container may need to handle shutdown signals properly.

**If pod remains stuck after investigation**: Consider force-deleting with `kubectl delete pod --force --grace-period=0` if the underlying resources are confirmed cleaned up. For stuck finalizers, manually patch the pod to remove finalizers only after verifying dependent resources are properly cleaned.
