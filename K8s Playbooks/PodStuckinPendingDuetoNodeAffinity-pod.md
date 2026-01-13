---
title: Pod Stuck in Pending Due to Node Affinity - Pod
weight: 291
categories:
  - kubernetes
  - pod
---

# PodStuckinPendingDuetoNodeAffinity-pod

## Meaning

Pods remain stuck in Pending state (triggering KubePodPending alerts) because the scheduler cannot find any node that satisfies the pod's affinity or anti-affinity rules. Pods show Pending state in kubectl, pod events show "0/X nodes are available" messages with affinity mismatch reasons, and node labels may not match pod affinity requirements. This affects the workload plane and prevents pod placement, typically caused by node label mismatches or restrictive affinity rules; applications cannot start.

## Impact

Pods cannot be scheduled; deployments fail to scale; applications remain unavailable; services cannot get new pods; pods remain in Pending state indefinitely; scheduler cannot place pods; replica counts mismatch desired state; KubePodPending alerts fire; pod events show "0/X nodes are available" messages with affinity mismatch reasons. Pods show Pending state indefinitely; pod events show affinity mismatch reasons; node labels may not match pod affinity requirements; applications cannot start and may show errors.

## Playbook

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect `spec.affinity.nodeAffinity` to identify the required or preferred node affinity rules.

2. List events in namespace `<namespace>` and filter for scheduler events associated with the pod, focusing on events with messages indicating affinity mismatches or "0/X nodes are available" with affinity reasons.

3. List all nodes and retrieve their labels to compare with the pod's affinity requirements and identify which labels are missing or mismatched.

4. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review the pod template's affinity configuration to verify the affinity rules are correctly specified.

5. Check if anti-affinity rules are too restrictive by verifying if any nodes satisfy the requirements or if the rules conflict with each other.

6. Verify if node labels were recently removed or changed that may have caused previously schedulable pods to become unschedulable.

## Diagnosis

1. Compare the pod Pending timestamps with node label modification timestamps, and check whether required node labels were removed or changed within 30 minutes before pods became Pending.

2. Compare the pod Pending timestamps with deployment affinity rule modification timestamps, and check whether affinity rules were added or made more restrictive within 30 minutes before pods became Pending.

3. Compare the pod Pending timestamps with node removal or cordoning timestamps, and check whether nodes that previously satisfied affinity requirements were removed or made unschedulable within 30 minutes before scheduling failures.

4. Compare the pod Pending timestamps with anti-affinity rule modification timestamps, and check whether anti-affinity rules were added or made more restrictive within 30 minutes before pods became Pending, preventing placement on available nodes.

5. Compare the pod Pending timestamps with cluster scaling events or node provisioning timestamps, and check whether new nodes were added but lack required labels within 30 minutes before scheduling failures.

6. Compare the pod Pending timestamps with deployment rollout or pod template update timestamps, and check whether affinity configuration changes occurred within 1 hour before pods became Pending, indicating new affinity requirements may be incompatible with current cluster nodes.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review scheduler logs for detailed affinity evaluation reasons, check for gradual node label drift over time, examine if affinity rules were always incompatible but only recently enforced, verify if node capacity changes affected affinity satisfaction, and check for cumulative scheduling constraints from multiple affinity rules. Affinity-related scheduling failures may result from gradual cluster state changes rather than immediate configuration modifications.

