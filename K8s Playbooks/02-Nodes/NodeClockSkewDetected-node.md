---
title: Node Clock Skew Detected
weight: 35
categories: [kubernetes, node]
---

# NodeClockSkewDetected

## Meaning

Node clock is skewed or not synchronized (triggering NodeClockSkewDetected, NodeClockNotSynchronising, NodeClockSkew alerts) because the system clock has drifted from accurate time sources or NTP synchronization is failing. Node time differs from reference time sources by more than acceptable thresholds, and time-dependent operations become unreliable. This affects time-sensitive operations across all workloads; certificate validation fails; authentication tokens expire incorrectly; log timestamps are wrong; distributed systems coordination fails.

## Impact

NodeClockSkewDetected alerts fire; TLS certificate validation may fail; JWT tokens are rejected as expired or not-yet-valid; log timestamps are incorrect making debugging difficult; distributed consensus fails (etcd, databases); scheduler timing is wrong; cron jobs fire at wrong times; lease expirations are miscalculated; Kubernetes node heartbeats may be affected; authentication and authorization failures increase.

## Playbook

1. Retrieve the Node `<node-name>` and verify current system time compared to accurate reference.

2. Check NTP service status (chrony, ntpd, systemd-timesyncd) on the node.

3. Verify NTP server configuration and whether the node can reach configured time servers.

4. Check for NTP synchronization issues including stratum level and offset from reference.

5. Verify if virtualization layer (hypervisor) is affecting time synchronization.

6. Check for kernel clock drift issues or hardware clock problems.

7. Verify if any pods are affected by running time-sensitive validations.

## Diagnosis

Check NTP daemon status and verify whether the service is running and actively synchronizing, using service status and sync status output as supporting evidence.

Verify NTP server reachability and confirm network connectivity to time servers (NTP traffic on UDP 123), using network connectivity tests and firewall rules as supporting evidence.

Analyze clock offset trend and determine if clock is drifting continuously (hardware issue) or jumped suddenly (configuration change, VM migration), using time offset history as supporting evidence.

Compare clock across nodes and verify whether clock skew affects single node or multiple nodes (suggesting NTP server issues), using cross-node time comparison as supporting evidence.

Check virtualization time sync settings and verify whether guest additions or hypervisor time sync is conflicting with NTP, using VM configuration and hypervisor settings as supporting evidence.

If no correlation is found within the specified time windows: restart NTP service, reconfigure NTP with reliable servers, check for hardware clock battery issues, verify VM time synchronization settings, consider dedicated time server for cluster, check for leap second handling issues.
