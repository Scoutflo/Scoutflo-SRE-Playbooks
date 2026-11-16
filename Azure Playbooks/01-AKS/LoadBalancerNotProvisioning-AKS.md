# AKS LoadBalancer Service Not Provisioning

## Meaning

A Kubernetes `Service` of type `LoadBalancer` (or an ingress controller's service) keeps `EXTERNAL-IP <pending>` and the Azure load balancer or public IP is not created or not attached. The cluster identity lacks permission on the node resource group, subnet or public IP resource group, the subscription has run out of public IP or load balancer quota, an annotation references a missing subnet, public IP or resource group, a static IP is in use elsewhere or in a different region/SKU, or the Azure cloud provider controller is erroring.

## Impact

The service is unreachable from outside the cluster, so new ingress, API endpoints or customer-facing apps cannot go live, and changes to an existing service may leave it half-configured.

## Playbook

### For AI Agents (NLP)

1. Describe the Service `<service-name>` in `<namespace>` and read its events and annotations (internal/external, subnet, static IP, resource group).
2. Read the cloud provider error from the service events (for example quota exceeded, AuthorizationFailed, subnet not found, public IP not found) and record the exact message.
3. Retrieve the cluster's identity and its role assignments, and check it has the needed permissions on the node resource group and, for custom subnet or public IP resource groups, on those scopes.
4. List the load balancers and public IPs in the node resource group `MC_<resource-group>_<cluster-name>_<region>` and see whether partial resources were created.
5. Check regional network quota (public IP addresses, load balancers) for subscription `<subscription-id>` in `<region>`.
6. If a static IP or annotation is used, verify the resource exists, is in the right region/SKU/resource group and is not already attached.
7. Fix the cause with approval (grant the role, free or raise quota, correct the annotation or IP) and confirm the Service receives an external IP.

### For DevOps/SREs (CLI)

1. Read the service state and events:
   ```bash
   kubectl get svc <service-name> -n <namespace> -o wide
   kubectl describe svc <service-name> -n <namespace> | sed -n '/Annotations:/,$p'
   ```

2. Look for provider errors:
   ```bash
   kubectl get events -n <namespace> --field-selector involvedObject.name=<service-name> --sort-by=.lastTimestamp
   ```

3. Check the cluster identity and its roles:
   ```bash
   az aks show --name <cluster-name> --resource-group <resource-group> --query '{identity:identity,nodeRG:nodeResourceGroup}' -o json
   PRINCIPAL=$(az aks show --name <cluster-name> --resource-group <resource-group> --query identity.principalId -o tsv)
   az role assignment list --assignee "$PRINCIPAL" --all -o table
   ```

4. Inspect what exists in the node resource group:
   ```bash
   NODE_RG=$(az aks show --name <cluster-name> --resource-group <resource-group> --query nodeResourceGroup -o tsv)
   az network lb list --resource-group "$NODE_RG" -o table
   az network public-ip list --resource-group "$NODE_RG" -o table
   ```

5. Check network quota in the region:
   ```bash
   az network list-usages --location <region> -o table | grep -i -E "Public IP|Load Balancers"
   ```

6. Grant the cluster identity access to a custom scope (change, needs approval):
   ```bash
   az role assignment create --assignee "$PRINCIPAL" --role "Network Contributor" --scope <subnet-or-resource-group-id>
   ```

## Diagnosis

1. If events show `AuthorizationFailed`, the cluster identity lacks permission on the named scope (often a custom VNet subnet or a public IP in another resource group): add the narrowest role at that scope.
2. If events or usage show quota exhausted for public IPs or load balancers, free unused resources or request a quota increase.
3. If an annotation references a subnet, IP or resource group that does not exist, correct the annotation; for a static IP, make sure it is a Standard SKU IP in the right region and not attached elsewhere.
4. If the node resource group contains a partially created load balancer or orphaned public IPs, the provider may be retrying: fix the underlying error first, then let it reconcile.
5. If no events appear at all, check the cloud-controller-manager or cluster health and that the cluster is not in a failed or upgrading state.
6. If the IP is assigned but traffic fails, the problem moved to NSG rules, health probes or the backend pods rather than provisioning.

Inline references:
- [AKS load balancer](https://learn.microsoft.com/azure/aks/load-balancer-standard)
- [Troubleshoot LoadBalancer service pending](https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/connectivity/troubleshoot-loadbalancer-service-pending-state)
