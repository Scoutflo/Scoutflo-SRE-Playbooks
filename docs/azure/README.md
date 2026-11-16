# Azure Playbooks

> **4 playbooks** for Azure (AKS first). New category, contributions welcome ([issue 14](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/issues/14)).

| Playbook | Description |
|----------|-------------|
| [NodePoolNotScaling](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/Azure%20Playbooks/01-AKS/NodePoolNotScaling-AKS.md) | Pods Pending but the node pool does not scale: autoscaler, max count, quota, pod fit |
| [ImagePullFailedFromACR](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/Azure%20Playbooks/01-AKS/ImagePullFailedFromACR-AKS.md) | ErrImagePull from ACR: AcrPull role, attach, network, image reference |
| [LoadBalancerNotProvisioning](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/Azure%20Playbooks/01-AKS/LoadBalancerNotProvisioning-AKS.md) | Service EXTERNAL-IP pending: identity permissions, quota, annotations, static IP |
| [ManagedIdentityAuthorizationFailed](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/Azure%20Playbooks/01-AKS/ManagedIdentityAuthorizationFailed-AKS.md) | 403 / AuthorizationFailed from pods: workload identity, federated credential, role assignment |
