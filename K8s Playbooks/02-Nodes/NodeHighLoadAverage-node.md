---
title: Node High Load Average
weight: 38
categories: [kubernetes, node]
---

# NodeHighLoadAverage

## Meaning

Node is experiencing high load average (triggering NodeHighLoadAverage, NodeSystemSaturation alerts) because there are more processes wanting to run than available CPU cores can handle, causing processes to queue. Node metrics show load average significantly higher than CPU count, system responsiveness degrades, and all operations slow down. This affects all workloads on the node; response times increase; throughput decreases; system becomes sluggish.

## Impact

NodeHighLoadAverage alerts fire; all processes on node slow down; container operations are delayed; kubelet responsiveness decreases; health checks may timeout; network operations queue; disk I/O queues; system appears unresponsive; SSH access is slow; kubectl commands targeting node timeout; application latency increases significantly.

## Playbook

1. Retrieve the Node `<node-name>` and verify load average (1m, 5m, 15m) compared to CPU core count.

2. Identify what is causing the load: CPU saturation, I/O wait, or uninterruptible sleep processes.

3. Retrieve top CPU-consuming processes and pods running on the node.

4. Check for high I/O wait which indicates disk bottleneck contributing to load.

5. Check for processes in uninterruptible sleep (D state) indicating I/O or NFS issues.

6. Verify if the node has appropriate resources for its workload.

7. Check for runaway processes or fork bombs creating excessive process count.

## Diagnosis

Compare load average with CPU utilization and verify whether load is CPU-bound (high CPU%) or I/O-bound (high iowait), using CPU breakdown metrics as supporting evidence.

Analyze process states and identify processes in D state (uninterruptible sleep) which may indicate stuck I/O or NFS hangs, using process state counts as supporting evidence.

Correlate load spikes with workload changes and verify whether specific pods or jobs cause load increases, using job schedules and load timeline as supporting evidence.

Check for process count explosion which increases load without increasing CPU usage, using process count metrics and fork events as supporting evidence.

Compare with other nodes and verify whether load is distributed evenly or this node is overloaded due to scheduling imbalance, using cross-node comparison as supporting evidence.

If no correlation is found within the specified time windows: drain and redistribute workload, investigate stuck I/O (NFS, disk issues), identify and kill runaway processes, review scheduling constraints causing imbalance, consider upgrading to larger instance type.
