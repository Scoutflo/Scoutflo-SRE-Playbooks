---
title: Pod Disruption Budget Violations - Workload
weight: 250
categories:
  - kubernetes
  - workload
  - pod-disruption-budget
---

# Pod Disruption Budget Violations - Workload

## Meaning

Pod Disruption Budget (PDB) violations happen when Kubernetes blocks voluntary disruptions because evicting a pod would break the availability guarantees defined in a PodDisruptionBudget. This commonly shows up during node drain operations, cluster autoscaler scale-down, or rolling updates when pods cannot be evicted safely. A typical symptom is that `disruptionsAllowed` is `0` for a PDB protecting the affected workload, so voluntary evictions stall. This is usually caused by an overly strict `minAvailable` / `maxUnavailable`, unhealthy pods reducing `currentHealthy`, or selector issues (PDB selecting the wrong pods or not matching the intended pods). For PDB concepts and behavior, refer to Kubernetes documentation: https://kubernetes.io/docs/tasks/run-application/configure-pdb/

## Impact

Node maintenance can be blocked because draining `<node-name>` hangs or fails when protected pods cannot be evicted without violating the PDB. Rolling updates for `<deployment-name>` / `<statefulset-name>` can stall because the cluster cannot safely remove old pods while preserving the minimum healthy count. Cluster autoscaler may be unable to scale down nodes, which increases cost and can keep workloads on suboptimal or degraded nodes. During incidents, this delays remediation steps like node replacement, OS patching, or rescheduling away from unhealthy hardware.

## Playbook

1. Describe the PodDisruptionBudget `<pdb-name>` in namespace `<namespace>` and note `minAvailable` / `maxUnavailable`, selector, and status fields (`currentHealthy`, `desiredHealthy`, `disruptionsAllowed`).
2. List pods in namespace `<namespace>` that match the PDB selector and identify which pods are `Ready` vs not `Ready`, including restart spikes or readiness probe failures.
3. Retrieve recent events in namespace `<namespace>` and look for eviction/drain messages that mention PDB blocking disruptions, noting timestamps for correlation.
4. If the issue is related to a rollout, check rollout status for `<deployment-name>` or `<statefulset-name>` in namespace `<namespace>` and identify whether it is waiting for pods to become `Ready` or unable to terminate old pods safely.
5. If the issue is related to node maintenance, inspect which pods on `<node-name>` are protected by the PDB and confirm whether draining `<node-name>` would require evicting pods that would reduce healthy replicas below the PDB threshold.
6. Check replica counts for the workload (`replicas`, `readyReplicas`, `availableReplicas`) and confirm whether there are enough replicas to allow at least one voluntary disruption.
7. List all PDBs in namespace `<namespace>` and verify there are no overlapping PDB selectors protecting the same pods with incompatible constraints.
8. If cluster autoscaler scale-down is impacted, review autoscaler events/log messages around the same time window to confirm that PDB constraints are preventing node removal.
9. Validate selector correctness by comparing `spec.selector.matchLabels` of `<pdb-name>` with actual pod labels for the intended workload, and ensure the PDB is protecting the right pods.
10. If disruptions must proceed urgently, coordinate with the service owner to temporarily relax the PDB or increase replicas for the workload so that `disruptionsAllowed` becomes greater than `0`, then re-run the drain/rollout safely.

## Diagnosis

1. If `disruptionsAllowed` is `0` and `currentHealthy` is at the minimum required by `minAvailable`, then the PDB is actively preventing any voluntary evictions until healthy capacity increases.
2. If events show eviction failures at time `T` and a node drain or rollout started at approximately time `T`, then the PDB constraint is the likely blocker for that operation.
3. If the workload has `replicas = N` but only `readyReplicas < N` (or readiness is flapping), then `currentHealthy` drops and the PDB will block disruptions until pod health stabilizes.
4. If draining `<node-name>` is blocked and the protected pods on `<node-name>` match the PDB selector, then the drain is waiting on PDB safety checks and will not proceed without additional healthy replicas elsewhere.
5. If multiple PDBs in `<namespace>` match the same pods and each enforces strict availability, then combined constraints can reduce or eliminate allowed disruptions even if each PDB looks reasonable alone.
6. If selector validation shows the PDB matches unexpected pods (or misses intended pods), then update the selector to target only the correct workload and re-check `disruptionsAllowed`.
7. If autoscaler scale-down messages align with PDB blocking and the pods on candidate nodes are protected, then autoscaler cannot remove the node without violating the PDB, so scale-down will remain blocked.

Inline references:
- Kubernetes PDB documentation: https://kubernetes.io/docs/tasks/run-application/configure-pdb/
- PDB API reference: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-disruption-budget-v1/
- kubectl drain behavior: https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/
- Cluster Autoscaler scale-down concepts: https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler
