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

1. Describe HPA <hpa-name> in namespace <namespace> to see:
   - Current replicas versus desired replicas
   - Current metrics versus target metrics
   - Conditions showing why replicas mismatch
   - Events showing scaling constraints or failures

2. Retrieve events for HPA <hpa-name> in namespace <namespace> sorted by timestamp to see the sequence of replica mismatch issues.

3. List pods managed by HPA in namespace <namespace> with label app=<app-label> and describe pods in Pending state to identify scheduling blockers (InsufficientCPU, InsufficientMemory, Unschedulable).

4. Describe ResourceQuota in namespace <namespace> and check resource quota status to verify if quotas are preventing pod creation.

5. Analyse node capacity by describing nodes and checking allocated resources to verify availability across the cluster for scheduling additional pods.

6. List PriorityClass resources and verify pod priority class configurations that may cause preemption of HPA-managed pods.

## Diagnosis

1. Analyze HPA and pod events from Playbook to identify why desired replicas cannot be achieved. If events show scheduling failures, quota errors, or scaling constraints, use event timestamps to determine when the mismatch began.

2. If events indicate pod scheduling failures (InsufficientCPU, InsufficientMemory, Unschedulable), examine pending pods from Playbook step 3. If scheduling events show specific resource constraints, cluster capacity is the limiting factor.

3. If events indicate resource quota exhaustion, verify ResourceQuota status from Playbook step 4. If quota events show limits reached, namespace quotas are preventing additional pod creation.

4. If events indicate node capacity issues, analyze node allocatable resources from Playbook step 5. If node capacity is exhausted across the cluster, insufficient cluster resources are preventing scaling.

5. If events indicate node taints or cordoning, verify node scheduling availability. If node events show cordoning or tainting at timestamps when mismatch began, reduced schedulable nodes caused the issue.

6. If events indicate cluster autoscaler activity, verify autoscaler response. If autoscaler events show pending scale-up or failures at HPA scaling timestamps, cluster autoscaler may be unable to provision additional nodes.

7. If events indicate PriorityClass or preemption issues, verify pod priority configurations from Playbook step 6. If lower-priority HPA pods are being preempted, priority adjustments may be needed.

**If no correlation is found**: Extend timeframes to 1 hour for capacity analysis, review HPA target metric configurations, check for persistent resource constraints, verify pod disruption budgets, examine historical HPA scaling patterns. HPA replica mismatch may result from cluster capacity limitations, misconfigured resource quotas, or persistent scheduling constraints rather than immediate changes.
