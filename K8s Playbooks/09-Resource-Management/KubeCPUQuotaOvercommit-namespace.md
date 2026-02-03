---
title: Kube CPU Quota Overcommit
weight: 20
---

# KubeCPUQuotaOvercommit

## Meaning

Cluster has overcommitted CPU resource requests for namespaces (triggering KubeCPUQuotaOvercommit alerts) because the total CPU requests across all pods exceed available cluster capacity, preventing the cluster from tolerating node failures. ResourceQuota resources show CPU request usage exceeding available cluster capacity, node allocatable CPU metrics indicate insufficient capacity, and pod scheduling may fail with InsufficientCPU errors. This indicates capacity planning issues in the compute plane, where resource allocation exceeds physical or allocatable resources, typically caused by inadequate capacity planning, misconfigured resource requests, or insufficient cluster scaling; cluster autoscaler may fail to add nodes.

## Impact

KubeCPUQuotaOvercommit alerts fire; in the event of a node failure, pods will be in Pending state due to insufficient CPU resources; new workloads cannot be scheduled; deployments fail to scale; cluster cannot tolerate node failures; pod scheduling fails with InsufficientCPU errors; capacity constraints prevent workload deployment. ResourceQuota resources show CPU request usage exceeding available cluster capacity; node allocatable CPU metrics indicate insufficient capacity; pod scheduling fails with InsufficientCPU errors; cluster autoscaler may fail to add nodes; applications cannot scale and may experience errors or performance degradation.

## Playbook

1. Describe the ResourceQuota `<quota-name>` in namespace `<namespace>` to inspect its status and check CPU request usage versus quota limits.

2. Retrieve events in namespace `<namespace>` sorted by timestamp to identify quota-related events and resource allocation issues.

3. List Pod resources in namespace `<namespace>` and aggregate CPU requests to compare with namespace quota.

4. Retrieve the Node `<node-name>` resources and check node allocatable CPU resources and current CPU request allocations across all nodes.

5. Verify cluster autoscaler status and logs for issues preventing node addition by checking cluster autoscaler configuration and logs.

6. Retrieve the Node `<node-name>` resources and check for cordoned or unschedulable nodes that reduce available cluster capacity.

7. Retrieve metrics for the Node `<node-name>` resources and compare CPU usage with CPU requests to identify overcommitment patterns.

## Diagnosis

1. Analyze events from Playbook to identify CPU-related scheduling failures. Events showing "InsufficientCPU" or "FailedScheduling" indicate pods that could not be placed due to CPU constraints. The timestamps indicate when overcommit became problematic.

2. If events indicate pods pending due to insufficient CPU, compare total CPU requests across all pods with total node allocatable CPU from Playbook. This shows the extent of overcommitment and how much additional CPU capacity is needed.

3. If overcommit correlates with node removal or cordoning events, capacity reduction caused the overcommit condition. Check node events for recently removed, cordoned, or NotReady nodes that reduced available cluster CPU.

4. If overcommit correlates with recent scaling or deployment events, those operations increased CPU requests beyond available capacity. Identify which deployments scaled up or which new workloads were deployed.

5. If cluster autoscaler events show scaling failures or no scaling activity despite pending pods, verify autoscaler status from Playbook. Check for node group maximum limits, cloud provider quota limits, or autoscaler configuration issues preventing capacity expansion.

6. If overcommit exists but no pods are currently pending, the cluster may tolerate the condition until a node failure occurs. A node failure would cause pods to be evicted but unable to reschedule due to insufficient remaining CPU capacity.

7. If CPU requests across namespaces significantly exceed actual CPU usage (high request-to-usage ratio), consider right-sizing pod CPU requests. Over-provisioned requests cause artificial overcommit that could be resolved by reducing requests to match actual usage patterns.
