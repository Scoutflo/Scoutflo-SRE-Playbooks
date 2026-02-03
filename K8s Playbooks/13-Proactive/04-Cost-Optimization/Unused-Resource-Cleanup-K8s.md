# Unused Resource Cleanup

## Meaning

Unused resource cleanup indicates that Kubernetes resources are no longer needed but remain provisioned, consuming costs without providing value (triggering alerts like UnusedResourceDetected or OrphanedResourceDetected) because pods are stopped but not deleted, persistent volume claims are unattached, services are not accessed, configmaps and secrets are unused, or resources show no activity over extended periods. Resources show no activity metrics, resources are in stopped or detached state, resources are not associated with active workloads, and resource creation timestamps indicate abandonment. This affects the cost management layer and resource lifecycle management, typically caused by resource lifecycle management failures, abandoned resource detection gaps, or resource cleanup automation issues; if unused resources are container workloads, container resources may be orphaned and applications may experience unnecessary cost overhead.

## Impact

UnusedResourceDetected alerts fire; OrphanedResourceDetected alerts fire; unnecessary costs accumulate; resources consume costs without providing value; resource lifecycle management fails; abandoned resources are not cleaned up. Resources show no activity or are in unused state; if unused resources are container workloads, container resources may be orphaned, pod resources may be abandoned, and container applications may experience unnecessary cost overhead; applications may experience cost inefficiencies or resource waste.

## Playbook

1. List pods in namespace <namespace> filtered by status phase Succeeded or Failed with wide output to identify completed or failed pods that may need cleanup.
2. List recent events in namespace <namespace> sorted by timestamp to identify resource lifecycle issues, orphaned resources, or cleanup-related warnings.
3. List persistent volume claims in namespace <namespace> to identify unattached or released PVCs that may be candidates for cleanup.
4. List services in namespace `<namespace>` and verify service endpoint access patterns to identify services with no access.
5. List configmaps and secrets in namespace `<namespace>` and verify usage by pods to identify unused configmaps and secrets.
6. Retrieve logs from resource monitoring pods and filter for patterns indicating resource inactivity or abandonment over the last 90 days.
7. Compare resource creation timestamps with last activity timestamps and verify whether resources have been inactive since creation, using resource activity logs as supporting evidence.
8. List jobs and cronjobs in namespace `<namespace>` with status 'Complete' or 'Failed' and verify whether completed jobs are cleaned up, checking job lifecycle management.
9. List deployments and statefulsets in namespace `<namespace>` with zero replicas and verify whether zero-replica workloads are still needed, checking workload lifecycle management.

## Diagnosis

1. Review the completed/failed pods from Step 1. If pods have been in Succeeded or Failed status for extended periods, they are candidates for cleanup. Verify that cleanup automation exists for completed jobs.

2. Analyze the PVC status from Step 3. If PVCs show Released or Unbound status, they are not attached to pods and may be candidates for cleanup. Verify whether the associated data is still needed before deletion.

3. If Step 4 service access analysis shows services with no endpoint activity for 90 days, these are likely orphaned services. If Step 5 configmap/secret analysis shows resources not referenced by any pods, they are candidates for cleanup.

4. Review the job/cronjob status from Step 8. If completed jobs are not being cleaned up automatically, then job TTL or cleanup automation is misconfigured. If zero-replica deployments exist from Step 9, verify whether they are intentionally scaled down or abandoned.

5. If Step 7 shows resources inactive since creation for over 90 days, these are strong candidates for abandoned resource cleanup. Check resource labels to identify ownership for verification.

If analysis is inconclusive: Examine events from Step 2 for resource lifecycle issues. Review the resource activity logs from Step 6 to identify resources that once were active but became inactive (suggesting application changes) versus resources never used (suggesting deployment errors). Verify that resource labeling standards exist to identify resource ownership.
