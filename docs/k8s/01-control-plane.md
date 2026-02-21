# Kubernetes Control Plane Playbooks

> **24 playbooks** for API Server, etcd, Scheduler, Controller Manager, and CertManager issues.

## API Server Playbooks

| Playbook | Description |
|----------|-------------|
| [API Server High Latency](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/APIServerHighLatency-control-plane.md) | Diagnose API server performance issues |
| [Cannot Access API](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/CannotAccessAPI-control-plane.md) | Troubleshoot API accessibility |
| [Connection Refused](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/ConnectionRefused-control-plane.md) | Fix connection refused errors |
| [Context Deadline Exceeded](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/ContextDeadlineExceeded-control-plane.md) | Resolve timeout issues |
| [Timeout](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/Timeout-control-plane.md) | General API timeout troubleshooting |
| [KubeAPIDown](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeAPIDown-control-plane.md) | API server down alert response |
| [KubeAPIErrorBudgetBurn](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeAPIErrorBudgetBurn-control-plane.md) | Error budget burn rate alert |
| [KubeAPITerminatedRequests](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeAPITerminatedRequests-control-plane.md) | Handle terminated API requests |
| [KubeAggregatedAPIDown](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeAggregatedAPIDown-control-plane.md) | Aggregated API server issues |
| [KubeAggregatedAPIErrors](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeAggregatedAPIErrors-control-plane.md) | Aggregated API error troubleshooting |
| [KubeClientErrors](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeClientErrors-control-plane.md) | Client-side error diagnosis |

## Control Plane Component Playbooks

| Playbook | Description |
|----------|-------------|
| [Control Plane Components Not Starting](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/ControlPlaneComponentsNotStarting-control-plane.md) | Fix control plane startup failures |
| [KubeControllerManagerDown](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeControllerManagerDown-control-plane.md) | Controller manager down alert |
| [KubeSchedulerDown](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeSchedulerDown-control-plane.md) | Scheduler down alert |
| [KubeVersionMismatch](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeVersionMismatch-control-plane.md) | Version skew issues |
| [Upgrade Fails](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/UpgradeFails-control-plane.md) | Cluster upgrade failures |

## Certificate Playbooks

| Playbook | Description |
|----------|-------------|
| [Certificate Expired](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/CertificateExpired-control-plane.md) | Handle expired cluster certificates |
| [KubeClientCertificateExpiration](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/KubeClientCertificateExpiration-control-plane.md) | Client certificate expiration |

## CertManager Playbooks

| Playbook | Description |
|----------|-------------|
| [CertificateExpiringCritical](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/CertificateExpiringCritical-cert.md) | Critical certificate expiration alert |
| [CertificateExpiringSoon](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/CertificateExpiringSoon-cert.md) | Certificate expiring soon warning |
| [CertificateNotReady](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/CertificateNotReady-cert.md) | Certificate not ready state |
| [CertManagerACMEOrderFailed](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/CertManagerACMEOrderFailed-cert.md) | ACME order failures |
| [CertManagerControllerHighError](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/CertManagerControllerHighError-cert.md) | High error rate in cert-manager |
| [CertManagerDown](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/01-Control-Plane/CertManagerDown-cert.md) | cert-manager down alert |

---

[Back to K8s Overview](/k8s/) | [View on GitHub](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/tree/master/K8s%20Playbooks/01-Control-Plane)
