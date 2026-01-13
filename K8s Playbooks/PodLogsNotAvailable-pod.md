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

1. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect its status and container states to verify if containers are running and should be producing logs.

2. Attempt to retrieve logs from the pod `<pod-name>` in namespace `<namespace>` and check for errors indicating why logs are not available.

3. On the node where the pod is scheduled, check container runtime logging configuration using Pod Exec tool or SSH if node access is available to verify if logging is enabled.

4. Check container runtime status on the node to verify if the runtime is functioning and can collect logs.

5. List events in namespace `<namespace>` and filter for logging-related events, focusing on events with reasons such as `Failed` or messages indicating log collection failures.

6. Verify if log files exist on the node filesystem and check file permissions that may prevent log access.

## Diagnosis

1. Compare the pod logs unavailability timestamps with container runtime restart or failure timestamps on the node, and check whether runtime issues occurred within 5 minutes before logs became unavailable.

2. Compare the pod logs unavailability timestamps with container runtime logging driver configuration modification timestamps, and check whether logging configuration changes occurred within 30 minutes before logs became unavailable.

3. Compare the pod logs unavailability timestamps with node disk space exhaustion timestamps, and check whether disk space issues occurred within 5 minutes before logs became unavailable, preventing log file creation.

4. Compare the pod logs unavailability timestamps with pod restart or crash timestamps, and check whether pod failures occurred within 5 minutes before logs became unavailable.

5. Compare the pod logs unavailability timestamps with cluster logging system restart or failure timestamps, and check whether logging infrastructure issues occurred within 1 hour before logs became unavailable.

6. Compare the pod logs unavailability timestamps with node filesystem or log directory permission modification timestamps, and check whether permission changes occurred within 30 minutes before logs became unavailable.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review container runtime logs for gradual logging issues, check for intermittent log file creation problems, examine if logging configurations drifted over time, verify if node disk space gradually exhausted, and check for logging driver issues that may have accumulated. Pod logs unavailability may result from gradual infrastructure degradation rather than immediate changes.

