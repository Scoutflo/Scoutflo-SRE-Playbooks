# Right-sizing Analysis

## Meaning

Right-sizing analysis indicates that AWS resources are over-provisioned or under-provisioned relative to actual utilization, leading to cost inefficiencies or performance issues (triggering alarms like OverProvisionedResource or UnderProvisionedResource) because EC2 instances have CPU/memory allocation exceeding utilization, RDS instances have instance class mismatches with workload requirements, EBS volumes have provisioned IOPS exceeding actual I/O needs, or resource metrics show consistent over or under-utilization patterns. Resources show utilization metrics significantly below or above allocation, cost metrics indicate over-provisioning, performance metrics indicate under-provisioning, and resource allocation does not match workload requirements. This affects the cost management layer and resource optimization, typically caused by initial over-provisioning, workload changes, or lack of utilization monitoring; if resources host container workloads, container resource requests may be misaligned and applications may experience cost inefficiencies or performance constraints.

## Impact

OverProvisionedResource alarms fire; UnderProvisionedResource alarms fire; unnecessary costs accumulate from over-provisioning; performance issues occur from under-provisioning; resource allocation does not match workload requirements; cost optimization opportunities are missed. Utilization metrics show significant allocation mismatches; if resources host container workloads, container resource requests may be misaligned, pod resource limits may be inappropriate, and container applications may experience cost inefficiencies or performance constraints; applications may experience cost waste or performance degradation.

## Playbook

1. Retrieve the EC2 Instance `<instance-id>` configuration and retrieve CloudWatch metrics for CPUUtilization, NetworkUtilization, and MemoryUtilization over the last 30 days to compare with instance type specifications.
2. Retrieve the RDS DB Instance `<db-instance-id>` configuration and retrieve CloudWatch metrics for CPUUtilization, DatabaseConnections, and FreeableMemory over the last 30 days to compare with instance class specifications.
3. Retrieve the EBS volume `<volume-id>` configuration and retrieve CloudWatch metrics for VolumeReadOps, VolumeWriteOps, and VolumeThroughputPercentage over the last 30 days to compare with provisioned IOPS.
4. List EC2 instances in region `<region>` and retrieve CloudWatch metrics for CPUUtilization and MemoryUtilization over the last 30 days to identify instances with consistent over or under-utilization patterns.
5. Query Cost Explorer data for EC2 instance types in region `<region>` over the last 30 days and compare instance type costs with utilization metrics to identify cost-utilization mismatches.
6. Retrieve CloudWatch metrics for RDS instance classes including CPUUtilization and DatabaseConnections over the last 30 days to identify instance classes with utilization mismatches.
7. Compare resource allocation specifications with actual utilization metrics over the last 30 days and verify whether allocations significantly exceed or fall below utilization, using CloudWatch metrics as supporting evidence.
8. Retrieve Cost Explorer recommendations for right-sizing opportunities in region `<region>` and verify recommendation alignment with utilization analysis.

## Diagnosis

1. **Analyze Cost Explorer recommendations from Step 8**: If recommendations suggest smaller instance types, cross-reference with utilization data from Step 1. If recommendations align with low utilization, the recommendation is valid. If utilization shows periodic spikes, smaller instance may cause performance issues during peaks.

2. **Evaluate EC2 utilization from Step 1 and Step 4**: If average CPUUtilization is below 20% and max is below 40% for 30 days, instance is over-provisioned. If average is above 80%, instance may be under-provisioned. If utilization varies significantly (high standard deviation), consider auto-scaling instead of right-sizing.

3. **Review RDS utilization from Step 2 and Step 6**: If FreeableMemory is consistently high (>70% of total), instance class is over-provisioned for memory. If CPUUtilization is consistently low but DatabaseConnections is high, the workload is I/O bound not compute bound. If both metrics are low, consider smaller instance class.

4. **Cross-reference EBS metrics from Step 3**: If VolumeThroughputPercentage is consistently below 20%, provisioned IOPS exceeds actual needs. If VolumeReadOps/WriteOps are near zero, volume may be unused. If metrics are high but not at capacity, current provisioning is appropriate.

5. **Assess cost impact from Step 5**: Calculate potential savings from right-sizing recommendations. If savings are minimal (<5%), the effort may not be worthwhile. If savings are significant (>20%), prioritize these instances for right-sizing.

If the above analysis is inconclusive: Review application performance metrics to correlate with infrastructure utilization. Consider memory utilization (requires CloudWatch agent) for memory-bound workloads. Analyze utilization during peak business hours separately from off-hours. Evaluate Graviton-based instances for potential cost-performance improvements.
