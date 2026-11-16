# Karpenter Node Provisioning Failed

## Meaning

Pods stay `Pending` (event `FailedScheduling`, often "no nodes available" or "Insufficient cpu/memory") and Karpenter does not bring up a node for them. Karpenter either never creates a `NodeClaim`, creates one that stays `Unknown`/not `Launched`, or the instance launches but never registers as a node. Common causes: no `NodePool` matches the pod's requirements (instance types, architecture, zone, taints/tolerations), NodePool `limits` reached, EC2 `InsufficientInstanceCapacity` or quota (vCPU) errors, an `EC2NodeClass` whose subnet or security-group selectors match nothing, missing IAM permissions for the Karpenter controller or the node role, or a bad AMI/user-data so the node never joins.

## Impact

New or rescheduled workloads cannot start, autoscaling stops working, and rollouts or recoveries stall. During traffic spikes this turns into capacity-related outages even though the cluster looks healthy.

## Playbook

### For AI Agents (NLP)

1. Identify the Pending pods for `<namespace>` and read their `FailedScheduling` events, noting the node selectors, affinities, tolerations, topology constraints and resource requests.
2. Check whether the Karpenter controller is running and healthy in namespace `<karpenter-namespace>`, and read its recent logs for provisioning errors for those pods.
3. List the `NodePool` objects and verify at least one matches the pod's requirements (instance family/size, architecture, capacity type, zones, taints) and that its `limits` are not exhausted.
4. List `NodeClaim` objects: for any claim not `Ready`, describe it and read the status conditions (Launched, Registered, Initialized) to see which stage failed.
5. Inspect the `EC2NodeClass` referenced by the NodePool and confirm subnet selectors, security-group selectors, AMI selector and instance profile/role resolve to real resources.
6. If the claim failed at launch, read the EC2 error in the controller logs or `NodeClaim` status (for example InsufficientInstanceCapacity, VcpuLimitExceeded, UnauthorizedOperation) and check the account's service quotas.
7. If the instance launched but never registered, check node bootstrap and the node IAM role/aws-auth or access entry mapping.
8. Recommend the minimal fix (widen NodePool requirements, raise limits, correct selectors/IAM, request quota) and apply it only after approval, then confirm the pods schedule.

### For DevOps/SREs (CLI)

1. Show Pending pods and why they are not scheduling:
   ```bash
   kubectl get pods -A --field-selector=status.phase=Pending
   kubectl describe pod <pod-name> -n <namespace> | sed -n '/Events:/,$p'
   ```

2. Check the Karpenter controller and its logs:
   ```bash
   kubectl get pods -n <karpenter-namespace> -l app.kubernetes.io/name=karpenter
   kubectl logs -n <karpenter-namespace> -l app.kubernetes.io/name=karpenter --since=30m | grep -i -E "error|fail|insufficient|unauthorized|could not|no instance type"
   ```

3. Inspect NodePools, including limits and usage:
   ```bash
   kubectl get nodepools
   kubectl describe nodepool <nodepool-name>
   ```

4. Inspect NodeClaims and their conditions:
   ```bash
   kubectl get nodeclaims -o wide
   kubectl describe nodeclaim <nodeclaim-name>
   ```

5. Inspect the EC2NodeClass selectors and resolved resources:
   ```bash
   kubectl get ec2nodeclass
   kubectl describe ec2nodeclass <nodeclass-name>
   ```

6. Check EC2 vCPU quota (use the AWS profile and region for this cluster):
   ```bash
   aws service-quotas get-service-quota --service-code ec2 --quota-code L-1216C47A \
     --profile <profile> --region <region> --query 'Quota.Value'
   ```

7. Check that nodes registered (or why not):
   ```bash
   kubectl get nodes -L karpenter.sh/nodepool,node.kubernetes.io/instance-type
   kubectl get events -A --field-selector reason=FailedScheduling --sort-by=.lastTimestamp | tail -20
   ```

## Diagnosis

1. If no `NodeClaim` is created and the controller logs say no instance type satisfies the pod's requirements, the pod's selectors/resources do not match any NodePool: relax the requirements or widen the NodePool.
2. If the NodePool shows usage at its `limits`, Karpenter will not provision more: raise the limit or free capacity.
3. If a `NodeClaim` exists but never becomes `Launched` and logs show `InsufficientInstanceCapacity`, allow more instance types, zones or the other capacity type; if logs show `VcpuLimitExceeded`, request a quota increase.
4. If logs show `UnauthorizedOperation` or access denied, fix the Karpenter controller IAM permissions; if the claim is `Launched` but not `Registered`, check the node role mapping and bootstrap (AMI, user data, security groups).
5. If the `EC2NodeClass` status shows no subnets or security groups resolved, correct the selector tags.
6. If pods are Pending only for a specific zone or volume, check topology and PVC zone affinity: Karpenter must launch in the volume's zone.
7. If the controller is not running or crash-looping, fix that first; nothing else will provision.

Inline references:
- [Karpenter troubleshooting](https://karpenter.sh/docs/troubleshooting/)
- [NodePools](https://karpenter.sh/docs/concepts/nodepools/)
