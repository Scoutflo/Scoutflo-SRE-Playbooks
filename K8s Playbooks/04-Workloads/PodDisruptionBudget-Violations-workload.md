---
title: Pod Disruption Budget Violations - Workload
weight: 250
categories:
  - kubernetes
  - workload
  - pod-disruption-budget
---

# PodDisruptionBudget-Violations-workload

## Meaning

Pod Disruption Budget (PDB) violations occur when voluntary disruptions (node drains, pod evictions, rolling updates) cannot proceed because they would violate the minimum availability constraints defined in a PodDisruptionBudget resource. This manifests as eviction failures, node drain operations hanging or failing, deployment rollouts stuck, or cluster autoscaler unable to remove nodes. PDBs protect application availability by ensuring a minimum number of pods remain available during voluntary disruptions, but misconfigured PDBs (too restrictive minAvailable/maxUnavailable values, incorrect label selectors, or overlapping PDBs) can prevent necessary maintenance operations, scaling actions, or deployments from completing. This affects the workload plane and indicates availability protection constraints blocking voluntary pod disruptions, typically caused by overly restrictive PDB configurations, PDB label selector mismatches, or PDB conflicts with scaling/deployment operations.

## Impact

PDB violation alerts fire; node drain operations fail or hang indefinitely; deployment rollouts cannot proceed; pods cannot be evicted for node maintenance; cluster autoscaler cannot scale down nodes; rolling updates are blocked; voluntary disruptions are prevented; maintenance windows cannot be executed; pods remain on unhealthy nodes; system updates and node replacements are delayed. Node drain operations show "cannot drain node" errors due to PDB violations; deployment rollouts show pods stuck in Terminating state; eviction API calls return 429 Too Many Requests errors; cluster autoscaler logs show scale-down blocked by PDB constraints; voluntary pod disruptions are prevented even when nodes need maintenance.

## Playbook

1. Describe PodDisruptionBudget resources in namespace `<namespace>` to see:
   - PDB configuration (minAvailable, maxUnavailable)
   - Label selectors matching pods
   - Current status (disruptionsAllowed, desiredHealthy, currentHealthy)
   - Conditions showing PDB health

2. List pods in namespace `<namespace>` matching PDB label selectors to verify which pods are protected by the PDB and their current status.

3. Retrieve events in namespace `<namespace>` filtered by involved object name `<pdb-name>` and sorted by last timestamp to see PDB violation events and eviction failures.

4. Describe deployment `<deployment-name>` or statefulset `<statefulset-name>` in namespace `<namespace>` to check if rollout is stuck due to PDB constraints preventing pod termination.

5. Check node drain status for node `<node-name>` if node maintenance is blocked, verifying if drain operation is hanging due to PDB violations.

6. List all PodDisruptionBudget resources across all namespaces to identify overlapping PDBs that may be protecting the same pods with conflicting constraints.

7. Retrieve cluster autoscaler logs or events if scale-down operations are blocked, checking for PDB-related scale-down prevention messages.

8. Describe pods in namespace `<namespace>` that are stuck in Terminating state to verify if PDB constraints are preventing their eviction.

9. Check eviction API response for pod `<pod-name>` in namespace `<namespace>` to see if eviction is blocked due to PDB violations (expect 429 status code).

10. Verify PDB label selector matches pod labels correctly by comparing PDB spec.selector.matchLabels with actual pod labels.

## Diagnosis

1. Analyze PDB status from Playbook step 1 to identify violation patterns. If `disruptionsAllowed` is 0 and `currentHealthy` equals `minAvailable`, the PDB is preventing any voluntary disruptions. If `disruptionsAllowed` is negative, the PDB configuration is invalid or pods are unhealthy.

2. If events from Playbook step 3 show "eviction blocked by PodDisruptionBudget" or similar messages, correlate the event timestamp with when node drain, deployment rollout, or eviction operations started. This establishes that PDB constraints are actively blocking disruptions.

3. If deployment rollout is stuck (from Playbook step 4) and pods remain in Terminating state, check if the PDB's `minAvailable` or `maxUnavailable` values prevent terminating old pods. For example, if `minAvailable: 2` and only 2 pods exist, no pods can be terminated during rollout.

4. If node drain operations are hanging (from Playbook step 5), verify that pods on the node match PDB selectors and that evicting them would violate PDB constraints. Check if `disruptionsAllowed` is 0 for the relevant PDBs protecting pods on that node.

5. If multiple PDBs are found (from Playbook step 6) with overlapping label selectors protecting the same pods, verify if their combined constraints create impossible requirements. For example, two PDBs each requiring `minAvailable: 2` for the same 3 pods would allow only 1 disruption total, potentially blocking necessary operations.

6. If cluster autoscaler scale-down is blocked (from Playbook step 7), check if pods on nodes targeted for removal are protected by PDBs that prevent their eviction. Autoscaler cannot remove nodes if doing so would violate PDB constraints.

7. If pods are stuck in Terminating state (from Playbook step 8), verify if PDB constraints are preventing final pod deletion. Check pod finalizers and PDB status to determine if PDB is the blocker versus other finalizers.

8. If eviction API returns 429 Too Many Requests (from Playbook step 9), this confirms PDB is actively blocking eviction. Check the response body for details about which PDB constraint is being violated.

9. If PDB label selector mismatch is suspected (from Playbook step 10), verify that pods intended to be protected actually match the PDB's selector. Mismatched selectors may cause PDB to protect wrong pods or fail to protect intended pods.

10. If PDB configuration appears correct but violations persist, check for gradual pod health degradation. If `currentHealthy` pods drop below `minAvailable` due to pod failures, `disruptionsAllowed` becomes 0, preventing any voluntary disruptions until pod health is restored.

**If no correlation is found**: Extend analysis to check for PDB configuration changes around the incident time, verify if PDB was recently created or modified, check for namespace-level resource quotas affecting pod creation, examine if pod readiness probe failures are reducing healthy pod count below PDB minimums, review historical PDB status to identify gradual constraint tightening, and verify if multiple workloads sharing nodes are creating cumulative PDB constraints that block node-level operations.

