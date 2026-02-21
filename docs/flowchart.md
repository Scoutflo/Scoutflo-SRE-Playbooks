# Troubleshooting Flowchart

> Follow this decision tree to find the right playbook.

## Start Here

**What type of system is affected?**

```
                    ┌─────────────────┐
                    │  What system?   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │   K8s   │        │   AWS   │        │ Sentry  │
    └────┬────┘        └────┬────┘        └────┬────┘
         │                  │                  │
         ▼                  ▼                  ▼
    See below          See below          See below
```

---

## Kubernetes Flowchart

```
┌──────────────────────────────────────────────────────────────┐
│                    KUBERNETES ISSUE                          │
└────────────────────────────┬─────────────────────────────────┘
                             │
         ┌───────────────────┴───────────────────┐
         │         What is affected?             │
         └───────────────────┬───────────────────┘
                             │
    ┌────────┬───────┬───────┼───────┬───────┬────────┐
    ▼        ▼       ▼       ▼       ▼       ▼        ▼
  Pods   Nodes  Services  Deploy  Storage  RBAC   Cluster
    │        │       │       │       │       │        │
    ▼        ▼       ▼       ▼       ▼       ▼        ▼
```

### Pod Issues

```
Pod not starting?
    │
    ├── Status: Pending ──────► PendingPods playbook
    │                           └── Resource issue? ► Check node capacity
    │                           └── Scheduling? ► Check affinity/taints
    │
    ├── Status: ImagePullBackOff ► ImagePullBackOff playbook
    │                              └── Image exists? ► Check registry
    │                              └── Auth issue? ► Check imagePullSecrets
    │
    ├── Status: CrashLoopBackOff ► CrashLoopBackOff playbook
    │                              └── Check logs with --previous
    │                              └── OOMKilled? ► Increase memory
    │
    └── Status: Terminating ──────► TerminatingPods playbook
                                    └── Stuck? ► Force delete
```

### Service/Network Issues

```
Service not working?
    │
    ├── DNS not resolving ────────► ServiceNotResolvingDNS playbook
    │                               └── CoreDNS running? ► Check CoreDNS
    │
    ├── Connection refused ───────► ServiceNotAccessible playbook
    │                               └── Endpoints empty? ► Check selectors
    │
    └── Ingress returning error ──► IngressNotWorking playbook
                                    └── 502? ► Backend unhealthy
                                    └── 404? ► Check path rules
```

---

## AWS Flowchart

```
┌──────────────────────────────────────────────────────────────┐
│                       AWS ISSUE                              │
└────────────────────────────┬─────────────────────────────────┘
                             │
         ┌───────────────────┴───────────────────┐
         │         What service?                 │
         └───────────────────┬───────────────────┘
                             │
    ┌────────┬───────┬───────┼───────┬───────┬────────┐
    ▼        ▼       ▼       ▼       ▼       ▼        ▼
   EC2   Lambda    RDS      S3     IAM    Network   Other
```

### EC2 Issues

```
EC2 issue?
    │
    ├── Cannot connect ───────────► Connection-Timeout-EC2 playbook
    │                               └── Security groups? ► Check rules
    │                               └── Instance state? ► Check status
    │
    ├── High CPU/Memory ──────────► High-Resource-Usage-EC2 playbook
    │                               └── Scale up? ► Resize instance
    │
    └── Instance terminated ──────► Unexpected-Termination-EC2 playbook
                                    └── Spot instance? ► Check interruption
```

### Lambda Issues

```
Lambda issue?
    │
    ├── Timeout ──────────────────► Lambda-Timeout playbook
    │                               └── Downstream slow? ► Check dependencies
    │
    ├── Memory error ─────────────► Lambda-Memory playbook
    │                               └── Increase memory allocation
    │
    └── Permission denied ────────► Lambda-Permission playbook
                                    └── Check IAM role
```

---

## Sentry Flowchart

```
┌──────────────────────────────────────────────────────────────┐
│                      SENTRY ISSUE                            │
└────────────────────────────┬─────────────────────────────────┘
                             │
         ┌───────────────────┴───────────────────┐
         │         What type of error?           │
         └───────────────────┬───────────────────┘
                             │
    ┌────────────┬───────────┼───────────┬────────────┐
    ▼            ▼           ▼           ▼            ▼
 Exception   Network    Performance   Memory     Release
    │            │           │           │            │
    ▼            ▼           ▼           ▼            ▼
 01-Error   01-Error   02-Performance 01-Error  03-Release
 Tracking   Tracking                  Tracking   Health
```

---

## Quick Decision Matrix

| Symptom | Provider | Category | Playbook |
|---------|----------|----------|----------|
| Pod crashing | K8s | 03-Pods | CrashLoopBackOff |
| Pod pending | K8s | 03-Pods | PendingPods |
| Service unreachable | K8s | 05-Networking | ServiceNotAccessible |
| Node NotReady | K8s | 02-Nodes | NodeNotReady |
| EC2 unreachable | AWS | 01-Compute | Connection-Timeout-EC2 |
| Lambda timeout | AWS | 01-Compute | Lambda-Timeout |
| S3 access denied | AWS | 03-Storage | S3-Access-Denied |
| App exception | Sentry | 01-Error-Tracking | See exception type |

---

[Back to Home](/)
