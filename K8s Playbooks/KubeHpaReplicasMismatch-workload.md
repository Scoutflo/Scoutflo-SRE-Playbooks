---
title: Kube HPA  Replicas Mismatch
weight: 20
---

# KubeHpaReplicasMismatch

## Meaning

Horizontal Pod Autoscaler has not matched the desired number of replicas for longer than 15 minutes (triggering KubeHpaReplicasMismatch alerts) because the HPA cannot schedule the desired number of pods due to resource constraints, quota limits, or scheduling failures. HPAs show replica count mismatches in kubectl, pods remain in Pending state, and pod events show InsufficientCPU, InsufficientMemory, or Unschedulable errors. This affects the workload plane and indicates capacity or configuration issues preventing HPA from achieving desired scaling, typically caused by cluster capacity limitations, resource quota exhaustion, or persistent scheduling constraints; ResourceQuota limits may prevent pod creation.

## Impact

KubeHpaReplicasMismatch alerts fire; HPA cannot achieve desired replica count; applications run with insufficient capacity; performance degradation or unavailability; desired replicas exceed current replicas; pod scheduling failures occur; autoscaling cannot meet demand; pods remain in Pending state; resource constraints, quota limits, or scheduling failures prevent HPA from achieving desired scaling. HPAs show replica count mismatches indefinitely; pods remain in Pending state; pod events show InsufficientCPU, InsufficientMemory, or Unschedulable errors; ResourceQuota limits may prevent pod creation; applications run with insufficient capacity and may experience errors or performance degradation.

## Playbook

1. Retrieve the HorizontalPodAutoscaler `<hpa-name>` in namespace `<namespace>` and inspect its status to check current replicas versus desired replicas and identify the mismatch.

2. Retrieve the Pod `<pod-name>` in namespace `<namespace>` managed by HPA and check pod status to identify pods in Pending state.

3. Retrieve events for the Pod `<pod-name>` in namespace `<namespace>` and filter for scheduling error patterns including 'InsufficientCPU', 'InsufficientMemory', 'Unschedulable' to identify scheduling blockers.

4. Retrieve the ResourceQuota `<quota-name>` in namespace `<namespace>` and check resource quota status to verify if quotas are preventing pod creation.

5. Retrieve the Node `<node-name>` resources and verify node capacity and availability across the cluster for scheduling additional pods.

6. Retrieve PriorityClass resources and check for pod priority class configurations that may cause preemption of HPA-managed pods.

## Diagnosis

Compare HPA desired replica increase timestamps with pod scheduling failure timestamps within 30 minutes and verify whether scheduling failures began when HPA attempted to scale up, using HPA events and pod scheduling events as supporting evidence.

Correlate HPA replica mismatch detection with resource quota exhaustion timestamps within 30 minutes and verify whether resource quotas prevented achieving desired replica count, using resource quota status and HPA scaling attempts as supporting evidence.

Analyze pod scheduling failure patterns over the last 15 minutes to determine if failures are due to resource constraints, node availability, or quota limits, using pod events and node conditions as supporting evidence.

Compare HPA desired replica count with available node capacity at mismatch times and verify whether insufficient cluster capacity prevented scaling, using node metrics and cluster capacity data as supporting evidence.

Correlate HPA replica mismatch with node removal or cordoning event timestamps within 30 minutes and verify whether node capacity reduction caused scheduling failures, using node condition changes and pod scheduling events as supporting evidence.

Compare HPA scaling attempts with cluster autoscaler activity timestamps within 30 minutes and verify whether autoscaler failed to add nodes when HPA needed capacity, using autoscaler logs and node creation events as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for capacity analysis, review HPA target metric configurations, check for persistent resource constraints, verify pod disruption budgets, examine historical HPA scaling patterns. HPA replica mismatch may result from cluster capacity limitations, misconfigured resource quotas, or persistent scheduling constraints rather than immediate changes.
