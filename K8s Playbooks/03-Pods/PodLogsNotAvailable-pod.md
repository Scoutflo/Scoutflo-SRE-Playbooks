---
title: Pod Logs Not Available - Pod
weight: 267
categories:
  - kubernetes
  - pod
---

# PodLogsNotAvailable-pod

## Meaning

Pod logs are not accessible (typically detected via monitoring gaps or log collection system failures rather than standard Prometheus alerts) because the container runtime (containerd, Docker) is not logging, log files are not being created on nodes, log collection systems are failing, or the logging driver is misconfigured. Pod logs cannot be retrieved using kubectl logs, container runtime logs show logging errors, and log collection systems show gaps in log data. This affects monitoring and troubleshooting capabilities, typically caused by container runtime logging issues, disk space problems, or log collection system failures; application errors cannot be diagnosed.

## Impact

Pod logs are unavailable; troubleshooting is blocked; application debugging is impossible; log collection fails; monitoring systems cannot access logs; container runtime logging is broken; log-based alerting fails; `kubectl logs` commands return errors or empty results; centralized logging systems show gaps in log data; application errors cannot be diagnosed. Pod logs cannot be retrieved indefinitely; container runtime logs show logging errors; application errors cannot be diagnosed; troubleshooting is blocked and application debugging is impossible.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to inspect its status and container states to verify if containers are running and should be producing logs.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify pod-related events, focusing on events with reasons such as Failed or messages indicating log collection failures.

3. Attempt to retrieve logs from the pod <pod-name> in namespace <namespace> and check for errors indicating why logs are not available.

4. On the node where the pod is scheduled, check container runtime logging configuration using Pod Exec tool or SSH if node access is available to verify if logging is enabled.

5. Check container runtime status on the node to verify if the runtime is functioning and can collect logs.

6. Verify if log files exist on the node filesystem and check file permissions that may prevent log access.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify any container or logging-related failures. Events showing container failures or runtime errors may explain why logs are unavailable.

2. If kubectl logs returns "container not found" or similar error (from Playbook step 3), the container may have terminated and logs were garbage collected. For terminated containers, use `kubectl logs --previous` to retrieve logs from the previous container instance.

3. If kubectl logs returns empty results but the container is running (from Playbook steps 1, 3), check:
   - Application is writing to stdout/stderr (not to files)
   - Container runtime is capturing stdout/stderr correctly
   - Log files exist on the node filesystem (Playbook step 6)

4. If container runtime status shows errors (from Playbook step 5), the logging subsystem may be broken. Restart the container runtime service on the affected node.

5. If node disk is full or log directory has permission issues (from Playbook step 6), logs cannot be written:
   - Check disk usage with `df -h` on the node
   - Verify /var/log/containers and /var/log/pods directories are writable
   - Check for SELinux or AppArmor policies blocking log writes

6. If logging driver is misconfigured (from Playbook step 4), logs may be sent to an unsupported destination. Verify the container runtime is configured to use the json-file or journald logging driver.

7. If the pod was recently restarted multiple times, older logs may have been rotated out. Kubernetes only keeps logs from the current and previous container instances.

**To restore log availability**: Fix underlying storage or runtime issues, ensure the container writes to stdout/stderr, verify container runtime configuration, and consider implementing persistent logging to an external system for long-term retention.

