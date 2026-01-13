---
title: Pod Logs Truncated - Pod
weight: 282
categories:
  - kubernetes
  - pod
---

# PodLogsTruncated-pod

## Meaning

Pod logs are being truncated (typically detected via log analysis or monitoring gaps rather than standard Prometheus alerts) because container runtime log rotation settings limit log size, log buffers are too small, or log retention policies are too aggressive. Pod logs show truncated entries, container runtime log rotation configuration shows aggressive limits, and log files on nodes are rotated before collection. This affects monitoring and troubleshooting capabilities, typically caused by log rotation settings or disk space constraints; important log information is lost.

## Impact

Pod logs are incomplete; log entries are truncated; troubleshooting is impaired; important log information is lost; log analysis is incomplete; container runtime log rotation is too aggressive; historical log data is unavailable; `kubectl logs` commands return partial log output; log files on nodes are rotated before collection; critical error messages may be lost in truncated logs. Pod logs show truncated entries indefinitely; container runtime log rotation configuration shows aggressive limits; important log information is lost; troubleshooting is impaired and critical error messages may be lost.

## Playbook

1. Retrieve logs from the pod `<pod-name>` in namespace `<namespace>` and verify if logs are truncated by checking for cut-off entries or missing log lines.

2. On the node where the pod is scheduled, check container runtime log rotation configuration using Pod Exec tool or SSH if node access is available to verify log size limits and rotation settings.

3. Check container runtime log buffer settings to verify if buffers are too small and causing truncation.

4. Verify log file sizes on the node filesystem to check if log files are being rotated or truncated.

5. Check cluster logging system configuration if centralized logging is used to verify if log collection is truncating logs.

6. Review container runtime documentation for default log size limits and rotation policies.

## Diagnosis

1. Compare the pod log truncation timestamps with container runtime log rotation configuration modification timestamps, and check whether rotation settings were changed within 30 minutes before log truncation began.

2. Compare the pod log truncation timestamps with container runtime log buffer size modification timestamps, and check whether buffer size changes occurred within 30 minutes before log truncation.

3. Compare the pod log truncation timestamps with node disk space pressure timestamps, and check whether disk space issues occurred within 5 minutes before log truncation, causing aggressive rotation.

4. Compare the pod log truncation timestamps with cluster logging system configuration modification timestamps, and check whether logging system changes occurred within 30 minutes before log truncation.

5. Compare the pod log truncation timestamps with container runtime update or upgrade timestamps, and check whether runtime changes occurred within 1 hour before log truncation, affecting default log settings.

6. Compare the pod log truncation timestamps with pod high log output rate timestamps, and check whether applications started producing excessive logs within 30 minutes before truncation, exceeding log limits.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review container runtime logs for gradual log rotation issues, check for intermittent log buffer overflow problems, examine if log rotation configurations drifted over time, verify if node disk space gradually decreased causing aggressive rotation, and check for application log output increases that may have accumulated. Log truncation may result from gradual log management policy changes or application behavior rather than immediate configuration modifications.

