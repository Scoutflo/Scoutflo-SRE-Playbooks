---
title: Node Systemd Service Failed
weight: 37
categories: [kubernetes, node]
---

# NodeSystemdServiceFailed

## Meaning

A systemd service on the node has failed (triggering NodeSystemdServiceFailed, NodeSystemdServiceCrashlooping alerts) because a critical system service is not running and cannot be automatically recovered. Node shows failed units in systemctl, service may be crash-looping, and dependent functionality is unavailable. This affects the node and potentially cluster functionality; kubelet may be affected; container runtime may fail; networking may be broken; logging may stop.

## Impact

NodeSystemdServiceFailed alerts fire; dependent services are affected; if kubelet fails, node becomes NotReady; if container runtime fails, containers cannot start; if networking services fail, pod networking breaks; log forwarding stops if logging services fail; monitoring data is lost if node-exporter fails; node functionality is degraded; cluster operations on this node fail.

## Playbook

1. Retrieve the Node `<node-name>` and identify which systemd service has failed using `systemctl --failed`.

2. Check the service status with `systemctl status <service-name>` to see the failure reason and recent logs.

3. Retrieve service logs using `journalctl -u <service-name>` to identify the root cause of failure.

4. Check service dependencies and verify whether a dependency failure is causing the cascade.

5. Verify service configuration files for syntax errors or misconfigurations.

6. Check system resources (disk space, memory) that may prevent service operation.

7. For critical services (kubelet, containerd, docker), check specific configuration and health.

## Diagnosis

Analyze service exit code and error messages and categorize failure type (configuration error, resource issue, dependency failure), using service status and logs as supporting evidence.

Check for recent changes to service configuration or system updates that may have introduced the failure, using configuration file timestamps and package update history as supporting evidence.

Verify resource availability for the service (disk space, memory, ports, file descriptors) and confirm resources are available, using system resource metrics and service requirements as supporting evidence.

Check for dependency chain failures where one service failure causes cascading failures, using service dependency tree and failure timestamps as supporting evidence.

Analyze restart patterns and verify whether the service is crash-looping (underlying issue) or failed once and stayed down (startup issue), using restart count and timestamps as supporting evidence.

If no correlation is found within the specified time windows: attempt manual service restart, review and fix configuration errors, check for corrupted state files, reinstall service if corrupted, escalate to node replacement if unrecoverable.
