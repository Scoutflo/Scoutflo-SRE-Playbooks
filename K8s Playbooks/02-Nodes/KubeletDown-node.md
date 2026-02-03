---
title: Kubelet Down
weight: 20
---

# KubeletDown

## Meaning

Kubelet service is unreachable or non-responsive on one or more nodes (triggering KubeletDown alerts) because the kubelet process has failed, lost network connectivity, or cannot communicate with the control plane. Nodes show NotReady or Unknown condition in kubectl, kubelet logs show connection timeout errors or process failures, and kubectl commands fail with connection refused or timeout errors. This affects the data plane and prevents nodes from managing pods, reporting status, or responding to API server requests, typically caused by kubelet process crashes, certificate expiration, network connectivity issues, or resource constraints; applications running on affected nodes may experience errors or become unreachable.

## Impact

KubeletDown alerts fire; nodes cannot manage pods; kubectl exec and kubectl logs fail; pod status updates stop; node condition transitions to NotReady or Unknown; pods on affected nodes may become unreachable; node cannot receive configuration changes; container runtime operations fail; node effectively becomes non-functional. Nodes show NotReady or Unknown condition indefinitely; kubelet logs show connection timeout errors; applications running on affected nodes may experience errors or become unreachable; pods on affected nodes may become unreachable or be evicted.

## Playbook

1. Describe node <node-name> to see:
   - Conditions section showing Ready status and kubelet communication status
   - Events section showing NodeNotReady, KubeletNotReady events with timestamps
   - Allocated resources and system information

2. Retrieve events for node <node-name> sorted by timestamp to see the sequence of kubelet-related issues including 'NodeNotReady', 'KubeletNotReady', 'NodeUnreachable'.

3. Check kubelet pod status if kubelet runs as a static pod, or check kubelet service status on the Node <node-name> by accessing via Pod Exec tool or SSH if node access is available to verify kubelet process status.

4. Retrieve kubelet logs from the Node <node-name> by accessing via Pod Exec tool or SSH if node access is available, and filter for error patterns including 'panic', 'fatal', 'connection refused', 'certificate', 'timeout' to identify kubelet failures.

5. Verify network connectivity between the Node <node-name> and API server endpoints to identify connectivity issues.

6. Check node resource conditions for node <node-name> to see MemoryPressure, DiskPressure, and PIDPressure that may affect kubelet operation.

## Diagnosis

1. Analyze node events from Playbook steps 1-2 to identify when kubelet became unavailable. Events with reason "NodeNotReady", "KubeletNotReady", or "NodeUnreachable" show the timeline of kubelet failure. Note event timestamps and messages to understand the failure pattern.

2. If node events indicate kubelet stopped posting status, check kubelet service status from Playbook step 3. Determine if kubelet process is running, crashed, or stopped to distinguish between process failure and communication issues.

3. If kubelet is not running, check kubelet logs from Playbook step 4 for error patterns. Look for "panic", "fatal", "OOM", "connection refused", or "certificate" errors that explain why kubelet crashed or failed to start.

4. If kubelet logs show certificate errors, this indicates certificate expiration or rotation failure. Verify certificate validity and compare expiration timestamps with when kubelet became unavailable.

5. If node events indicate network issues, verify network connectivity from Playbook step 5. Kubelet may be running but unable to communicate with the API server due to network partitioning or firewall rules.

6. If node events indicate resource pressure (MemoryPressure, DiskPressure, PIDPressure), check node conditions from Playbook step 6. Resource exhaustion can cause kubelet to be killed by OOM killer or fail health checks.

7. If kubelet logs show container runtime errors, verify container runtime health. Kubelet depends on the container runtime and cannot function properly if runtime is unavailable or unresponsive.

**If no root cause is identified from events**: Review system logs (journalctl, dmesg) for kernel-level issues, check for disk corruption or filesystem errors, verify node hardware health, and examine if kubelet was manually stopped or affected by node-level security policies.
