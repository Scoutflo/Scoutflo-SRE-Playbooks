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

1. Describe the cluster autoscaler deployment in namespace `kube-system` to inspect its status, configuration, and scaling behavior.

2. Retrieve events in the `kube-system` namespace sorted by timestamp to identify autoscaler scaling events and throttling indicators.

3. Retrieve cluster autoscaler ConfigMap in namespace `kube-system` and verify scaling rate parameters including scale-down-delay-after-add, max-node-provision-time, and max-nodes-per-time.

4. Retrieve logs from cluster autoscaler pod in namespace `kube-system` and filter for scaling rate messages or throttling indicators.

5. List all nodes and check node pool configuration and limits for capacity including current node count and maximum allowed nodes.

6. List pods across all namespaces with status phase Pending that require scaling and note pending duration.

## Diagnosis

1. Analyze cluster autoscaler events and logs from Playbook to identify scaling rate constraints. Events showing throttling messages, rate limiting, or delays indicate the specific bottleneck affecting scaling speed.

2. If autoscaler configuration shows conservative scaling parameters, these intentionally limit scaling speed. Check scale-down-delay-after-add, scan-interval, and max-node-provision-time settings from Playbook. Default values may be too conservative for fast-scaling workloads.

3. If events indicate node provisioning delays (long time between scale-up decision and node Ready), the cloud provider provisioning time is the bottleneck. Check node startup times in autoscaler logs. Some instance types or regions have longer provisioning times.

4. If pending pods have been waiting longer than expected, compare pending duration with autoscaler scan interval. The autoscaler evaluates pending pods at each scan interval (default 10s). Multiple pending pods may be batched together, which is more efficient but adds latency.

5. If autoscaler logs show scale-up decisions being made but nodes taking long to become Ready, check node startup sequence. Nodes must pass health checks, register with the cluster, and have system pods scheduled before accepting workloads.

6. If scaling appears slow but autoscaler is at maximum nodes per scale-up operation, check expander configuration. The autoscaler may be scaling one node at a time if configured conservatively. Check max-nodes-total and node group expansion settings.

7. If cloud provider rate limiting is occurring, autoscaler logs will show API throttling or retry messages. Cloud providers limit API call rates, which can slow down scaling during bursts. Consider requesting higher API limits or optimizing autoscaler configuration to reduce API calls.
