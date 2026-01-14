# RBAC Playbooks

This folder contains **6 playbooks** for troubleshooting Kubernetes RBAC (Role-Based Access Control) and authorization issues.

## What is RBAC?

RBAC (Role-Based Access Control) is Kubernetes' authorization system that controls who can do what in the cluster. Key components:
- **ServiceAccount**: Identity for processes running in pods
- **Role**: Defines permissions within a namespace
- **ClusterRole**: Defines permissions across the entire cluster
- **RoleBinding**: Grants Role permissions to users/groups
- **ClusterRoleBinding**: Grants ClusterRole permissions cluster-wide

## Common Issues Covered

- Permission denied errors
- ServiceAccount issues
- Role binding problems
- Unauthorized access errors
- API server authorization failures

## Playbooks in This Folder

1. `ClusterRoleBindingMissingPermissions-rbac.md` - ClusterRoleBinding missing permissions
2. `ErrorForbiddenwhenRunningkubectlCommands-rbac.md` - Forbidden errors when running kubectl
3. `ErrorUnauthorizedwhenAccessingAPIServer-rbac.md` - Unauthorized when accessing API server
4. `RBACPermissionDeniedError-rbac.md` - RBAC permission denied errors
5. `ServiceAccountNotFound-rbac.md` - ServiceAccount not found
6. `UnauthorizedErrorWhenAccessingKubernetesAPI-rbac.md` - Unauthorized error accessing API

## Quick Start

If you're experiencing RBAC issues:

1. **Permission Denied**: Start with `RBACPermissionDeniedError-rbac.md` or `ErrorForbiddenwhenRunningkubectlCommands-rbac.md`
2. **ServiceAccount Issues**: See `ServiceAccountNotFound-rbac.md`
3. **Unauthorized Errors**: Check `UnauthorizedErrorWhenAccessingKubernetesAPI-rbac.md` or `ErrorUnauthorizedwhenAccessingAPIServer-rbac.md`
4. **Missing Permissions**: See `ClusterRoleBindingMissingPermissions-rbac.md`

## Related Categories

- **01-Control-Plane/**: API server issues that might appear as RBAC problems
- **03-Pods/**: Pod issues related to ServiceAccount problems
- **08-Configuration/**: ConfigMap/Secret access issues (often RBAC-related)

## Understanding Playbook Steps

**Important**: These playbooks are designed for **AI agents** using natural language processing. The playbook steps use natural language instructions like:

- "Retrieve ServiceAccount `<serviceaccount-name>` in namespace `<namespace>` and verify ServiceAccount exists"
- "Retrieve RoleBinding `<rolebinding-name>` in namespace `<namespace>` and check role binding configuration"
- "Verify permissions for ServiceAccount `<serviceaccount-name>` in namespace `<namespace>`"

AI agents interpret these instructions and execute the appropriate actions using available tools.

### Manual Verification Commands

If you need to manually verify or troubleshoot (outside of AI agent usage), here are equivalent kubectl commands:

**ServiceAccounts:**
```bash
# Check ServiceAccounts
kubectl get serviceaccounts -n <namespace>

# Describe ServiceAccount
kubectl describe serviceaccount <serviceaccount-name> -n <namespace>
```

**Roles and ClusterRoles:**
```bash
# Check Roles
kubectl get roles -n <namespace>

# Check ClusterRoles
kubectl get clusterroles

# Describe Role
kubectl describe role <role-name> -n <namespace>
```

**RoleBindings:**
```bash
# Check RoleBindings
kubectl get rolebindings -n <namespace>

# Describe RoleBinding
kubectl describe rolebinding <rolebinding-name> -n <namespace>
```

**Permission Checking:**
```bash
# Check if current user can perform action
kubectl auth can-i create pods -n <namespace>

# Check permissions for ServiceAccount
kubectl auth can-i --list --as=system:serviceaccount:<namespace>:<serviceaccount-name> -n <namespace>
```

## Best Practices

### RBAC Design
- **Least Privilege**: Grant minimum permissions necessary
- **Role vs ClusterRole**: Use Role for namespace-scoped, ClusterRole for cluster-scoped
- **ServiceAccounts**: Use dedicated ServiceAccounts for each application
- **Resource Names**: Be specific with resource names in rules

### Security Best Practices
- **Avoid Cluster-admin**: Don't use cluster-admin unless absolutely necessary
- **Regular Audits**: Regularly audit RBAC permissions
- **ServiceAccount Tokens**: Rotate ServiceAccount tokens regularly
- **RBAC Policies**: Document RBAC policies and review regularly

### Troubleshooting Tips
- **Check ServiceAccount**: Verify pod is using correct ServiceAccount
- **Verify Bindings**: Check RoleBinding/ClusterRoleBinding exists
- **Test Permissions**: Use `kubectl auth can-i` to test permissions
- **Review Logs**: Check API server logs for authorization failures
- **Check Subjects**: Verify subjects in bindings match users/ServiceAccounts

### Common Patterns
- **Read-only Access**: Create read-only roles for monitoring tools
- **Namespace Admin**: Create namespace-specific admin roles
- **Pod Creator**: Allow users to create pods but not modify other resources
- **Resource Quota Viewer**: Allow viewing resource quotas without modification

## Additional Resources

### Official Documentation
- [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) - RBAC guide
- [ServiceAccounts](https://kubernetes.io/docs/concepts/security/service-accounts/) - ServiceAccount guide
- [Authorization](https://kubernetes.io/docs/reference/access-authn-authz/authorization/) - Authorization overview
- [RBAC API Reference](https://kubernetes.io/docs/reference/kubernetes-api/authorization-resources/role-v1/) - API reference

### Learning Resources
- [RBAC Examples](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-example) - Role examples
- [RBAC Best Practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/) - Best practices guide
- [ServiceAccount Tokens](https://kubernetes.io/docs/concepts/security/service-accounts/#service-account-tokens) - Token management

### Tools & Utilities
- [kubectl-whoami](https://github.com/rajatjindal/kubectl-whoami) - Check current user context
- [rbac-lookup](https://github.com/FairwindsOps/rbac-lookup) - Reverse RBAC lookup
- [kubectl-rbac](https://github.com/alcideio/rbac-tool) - RBAC analysis tool

### Community Resources
- [Kubernetes Slack #sig-auth](https://slack.k8s.io/) - Authentication/authorization discussions
- [Stack Overflow - Kubernetes RBAC](https://stackoverflow.com/questions/tagged/kubernetes+rbac) - Q&A

[Back to Main K8s Playbooks](../README.md)
