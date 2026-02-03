# Frequently Asked Questions (FAQ)

Common questions about using the SRE Playbooks repository.

## General Questions

### What are these playbooks?

These are step-by-step troubleshooting guides for common AWS, Kubernetes, and Sentry issues. Each playbook provides systematic diagnostic steps to help SREs and on-call engineers resolve infrastructure problems faster.

### How many playbooks are there?

- **376 total playbooks**
  - 157 AWS playbooks (organized in 8 categories)
  - 194 Kubernetes playbooks (organized in 13 categories)
  - 25 Sentry playbooks (organized in 3 categories)

### Are these playbooks free to use?

Yes! This is an open-source repository under the MIT License. You can use, modify, and distribute these playbooks freely.

### Can I contribute to these playbooks?

Absolutely! We welcome contributions. See our [Contributing Guide](CONTRIBUTING.md) for details on how to:
- Report bugs
- Improve existing playbooks
- Add new playbooks

## Using the Playbooks

### How do I find the right playbook for my issue?

1. **Identify the service**: Is it AWS, Kubernetes, or Sentry?
2. **Match symptoms**: Look for playbooks with titles matching your issue
3. **Check categories**: Browse the numbered category folders (8 for AWS, 13 for K8s, 3 for Sentry)
4. **Search**: Use GitHub's search or Ctrl+F to find keywords

### What if I can't find a playbook for my issue?

- **Create an issue**: Request a new playbook via [GitHub Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues/new?template=feature_request.md)
- **Contribute**: Create the playbook yourself following our [Contributing Guide](CONTRIBUTING.md)
- **Ask the community**: Post in [GitHub Discussions](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)

### How do I use placeholders in playbooks?

Replace placeholders like `<instance-id>` or `<pod-name>` with your actual resource identifiers:

**Example:**
```
Playbook says: kubectl get pod <pod-name> -n <namespace>
You type: kubectl get pod my-app-pod-123 -n production
```

### Should I follow playbook steps in order?

Yes, generally follow steps sequentially. Steps are ordered from most common to specific causes. However, if you have strong evidence pointing to a specific step, you can jump ahead.

### What is the "Diagnosis" section for?

The Diagnosis section helps you correlate events with failures using time-based analysis. It's useful for:
- Finding root causes
- Identifying when issues started
- Correlating configuration changes with failures

## AWS Playbooks

### Do I need AWS credentials to use AWS playbooks?

Yes, you need appropriate AWS credentials and permissions to execute the diagnostic steps in AWS playbooks.

### Which AWS services are covered?

AWS playbooks are organized into 8 categories covering:
- **Compute**: EC2, Lambda, ECS, EKS, Fargate, Auto Scaling
- **Database**: RDS, DynamoDB
- **Storage**: S3
- **Networking**: VPC, ELB, Route 53, API Gateway, CloudFront
- **Security**: IAM, KMS, GuardDuty, WAF, Shield, Cognito
- **Monitoring**: CloudWatch, CloudTrail, Config, X-Ray
- **CI/CD**: CodePipeline, CodeBuild, CloudFormation
- **Proactive**: Capacity planning, cost optimization, compliance

### Can I use these playbooks in any AWS region?

Yes, but remember to replace `<region>` placeholders with your actual AWS region (e.g., `us-east-1`, `eu-west-1`).

## Kubernetes Playbooks

### Do I need kubectl access to use K8s playbooks?

Yes, you need `kubectl` configured with access to your Kubernetes cluster.

### How are Kubernetes playbooks organized?

K8s playbooks are organized into 13 numbered folders:
- `01-Control-Plane/` - Control plane issues
- `02-Nodes/` - Node problems
- `03-Pods/` - Pod issues (most common)
- `04-Workloads/` - Deployments, StatefulSets, etc.
- `05-Networking/` - Services, Ingress, DNS
- `06-Storage/` - Volumes, PVCs
- `07-RBAC/` - Permissions
- `08-Configuration/` - ConfigMaps, Secrets
- `09-Resource-Management/` - Quotas, limits
- `10-Monitoring-Autoscaling/` - Metrics, HPA
- `11-Installation-Setup/` - Installation issues
- `12-Namespaces/` - Namespace management
- `13-Proactive/` - Proactive monitoring and compliance

