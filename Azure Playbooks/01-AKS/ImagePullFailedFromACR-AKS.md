# AKS Image Pull Failed from ACR

## Meaning

Pods show `ErrImagePull` or `ImagePullBackOff` for an image in Azure Container Registry (ACR) with errors such as "unauthorized: authentication required", "failed to authorize", "401", "not found" or timeouts. The AKS kubelet identity lacks the `AcrPull` role on the registry, the registry is not attached, the image name/tag or registry FQDN is wrong, ACR has network restrictions (firewall, private endpoint, disabled public access) the cluster cannot reach, or an `imagePullSecret` is wrong.

## Impact

New pods and rollouts cannot start, autoscaled capacity is useless, and deployments stall or roll back. Existing pods keep running until they are rescheduled.

## Playbook

### For AI Agents (NLP)

1. Retrieve the failing pod's events in `<namespace>` and extract the exact image reference and error message.
2. Confirm the image name, registry FQDN and tag exist in ACR `<acr-name>` by listing the repository tags.
3. Run the AKS-to-ACR connectivity and authorization check for cluster `<cluster-name>` against `<acr-name>.azurecr.io`.
4. Retrieve the cluster's kubelet identity and check it has the `AcrPull` role assignment scoped to the registry (or a parent scope).
5. Check the registry network settings (public access, firewall rules, private endpoint and DNS) against how the cluster nodes reach it.
6. If the pod uses `imagePullSecrets`, verify the secret exists in the namespace and covers the registry host, without printing credentials.
7. Fix the cause with approval (attach ACR or add the role, correct the image reference, open network access) and confirm the pod pulls the image.

### For DevOps/SREs (CLI)

1. Read the pull error:
   ```bash
   kubectl describe pod <pod-name> -n <namespace> | sed -n '/Events:/,$p'
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].image}{"\n"}'
   ```

2. Confirm the image and tag exist:
   ```bash
   az acr repository show-tags --name <acr-name> --repository <repository> --orderby time_desc --top 10 -o table
   ```

3. Run the built-in AKS-to-ACR check:
   ```bash
   az aks check-acr --name <cluster-name> --resource-group <resource-group> --acr <acr-name>.azurecr.io
   ```

4. Check the kubelet identity's role on the registry:
   ```bash
   KUBELET_ID=$(az aks show --name <cluster-name> --resource-group <resource-group> --query identityProfile.kubeletidentity.objectId -o tsv)
   ACR_ID=$(az acr show --name <acr-name> --query id -o tsv)
   az role assignment list --assignee "$KUBELET_ID" --scope "$ACR_ID" -o table
   ```

5. Check the registry network rules:
   ```bash
   az acr show --name <acr-name> --query '{publicAccess:publicNetworkAccess,firewall:networkRuleSet,sku:sku.name}' -o json
   ```

6. If the secret path is used, list only the registry hosts in the pull secret (never print credentials):
   ```bash
   kubectl get secret <secret-name> -n <namespace> -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d \
     | python3 -c 'import json,sys; print("\n".join(json.load(sys.stdin).get("auths",{})))'
   ```

7. Grant pull access to the cluster (change, needs approval):
   ```bash
   az aks update --name <cluster-name> --resource-group <resource-group> --attach-acr <acr-name>
   ```

## Diagnosis

1. If the repository or tag does not exist in step 2, the image reference is wrong or the build never pushed: fix the manifest or the pipeline.
2. If `check-acr` or the role listing shows no `AcrPull` for the kubelet identity, attach the registry or add the role at the registry scope.
3. If the role exists but pulls still return 401 right after assignment, allow a few minutes for propagation, then restart the pods.
4. If the registry has public access disabled or a firewall without the cluster's egress/subnet, or a private endpoint without working private DNS from the nodes, fix the network path.
5. If the image is in a different tenant or non-ACR registry, an `imagePullSecret` is required; check the secret's registry host and that it is in the pod's namespace.
6. If only some nodes fail, check node-level DNS and outbound connectivity (NSG, firewall, UDR) for those nodes.

Inline references:
- [Authenticate with ACR from AKS](https://learn.microsoft.com/azure/aks/cluster-container-registry-integration)
- [Troubleshoot ACR authentication](https://learn.microsoft.com/azure/container-registry/container-registry-troubleshoot-login)
