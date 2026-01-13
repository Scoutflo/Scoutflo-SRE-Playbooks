---
title: ConfigMap Too Large - ConfigMap
weight: 287
categories:
  - kubernetes
  - configmap
---

# ConfigMapTooLarge-configmap

## Meaning

ConfigMaps exceed the 1MB size limit (triggering KubePodPending alerts when pods fail to start due to ConfigMap mount failures) because configuration data is too large, multiple large files are stored in a single ConfigMap, or configuration has grown over time. ConfigMap creation or updates fail with validation errors, pod events show ConfigMap size limit exceeded errors, and pods remain in Pending or ContainerCreating state. This affects the workload plane and prevents applications from accessing configuration data, typically caused by configuration data growth over time; applications cannot start.

## Impact

ConfigMap creation fails with validation errors; ConfigMap updates are rejected by API server; applications cannot access configuration; pods cannot start if they depend on the ConfigMap and remain in Pending state; KubePodPending alerts fire when pods fail to mount ConfigMap volumes; configuration data is unavailable; services cannot start without required config; deployment updates fail; pod events show ConfigMap size limit exceeded errors. ConfigMap creation or updates fail with validation errors indefinitely; pod events show ConfigMap size limit exceeded errors; applications cannot start and may show errors; configuration data is unavailable.

## Playbook

1. Retrieve the ConfigMap `<configmap-name>` in namespace `<namespace>` and inspect its data size and content to verify if it exceeds the 1MB limit.

2. List events in namespace `<namespace>` and filter for ConfigMap-related events, focusing on events with reasons such as `Failed` or messages indicating size limit exceeded.

3. Calculate the total size of all keys and values in the ConfigMap to identify which data is causing the size limit to be exceeded.

4. Check if the ConfigMap contains large binary data, files, or configuration that should be stored elsewhere.

5. Review ConfigMap usage in pods and deployments to understand how the ConfigMap is being used and if it can be split.

6. Verify if the ConfigMap size has grown over time by checking ConfigMap modification history or metrics.

## Diagnosis

1. Compare the ConfigMap size limit error timestamps with ConfigMap data modification timestamps, and check whether large data was added within 30 minutes before size limit errors.

2. Compare the ConfigMap size limit error timestamps with ConfigMap key addition timestamps, and check whether new keys were added within 30 minutes before size limit errors.

3. Compare the ConfigMap size limit error timestamps with application configuration update timestamps, and check whether configuration changes increased size within 30 minutes before errors.

4. Compare the ConfigMap size limit error timestamps with ConfigMap merge or update operation timestamps, and check whether updates combined multiple ConfigMaps within 30 minutes before size limit errors.

5. Compare the ConfigMap size limit error timestamps with deployment rollout or configuration change timestamps, and check whether application updates introduced larger configurations within 1 hour before size limit errors.

6. Compare the ConfigMap size limit error timestamps with cluster upgrade or Kubernetes version update timestamps, and check whether size limit enforcement changed within 1 hour before errors, though the limit is typically constant.

**If no correlation is found within the specified time windows**: Extend the search window (30 minutes → 1 hour, 1 hour → 2 hours), review ConfigMap modification history for gradual size growth, check for cumulative configuration additions over time, examine if binary data or large files were gradually added, verify if ConfigMap data accumulated without cleanup, and check for configuration management tools that may have increased ConfigMap size gradually. ConfigMap size limit errors may result from gradual configuration growth rather than immediate large additions.

