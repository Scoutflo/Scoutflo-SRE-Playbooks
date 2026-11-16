# AKS Managed Identity / RBAC Authorization Failed

## Meaning

A workload in AKS or the cluster itself calls an Azure API and gets `AuthorizationFailed`, `403`, `AADSTS` errors, `ManagedIdentityCredential authentication failed` or `No Azure credential available`. The identity (workload identity, kubelet identity or cluster identity) lacks the required role assignment at the right scope, the federated credential does not match the service account/issuer/subject, the pod is missing the workload identity label or service account annotation, or the OIDC issuer/workload identity features are not enabled.

## Impact

Applications cannot read secrets from Key Vault, access storage or databases, or call other Azure services, causing application errors and failed deployments. Granting overly broad roles as a quick fix creates a security risk.

## Playbook

### For AI Agents (NLP)

1. Capture the exact error (error code, resource ID, action, and identity object/client ID if shown) from the pod logs of `<pod-name>` in `<namespace>`.
2. Determine which identity the workload is meant to use: workload identity (service account `<service-account>`), kubelet identity, or cluster identity.
3. For workload identity, verify the cluster has the OIDC issuer and workload identity enabled, the pod has the label `azure.workload.identity/use: "true"`, and the service account carries the `azure.workload.identity/client-id` annotation.
4. List the federated credentials of the user-assigned identity and confirm the issuer, subject (`system:serviceaccount:<namespace>:<service-account>`) and audience match the cluster and service account exactly.
5. List the identity's role assignments and check a role granting the failing action exists at the scope of the target resource (or a parent scope).
6. Check whether a recent role assignment was just created (propagation can take minutes) or removed, using the Activity Log.
7. Fix the narrowest cause with approval (correct the annotation or federated credential, add a scoped role) and verify by restarting the pod and retrying the call.

### For DevOps/SREs (CLI)

1. Read the error from the pod:
   ```bash
   kubectl logs <pod-name> -n <namespace> --tail=100 | grep -i -E "authorizationfailed|403|aadsts|credential|identity"
   ```

2. Check workload identity prerequisites on the cluster:
   ```bash
   az aks show --name <cluster-name> --resource-group <resource-group> \
     --query '{oidcEnabled:oidcIssuerProfile.enabled,issuer:oidcIssuerProfile.issuerUrl,workloadIdentity:securityProfile.workloadIdentity.enabled}' -o json
   ```

3. Check the service account and pod configuration:
   ```bash
   kubectl get sa <service-account> -n <namespace> -o jsonpath='{.metadata.annotations}{"\n"}'
   kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.metadata.labels.azure\.workload\.identity/use}{"\n"}'
   ```

4. Check the federated credential matches:
   ```bash
   az identity federated-credential list --identity-name <identity-name> --resource-group <identity-resource-group> \
     --query '[].{name:name,issuer:issuer,subject:subject,audiences:audiences}' -o json
   ```

5. List the identity's role assignments:
   ```bash
   PRINCIPAL=$(az identity show --name <identity-name> --resource-group <identity-resource-group> --query principalId -o tsv)
   az role assignment list --assignee "$PRINCIPAL" --all -o table
   ```

6. Add the narrowest needed role at the target resource scope (change, needs approval):
   ```bash
   az role assignment create --assignee-object-id "$PRINCIPAL" --assignee-principal-type ServicePrincipal \
     --role "<role-name>" --scope <target-resource-id>
   ```

## Diagnosis

1. If `oidcEnabled` or `workloadIdentity` is false, enable them on the cluster (a change) and re-create the pods.
2. If the pod lacks the `azure.workload.identity/use` label or the service account lacks the client-id annotation, the webhook does not inject the token: fix the manifests.
3. If the federated credential issuer or subject does not exactly match the cluster issuer URL and `system:serviceaccount:<namespace>:<service-account>`, correct it; a one-character mismatch fails with AADSTS70021-style errors.
4. If the identity authenticates (no AADSTS error) but the call returns AuthorizationFailed, a role assignment is missing or at the wrong scope: add the narrowest built-in role that covers the failing action.
5. If the role was assigned minutes ago, wait for propagation and retry before changing anything else.
6. If Key Vault is involved and uses access policies instead of RBAC (or vice versa), grant access using the vault's actual authorization model.
7. Avoid fixing by assigning Owner/Contributor at subscription scope; use the least privilege role instead.

Inline references:
- [AKS workload identity](https://learn.microsoft.com/azure/aks/workload-identity-overview)
- [Troubleshoot workload identity](https://learn.microsoft.com/azure/aks/workload-identity-deploy-cluster)
