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

1. Describe the cluster autoscaler deployment in namespace `kube-system` to inspect its status, configuration, and events.

2. Retrieve events in namespace `kube-system` sorted by timestamp to identify autoscaler-related events and scaling failures.

3. Retrieve cluster autoscaler ConfigMap in namespace `kube-system` and verify configuration parameters including scale-down-delay-after-add, max-node-provision-time, min-nodes, max-nodes, and node group settings.

4. List all nodes and check node pool configuration and limits including current node count versus maximum node limits.

5. Retrieve logs from cluster autoscaler pod in namespace `kube-system` and filter for error patterns including "failed to scale", "node group limit reached", "insufficient permissions", or "API rate limit exceeded".

6. List pods across all namespaces with status phase Pending and filter for pods that require scaling based on resource requests.

7. Retrieve cluster autoscaler service account and role bindings in namespace `kube-system` to verify RBAC permissions.

8. List PodDisruptionBudget resources across all namespaces to verify if PDBs prevent evictions required for scaling.

## Diagnosis

1. Analyze cluster autoscaler events and logs from Playbook to identify why nodes are not being added. Events showing "ScaleUpFailed" or error messages indicate the specific blocker. Common messages include "node group limit reached", "failed to create node", or "no available node groups".

2. If events indicate node group limit reached, compare current node count with maximum node limits from Playbook. The autoscaler cannot add nodes beyond the configured maximum for each node group. This is a configuration limit, not a failure.

3. If events indicate cloud provider errors (API failures, quota exceeded, instance type unavailable), the autoscaler is attempting to add nodes but the cloud provider is rejecting requests. Check cloud provider quotas, regional capacity, and instance type availability.

4. If events indicate no schedulable node groups, verify that pending pods' requirements (node selectors, tolerations, resource requests) can be satisfied by at least one node group. The autoscaler will not scale a node group if pending pods cannot schedule there.

5. If autoscaler logs show permission errors (forbidden, access denied), verify RBAC permissions from Playbook. The autoscaler service account needs permissions to create nodes, read node groups, and interact with cloud provider APIs.

6. If pending pods exist but autoscaler shows no scale-up activity, check if pods have scheduling constraints that exclude all node groups. Also verify that pending pods are not owned by DaemonSets (which do not trigger autoscaling).

7. If autoscaler pod is not running or is restarting, check autoscaler deployment status and pod logs. The autoscaler cannot add nodes if the autoscaler controller itself is unhealthy.
