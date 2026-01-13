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

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect pod deletion timestamp and finalizers to confirm the pod is in Terminating state and identify which finalizers are present.

2. Check the node where the pod was scheduled and verify its Ready condition and communication status with the control plane by checking node status conditions to determine if the node is reachable.

3. Verify node-to-control-plane connectivity by checking if kubelet on the node can communicate with the API server.

4. List events in namespace `<namespace>` and filter for events related to the pod, focusing on volume unmount failures, finalizer errors, or node communication issues.

5. Retrieve the PersistentVolumeClaim objects referenced by the pod and check their status to verify if volumes are stuck in use or cannot be released.

6. Retrieve the pod `<pod-name>` and inspect pod volume configuration to identify all volume types and their mount points, then verify if any volumes have unmount issues.

7. List all finalizers on the pod and check if any custom resource controllers or operators are responsible for those finalizers and verify their status by checking controller pod logs.

## Diagnosis

1. Compare the pod deletion initiation timestamps with node Ready condition transition times, and check whether the node became NotReady or unreachable within 5 minutes after deletion was initiated.

2. Compare the pod deletion initiation timestamps with node-to-control-plane connectivity failure timestamps, and check whether node communication failures occurred within 5 minutes after deletion was initiated.

3. Compare the pod deletion initiation timestamps with volume unmount failure event timestamps, and check whether volume unmount errors occurred within 5 minutes of deletion initiation.

4. Compare the pod deletion initiation timestamps with finalizer controller restart or failure timestamps, and check whether finalizer processing failures began within 5 minutes of deletion.

5. Compare the pod deletion initiation timestamps with finalizer controller unavailability timestamps from controller logs, and check whether finalizer controllers became unavailable within 5 minutes of deletion.

6. Compare the pod deletion initiation timestamps with PersistentVolumeClaim status change timestamps, and check whether PVCs became stuck or bound to terminating pods within 5 minutes of deletion.

7. Compare the pod deletion initiation timestamps with network policy or security policy modification timestamps that may affect pod-to-control-plane communication, and check whether policy changes occurred within 10 minutes before deletion issues.

8. Compare the pod deletion initiation timestamps with cluster upgrade or maintenance windows, and check whether deletion issues began within 1 hour of infrastructure changes that may have affected finalizer processing or volume management.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 1 hour → 2 hours), review finalizer controller logs for processing delays, check for gradual node communication degradation, examine volume provider issues that may have developed over time, verify if custom resource definitions or operators responsible for finalizers are experiencing issues, and check for resource quota or limit constraints that may prevent cleanup operations. Pod termination issues may result from cumulative system problems rather than immediate failures.

