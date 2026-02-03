---
title: Kube Persistent Volume Filling Up
weight: 20
---

# KubePersistentVolumeFillingUp

## Meaning

PersistentVolume is filling up and approaching capacity limits (triggering alerts related to PersistentVolume capacity issues) because disk usage is increasing and may soon exhaust available storage space. PersistentVolumes show high disk usage approaching capacity limits in cluster dashboards, storage usage metrics indicate increasing trends, and application logs may show storage-related errors. This affects the storage plane and indicates data growth, lack of retention policies, or insufficient storage capacity that will prevent applications from writing data, typically caused by normal data growth, inadequate retention policies, or insufficient storage capacity; applications may show errors when storage fills.

## Impact

PersistentVolume capacity alerts fire; service degradation; applications may switch to read-only mode; data writes may fail; storage exhaustion prevents new data; applications may crash or become unavailable; data loss risk if storage fills completely; volume may become unusable. PersistentVolumes show high disk usage approaching capacity limits; storage usage metrics indicate increasing trends; applications may switch to read-only mode or crash when storage fills; data writes may fail; applications may show errors or become unavailable.

## Playbook

1. Describe PersistentVolume <pv-name> to inspect the volume status, capacity, used space, reclaim policy, and any conditions indicating storage issues.

2. Retrieve events for PersistentVolume <pv-name> sorted by timestamp to identify capacity warnings or storage backend issues.

3. Describe PersistentVolumeClaim <pvc-name> in namespace <namespace> to inspect the PVC status, requested capacity, and actual usage.

4. Retrieve metrics for storage usage trends for PersistentVolume <pv-name> over the last 7 days to identify growth patterns.

5. Verify application data retention policies and configurations that may affect storage usage by checking application configurations and retention settings.

6. Check for snapshot or backup configurations that may be consuming storage space by reviewing snapshot and backup resource configurations.

7. Retrieve logs from pod <pod-name> in namespace <namespace> using the PersistentVolume <pv-name> to identify data growth patterns.

8. SSH to the node and check disk usage for common storage consumers: accumulated logs in /var/log, cached container images, and orphaned pod data.

## Diagnosis

1. Analyze PV events from Playbook step 2 to identify any capacity warnings or storage errors. Events showing capacity thresholds being crossed indicate when the filling started. If events show recent warnings, correlate timestamps with application activity.

2. If events indicate recent capacity warnings, examine storage usage trends from Playbook step 4 to determine the growth pattern:
   - Sudden spike (within hours) - Likely a misconfiguration, data leak, or unexpected bulk data import
   - Gradual increase (over days/weeks) - Normal data growth exceeding capacity planning
   - Step increases - Correlate with deployment or scaling events

3. If growth pattern is sudden, check application logs from Playbook step 7 for:
   - Excessive logging or debug mode enabled
   - Bulk data operations or imports
   - Failed cleanup jobs leaving temporary data
   - Application errors causing retry storms with data accumulation

4. If growth pattern is gradual, examine data retention policies from Playbook step 5. If retention policies are missing or set to "keep forever", data accumulation is expected. Compare current retention settings with actual storage usage to determine if policies are being enforced.

5. If snapshot or backup configurations exist from Playbook step 6, check if snapshots are consuming space on the same volume. Some storage backends count snapshots against volume capacity.

6. If the PV is on a node, check node-level disk consumers from Playbook step 8. If /var/log or container images are the primary consumers, the issue is node disk pressure rather than application data growth.

7. If no single cause is identified, compare the current fill rate with historical data to project when the volume will be full. This helps prioritize whether immediate cleanup or capacity expansion is needed.

**If no correlation is found within the specified time windows**: Extend timeframes to 90 days for capacity planning analysis, review application data retention requirements, check for data leaks or misconfigurations, verify snapshot and backup retention policies, examine historical storage growth patterns. PersistentVolume filling up may result from normal data growth, inadequate retention policies, or insufficient storage capacity rather than immediate operational changes.
