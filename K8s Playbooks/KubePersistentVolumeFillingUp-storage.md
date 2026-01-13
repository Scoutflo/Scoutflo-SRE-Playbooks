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

1. Retrieve the PersistentVolume `<pv-name>` and inspect its status to check capacity, used space, and available space to verify storage usage.

2. Retrieve the PersistentVolumeClaim `<pvc-name>` in namespace `<namespace>` and inspect its status to verify storage usage.

3. Retrieve metrics for storage usage trends for the PersistentVolume `<pv-name>` over the last 7 days to identify growth patterns.

4. Verify application data retention policies and configurations that may affect storage usage by checking application configurations and retention settings.

5. Check for snapshot or backup configurations that may be consuming storage space by reviewing snapshot and backup resource configurations.

6. Retrieve logs from the Pod `<pod-name>` in namespace `<namespace>` using the PersistentVolume `<pv-name>` to identify data growth patterns.

## Diagnosis

Compare PersistentVolume filling up detection timestamps with application data creation or write event timestamps over the last 24 hours and verify whether data growth accelerated recently, using storage usage metrics and application logs as supporting evidence.

Correlate PersistentVolume capacity usage with data retention policy configuration changes within 1 hour and verify whether retention policy changes caused increased storage usage, using retention policy configurations and storage usage trends as supporting evidence.

Compare PersistentVolume usage growth trends with application scaling event timestamps over the last 7 days and verify whether application scaling increased data volume, using storage metrics and application scaling history as supporting evidence.

Analyze storage usage growth patterns over the last 30 days to determine if growth is gradual (normal data accumulation) or sudden (data leak or misconfiguration), using storage usage metrics and historical patterns as supporting evidence.

Correlate PersistentVolume filling up with snapshot or backup creation event timestamps within 24 hours and verify whether snapshot or backup operations increased storage usage, using snapshot events and storage usage changes as supporting evidence.

Compare current storage usage with historical baseline usage over the last 90 days and verify whether storage growth is within expected patterns or represents abnormal growth, using storage metrics and historical usage data as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 90 days for capacity planning analysis, review application data retention requirements, check for data leaks or misconfigurations, verify snapshot and backup retention policies, examine historical storage growth patterns. PersistentVolume filling up may result from normal data growth, inadequate retention policies, or insufficient storage capacity rather than immediate operational changes.
