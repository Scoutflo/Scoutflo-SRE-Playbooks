# Configuration Playbooks

This folder contains **6 playbooks** for troubleshooting Kubernetes ConfigMap and Secret access issues.

## What are ConfigMaps and Secrets?

- **ConfigMap**: Stores non-confidential configuration data in key-value pairs. Pods can consume ConfigMaps as environment variables, configuration files, or command-line arguments.
- **Secret**: Stores sensitive information like passwords, tokens, or keys. Similar to ConfigMap but for sensitive data.

## Common Issues Covered

- ConfigMap not found or not accessible
- ConfigMap too large
- Secret access problems
- Pods cannot access ConfigMaps or Secrets
- Configuration not being applied

## Playbooks in This Folder

1. `ConfigMapNotFound-configmap.md` - ConfigMap not found
2. `ConfigMapTooLarge-configmap.md` - ConfigMap exceeds size limit
3. `PodCannotAccessConfigMap-configmap.md` - Pod cannot access ConfigMap
4. `PodCannotAccessSecret-secret.md` - Pod cannot access Secret
5. `PodsCannotPullSecrets-secret.md` - Pods cannot pull Secrets
6. `SecretsNotAccessible-secret.md` - Secrets not accessible

## Quick Start

If you're experiencing configuration issues:

1. **ConfigMap Not Found**: Start with `ConfigMapNotFound-configmap.md`
2. **ConfigMap Access**: See `PodCannotAccessConfigMap-configmap.md`
3. **Secret Access**: Check `PodCannotAccessSecret-secret.md` or `SecretsNotAccessible-secret.md`
4. **Size Issues**: See `ConfigMapTooLarge-configmap.md`

## Related Categories

- **03-Pods/**: Pod issues related to ConfigMap/Secret access
- **07-RBAC/**: Permission issues affecting ConfigMap/Secret access
- **04-Workloads/**: Workload-level configuration issues

## Useful Commands

### ConfigMaps
```bash
# Check ConfigMaps
kubectl get configmaps -n <namespace>
kubectl get cm -n <namespace>  # Short form

# Describe ConfigMap
kubectl describe configmap <configmap-name> -n <namespace>

# View ConfigMap data
kubectl get configmap <configmap-name> -n <namespace> -o yaml

# View specific ConfigMap key
kubectl get configmap <configmap-name> -n <namespace> -o jsonpath='{.data.<key>}'

# Edit ConfigMap
kubectl edit configmap <configmap-name> -n <namespace>

# Create ConfigMap from file
kubectl create configmap <configmap-name> --from-file=<file-path> -n <namespace>

# Create ConfigMap from literal
kubectl create configmap <configmap-name> --from-literal=key=value -n <namespace>
```

### Secrets
```bash
# Check Secrets
kubectl get secrets -n <namespace>

# Describe Secret
kubectl describe secret <secret-name> -n <namespace>

# View Secret data (base64 encoded)
kubectl get secret <secret-name> -n <namespace> -o yaml

# Decode Secret value
kubectl get secret <secret-name> -n <namespace> -o jsonpath='{.data.<key>}' | base64 -d

# Create Secret from file
kubectl create secret generic <secret-name> --from-file=<file-path> -n <namespace>

# Create Secret from literal
kubectl create secret generic <secret-name> --from-literal=key=value -n <namespace>

# Create Secret from env file
kubectl create secret generic <secret-name> --from-env-file=<env-file> -n <namespace>
```

### Pod Configuration
```bash
# Check pod environment variables from ConfigMap
kubectl describe pod <pod-name> -n <namespace> | grep -A 20 "Environment:"

# Check pod environment variables
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].env}'

# Check pod volume mounts for ConfigMap/Secret
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 "Mounts:"

# Check mounted ConfigMap/Secret in pod
kubectl exec <pod-name> -n <namespace> -- ls /path/to/mount

# View ConfigMap/Secret file content in pod
kubectl exec <pod-name> -n <namespace> -- cat /path/to/configmap/file
```

### Configuration Debugging
```bash
# Check which pods use a ConfigMap
kubectl get pods -n <namespace> -o json | jq '.items[] | select(.spec.volumes[]?.configMap.name=="<configmap-name>")'

# Check which pods use a Secret
kubectl get pods -n <namespace> -o json | jq '.items[] | select(.spec.volumes[]?.secret.secretName=="<secret-name>")'

# Check ConfigMap size
kubectl get configmap <configmap-name> -n <namespace> -o json | jq '.data | to_entries | map(.value | length) | add'
```

## Best Practices

### ConfigMap Best Practices
- **Size Limits**: ConfigMaps have a 1MB size limit per ConfigMap
- **Immutable ConfigMaps**: Use immutable ConfigMaps for better performance
- **Data Organization**: Organize related configuration together
- **Version Control**: Store ConfigMap definitions in version control

### Secret Best Practices
- **Encryption at Rest**: Enable encryption at rest for etcd
- **Secret Rotation**: Implement regular secret rotation
- **External Secret Management**: Consider external secret managers (Vault, AWS Secrets Manager)
- **Never Commit Secrets**: Never commit secrets to version control
- **RBAC**: Restrict access to secrets using RBAC

### Configuration Management
- **Environment-specific**: Use different ConfigMaps/Secrets per environment
- **Hot Reloading**: Use volume mounts for hot-reloading configuration
- **Validation**: Validate configuration before applying
- **Documentation**: Document all configuration keys and their purposes

### Troubleshooting Tips
- **Check Mounts**: Verify ConfigMap/Secret is mounted in pod
- **Check Permissions**: Ensure pod has permissions to read ConfigMap/Secret
- **Size Limits**: Verify ConfigMap doesn't exceed 1MB limit
- **Encoding**: Remember Secrets are base64 encoded
- **RBAC**: Check if ServiceAccount has permissions to read ConfigMap/Secret

## Additional Resources

### Official Documentation
- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) - ConfigMap guide
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) - Secret guide
- [Managing Secrets](https://kubernetes.io/docs/tasks/configmap-secret/) - Secret management tasks
- [Immutable ConfigMaps and Secrets](https://kubernetes.io/docs/concepts/configuration/configmap/#immutable-configmaps) - Immutability

### Learning Resources
- [ConfigMap Patterns](https://kubernetes.io/docs/concepts/configuration/configmap/#using-configmaps) - Usage patterns
- [Secret Management](https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets) - Secret usage
- [External Secrets Operator](https://external-secrets.io/) - External secret management

### Tools & Utilities
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) - Encrypted secrets for Git
- [External Secrets Operator](https://external-secrets.io/) - Sync secrets from external systems
- [SOPS](https://github.com/mozilla/sops) - Secrets management tool

### Community Resources
- [Kubernetes Slack #sig-apps](https://slack.k8s.io/) - Application configuration discussions
- [Stack Overflow - Kubernetes ConfigMap](https://stackoverflow.com/questions/tagged/kubernetes+configmap) - Q&A

[Back to Main K8s Playbooks](../README.md)
