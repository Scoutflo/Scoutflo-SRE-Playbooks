---
title: Evicted Pods - Pod
weight: 205
categories:
  - kubernetes
  - pod
---

# EvictedPods-pod

## Meaning

Pods are being forcibly evicted by the kubelet from a node because resource pressure thresholds (MemoryPressure, DiskPressure conditions triggering KubeNodeMemoryPressure or KubeNodeDiskPressure alerts) have been exceeded. Pods show Evicted state in kubectl, pod status reason shows Evicted with resource pressure type, and node conditions show MemoryPressure or DiskPressure. This affects the workload plane and indicates node resource exhaustion, typically caused by memory or disk pressure; applications experience unexpected restarts and may show errors.

## Impact

Pods are forcibly terminated; applications experience unexpected restarts; deployments lose replicas; services may become unavailable; applications may lose in-memory state; pod eviction events occur; node pressure conditions trigger alerts; pod status changes to Evicted; resource constraints prevent pod scheduling. Pods show Evicted state indefinitely; pod status reason shows Evicted with resource pressure type; applications experience unexpected restarts and may show errors; applications may lose in-memory state.

## Playbook

1. List evicted pods in namespace <namespace> and their eviction reasons to identify which pods were evicted and why.

2. Retrieve events in namespace <namespace> filtered by reason Evicted and sorted by timestamp to see eviction timestamps and which node triggered the eviction.

3. Describe node <node-name> that evicted pods and check:
   - Conditions section for MemoryPressure, DiskPressure, PIDPressure
   - Allocated resources section to see resource consumption
   - Events section for eviction events with timestamps

4. Retrieve the active conditions for node <node-name> to identify which resource pressure caused evictions.

5. Describe Deployment <deployment-name> in namespace <namespace> to check resource requests and limits - compare with node capacity to see if requests are too high.

6. Retrieve resource usage metrics for node <node-name> to see current CPU and memory consumption.

7. For disk pressure, SSH to node and check disk usage to identify what is consuming disk space.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify the eviction reason. Events showing "Evicted" include the specific resource pressure (memory, disk, PID) that triggered the eviction.

2. If events indicate MemoryPressure eviction (from Playbook step 2):
   - Node memory usage exceeded eviction threshold
   - Check node conditions (Playbook steps 3-4) for MemoryPressure=True
   - Identify memory-hungry pods using node metrics (Playbook step 6)
   - Pods are evicted in QoS order: BestEffort first, then Burstable, then Guaranteed

3. If events indicate DiskPressure eviction:
   - Node disk usage exceeded eviction threshold
   - Check disk usage on node (Playbook step 7)
   - Common causes: container logs, pulled images, emptyDir volumes
   - Clean up unused images and old logs on the node

4. If events indicate PIDPressure eviction:
   - Node has too many running processes
   - Check for runaway process spawning in containers
   - Review applications that fork many child processes

5. If deployment resource requests are low (from Playbook step 5):
   - BestEffort pods (no requests) are evicted first
   - Burstable pods (requests < limits) are evicted next
   - Set appropriate requests to improve eviction priority

6. If node resource usage shows sustained pressure (from Playbook step 6):
   - Node is consistently overcommitted
   - Consider adding more nodes or reducing workload
   - Review pod resource requests to ensure accurate scheduling

7. Evicted pods remain in Evicted status until deleted. The deployment controller creates replacement pods on other nodes.

**To prevent future evictions**: Set appropriate resource requests and limits, use Guaranteed QoS class for critical pods, implement resource monitoring and alerting, and ensure cluster has adequate capacity for workload peaks.

