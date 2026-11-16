# Roadmap

This document outlines the planned development and future direction of the SRE Playbooks repository.

## Vision

To become the most comprehensive, community-driven collection of SRE incident response playbooks, helping engineers worldwide resolve infrastructure issues faster and more systematically.

## Current Status (v2.1.0 + Unreleased)

- **431 Playbooks**: 160 AWS + 234 Kubernetes + 28 Sentry + 5 Terraform + 4 Azure
- **Structured Format**: All playbooks follow 4-section structure (Meaning, Impact, Playbook, Diagnosis)
- **Events-First Diagnosis**: Correlation analysis with conditional logic patterns
- **Proactive Monitoring**: 122 proactive playbooks for capacity planning and compliance
- **Dual-Format (NLP + CLI)**: 20 of 431 playbooks dual-format; converter and validator in `scripts/` (in progress)
- **CI**: structure validation, placeholder check, dual-format report and docs-consistency checks run on every PR

---

## Short-Term Goals (Q1 2026)

### New Playbooks
- [ ] Azure playbooks (target: 50+ playbooks)
- [ ] GCP playbooks (target: 50+ playbooks)
- [ ] Terraform/IaC playbooks (target: 20+ playbooks; 5 so far)
- [ ] Additional Sentry playbooks for Release Health category

### Platform Improvements
- [x] Automated playbook structure validation (CI/CD)
- [x] Broken link detection workflow
- [ ] Search functionality improvements
- [ ] Interactive troubleshooting flowcharts

### Community Building
- [ ] First-time contributor onboarding guide
- [ ] Monthly community office hours
- [ ] Contributor recognition program
- [ ] Video tutorial series

---

## Medium-Term Goals (Q2-Q3 2026)

### Multi-Cloud Expansion
- [ ] Complete Azure coverage (100+ playbooks)
- [ ] Complete GCP coverage (100+ playbooks)
- [ ] Multi-cloud comparison guides
- [ ] Cross-platform incident correlation

### Enhanced Tooling
- [ ] Playbook search API
- [ ] CLI tool for quick playbook access
- [ ] IDE extensions (VS Code, JetBrains)
- [ ] Slack/Teams bot integration

### Quality Improvements
- [ ] Playbook effectiveness metrics
- [ ] Community feedback ratings
- [ ] Version history for each playbook
- [ ] Automated testing for playbook accuracy

---

## Long-Term Goals (2027+)

### AI-Powered Features
- [ ] AI-assisted playbook recommendations
- [ ] Automated root cause suggestions
- [ ] Natural language playbook search
- [ ] Incident pattern recognition

### Enterprise Features
- [ ] Custom playbook templates
- [ ] Team collaboration features
- [ ] Integration with popular incident management tools
- [ ] Compliance and audit trails

### Ecosystem Growth
- [ ] Partner integrations
- [ ] Certification program
- [ ] SRE training curriculum
- [ ] Annual SRE community conference

---

## How to Contribute to the Roadmap

We welcome community input on our roadmap!

### Suggest Features
1. Check [existing discussions](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/discussions/categories/ideas-suggestions)
2. Create a new discussion with your idea
3. Vote on features you'd like to see

### Contribute Directly
1. Pick an item from the roadmap
2. Comment on the related issue to claim it
3. Submit a PR following our [contribution guidelines](CONTRIBUTING.md)

### Priority Requests
For enterprise or priority feature requests, contact us:
- Email: support@scoutflo.com
- Slack: [scoutflo.slack.com](https://scoutflo.slack.com)

---

## Release History

| Version | Date | Highlights |
|---------|------|------------|
| v2.2.0 | 2026-11-16 | Community playbooks (Lambda cold start, PDB), Terraform category, accuracy fixes, docs consistency checks |
| v2.1.0 | 2026-02-21 | 38 new K8s playbooks (CertManager, NodeExporter, containers, CoreDNS, NGINX Ingress) |
| v2.0.0 | 2026-02-03 | Added Sentry playbooks, AWS restructured, proactive monitoring |
| v1.0.0 | 2026-01-13 | Initial release with 163 playbooks (AWS + K8s) |

---

## Stay Updated

- **Watch this repo**: Get notifications for new releases
- **Star the repo**: Show your support
- **Join Slack**: [scoutflo.slack.com](https://scoutflo.slack.com)
- **Follow on Twitter**: [@scout_flo](https://x.com/scout_flo)

---

*Last updated: February 2026*
