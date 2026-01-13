---
title: Autoscaler Not Adding Nodes - Cluster Autoscaler
weight: 236
categories:
  - kubernetes
  - autoscaler
---

# AutoscalerNotAddingNodes-autoscaler

## Meaning

The cluster autoscaler is failing to provision additional worker nodes even though there are unschedulable or resource-starved pods (potentially triggering KubePodPending or KubeNodeUnschedulable alerts), typically due to autoscaler configuration issues, node group limits, cloud-provider integration problems, or insufficient RBAC permissions. This indicates autoscaler operational failures preventing cluster capacity expansion.

## Impact

New workloads cannot start; pending pods remain unscheduled; deployments fail to scale; services experience capacity constraints and potential unavailability; KubePodPending alerts fire; pods remain in Pending state; cluster capacity cannot expand; autoscaler fails to provision nodes; node group limits may be reached; autoscaler errors appear in logs.

## Playbook

1. Retrieve cluster autoscaler ConfigMap in namespace `kube-system` and verify configuration parameters including scale-down-delay-after-add, max-node-provision-time, min-nodes, max-nodes, and node group settings.

2. List all nodes and check node pool configuration and limits including current node count versus maximum node limits.

3. Retrieve logs from cluster autoscaler pod in namespace `kube-system` and filter for error patterns including "failed to scale", "node group limit reached", "insufficient permissions", or "API rate limit exceeded".

4. List pods in namespace `kube-system` and filter for cluster autoscaler pods to check status and restart count.

5. List pods across all namespaces with status phase Pending and filter for pods that require scaling based on resource requests.

6. Retrieve cluster autoscaler service account and role bindings in namespace `kube-system` to verify RBAC permissions.

7. List PodDisruptionBudget resources across all namespaces to verify if PDBs prevent evictions required for scaling.

## Diagnosis

1. Compare the timestamps when autoscaler failed to add nodes (from autoscaler error logs) with cluster autoscaler configuration change timestamps, and check whether autoscaler failures begin within 1 hour of configuration changes.

2. Compare the autoscaler failure timestamps with node pool limit exhaustion events by checking current node count against maximum node limits, and verify whether failures correlate with reaching node capacity limits at the same time.

3. Compare the autoscaler failure timestamps with RBAC permission change timestamps from service account and role binding modifications, and check whether permission changes occur within 1 hour before autoscaler failures.

4. Compare the autoscaler failure timestamps with cluster autoscaler pod restart timestamps, and check whether autoscaler pod restarts occur within 5 minutes before failures.

5. Compare the autoscaler failure timestamps with pending pod creation timestamps, and verify whether pending pods require scaling by checking pod resource requests against available node capacity.

6. Compare the autoscaler failure timestamps with cluster upgrade or infrastructure change timestamps, and check whether failures start within 1 hour of those activities.

**If no correlation is found within the specified time windows**: Extend the search window (1 hour → 2 hours, 5 minutes → 10 minutes), review autoscaler logs for earlier warning signs, check cloud provider API rate limits and quotas, examine node group configuration for hidden constraints, verify if autoscaler has sufficient permissions to query cloud provider APIs, and check for gradual capacity exhaustion patterns. Autoscaler failures may result from cumulative constraints or cloud provider limitations not immediately visible in cluster events.
