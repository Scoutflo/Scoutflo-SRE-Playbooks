---
title: Node RAID Degraded
weight: 45
categories: [kubernetes, node]
---

# NodeRAIDDegraded

## Meaning

Node RAID array is in degraded state (triggering NodeRAIDDegraded, NodeRAIDDiskFailure alerts) because one or more disks in the RAID array have failed or been removed, and the array is operating with reduced redundancy. Node metrics show RAID array not in optimal state, data redundancy is compromised, and another disk failure could cause data loss. This affects data durability on the node; immediate disk replacement is needed; performance may be degraded during rebuild.

## Impact

NodeRAIDDegraded alerts fire; data redundancy is lost; another disk failure will cause data loss; performance may be degraded; RAID rebuild needed after disk replacement; potential data corruption risk; node should be scheduled for maintenance; workloads should be migrated if possible.

## Playbook

1. Retrieve the Node `<node-name>` and identify which RAID array is degraded.

2. Check RAID status using mdadm or vendor-specific tools to identify failed disk(s).

3. Verify which physical disk has failed using disk serial number and slot information.

4. Check if hot spare disk is available and rebuild has started automatically.

5. Plan disk replacement with minimal workload disruption.

6. Verify data integrity on critical volumes after rebuild.

7. Consider draining node to other nodes during disk replacement.

## Diagnosis

Identify which disk(s) failed by examining RAID array member status and disk SMART data, using mdadm status and smartctl output as supporting evidence.

Check disk SMART attributes for warning signs on remaining disks that may indicate imminent failure, using SMART logs and predictive failure indicators as supporting evidence.

Verify RAID rebuild is progressing if hot spare is available, using rebuild progress and estimated completion time as supporting evidence.

Check for underlying causes: power issues, thermal problems, vibration, firmware bugs, using system logs and environmental monitoring as supporting evidence.

Assess data risk based on RAID level and number of failed disks (RAID 1 or 5 can tolerate 1 failure, RAID 6 can tolerate 2), using RAID configuration as supporting evidence.

If no correlation is found within the specified time windows: immediately replace failed disk, verify remaining disks are healthy, consider node evacuation during rebuild, review disk vendor and model for known issues, consider upgrading to more resilient RAID level.