### What if my pod is in CrashLoopBackOff?

Start with `03-Pods/CrashLoopBackOff-pod.md`. This is one of the most common issues and has a comprehensive troubleshooting guide.

### How do I know which category my issue belongs to?

- **Pod not starting?** → `03-Pods/`
- **Service not accessible?** → `05-Networking/`
- **Permission denied?** → `07-RBAC/`
- **Volume mount failed?** → `06-Storage/`
- **Deployment not scaling?** → `04-Workloads/`

Each category folder has a README explaining what it covers.

## Technical Questions

### What is MTTR and how do playbooks help?

**MTTR (Mean Time To Recovery)** is the average time to restore a service after an incident. Playbooks help reduce MTTR by providing systematic troubleshooting steps, reducing guesswork and time spent searching for solutions.

### What is correlation analysis?

Correlation analysis helps you find relationships between events (like configuration changes) and symptoms (like service failures) by comparing timestamps. The Diagnosis section in each playbook guides you through this process.

### Can I customize these playbooks for my organization?

Yes! Since they're open-source, you can:
- Fork the repository
- Modify playbooks for your specific environment
- Add organization-specific steps
- Create internal versions

### Do these playbooks work with managed Kubernetes services?

Yes! These playbooks work with:
- **AWS EKS** (Elastic Kubernetes Service)
- **GKE** (Google Kubernetes Engine)
- **AKS** (Azure Kubernetes Service)
- **Self-managed clusters**

Some steps may vary slightly for managed services, but the core troubleshooting approach remains the same.

## Contributing

### How do I report a bug in a playbook?

1. Go to [GitHub Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues/new?template=bug_report.md)
2. Use the bug report template
3. Include the playbook name and what's wrong
4. Tag with appropriate labels

### How do I suggest a new playbook?

1. Check if a similar playbook exists
2. Create a [feature request](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues/new?template=feature_request.md)
3. Describe the issue and why a playbook would help
4. Optionally, create the playbook yourself!

### What makes a good playbook?

A good playbook:
- Follows the standard structure (Title, Meaning, Impact, Playbook, Diagnosis)
- Has 8-10 actionable diagnostic steps
- Uses placeholders for resource identifiers
- Includes correlation analysis in Diagnosis section
- Is clear and easy to follow

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Support

### Where can I get help?

- **GitHub Discussions**: [Ask questions](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)
- **GitHub Issues**: [Report problems](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues)
- **Slack**: [Join our community](https://scoutflo.slack.com)
- **Documentation**: Check the README files in each folder

### How quickly will I get a response?

We aim to respond within:
- **Critical Issues**: 24 hours
- **Bug Reports**: 48 hours
- **Feature Requests**: 1 week
- **Questions**: 2-3 business days

### Can I use these playbooks in production?

Yes, but always:
- Test in non-production first
- Review steps before executing
- Understand what each command does
- Have a rollback plan
- Follow your organization's change management process

## Best Practices

### Should I bookmark specific playbooks?

Yes! Bookmark playbooks for issues you encounter frequently. You can also:
- Clone the repository locally
- Add to your team's runbook collection
- Integrate into your incident response tools

### How often are playbooks updated?

Playbooks are updated:
- When bugs are reported and fixed
- When new best practices emerge
- When community contributions are merged
- Continuously as the project evolves

### Can I share these playbooks with my team?

Absolutely! These are open-source and designed to be shared. You can:
- Share the repository link
- Print specific playbooks
- Integrate into your documentation
- Use in training sessions

---

**Still have questions?** 
- [Open a Discussion](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)
- [Create an Issue](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues)
- [Join Slack](https://scoutflo.slack.com)
