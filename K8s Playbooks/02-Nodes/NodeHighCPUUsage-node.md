---
title: Node High CPU Usage
weight: 30
categories: [kubernetes, node]
---

# NodeHighCPUUsage

## Meaning

Node is experiencing high CPU utilization (triggering NodeHighCPUUsage, NodeCPUHighUsage alerts, typically when CPU usage exceeds 80-90%) because the node's processors are heavily loaded by running workloads, system processes, or runaway tasks. Node metrics show high CPU utilization across cores, system load average is elevated, and pod performance may be degraded. This affects the node and all workloads running on it; containers experience CPU throttling; application latency increases; system responsiveness degrades.

## Impact

NodeHighCPUUsage alerts fire; all pods on node experience degraded performance; CPU-intensive workloads are throttled; system processes may be delayed; kubelet responsiveness decreases; health checks may timeout; container scheduling may be affected; node may become unresponsive in extreme cases; pod latency increases; SLO violations occur; overall cluster capacity is reduced.

## Playbook

1. Retrieve the Node `<node-name>` and verify current CPU utilization, load average, and allocatable resources.

2. Retrieve all pods running on the node and identify which pods are consuming the most CPU using container_cpu_usage_seconds_total metrics.

3. Check for pods without CPU limits that may be consuming excessive resources.

4. Retrieve node system processes CPU usage to identify if host-level processes (not containers) are consuming CPU.

5. Verify if kubelet and container runtime processes are consuming excessive CPU indicating system-level issues.

6. Check for nodes experiencing CPU steal (in virtualized environments) indicating hypervisor-level contention.

7. Review pod scheduling to determine if the node is over-committed beyond reasonable burst capacity.

## Diagnosis

Compare pod CPU usage with requests and limits and verify whether specific pods are consuming more than allocated, causing node-wide pressure, using container metrics and resource specs as supporting evidence.

Correlate CPU spikes with specific workload patterns (batch jobs, traffic peaks) and verify whether high usage is expected during certain periods, using job schedules and traffic metrics as supporting evidence.

Analyze CPU usage breakdown (user, system, iowait, steal) and verify whether the issue is application load (user), kernel operations (system), disk bottleneck (iowait), or virtualization (steal), using detailed CPU metrics as supporting evidence.

Check for runaway processes or infinite loops in containers by identifying pods with continuously high CPU without corresponding work being done, using container metrics and application throughput as supporting evidence.

Verify if node selector, affinity, or anti-affinity rules are causing uneven pod distribution creating hot spots, using pod placement and node resource comparison as supporting evidence.

If no correlation is found within the specified time windows: cordon node and drain pods to redistribute workload, check for kernel bugs or driver issues, verify no cryptocurrency mining, review hypervisor resource allocation in virtualized environments, consider right-sizing node instance type.
