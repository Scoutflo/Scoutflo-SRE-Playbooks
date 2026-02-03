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

1. Describe pod <pod-name> in namespace <namespace> to inspect pod status and container states to understand the pod configuration and logging context.

2. Retrieve events in namespace <namespace> for pod <pod-name> sorted by timestamp to identify pod-related events that may indicate logging or storage issues.

3. Retrieve logs from the pod <pod-name> in namespace <namespace> and verify if logs are truncated by checking for cut-off entries or missing log lines.

4. On the node where the pod is scheduled, check container runtime log rotation configuration using Pod Exec tool or SSH if node access is available to verify log size limits and rotation settings.

5. Check container runtime log buffer settings to verify if buffers are too small and causing truncation.

6. Verify log file sizes on the node filesystem to check if log files are being rotated or truncated.

7. Check cluster logging system configuration if centralized logging is used to verify if log collection is truncating logs.

8. Review container runtime documentation for default log size limits and rotation policies.

## Diagnosis

1. Analyze pod events from Playbook steps 1-2 to identify any storage or logging-related issues. Events showing disk pressure or container runtime errors may indicate the cause of log truncation.

2. If pod logs show cut-off entries or missing lines (from Playbook step 3), verify container runtime log rotation settings (from Playbook step 4):
   - Docker: Check --log-opt max-size and --log-opt max-file settings
   - Containerd: Check max-size and max-file in config.toml

3. If log files on the node are small despite heavy log output (from Playbook step 6), the container runtime is rotating logs aggressively. Common default limits:
   - Docker: 10MB per log file, 1 file (no rotation)
   - Containerd: configurable, often 10-100MB

4. If node shows DiskPressure condition or low disk space, the runtime may be truncating logs to free space. Clear disk space or increase node storage capacity.

5. If container runtime log buffer is too small (from Playbook step 5), individual log lines may be truncated. This typically affects very long log lines (>16KB).

6. If centralized logging is configured (from Playbook step 7), check if the log shipper (Fluentd, Filebeat, etc.) is failing to collect logs before rotation. Common issues include:
   - Log shipper pod not running
   - Log shipper falling behind on high-volume logs
   - Network issues preventing log delivery

7. If application produces excessive logs, consider implementing application-level log rate limiting or adjusting log verbosity to reduce output volume.

**To prevent log truncation**: Increase container runtime log size limits, ensure adequate node disk space, configure centralized logging with sufficient collection capacity, and review application logging patterns to reduce unnecessary verbose output.

