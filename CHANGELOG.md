# Changelog

All notable changes to the SRE Playbooks repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 11 new dual-format playbooks completing the contributor starter issues:
  - K8s: KarpenterNodeProvisioningFailed (#7)
  - AWS: SQS Queue Backlog and DLQ Growth (#8), SNS Delivery Failures (#9)
  - Sentry Release Health: CrashFreeRateDropAfterRelease (#10), ReleaseOrDeployMissing (#11)
  - Terraform: RemoteStateAccessDenied, DependencyCycle (#13)
  - New **Azure Playbooks/** category with 4 AKS playbooks (#14): NodePoolNotScaling, ImagePullFailedFromACR, LoadBalancerNotProvisioning, ManagedIdentityAuthorizationFailed
- Verification notes: Terraform commands were run locally; AWS/Azure CLI commands were checked for valid subcommands and flags only (not run against live accounts) - see issue #15 for live verification
- Sentry source-map troubleshooting playbook (minified JavaScript stack traces) — community contribution (#17, @Golden007-prog)

## [2.2.0] - 2026-11-16

### Added
- Lambda Cold Start Optimization proactive playbook (AWS 08-Proactive/01-Capacity-Performance) — community contribution (#5)
- Pod Disruption Budget Violations workload playbook (K8s 04-Workloads) — community contribution (#4)
- Dual-format (NLP + CLI) sections on both new playbooks
- `scripts/check_docs.py`, `scripts/sync_readmes.py`, `scripts/sync_docs.py`: link/listing checks and generators that keep counts and listings in sync; enforced by a new `docs-consistency` CI job

### Changed
- Corrected the Lambda playbook: InitDuration is read from REPORT log lines via Logs Insights (it is not an AWS/Lambda CloudWatch metric); date handling is portable across GNU/macOS
- Total playbooks: 414 → **416** (K8s 233, AWS 158, Sentry 25); refreshed counts and listings across README, ROADMAP, FAQ, CONTRIBUTORS, QUICK_REFERENCE and `docs/`
- Rebuilt `docs/aws/08-proactive.md` and `docs/k8s/13-proactive.md` from the real playbook files (the AWS page listed playbook names that did not exist)
- Rewrote the stale `AWS Playbooks/08-Proactive/README.md`
- Dual-format converter model is now configurable via `CONVERT_MODEL` (default `claude-sonnet-5-5`)
- Dual-format CI check no longer relies on `grep -c || echo 0` output quirks
- Added `AGENTS.md` for coding agents
- **Terraform Playbooks/** (new category, 3 playbooks, tested locally): StateLockStuck, DriftDetected, ProviderAuthenticationFailure
- `docs/using-with-ai-sre.md` ("Using These Playbooks") and a clearer docs search placeholder/depth
- Monthly changelog and PR-review-reminder workflows; review SLA documented in MAINTAINERS.md
- Contributor pipeline: 9 new good-first/help-wanted issues (#7–#15) and a pinned "How to contribute" issue (#16)

### Fixed
- Verified the command-bearing playbooks against a local kind cluster and corrected issues:
  - PodDisruptionBudgetViolations: `kubectl drain --dry-run=server` hangs under a blocking PDB; added `--timeout`
  - ImagePullBackOff: no longer prints decoded registry credentials; node disk check uses `/host`
  - Connection-Timeout-SSH-Issues-EC2: VPC Flow Logs filter used instance ID (flow logs record ENIs); security-group query now handles port ranges and all-traffic rules; AWS Health API notes

## [2.1.0] - 2026-02-21

### Added
- **38 new Kubernetes playbooks** synced from internal repository
  - 01-Control-Plane/ (+6): CertManager playbooks for certificate lifecycle management
    - CertificateExpiringCritical, CertificateExpiringSoon, CertificateNotReady
    - CertManagerACMEOrderFailed, CertManagerControllerHighError, CertManagerDown
  - 02-Nodes/ (+12): NodeExporter playbooks for node-level monitoring
    - NodeClockSkewDetected, NodeDiskIOSaturation, NodeExporterDown
    - NodeFileDescriptorLimit, NodeFilesystemAlmostOutOfSpace, NodeHighCPUUsage
    - NodeHighLoadAverage, NodeHighMemoryUsage, NodeMemoryMajorPagesFaults
    - NodeNetworkReceiveErrors, NodeRAIDDegraded, NodeSystemdServiceFailed
  - 03-Pods/ (+10): Container resource and lifecycle playbooks
    - ContainerHighCPUThrottling, ContainerHighMemoryUsage, ContainerMemoryNearLimit
    - ContainerRestartsFrequent, CPUThrottlingHigh, KubeContainerOOMKilled
    - KubePodContainerWaiting, KubePodFrequentlyRestarting, KubePodImagePullBackOff, KubePodPending
  - 04-Workloads/ (+2): Workload state playbooks
    - KubeDaemonSetNotReady, KubeDeploymentRolloutStuck
  - 05-Networking/ (+8): CoreDNS and NGINX Ingress playbooks
    - CoreDNSDown, CoreDNSLatencyHigh, IngressCertificateExpiring
    - NginxIngress4xxErrorsHigh, NginxIngress5xxErrorsHigh, NginxIngressConfigReloadFailed
    - NginxIngressDown, NginxIngressHighLatency

### Changed
- Updated all K8s folder READMEs with new playbook counts and listings
- Updated main README.md with new statistics

### Statistics
- Total Playbooks: 376 → **414** (+38 new playbooks)
- Kubernetes: 194 → **232** (+38 playbooks)
  - 01-Control-Plane: 18 → 24
  - 02-Nodes: 12 → 24
  - 03-Pods: 31 → 41
  - 04-Workloads: 23 → 25
  - 05-Networking: 19 → 27

## [2.0.0] - 2026-02-03

### Added
- **Sentry Playbooks**: 25 new playbooks for application error tracking
  - 01-Error-Tracking/ (19 playbooks) - Exception handling, error patterns
  - 02-Performance/ (6 playbooks) - Timeout, latency, performance issues
  - 03-Release-Health/ - Release correlation playbooks
- **AWS Proactive Playbooks**: 65 new proactive monitoring playbooks
  - Capacity & Performance planning
  - Security & Compliance auditing
  - Backup & Disaster Recovery verification
  - Cost Optimization analysis
  - Observability coverage gaps
  - Data Integrity checks
  - Operational Readiness assessments
- **K8s Proactive Playbooks**: 56 new proactive monitoring playbooks in 13-Proactive/
  - Same categories as AWS proactive

### Changed
- **AWS Playbooks Reorganized**: Restructured from flat to service-based folders
  - 01-Compute/ (27 playbooks) - EC2, Lambda, ECS, EKS, Fargate
  - 02-Database/ (8 playbooks) - RDS, DynamoDB
  - 03-Storage/ (7 playbooks) - S3
  - 04-Networking/ (17 playbooks) - VPC, ELB, Route53, API Gateway
  - 05-Security/ (16 playbooks) - IAM, KMS, GuardDuty, WAF
  - 06-Monitoring/ (8 playbooks) - CloudTrail, CloudWatch, Config
  - 07-CI-CD/ (9 playbooks) - CodePipeline, CodeBuild, CodeDeploy
  - 08-Proactive/ (65 playbooks) - Proactive monitoring
- **Diagnosis Sections Improved**: All 376 playbooks updated with:
  - Events-first approach (analyze events before timestamps)
  - Conditional logic patterns ("If X, then Y. If inconclusive, then Z.")
  - Early permission checks (RBAC for K8s, IAM for AWS, Release correlation for Sentry)
  - Logical ordering (most likely causes first)
- **K8s Reactive Playbooks**: Updated counts in existing folders

### Statistics
- Total Playbooks: 163 → **376** (+213 new playbooks)
- AWS: 25 → **157** (+132 playbooks)
- Kubernetes: 138 → **194** (+56 playbooks)
- Sentry: 0 → **25** (new provider)

## [1.0.0] - 2026-01-13

### Added
- 25 AWS incident response playbooks
- 138 Kubernetes incident response playbooks
- Organized K8s playbooks into categories:
  - Control Plane (18 playbooks)
  - Nodes (12 playbooks)
  - Pods (31 playbooks)
  - Workloads (23 playbooks)
  - Networking (19 playbooks)
  - Storage (9 playbooks)
  - RBAC (6 playbooks)
  - Configuration (8 playbooks)
  - Resource Management (8 playbooks)
  - Monitoring & Autoscaling (3 playbooks)
  - Installation & Setup (1 playbook)
  - Namespaces (2 playbooks)

### Documentation
- Root README with comprehensive overview
- AWS Playbooks README with complete playbook list
- Kubernetes Playbooks README with categorized structure
- Contribution guidelines
- Maintainer documentation

---

## Types of Changes

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes
