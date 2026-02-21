---
title: Kube DaemonSet Not Ready
weight: 47
categories: [kubernetes, daemonset]
---

# KubeDaemonSetNotReady

## Meaning

DaemonSet pods are not ready on expected nodes (triggering KubeDaemonSetNotReady alerts) because DaemonSet pods are failing to start, crashing, or not passing readiness checks on one or more nodes. DaemonSet status shows fewer ready pods than desired, node-level functionality provided by the DaemonSet is unavailable on affected nodes. This affects cluster functionality depending on what the DaemonSet provides; monitoring, logging, networking, or security features may be missing on affected nodes.

## Impact

KubeDaemonSetNotReady alerts fire; DaemonSet functionality missing on affected nodes; if CNI plugin: networking broken on those nodes; if log collector: logs not collected; if monitoring agent: metrics missing; if security agent: security gaps; node functionality is degraded; newly scheduled pods may fail if they depend on DaemonSet services.

## Playbook

1. Retrieve the DaemonSet `<daemonset-name>` in namespace `<namespace>` and identify how many pods are not ready and on which nodes.

2. Retrieve DaemonSet pods and identify which specific pods are not ready and their status.

3. Retrieve events for the not-ready pods to identify failure reasons.

4. Retrieve logs from failing DaemonSet pods to identify application-level issues.

5. Check node conditions on affected nodes (Ready, MemoryPressure, DiskPressure).

6. Verify DaemonSet tolerations match node taints where pods should run.

7. Check resource requests against node available resources.

## Diagnosis

Categorize pod failures: CrashLoopBackOff indicates application issues, Pending indicates scheduling issues, ImagePullBackOff indicates image issues, using pod status as supporting evidence.

Compare affected nodes with healthy nodes to identify node-specific issues (resources, taints, labels), using node characteristics and pod placement as supporting evidence.

Check if DaemonSet update is in progress and pods are being rolled out, causing temporary not-ready state, using rollout status and update strategy as supporting evidence.

Verify DaemonSet spec changes that may have introduced failures (resource changes, image changes, configuration changes), using DaemonSet revision history as supporting evidence.

Check for node-specific issues like disk pressure or memory pressure that may prevent DaemonSet pod operation, using node conditions as supporting evidence.

If no correlation is found within the specified time windows: check DaemonSet tolerations for new taints, verify image is available on all nodes, review resource constraints, check for PodSecurityPolicy or admission controller blocks, review node-specific configurations.
