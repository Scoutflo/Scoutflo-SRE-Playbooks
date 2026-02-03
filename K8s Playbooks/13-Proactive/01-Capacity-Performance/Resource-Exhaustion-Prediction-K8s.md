# Resource Exhaustion Prediction

## Meaning

Resource exhaustion prediction indicates that resource capacity exhaustion cannot be accurately predicted or resource exhaustion warnings are not generated (triggering alerts like ResourceExhaustionPredictionUnavailable or CapacityExhaustionWarningFailed) because resource exhaustion prediction models fail, resource capacity trends cannot be analyzed, resource exhaustion warnings are not generated, resource quota utilization predictions are unavailable, or resource exhaustion timelines cannot be calculated. Resource exhaustion predictions are unavailable, resource capacity trends show unpredictable patterns, resource exhaustion warnings are not generated, and resource exhaustion timeline calculations fail. This affects the capacity planning layer and resource management, typically caused by insufficient resource usage data, exhaustion prediction model failures, resource trend analysis issues, or exhaustion warning automation failures; if resource exhaustion affects container workloads, container resources may be exhausted unexpectedly and applications may experience capacity failures.

## Impact

ResourceExhaustionPredictionUnavailable alerts fire; CapacityExhaustionWarningFailed alerts fire; resource exhaustion cannot be predicted; resource exhaustion warnings are not generated; capacity failures may occur unexpectedly; resource provisioning may be delayed. Resource exhaustion predictions are unavailable; if resource exhaustion affects container workloads, container resources may be exhausted unexpectedly, pod resources may be depleted, and container applications may experience capacity failures; applications may experience resource exhaustion or unexpected capacity constraints.

## Playbook

1. Describe all nodes to inspect node capacity, allocatable resources, and current utilization to identify potential resource exhaustion points.
2. List recent events across all namespaces sorted by timestamp to identify recent events related to resource pressure, OOMKilled pods, or capacity constraints.
3. Retrieve resource quota in namespace <namespace> with YAML output to retrieve current resource quota usage and limits for exhaustion prediction analysis.
4. Retrieve Prometheus metrics for pod resource utilization including CPU utilization, memory utilization, and storage utilization over the last 90 days to analyze resource exhaustion trends.
5. Retrieve Prometheus metrics for resource quota utilization including quota usage percentage and quota limit proximity over the last 90 days to identify approaching quota exhaustion.
6. Retrieve logs from resource monitoring pods and filter for patterns indicating resource depletion or capacity exhaustion within the last 90 days.
7. Retrieve Prometheus metrics for node capacity including available capacity and capacity utilization over the last 90 days to identify capacity exhaustion trends.
8. Compare resource utilization trend data with resource exhaustion prediction model outputs and verify whether predictions identify approaching exhaustion, using Prometheus metrics as supporting evidence.

## Diagnosis

1. Review the node capacity and resource quota data from Steps 1 and 3. If current utilization is approaching limits, verify that exhaustion predictions are accurately forecasting when limits will be reached.

2. Analyze the 90-day utilization trends from Steps 4-5. If trends show consistent growth, predictions should identify exhaustion timelines. If trends are erratic, predictions may be unreliable and reactive monitoring should be emphasized.

3. If Step 6 resource monitoring logs show depletion patterns, identify which resources (CPU, memory, storage, pods) are approaching exhaustion and prioritize capacity expansion for those resources.

4. Review the capacity trend data from Step 7. If capacity utilization is increasing faster than capacity growth, then exhaustion is likely. If capacity growth outpaces utilization growth, then current capacity planning is adequate.

5. If Step 8 prediction model outputs diverge significantly from actual utilization, then prediction models need recalibration with current data patterns.

If analysis is inconclusive: Examine events from Step 2 for resource pressure or OOMKilled events that indicate exhaustion already occurring. Determine whether exhaustion risks are concentrated in specific resource types (suggesting targeted expansion) or distributed (suggesting overall capacity planning needs). Verify that prediction models have sufficient historical data for accurate forecasting.
