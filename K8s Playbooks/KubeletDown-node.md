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

1. Retrieve the Node `<node-name>` and inspect its status to verify Ready condition status and kubelet communication to identify kubelet issues.

2. Retrieve events for the Node `<node-name>` and filter for error patterns including 'NodeNotReady', 'KubeletNotReady', 'NodeUnreachable' to identify kubelet-related errors.

3. Check kubelet pod status if kubelet runs as a static pod, or check kubelet service status on the Node `<node-name>` by accessing via Pod Exec tool or SSH if node access is available to verify kubelet process status.

4. Retrieve kubelet logs from the Node `<node-name>` by accessing via Pod Exec tool or SSH if node access is available, and filter for error patterns including 'panic', 'fatal', 'connection refused', 'certificate', 'timeout' to identify kubelet failures.

5. Verify network connectivity between the Node `<node-name>` and API server endpoints to identify connectivity issues.

6. Retrieve the Node `<node-name>` and check node resource conditions including MemoryPressure, DiskPressure, and PIDPressure that may affect kubelet operation.

## Diagnosis

Compare kubelet unavailability timestamps with node condition transition times within 5 minutes and verify whether kubelet failures coincide with node NotReady condition changes, using node conditions and kubelet status as supporting evidence.

Correlate kubelet failure timestamps with node resource pressure condition transitions within 5 minutes and verify whether kubelet failures align with MemoryPressure, DiskPressure, or PIDPressure conditions, using node conditions and resource metrics as supporting evidence.

Compare kubelet log error timestamps with certificate expiration times within 2 minutes and verify whether kubelet failures began after certificate expiration, using kubelet logs and certificate metadata as supporting evidence.

Analyze kubelet error patterns over the last 15 minutes to determine if failures are sudden (crash) or gradual (resource exhaustion), using kubelet logs and node resource metrics as supporting evidence.

Correlate kubelet unavailability with network policy or firewall rule change timestamps within 10 minutes and verify whether connectivity issues began after network configuration changes, using network policy events and kubelet connection logs as supporting evidence.

Compare kubelet process resource usage with node available resources at failure times and verify whether resource constraints caused kubelet failures, using node metrics and process resource usage as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for infrastructure changes, review node system logs, check for storage issues affecting kubelet, verify container runtime health, examine historical kubelet stability patterns. Kubelet failures may result from node hardware issues, operating system problems, or container runtime failures rather than immediate configuration changes.
