---
title: Autoscaler Scaling Too Slowly - Cluster Autoscaler
weight: 281
categories:
  - kubernetes
  - autoscaler
---

# AutoscalerScalingTooSlowly-autoscaler

## Meaning

The cluster autoscaler is adjusting node capacity too slowly relative to workload demand (potentially triggering KubePodPending alerts), so node scale-out and scale-in lag behind real-time load even when pending pods or high utilization clearly signal the need for more capacity. This indicates autoscaler rate limiting, configuration constraints, or throttling issues preventing timely capacity adjustments.

## Impact

Pods remain pending longer than expected; deployments scale slowly; applications experience delayed startup; services may have insufficient capacity during traffic spikes; KubePodPending alerts fire; pods remain in Pending state; autoscaler scaling rate is insufficient; node provisioning delays occur; workload demand exceeds available capacity.

## Playbook

1. Retrieve cluster autoscaler ConfigMap in namespace `kube-system` and verify scaling rate parameters including scale-down-delay-after-add, max-node-provision-time, and max-nodes-per-time.

2. List pods in namespace `kube-system` and filter for cluster autoscaler pods to check status and restart count.

3. Retrieve logs from cluster autoscaler pod in namespace `kube-system` and filter for scaling rate messages or throttling indicators.

4. List all nodes and check node pool configuration and limits for capacity including current node count and maximum allowed nodes.

5. List pods across all namespaces with status phase Pending that require scaling and note pending duration.

## Diagnosis

1. Compare the timestamps when slow scaling was observed (from autoscaler logs) with cluster autoscaler configuration change timestamps, and check whether slow scaling begins within 1 hour of configuration changes affecting scaling rates.

2. Compare the slow scaling timestamps with node pool capacity constraint events by checking node pool configuration limits and current node counts, and verify whether slow scaling correlates with approaching node capacity limits.

3. Compare the slow scaling timestamps with pending pod creation timestamps, and verify whether pending pods require scaling by checking pod resource requests against available capacity.

4. Compare the slow scaling timestamps with cluster autoscaler pod restart timestamps, and check whether autoscaler pod restarts occur within 5 minutes before slow scaling is observed.

5. Compare the slow scaling timestamps with cluster upgrade or maintenance window timestamps, and check whether slow scaling correlates with infrastructure changes within 1 hour.

6. Compare the slow scaling timestamps with deployment resource request increase timestamps, and verify whether resource request increases correlate with increased pending pod counts at the same time.

**If no correlation is found within the specified time windows**: Extend the search window (1 hour → 2 hours, 5 minutes → 10 minutes), review autoscaler logs for throttling or rate limiting messages, check cloud provider API rate limits, examine autoscaler scaling rate configuration for conservative settings, verify if node provisioning times are longer than expected, and check for gradual resource exhaustion patterns. Slow scaling may result from conservative configuration or cloud provider provisioning delays not immediately visible in cluster metrics.
