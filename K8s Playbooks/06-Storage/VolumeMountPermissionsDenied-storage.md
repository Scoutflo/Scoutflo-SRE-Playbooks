---
title: Volume Mount Permissions Denied - Storage
weight: 247
categories:
  - kubernetes
  - storage
---

# VolumeMountPermissionsDenied-storage

## Meaning

Containers cannot access mounted volumes due to permission issues (triggering KubePodCrashLooping or KubePodNotReady alerts) because the volume has incorrect file permissions on the storage backend, the container's security context runAsUser does not match volume ownership, or the filesystem group ID (fsGroup) in pod security context is not set correctly. Pods show permission denied errors in logs, pod events show FailedMount errors with permission issues, and PersistentVolumeClaim resources may show access problems. This affects the storage plane and prevents applications from accessing persistent data, typically caused by security context mismatches or volume permission issues; applications fail to access persistent data and may show errors.

## Impact

Containers cannot read or write to volumes; volume mount permissions are denied; applications fail to access persistent data; pods start but applications crash with permission denied errors; KubePodCrashLooping alerts fire when containers restart due to permission failures; KubePodNotReady alerts fire when pods cannot access required volumes; file permission errors occur in pod logs; database pods cannot access data directories; log collection fails; persistent storage is inaccessible; pod events show permission denied errors. Pods show permission denied errors in logs indefinitely; pod events show FailedMount errors; applications fail to access persistent data and may experience errors or performance degradation; persistent storage is inaccessible.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to inspect pod security context, container security context, user ID (runAsUser), group ID (fsGroup), and volume mount configurations.

2. Retrieve events for pod <pod-name> in namespace <namespace> sorted by timestamp to identify FailedMount errors or permission-related issues.

3. Retrieve logs from pod <pod-name> in namespace <namespace> and filter for permission denied errors, access denied messages, or filesystem permission failures.

4. Describe PersistentVolumeClaim <pvc-name> in namespace <namespace> to inspect the PVC status and verify volume ownership settings.

5. Describe PersistentVolume <pv-name> to inspect the volume status and verify permissions on the storage backend.

6. Execute a directory listing on the mounted volume path from pod <pod-name> to check file permissions and ownership.

7. Describe Deployment <deployment-name> in namespace <namespace> and review security context configuration in the pod template to verify fsGroup and runAsUser settings.

## Diagnosis

1. Analyze pod events from Playbook step 2 to identify the specific permission error type. Events showing "FailedMount" with permission-related messages indicate the exact failure point. If the error mentions "permission denied" on a specific path, the issue is filesystem-level; if it mentions "operation not permitted", the issue is security context-related.

2. If events indicate FailedMount errors, examine the pod logs from Playbook step 3 for the specific permission denied message. The error path and operation (read/write/execute) will indicate whether the issue is:
   - File ownership mismatch (check runAsUser from step 1 against volume permissions from step 6)
   - Group permission mismatch (check fsGroup from step 1 against volume group ownership from step 6)
   - SELinux or seccomp restrictions (security context from step 1/7)

3. If pod security context from Playbook step 1 shows runAsUser or fsGroup settings, compare these values against the actual file ownership from step 6. A mismatch between container UID/GID and volume ownership is the most common cause of permission denied errors.

4. If security context appears correct, check the PVC and PV status from Playbook steps 4-5. If the volume was recently provisioned or migrated, default permissions from the storage backend may not match application requirements.

5. If the deployment security context from Playbook step 7 differs from the running pod (step 1), a recent deployment rollout likely introduced the permission mismatch. Correlate deployment timestamps with when permission errors first appeared in events.

6. If all security contexts appear consistent, the issue may be at the storage backend level. Check if the PV storage backend (from step 5) has its own permission model that overrides Kubernetes fsGroup settings.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review pod logs for gradual permission issues, check for intermittent filesystem permission problems, examine if security context configurations drifted over time, verify if volume ownership changed gradually, and check for storage backend permission changes that may have accumulated. Volume permission issues may result from gradual security context or storage configuration drift rather than immediate changes.

