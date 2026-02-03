# Right-sizing Analysis

## Meaning

Right-sizing analysis indicates that Kubernetes resources are over-provisioned or under-provisioned relative to actual utilization, leading to cost inefficiencies or performance issues (triggering alerts like OverProvisionedResource or UnderProvisionedResource) because pods have CPU/memory allocation exceeding utilization, deployments have resource requests mismatched with workload requirements, persistent volume claims have storage allocation exceeding actual usage, or resource metrics show consistent over or under-utilization patterns. Resources show utilization metrics significantly below or above allocation, cost metrics indicate over-provisioning, performance metrics indicate under-provisioning, and resource allocation does not match workload requirements. This affects the cost management layer and resource optimization, typically caused by initial over-provisioning, workload changes, or lack of utilization monitoring; if resources are container workloads, container resource requests may be misaligned and applications may experience cost inefficiencies or performance constraints.

## Impact

OverProvisionedResource alerts fire; UnderProvisionedResource alerts fire; unnecessary costs accumulate from over-provisioning; performance issues occur from under-provisioning; resource allocation does not match workload requirements; cost optimization opportunities are missed. Utilization metrics show significant allocation mismatches; if resources are container workloads, container resource requests may be misaligned, pod resource limits may be inappropriate, and container applications may experience cost inefficiencies or performance constraints; applications may experience cost waste or performance degradation.

## Playbook

1. Describe pod <pod-name> in namespace <namespace> to inspect pod resource requests, limits, and current resource consumption for right-sizing analysis.
2. List recent events in namespace <namespace> sorted by timestamp to identify recent events related to resource constraints, OOMKilled, or CPU throttling.
3. List pods in namespace <namespace> and retrieve their resource specifications for right-sizing analysis.
4. Retrieve Prometheus metrics for CPU utilization and memory utilization over the last 30 days to compare with pod resource requests and limits.
5. Describe PVC <pvc-name> in namespace <namespace> to inspect storage allocation and compare with actual usage for storage right-sizing.
6. Compare resource request specifications with actual utilization metrics over the last 30 days and verify whether requests significantly exceed or fall below utilization, using Prometheus metrics as supporting evidence.
7. Retrieve resource quota usage for namespace `<namespace>` and compare with resource utilization metrics to identify cost-utilization mismatches.
8. Describe HPA <hpa-name> in namespace <namespace> to verify HPA resource target utilization settings align with actual usage patterns.

## Diagnosis

1. Review the pod resource consumption from Steps 1, 3, and 4. If pods consistently use less than 30% of requested CPU/memory, they are over-provisioned and candidates for right-sizing. If pods are frequently throttled or OOMKilled, they are under-provisioned.

2. Analyze the 30-day utilization metrics from Step 4. If utilization is consistently low, reduce resource requests. If utilization shows occasional spikes, maintain current requests but consider autoscaling.

3. If Step 5 PVC inspection shows storage allocation significantly exceeding usage, then storage right-sizing opportunities exist. Consider smaller storage classes or data cleanup.

4. Review the resource quota comparison from Step 7. If quota usage is high but individual pod utilization is low, then many over-provisioned pods are consuming quota unnecessarily.

5. If Step 8 HPA settings show target utilization not matching actual patterns, then autoscaler configuration may need adjustment to better match workload characteristics.

If analysis is inconclusive: Examine events from Step 2 for OOMKilled or CPU throttling events that indicate under-provisioning. Review the utilization comparison from Step 6 to identify pods with the largest allocation-utilization gaps. Prioritize right-sizing based on cost impact (large resources with low utilization first).
