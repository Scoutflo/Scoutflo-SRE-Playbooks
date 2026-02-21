---
title: Node Memory Major Page Faults
weight: 46
categories: [kubernetes, node]
---

# NodeMemoryMajorPagesFaults

## Meaning

Node is experiencing high rate of major page faults (triggering NodeMemoryMajorPagesFaults alerts) because processes are frequently accessing memory pages that must be read from disk, indicating memory pressure or swap usage. Node metrics show elevated major fault rate, I/O wait increases, and overall system performance degrades. This affects all workloads on the node; application latency increases; throughput decreases; system becomes sluggish.

## Impact

NodeMemoryMajorPagesFaults alerts fire; application performance degrades significantly; I/O wait increases; disk becomes bottleneck; latency spikes occur when pages are faulted; memory-intensive operations slow dramatically; swap thrashing may occur; overall system throughput decreases; user experience degrades.

## Playbook

1. Retrieve the Node `<node-name>` and verify memory utilization, swap usage, and page fault rates.

2. Check if swap is enabled and actively being used.

3. Identify which pods or processes are causing the most memory pressure.

4. Verify node memory is adequate for the workloads scheduled on it.

5. Check for memory leaks in containers that are forcing page-outs.

6. Evaluate if memory-intensive workloads should be rescheduled to nodes with more memory.

7. Check memory overcommit settings (vm.overcommit_memory) on the node.

## Diagnosis

Correlate major page faults with swap usage and verify whether pages are being swapped to disk due to memory pressure, using swap metrics and fault rates as supporting evidence.

Identify memory-intensive pods that may be forcing other workloads' pages to be swapped out, using per-container memory metrics and node allocation as supporting evidence.

Check for bursty memory usage patterns that temporarily exceed available memory and cause page faults, using memory usage timeline as supporting evidence.

Verify if memory overcommitment is too aggressive, allowing more memory to be promised than available, using memory requests, limits, and actual usage as supporting evidence.

Analyze whether adding more nodes (horizontal) or larger nodes (vertical) would address the memory pressure, using cluster capacity and workload requirements as supporting evidence.

If no correlation is found within the specified time windows: disable swap to prevent swap thrashing and allow OOMKill instead, increase node memory, redistribute workloads, add memory limits to unbounded pods, implement memory-based pod scheduling.
