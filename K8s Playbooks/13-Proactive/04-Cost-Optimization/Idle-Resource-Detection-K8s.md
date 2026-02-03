# Idle Resource Detection

## Meaning

Idle resource detection indicates that Kubernetes resources are running but not actively utilized, consuming costs without providing value (triggering alerts like IdleResourceDetected or UnusedResourceDetected) because pods show low CPU utilization, deployments have minimal traffic, persistent volume claims have no I/O operations, services are not accessed, or resource metrics indicate minimal usage. Resources show low utilization metrics, resource activity logs indicate minimal usage, cost metrics show resources consuming costs without activity, and resource monitoring indicates idle state. This affects the cost management layer and resource optimization, typically caused by over-provisioning, abandoned resources, or resource lifecycle management failures; if idle resources are container workloads, container resources may be wasted and applications may experience unnecessary cost overhead.

## Impact

IdleResourceDetected alerts fire; UnusedResourceDetected alerts fire; unnecessary costs accumulate; resources consume costs without providing value; cost optimization opportunities are missed; resource utilization is inefficient. Low utilization metrics indicate idle resources; if idle resources are container workloads, container resources may be wasted, pod resources may be over-provisioned, and container applications may experience unnecessary cost overhead; applications may experience cost inefficiencies or resource waste.

## Playbook

1. List pods, deployments, services, and PVCs in namespace <namespace> with wide output and describe deployment <deployment-name> in namespace <namespace> to understand the current resource state and configuration.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent activity or state changes indicating resource usage.

3. List pods in namespace `<namespace>` and retrieve Prometheus metrics for CPU utilization and memory utilization over the last 30 days to identify pods with consistently low utilization.

4. List deployments in namespace `<namespace>` and retrieve Prometheus metrics for request count and traffic metrics over the last 30 days to identify deployments with minimal activity.

5. List persistent volume claims in namespace `<namespace>` and retrieve Prometheus metrics for volume I/O operations over the last 30 days to identify PVCs with no I/O operations.

6. List services in namespace `<namespace>` and retrieve Prometheus metrics for service request count and endpoint activity over the last 30 days to identify services with no access patterns.

7. Retrieve logs from pods in namespace `<namespace>` and filter for patterns indicating resource inactivity or minimal usage over the last 30 days.

8. Compare resource creation timestamps with last activity timestamps and verify whether resources have been idle since creation, using resource activity logs as supporting evidence.

9. Retrieve resource quota usage for namespace `<namespace>` and compare with resource utilization metrics to identify cost-utilization mismatches.

10. List jobs and cronjobs in namespace `<namespace>` and verify execution frequency to identify jobs that are not running or have low execution rates.

## Diagnosis

1. Review the CPU and memory utilization metrics from Step 3. If pods show consistently below 10% utilization over 30 days, these are strong candidates for idle resource cleanup or right-sizing.

2. Analyze the deployment traffic metrics from Step 4. If request counts are zero or near-zero for 30 days, then the deployment is likely abandoned or misconfigured. If traffic exists but is minimal, then the deployment may be over-provisioned.

3. If Step 5 PVC I/O metrics show no operations since creation, then storage is being consumed without providing value. If I/O exists but is minimal, consider storage tier optimization rather than cleanup.

4. Review service access patterns from Step 6. If services show no endpoint activity, verify whether the service is part of an inactive application or a configuration error. If services are accessed but pods behind them are idle, then scaling configuration may be the issue.

5. Compare creation timestamps from Step 8. If resources were created recently and show no activity, they may be in deployment phase. If resources have been idle since creation for over 30 days, they are likely abandoned.

If analysis is inconclusive: Review job and cronjob execution from Step 10 to identify batch workloads that may appear idle between runs. Check resource labels for ownership information to identify responsible teams. Examine resource quota utilization from Step 9 to prioritize cleanup of idle resources consuming significant quota allocations.
