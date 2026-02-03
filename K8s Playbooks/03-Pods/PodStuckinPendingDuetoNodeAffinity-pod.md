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

1. Describe pod <pod-name> in namespace <namespace> to inspect spec.affinity.nodeAffinity to identify the required or preferred node affinity rules.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify scheduler events, focusing on events with messages indicating affinity mismatches or "0/X nodes are available" with affinity reasons.

3. List all nodes and retrieve their labels to compare with the pod's affinity requirements and identify which labels are missing or mismatched.

4. Retrieve the Deployment <deployment-name> in namespace <namespace> and review the pod template's affinity configuration to verify the affinity rules are correctly specified.

5. Check if anti-affinity rules are too restrictive by verifying if any nodes satisfy the requirements or if the rules conflict with each other.

6. Verify if node labels were recently removed or changed that may have caused previously schedulable pods to become unschedulable.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify the affinity constraint causing scheduling failure. Events showing "0/X nodes are available" with affinity-related reasons indicate which constraint cannot be satisfied.

2. If events indicate nodeAffinity mismatch (from Playbook step 2):
   - requiredDuringSchedulingIgnoredDuringExecution cannot be satisfied
   - Check pod affinity rules (Playbook step 1) against node labels (Playbook step 3)
   - Identify which label selector expression is not matched

3. If events indicate podAntiAffinity conflict:
   - Pod cannot be placed without violating anti-affinity with existing pods
   - Check if topologyKey is too restrictive (e.g., kubernetes.io/hostname)
   - Consider using preferredDuringSchedulingIgnoredDuringExecution for soft rules

4. If events indicate podAffinity cannot be satisfied:
   - No nodes have pods matching the affinity selector
   - The required pod may be on an unschedulable node
   - Check if affinity target pods exist and are running

5. If deployment affinity rules (from Playbook step 4) conflict with available nodes:
   - requiredDuringScheduling rules are hard constraints
   - preferredDuringScheduling rules should allow scheduling with lower score
   - Convert hard constraints to soft preferences if flexibility is acceptable

6. If anti-affinity rules are too restrictive (from Playbook step 5):
   - Each replica needs a unique node but not enough nodes exist
   - Relax topologyKey from hostname to zone or region
   - Reduce replica count or add more nodes

7. If nodes with matching labels exist but are not schedulable (from Playbook step 6):
   - Node is cordoned or tainted
   - Node resources are exhausted
   - Other scheduling constraints block placement

**To resolve affinity scheduling issues**: Either add/update node labels to match affinity requirements, add nodes with required labels, relax affinity rules (convert required to preferred), or remove conflicting anti-affinity constraints. Use `kubectl describe pod` to see the exact scheduling failure reason.

