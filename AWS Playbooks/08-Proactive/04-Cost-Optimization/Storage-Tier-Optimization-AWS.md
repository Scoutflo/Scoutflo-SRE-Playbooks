# Storage Tier Optimization

## Meaning

Storage tier optimization indicates that storage objects are not in optimal storage tiers, storage tier transitions are not occurring, or storage tier costs are not minimized (triggering alarms like StorageTierNotOptimized or StorageTierTransitionFailed) because S3 objects remain in expensive storage classes, S3 Intelligent-Tiering is not moving objects, Glacier retrieval times are not optimized, EBS volume types are not cost-optimized, or storage tier lifecycle policies are not configured. Storage tier metrics show objects in suboptimal tiers, S3 Intelligent-Tiering metrics indicate no transitions, storage tier costs exceed optimal costs, and storage tier lifecycle policies are not active. This affects the cost management layer and storage lifecycle management, typically caused by storage tier lifecycle policy misconfigurations, S3 Intelligent-Tiering failures, storage tier transition automation issues, or storage tier cost analysis gaps; if storage tiers protect container workloads, container persistent volume storage may not be optimized and applications may experience unnecessary storage costs.

## Impact

StorageTierNotOptimized alarms fire; StorageTierTransitionFailed alarms fire; storage costs are not minimized; storage objects remain in expensive tiers; storage tier transitions do not occur; storage tier lifecycle policies are not effective. Storage tier metrics show suboptimal tier usage; if storage tiers protect container workloads, container persistent volume storage may not be optimized, PVC storage classes may be misconfigured, and container applications may experience unnecessary storage costs; applications may experience cost inefficiencies or storage tier optimization failures.

## Playbook

1. List S3 buckets in region `<region>` and retrieve S3 bucket storage class distribution to identify buckets with objects in expensive storage classes.
2. Retrieve S3 bucket `<bucket-name>` Intelligent-Tiering configuration and inspect its transition status and object movement metrics, verifying Intelligent-Tiering functionality.
3. Retrieve S3 bucket `<bucket-name>` lifecycle policy configuration and verify whether lifecycle policies are configured and active, checking lifecycle policy effectiveness.
4. Retrieve CloudWatch metrics for S3 storage classes including StandardStorage, IntelligentTieringStorage, and GlacierStorage over the last 30 days to identify storage tier distribution patterns.
5. Query CloudWatch Logs for log groups containing S3 lifecycle events and filter for tier transition failures or lifecycle policy execution errors within the last 7 days.
6. Retrieve Cost Explorer data for S3 storage costs by storage class over the last 30 days and compare with optimal storage tier costs to identify cost optimization opportunities.
7. List EBS volumes in region `<region>` and retrieve volume type configurations to identify volumes that could be migrated to cost-optimized types.
8. Compare S3 object access pattern timestamps with storage tier transition timestamps and verify whether tier transitions occur based on access patterns, using S3 access logs as supporting evidence.

## Diagnosis

1. **Analyze storage class distribution from Step 1 and Step 4**: If significant data remains in Standard storage class for 30+ days without access, it should transition to Intelligent-Tiering or Infrequent Access. If Glacier contains frequently accessed data, retrieval costs may be high.

2. **Evaluate Intelligent-Tiering from Step 2**: If Intelligent-Tiering is enabled but no objects are in Archive tiers, objects are accessed too frequently for tiering. If Archive tiers contain objects but costs are still high, the minimum object size (128KB) may be filtering out small objects.

3. **Review lifecycle policies from Step 3**: If lifecycle policies are missing, create policies to transition infrequently accessed data. If policies exist but are not executing (Step 5 shows errors), fix the policy configuration. If policies are too aggressive, data may be in cold storage that is frequently accessed.

4. **Cross-reference with access patterns from Step 8**: If access logs show frequent access to objects in cold storage, transition policies are too aggressive. If access logs show rarely accessed objects in Standard, policies are too conservative.

5. **Assess EBS optimization from Step 7**: If GP2 volumes exist that could use GP3, consider migration for cost savings. If Provisioned IOPS volumes have low IOPS utilization, consider GP3. If volumes are in cold storage tiers, verify they are not needed.

If the above analysis is inconclusive: Review S3 Storage Lens for comprehensive storage analysis. Analyze access patterns by prefix to identify tiering candidates. Consider S3 Object Lock requirements that may prevent tiering. Evaluate retrieval patterns for Glacier data.
