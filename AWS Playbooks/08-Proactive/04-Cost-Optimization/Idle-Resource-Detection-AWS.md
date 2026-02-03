# Idle Resource Detection

## Meaning

Idle resource detection indicates that AWS resources are running but not actively utilized, consuming costs without providing value (triggering alarms like IdleResourceDetected or UnusedResourceDetected) because EC2 instances show low CPU utilization, RDS databases have minimal connection activity, EBS volumes have no I/O operations, Lambda functions are not invoked, or S3 buckets have no access patterns. Resources show low utilization metrics, resource activity logs indicate minimal usage, cost metrics show resources consuming costs without activity, and resource monitoring indicates idle state. This affects the cost management layer and resource optimization, typically caused by over-provisioning, abandoned resources, or resource lifecycle management failures; if idle resources host container workloads, container resources may be wasted and applications may experience unnecessary cost overhead.

## Impact

IdleResourceDetected alarms fire; UnusedResourceDetected alarms fire; unnecessary costs accumulate; resources consume costs without providing value; cost optimization opportunities are missed; resource utilization is inefficient. Low utilization metrics indicate idle resources; if idle resources host container workloads, container resources may be wasted, pod resources may be over-provisioned, and container applications may experience unnecessary cost overhead; applications may experience cost inefficiencies or resource waste.

## Playbook

1. List EC2 instances in region `<region>` and retrieve CloudWatch metrics for CPUUtilization and NetworkIn over the last 30 days to identify instances with consistently low utilization.
2. List RDS DB instances in region `<region>` and retrieve CloudWatch metrics for DatabaseConnections and CPUUtilization over the last 30 days to identify databases with minimal activity.
3. List EBS volumes in region `<region>` and retrieve CloudWatch metrics for VolumeReadOps and VolumeWriteOps over the last 30 days to identify volumes with no I/O operations.
4. List Lambda functions in region `<region>` and retrieve CloudWatch metrics for Invocations and Duration over the last 30 days to identify functions with no invocations.
5. List S3 buckets in region `<region>` and retrieve CloudWatch metrics for BucketSizeBytes and NumberOfObjects, then query S3 access logs to identify buckets with no access patterns over the last 30 days.
6. Query CloudWatch Logs for log groups containing resource activity logs and filter for patterns indicating resource inactivity or minimal usage over the last 30 days.
7. Retrieve Cost Explorer data for resource types in region `<region>` over the last 30 days and compare with resource utilization metrics to identify cost-utilization mismatches.
8. Compare resource creation timestamps with last activity timestamps and verify whether resources have been idle since creation, using resource activity logs as supporting evidence.

## Diagnosis

1. **Analyze EC2 utilization from Step 1**: If CPUUtilization is consistently below 10% and NetworkIn is near zero for 30+ days, the instance is idle. If utilization shows periodic spikes, the resource may be used for batch jobs and is not truly idle. Cross-reference with Cost Explorer data from Step 7 to confirm cost-utilization mismatch.

2. **Evaluate RDS activity from Step 2**: If DatabaseConnections is zero or near-zero for 30+ days, the database is unused. If connections exist but are minimal, verify whether these are health checks versus actual application usage. Check if the database is a replica or standby for DR purposes.

3. **Assess EBS volume activity from Step 3**: If VolumeReadOps and VolumeWriteOps are both zero for 30+ days and the volume state is 'available' (unattached), this is a confirmed orphaned volume. If attached but showing no I/O, verify the attached instance is also idle.

4. **Review Lambda function activity from Step 4**: If Invocations metric is zero since function creation, the function is unused. If the function was recently created (within 7 days), it may be in development. Cross-reference with S3 bucket access patterns from Step 5 for related resources.

5. **Determine resource purpose from Step 8**: If resource creation timestamps are old and last activity timestamps are equally old, resources were likely abandoned after a project completed. If resources have environment tags indicating "dev" or "test", they may be candidates for immediate cleanup.

If the above analysis is inconclusive: Check resource tags for owner and purpose information. Query CloudTrail for any API calls to the resources. Verify whether resources are part of CloudFormation stacks that may be cleaned up together. Consult with application teams before recommending termination of any resources with unclear purpose.
