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

1. Describe ConfigMap <configmap-name> in namespace <namespace> to inspect its data size and content to verify if it exceeds the 1MB limit - look for the data keys and their sizes.

2. Retrieve events in namespace <namespace> for ConfigMap <configmap-name> sorted by timestamp to see the sequence of ConfigMap-related events, focusing on events with reasons such as Failed or messages indicating size limit exceeded.

3. Retrieve the ConfigMap <configmap-name> in namespace <namespace> and calculate its total size to identify if it is approaching or exceeding the 1MB limit.

4. Check if the ConfigMap <configmap-name> in namespace <namespace> contains large binary data, files, or configuration that should be stored elsewhere.

5. List pods in namespace <namespace> and analyse their ConfigMap references to understand how the ConfigMap is being used and if it can be split.

6. Verify if the ConfigMap size has grown over time by checking ConfigMap <configmap-name> modification history and resourceVersion in namespace <namespace>.

## Diagnosis

1. Analyze events from Playbook to identify the ConfigMap size limit error. Events showing "exceeds maximum size" or "too large" indicate the ConfigMap has exceeded the 1MB etcd object size limit. Note the exact error message and timestamp for correlation.

2. If events indicate size limit exceeded during creation, calculate the current ConfigMap size from Playbook inspection. Identify which keys contain the largest data values and determine if they can be split or stored externally.

3. If events indicate size limit exceeded during update, compare the current ConfigMap data with recent changes. Identify if new keys were added or existing keys were expanded that pushed the total size over 1MB.

4. If the ConfigMap contains binary data (binaryData field), evaluate if this data should be stored in a different resource type such as a Secret (for sensitive data) or external storage (for large files).

5. If the ConfigMap has grown over time, review the ConfigMap's resourceVersion and modification history from Playbook output. Identify patterns of incremental growth and determine if old or unused keys can be removed.

6. If events indicate pod mount failures due to ConfigMap size, verify if the ConfigMap can be split into multiple smaller ConfigMaps. Consider using subPath mounts to mount only specific keys rather than the entire ConfigMap.

**If no clear cause is identified from events**: Examine if configuration management tools (Helm, Kustomize, operators) are generating large ConfigMaps, check if the ConfigMap is being used as a general data store rather than for configuration, and evaluate alternative storage solutions for large data such as PersistentVolumes or external configuration services.

