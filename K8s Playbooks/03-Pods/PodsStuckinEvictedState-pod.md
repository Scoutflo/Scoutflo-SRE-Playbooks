---
title: Pods Stuck in Evicted State - Pod
weight: 283
categories:
  - kubernetes
  - pod
---

# PodsStuckinEvictedState-pod

## Meaning

Pods remain in Evicted state (triggering KubePodNotReady alerts) because they were evicted by kubelet due to node resource pressure (MemoryPressure, DiskPressure, PIDPressure) but were not automatically cleaned up. Pods show Evicted state in kubectl, pod status reason shows Evicted with resource pressure type, and node conditions may show MemoryPressure, DiskPressure, or PIDPressure. This affects the workload plane and blocks cleanup, typically caused by node resource exhaustion; applications cannot run on affected nodes.

## Impact

Evicted pods remain in the cluster; pod resources are not released; deployments cannot achieve desired replica count; new pods may fail to schedule due to resource constraints; namespace cleanup is blocked; pod status shows Evicted state; KubePodNotReady alerts fire; node resources remain allocated to evicted pods; cluster resource management is impaired. Pods show Evicted state indefinitely; pod status reason shows Evicted with resource pressure type; node conditions show MemoryPressure, DiskPressure, or PIDPressure; applications cannot run on affected nodes and may show errors.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to inspect status.reason and status.message to confirm eviction reason and identify which resource pressure caused the eviction.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify eviction events, focusing on events with reasons such as Evicted and messages indicating the resource pressure type (memory, disk, PID).

3. List pods in namespace <namespace> and filter for pods with status Evicted to identify all evicted pods.

4. Check the node where the pod was evicted and verify its resource pressure conditions (MemoryPressure, DiskPressure, PIDPressure) to understand current node state.

5. Retrieve the Deployment <deployment-name> in namespace <namespace> and review resource requests to verify if requests are reasonable relative to node capacity.

6. Check node resource usage metrics to verify current available resources and identify if node-level resource pressure persists.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify the eviction reason. The status.reason field shows "Evicted" and status.message indicates the specific resource pressure (memory, disk, PID) that triggered the eviction.

2. If eviction message indicates MemoryPressure (from Playbook step 1), the node ran out of memory. Check node conditions (Playbook step 4) to confirm MemoryPressure and review node memory usage metrics (Playbook step 6) to identify memory-hungry pods.

3. If eviction message indicates DiskPressure, the node ran out of disk space. Common causes include:
   - Container logs consuming too much space
   - Container images filling the disk
   - emptyDir volumes growing unbounded
   - Application writing excessive data to ephemeral storage

4. If eviction message indicates PIDPressure, the node has too many running processes. Check for runaway process spawning in containers.

5. If multiple pods were evicted simultaneously (from Playbook step 3), there was a significant resource pressure event on the node. Lower-priority pods are evicted first based on QoS class (BestEffort, then Burstable, then Guaranteed).

6. If deployment resource requests (from Playbook step 5) are too low relative to actual usage, pods may be scheduled on nodes with insufficient capacity. Increase resource requests to ensure proper scheduling.

7. Evicted pods remain in Evicted state until manually deleted or garbage collected. They do not automatically restart; the deployment controller creates new pods on other nodes.

**To prevent future evictions**: Set appropriate resource requests and limits, configure pod priority classes for critical workloads, implement horizontal pod autoscaling, add more nodes to the cluster, or reduce resource consumption in applications.

