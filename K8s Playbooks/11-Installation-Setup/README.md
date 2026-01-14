# Installation & Setup Playbooks

This folder contains **1 playbook** for troubleshooting Kubernetes installation and setup issues.

## What is Installation & Setup?

This category covers issues related to:
- Kubernetes cluster installation
- Helm chart installations
- Add-on installations
- Setup and configuration problems

## Common Issues Covered

- Helm release stuck
- Installation failures
- Setup configuration issues

## Playbooks in This Folder

1. `HelmReleaseStuckInPending-install.md` - Helm release stuck in pending state

## Quick Start

If you're experiencing installation issues:

1. **Helm Issues**: Start with `HelmReleaseStuckInPending-install.md`

## Related Categories

- **01-Control-Plane/**: Control plane issues affecting installations
- **03-Pods/**: Pod issues related to installed applications
- **04-Workloads/**: Workload issues from installations

## Understanding Playbook Steps

**Important**: These playbooks are designed for **AI agents** using natural language processing. The playbook steps use natural language instructions like:

- "Retrieve Helm release `<release-name>` in namespace `<namespace>` and check release status and resources"
- "Retrieve pods in namespace `<namespace>` with label matching Helm release and verify pod status"
- "Retrieve events in namespace `<namespace>` and filter for Helm release-related errors"

AI agents interpret these instructions and execute the appropriate actions using available tools (like Helm MCP tools or Kubernetes MCP tools).

### Manual Verification Commands

If you need to manually verify or troubleshoot (outside of AI agent usage), here are equivalent Helm and kubectl commands:

**Helm Operations:**
```bash
# Check Helm releases
helm list -n <namespace>

# Check Helm release status
helm status <release-name> -n <namespace>

# Check Helm release history
helm history <release-name> -n <namespace>
```

**Installation Debugging:**
```bash
# Check installed resources
kubectl get all -n <namespace>

# Check Helm pods
kubectl get pods -n <namespace> | grep <release-name>

# Check Helm release events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

## Best Practices

### Installation Best Practices
- **Dry Run First**: Always use `--dry-run` before installing
- **Version Pinning**: Pin chart versions for reproducibility
- **Namespace Isolation**: Install in dedicated namespaces
- **Resource Limits**: Set resource limits for installed components

### Helm Best Practices
- **Chart Versioning**: Use semantic versioning for charts
- **Values Management**: Use values files for different environments
- **Release Naming**: Use consistent naming conventions
- **Backup**: Backup Helm releases before upgrades

### Troubleshooting Tips
- **Check Release Status**: Use `helm status` to see release state
- **Review History**: Check `helm history` for previous installations
- **Check Events**: Review Kubernetes events for installation issues
- **Verify Resources**: Ensure all required resources are created
- **Check Dependencies**: Verify chart dependencies are met

## Additional Resources

### Official Documentation
- [Helm Documentation](https://helm.sh/docs/) - Complete Helm guide
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/) - Chart best practices
- [Kubernetes Installation](https://kubernetes.io/docs/setup/) - Installation guide
- [Helm Release Management](https://helm.sh/docs/intro/using_helm/) - Release management

### Learning Resources
- [Helm Tutorial](https://helm.sh/docs/intro/quickstart/) - Quick start guide
- [Chart Development](https://helm.sh/docs/topics/charts/) - Creating charts
- [Helm Plugins](https://helm.sh/docs/topics/plugins/) - Extending Helm

### Tools & Utilities
- [Helmfile](https://helmfile.readthedocs.io/) - Declarative Helm deployments
- [Helm Secrets](https://github.com/jkroepke/helm-secrets) - Secret management for Helm
- [Helm Diff](https://github.com/databus23/helm-diff) - Preview changes

### Community Resources
- [Helm GitHub](https://github.com/helm/helm) - Helm source code
- [Helm Slack](https://slack.helm.sh/) - Helm community
- [Stack Overflow - Helm](https://stackoverflow.com/questions/tagged/helm) - Q&A

[Back to Main K8s Playbooks](../README.md)
