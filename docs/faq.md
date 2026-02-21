# Frequently Asked Questions

## General

### What are SRE Playbooks?

SRE Playbooks are step-by-step guides for diagnosing and resolving incidents in production systems. They provide a consistent approach to incident response.

### Who are these playbooks for?

- Site Reliability Engineers (SREs)
- DevOps Engineers
- Platform Engineers
- On-call responders
- AI agents and automation systems

### Why use NLP-friendly language?

These playbooks are designed to be consumed by both humans and AI agents. NLP-friendly language uses action verbs and clear instructions that AI systems can interpret and execute.

### Can I use kubectl commands instead?

Yes! Each playbook step includes a collapsible "CLI Equivalent" section with kubectl/AWS CLI commands for manual troubleshooting.

---

## Using Playbooks

### How do I find the right playbook?

1. **Use Search**: Type keywords in the search box
2. **Browse Categories**: Navigate by provider and category
3. **Quick Reference**: Use the [Quick Reference](/quick-reference) for common issues
4. **Troubleshooting Flowchart**: Follow the decision tree

### What do the placeholders mean?

Placeholders like `<pod-name>` and `<namespace>` should be replaced with your actual values:

| Placeholder | Replace With |
|-------------|--------------|
| `<pod-name>` | Your pod name (e.g., `my-app-xyz123`) |
| `<namespace>` | Your namespace (e.g., `production`) |
| `<instance-id>` | Your EC2 instance ID (e.g., `i-0123456789`) |

### How do I contribute CLI equivalents?

Add a collapsible section after each step:

```markdown
<details>
<summary>CLI Equivalent</summary>

```bash
kubectl get pod <pod-name> -n <namespace>
```

</details>
```

---

## Contributing

### How do I contribute?

See our [Contributing Guide](/contributing). Quick steps:
1. Fork the repository
2. Make changes
3. Submit a pull request

### What's the easiest way to contribute?

Adding CLI equivalents to existing playbooks is the easiest way. Find a playbook without CLI sections and add them!

### Do I need to be an expert?

No! We welcome contributions of all levels:
- Fix typos
- Improve clarity
- Add examples
- Create new playbooks

### How long does PR review take?

Typically 2-3 business days. Maintainers are notified automatically.

---

## Technical

### What's the difference between Playbook and Diagnosis sections?

- **Playbook**: Step-by-step data gathering and investigation
- **Diagnosis**: Conditional logic for root cause analysis based on gathered data

### Why "events-first" approach?

Kubernetes and AWS events contain critical information about what happened. Analyzing events before timestamps ensures you understand the sequence of failures.

### What are cross-domain keywords?

Keywords that help correlate issues across different systems. For example, an `OOMKilled` pod might correlate with a Sentry `OutOfMemoryError`.

---

## Support

### Where can I get help?

- [GitHub Discussions](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions)
- [GitHub Issues](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues)
- Email: support@scoutflo.com

### How do I report a bug?

Open a [GitHub Issue](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/issues/new) with:
- Playbook name
- What's wrong
- Suggested fix (if you have one)

---

[Back to Home](/)
