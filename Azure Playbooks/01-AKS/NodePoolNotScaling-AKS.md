# AKS Node Pool Not Scaling

## Meaning

Pods stay `Pending` for lack of capacity but the AKS node pool does not add nodes, or nodes are not removed when idle. The cluster autoscaler is disabled for the pool, the pool already reached `maxCount`, the VM size lacks regional quota, the subscription's vCPU or other quota is exhausted, pods cannot fit on any node shape in the pool (selectors, taints, zone constraints), or the autoscaler is blocked or erroring.

## Impact

Workloads cannot start, deployments and autoscaling stall, and capacity-related outages occur during load spikes. If scale-down is blocked, cost rises.

## Playbook

### For AI Agents (NLP)

1. Identify the Pending pods and their scheduling events in `<namespace>`, noting resource requests, node selectors, taints/tolerations and zone constraints.
2. Retrieve the node pool `<nodepool-name>` configuration for cluster `<cluster-name>` in resource group `<resource-group>`: node count, autoscaler enabled, `minCount`, `maxCount`, VM size, zones, provisioning and power state.
3. Read the cluster autoscaler status ConfigMap and recent autoscaler events to see whether it considers the pods unschedulable and why scale-up is skipped or failing.
4. Check regional compute quota for the pool's VM family in region `<region>`, and the subscription's total regional vCPU quota.
5. Check that the pod's requirements can be met by a new node of the pool's VM size (a pod larger than one node can never schedule).
6. Check recent Azure Activity Log or scale operation failures for the node resource group.
7. Recommend the minimal fix (enable autoscaler, raise `maxCount`, request quota, change VM size, relax pod constraints) and apply only after approval; confirm pods schedule afterwards.

### For DevOps/SREs (CLI)

1. Show Pending pods and why:
   ```bash
   kubectl get pods -A --field-selector=status.phase=Pending
   kubectl describe pod <pod-name> -n <namespace> | sed -n '/Events:/,$p'
   ```

2. Show the node pool scaling configuration:
   ```bash
   az aks nodepool show --cluster-name <cluster-name> --resource-group <resource-group> --name <nodepool-name> \
     --query '{count:count,autoscale:enableAutoScaling,min:minCount,max:maxCount,vmSize:vmSize,zones:availabilityZones,state:provisioningState,power:powerState.code}' -o json
   ```

3. Read the autoscaler's view of the cluster:
   ```bash
   kubectl -n kube-system get configmap cluster-autoscaler-status -o yaml
   kubectl get events -A --field-selector reason=NotTriggerScaleUp --sort-by=.lastTimestamp | tail
   ```

4. Check regional quota:
   ```bash
   az vm list-usage --location <region> -o table | grep -i -E "Total Regional vCPUs|<vm-family>"
   ```

5. Raise limits or enable the autoscaler (change, needs approval):
   ```bash
   az aks nodepool update --cluster-name <cluster-name> --resource-group <resource-group> --name <nodepool-name> \
     --enable-cluster-autoscaler --min-count <min> --max-count <max>
   ```

## Diagnosis

1. If `autoscale` is false, the pool never scales automatically: enable the autoscaler or scale manually.
2. If `count` equals `max`, the pool is capped: raise `maxCount` if the budget allows.
3. If the autoscaler status or `NotTriggerScaleUp` events say pods do not fit or no node group can host them, the pod requests, selectors or taints are the problem, not the pool size.
4. If quota usage for the VM family or regional vCPUs is at the limit, request a quota increase or use another VM size/region.
5. If scale-up was triggered but nodes fail to appear, check the Activity Log for VMSS errors (allocation failure, SKU unavailable in zone) and try another zone or VM size.
6. If only scale-down is wrong, look for pods with local storage, PDBs or annotations that block eviction.
7. If `state` is `Failed` or the pool is stopped, repair or restart the pool before anything else.

Inline references:
- [AKS cluster autoscaler](https://learn.microsoft.com/azure/aks/cluster-autoscaler)
- [Troubleshoot autoscaler](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/availability-performance/cluster-autoscaler-fails-to-scale)
