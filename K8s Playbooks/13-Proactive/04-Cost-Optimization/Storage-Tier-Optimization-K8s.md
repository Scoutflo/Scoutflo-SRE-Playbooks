# Storage Tier Optimization

## Meaning

Storage tier optimization indicates that persistent volume storage classes are not in optimal storage tiers, storage tier transitions are not occurring, or storage tier costs are not minimized (triggering alerts like StorageTierNotOptimized or StorageTierTransitionFailed) because persistent volume claims remain in expensive storage classes, storage tier lifecycle policies are not configured, storage tier transitions do not occur, storage tier costs exceed optimal costs, or storage tier optimization analysis indicates problems. Storage tier metrics show PVCs in suboptimal tiers, storage tier lifecycle policies are not active, storage tier costs exceed optimal costs, and storage tier optimization fails. This affects the cost management layer and storage lifecycle management, typically caused by storage tier lifecycle policy misconfigurations, storage tier transition automation issues, storage tier cost analysis gaps, or storage class configuration problems; if storage tiers protect container workloads, container persistent volume storage may not be optimized and applications may experience unnecessary storage costs.

## Impact

StorageTierNotOptimized alerts fire; StorageTierTransitionFailed alerts fire; storage costs are not minimized; persistent volume claims remain in expensive tiers; storage tier transitions do not occur; storage tier lifecycle policies are not effective. Storage tier metrics show suboptimal tier usage; if storage tiers protect container workloads, container persistent volume storage may not be optimized, PVC storage classes may be misconfigured, and container applications may experience unnecessary storage costs; applications may experience cost inefficiencies or storage tier optimization failures.

## Playbook

1. List all persistent volume claims in namespace <namespace> with wide output to retrieve their storage class assignments and capacity.
2. List recent events in namespace <namespace> sorted by timestamp to identify storage provisioning issues, tier transition failures, or PVC-related warnings.
3. Describe PVC <pvc-name> in namespace <namespace> to inspect the PVC configuration including storage class, access modes, and current status.
4. List all storage classes to retrieve their provisioner configurations and understand available storage tiers.
5. Retrieve Prometheus metrics for storage classes including storage_class_usage and storage_class_cost over the last 30 days to identify storage tier distribution patterns.
6. Retrieve logs from storage controller pods and filter for tier transition failures or lifecycle policy execution errors within the last 7 days.
7. Compare storage tier cost data with optimal storage tier costs over the last 30 days to identify cost optimization opportunities.
8. List persistent volumes in cluster and retrieve volume type configurations to identify volumes that could be migrated to cost-optimized storage classes.
9. Compare PVC access pattern timestamps with storage tier transition timestamps and verify whether tier transitions occur based on access patterns, using PVC access logs as supporting evidence.

## Diagnosis

1. Review the PVC storage class assignments from Steps 1 and 3. If PVCs are using premium storage classes but Step 5 cost metrics show minimal I/O operations, these are candidates for tier transition to reduce costs.

2. Analyze the storage class configurations from Step 4. If cost-optimized storage classes are available but not being used for appropriate workloads, then tier optimization policies are not functioning correctly.

3. If Step 6 storage controller logs show tier transition failures, identify the failure reasons (permissions, capacity, or policy configuration). If no transition attempts are logged, then lifecycle policies may not be triggering.

4. Review the cost comparison from Step 7. If actual costs significantly exceed optimal tier costs, prioritize the PVCs with the largest cost gaps for immediate optimization.

5. If Step 9 access pattern analysis shows PVCs with consistently low I/O that should have transitioned but have not, then either lifecycle policies are misconfigured or transition automation is failing.

If analysis is inconclusive: Examine events from Step 2 for storage provisioning issues or tier transition failures. Review the PV type configurations from Step 8 to identify volumes that could be migrated but have not been. Determine whether optimization failures are concentrated in specific storage classes (suggesting class-specific issues) or distributed (suggesting policy-level problems).
