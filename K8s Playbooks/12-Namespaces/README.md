# Namespaces Playbooks

This folder contains **2 playbooks** for troubleshooting Kubernetes namespace management issues.

## What are Namespaces?

Namespaces are a way to divide cluster resources between multiple users or teams. They provide:
- Resource isolation
- Access control boundaries
- Resource quotas per namespace
- Organization of resources

## Common Issues Covered

- Namespace deletion stuck
- Namespace cannot be deleted
- Namespace management problems

## Playbooks in This Folder

1. `CannotDeleteNamespace-namespace.md` - Cannot delete namespace
2. `NamespaceDeletionStuck-namespace.md` - Namespace deletion stuck

## Quick Start

If you're experiencing namespace issues:

1. **Deletion Problems**: Start with `CannotDeleteNamespace-namespace.md` or `NamespaceDeletionStuck-namespace.md`

## Related Categories

- **09-Resource-Management/**: Resource quota issues in namespaces
- **07-RBAC/**: RBAC issues related to namespaces
- **03-Pods/**: Pod issues within namespaces

## Understanding Playbook Steps

**Important**: These playbooks are designed for **AI agents** using natural language processing. The playbook steps use natural language instructions like:

- "Retrieve namespace `<namespace>` and check namespace status and finalizers"
- "Retrieve all resources in namespace `<namespace>` and verify resources are deleted"
- "Retrieve events in namespace `<namespace>` and check for namespace deletion errors"

AI agents interpret these instructions and execute the appropriate actions using available tools.

### Manual Verification Commands

If you need to manually verify or troubleshoot (outside of AI agent usage), here are equivalent kubectl commands:

**Namespace Operations:**
```bash
# List namespaces
kubectl get namespaces

# Describe namespace
kubectl describe namespace <namespace>

# Check namespace status
kubectl get namespace <namespace> -o yaml
```

**Namespace Resources:**
```bash
# Check resources in namespace
kubectl get all -n <namespace>

# Check namespace resource quota
kubectl get resourcequota -n <namespace>
```

**Namespace Finalizers:**
```bash
# Check finalizers blocking deletion
kubectl get namespace <namespace> -o jsonpath='{.metadata.finalizers}'

# Check namespace deletion status
kubectl get namespace <namespace> -o jsonpath='{.status.phase}'
```

## Best Practices

### Namespace Design
- **Logical Grouping**: Organize resources by application, team, or environment
- **Resource Isolation**: Use namespaces for resource and network isolation
- **Naming Conventions**: Use consistent naming conventions
- **Namespace Quotas**: Set resource quotas per namespace

### Namespace Management
- **RBAC**: Use RBAC to control access to namespaces
- **Network Policies**: Use network policies for namespace isolation
- **Resource Quotas**: Set quotas to prevent resource exhaustion
- **Limit Ranges**: Use limit ranges for default resource limits

### Troubleshooting Tips
- **Check Finalizers**: Finalizers can prevent namespace deletion
- **Check Resources**: Ensure all resources are deleted before namespace deletion
- **Check RBAC**: Verify you have permissions to delete namespace
- **Check Events**: Review events for namespace-related issues
- **Force Deletion**: Only use force deletion as last resort

## Additional Resources

### Official Documentation
- [Kubernetes Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) - Namespace guide
- [Namespace Lifecycle](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#namespaces-and-dns) - Lifecycle details
- [Namespace Operations](https://kubernetes.io/docs/tasks/administer-cluster/namespaces/) - Administration tasks

### Learning Resources
- [Namespace Best Practices](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#when-to-use-multiple-namespaces) - When to use namespaces
- [Multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/) - Multi-tenancy patterns

### Tools & Utilities
- [kubectx & kubens](https://github.com/ahmetb/kubectx) - Context and namespace switching
- [kubectl-ns](https://github.com/ahmetb/kubectx) - Namespace management

### Community Resources
- [Kubernetes Slack #sig-multitenancy](https://slack.k8s.io/) - Multi-tenancy discussions
- [Stack Overflow - Kubernetes Namespaces](https://stackoverflow.com/questions/tagged/kubernetes+namespaces) - Q&A

[Back to Main K8s Playbooks](../README.md)
