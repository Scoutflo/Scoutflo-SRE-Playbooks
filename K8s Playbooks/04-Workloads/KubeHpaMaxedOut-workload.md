---
title: Kube HPA Maxed Out
weight: 20
---

# KubeHpaMaxedOut

## Meaning

Horizontal Pod Autoscaler has been running at maximum replicas for longer than 15 minutes (triggering KubeHpaMaxedOut alerts) because the HPA cannot scale beyond the configured maximum replica limit despite continued high resource demand. HPAs show current replicas matching maximum replicas, HPA target metrics show high resource utilization, and pod resource usage metrics indicate sustained high demand. This affects the workload plane and indicates that either the maximum replica limit is too low, resource requests are misconfigured, or the application requires more capacity than currently allocated, typically caused by sustained high load, inadequate maximum replica configuration, or resource quota constraints; ResourceQuota limits may prevent further scaling.

## Impact

KubeHpaMaxedOut alerts fire; HPA cannot add new pods to handle increased load; applications may experience performance degradation; autoscaling is ineffective; desired replica count matches maximum replicas; applications may become unavailable under sustained high load; scaling operations are blocked; HPA target metrics consistently indicate need for more replicas; applications cannot scale to meet demand despite high resource utilization. HPAs show current replicas matching maximum replicas indefinitely; HPA target metrics show sustained high resource utilization; ResourceQuota limits may prevent further scaling; applications may experience performance degradation or become unavailable under sustained high load.

## Playbook

1. Describe HPA <hpa-name> in namespace <namespace> to see:
   - Current replicas, desired replicas, and maximum replicas
   - Current metrics versus target metrics
   - Conditions showing HPA is maxed out
   - Events showing scaling constraints or high utilization

2. Retrieve events for HPA <hpa-name> in namespace <namespace> sorted by timestamp to see the sequence of scaling events and constraints.

3. Retrieve resource usage metrics for pods in namespace <namespace> with label app=<app-label> to verify high resource demand.

4. Describe pod <pod-name> in namespace <namespace> to check resource requests and limits and compare with actual usage to identify misconfigurations.

5. Describe ResourceQuota in namespace <namespace> and check for resource quota limits that may prevent scaling beyond current levels.

6. Analyse node capacity by describing nodes and checking allocated resources to verify if additional pod replicas can be supported if HPA could scale further.

## Diagnosis

1. Analyze HPA events from Playbook to identify when HPA reached maximum replicas. If events show scaling attempts that hit the maximum limit, use event timestamps to determine the duration of maxed-out state.

2. If events indicate sustained high resource utilization, verify pod resource metrics from Playbook step 3. If target metrics consistently exceed thresholds while at maximum replicas, the maximum replica limit is too low for current demand.

3. If events indicate resource quota constraints, verify ResourceQuota status from Playbook step 5. If quota limits prevent creating additional pods even if HPA maximum were increased, quota adjustment is required first.

4. If events indicate node capacity exhaustion, analyze node capacity from Playbook step 6. If cluster has no capacity for additional pods, increasing HPA maximum would not help until cluster capacity is expanded.

5. If events indicate misconfigured resource requests, compare pod resource requests with actual usage from Playbook step 4. If pods request more resources than they use, reducing requests would allow more replicas within the same capacity.

6. If events show HPA regularly hitting maximum at predictable times, analyze historical patterns. If maxed-out periods align with traffic patterns (e.g., business hours), the maximum limit needs adjustment for peak demand.

7. If events indicate application performance issues, verify if high resource usage is due to inefficient application behavior. If resource usage is higher than expected for the workload, application optimization may reduce scaling needs.

**If no correlation is found**: Extend timeframes to 7 days for capacity analysis, review HPA target metric configurations, check for application performance issues causing high resource usage, verify cluster autoscaler effectiveness, examine historical scaling patterns. HPA may be maxed out due to sustained high load, inadequate maximum replica limits, or application inefficiencies rather than immediate configuration issues.
