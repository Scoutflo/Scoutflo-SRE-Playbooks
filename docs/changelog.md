# Changelog

All notable changes to the SRE Playbooks repository.

## [2.2.0] - 2026-11-16

- Added community playbooks: Lambda Cold Start Optimization (AWS) and Pod Disruption Budget Violations (K8s), both dual-format
- Total playbooks: 414 → **416**; refreshed counts and listings across the docs
- Added Terraform Playbooks (3), "Using These Playbooks" page, and fixes to command accuracy (PDB drain timeout, no credential printing in ImagePullBackOff, VPC Flow Logs filter)
- Added docs consistency checks and generators (`scripts/check_docs.py`, `sync_readmes.py`, `sync_docs.py`)

## [2.1.0] - 2026-02-21

### Added
- **38 new Kubernetes playbooks** synced from internal repository
  - 01-Control-Plane (+6): CertManager playbooks
  - 02-Nodes (+12): NodeExporter playbooks
  - 03-Pods (+10): Container resource playbooks
  - 04-Workloads (+2): DaemonSet and Deployment playbooks
  - 05-Networking (+8): CoreDNS and NGINX Ingress playbooks

### Statistics
- Total Playbooks: 376 → **414** (+38)
- Kubernetes: 194 → **232** (+38)

---

## [2.0.0] - 2026-02-03

### Added
- **Sentry Playbooks**: 25 new playbooks for application error tracking
  - 01-Error-Tracking (19 playbooks)
  - 02-Performance (6 playbooks)
- **AWS Proactive Playbooks**: 65 new proactive monitoring playbooks
- **K8s Proactive Playbooks**: 56 new proactive monitoring playbooks

### Changed
- **AWS Playbooks Reorganized**: From flat to 8 service-based folders
- **Diagnosis Sections Improved**: All playbooks updated with:
  - Events-first approach
  - Conditional logic patterns
  - Early permission checks
  - Logical ordering

### Statistics
- Total: 163 → **376** (+213)
- AWS: 25 → **157** (+132)
- K8s: 138 → **194** (+56)
- Sentry: 0 → **25** (new)

---

## [1.0.0] - 2026-01-13

### Added
- Initial release with 163 playbooks
- 25 AWS incident response playbooks
- 138 Kubernetes incident response playbooks
- Comprehensive documentation

---

[View full changelog on GitHub](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/CHANGELOG.md)

[Back to Home](/)
