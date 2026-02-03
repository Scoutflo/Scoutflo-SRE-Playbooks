# Unused Resource Cleanup

## Meaning

Unused resource cleanup indicates that AWS resources are no longer needed but remain provisioned, consuming costs without providing value (triggering alarms like UnusedResourceDetected or OrphanedResourceDetected) because EC2 instances are stopped but not terminated, EBS volumes are unattached, Elastic IPs are unassociated, security groups are unattached, or resources show no activity over extended periods. Resources show no activity metrics, resources are in stopped or detached state, resources are not associated with active workloads, and resource creation timestamps indicate abandonment. This affects the cost management layer and resource lifecycle management, typically caused by resource lifecycle management failures, abandoned resource detection gaps, or resource cleanup automation issues; if unused resources relate to container workloads, container resources may be orphaned and applications may experience unnecessary cost overhead.

## Impact

UnusedResourceDetected alarms fire; OrphanedResourceDetected alarms fire; unnecessary costs accumulate; resources consume costs without providing value; resource lifecycle management fails; abandoned resources are not cleaned up. Resources show no activity or are in unused state; if unused resources relate to container workloads, container resources may be orphaned, pod resources may be abandoned, and container applications may experience unnecessary cost overhead; applications may experience cost inefficiencies or resource waste.

## Playbook

1. List EC2 instances in region `<region>` with state 'stopped' and retrieve instance stop timestamps to identify instances stopped for extended periods without termination.
2. List EBS volumes in region `<region>` with state 'available' and retrieve volume attachment status to identify unattached volumes.
3. List Elastic IP addresses in region `<region>` and verify association status to identify unassociated Elastic IPs.
4. List security groups in region `<region>` and verify attachment to EC2 instances or other resources to identify unattached security groups.
5. Query CloudWatch Logs for log groups containing resource activity logs and filter for patterns indicating resource inactivity or abandonment over the last 90 days.
6. Retrieve Cost Explorer data for resource costs in region `<region>` over the last 30 days and compare with resource activity metrics to identify cost-activity mismatches.
7. Compare resource creation timestamps with last activity timestamps and verify whether resources have been inactive since creation, using resource activity logs as supporting evidence.
8. List CloudFormation stacks in region `<region>` with status 'DELETE_FAILED' or 'ROLLBACK_COMPLETE' and verify whether stacks contain unused resources, checking stack resource status.

## Diagnosis

1. **Analyze stopped instances from Step 1**: If instances have been stopped for 30+ days, they are likely abandoned. If instances have AMIs or snapshots created, they may be intentionally stopped for reference. If instances have no tags indicating purpose, they are candidates for termination.

2. **Evaluate unattached EBS volumes from Step 2**: If volumes have been unattached for 30+ days, create snapshots and delete the volumes. If volumes have recent detachment, they may be awaiting re-attachment. If volumes have no snapshots, snapshot before deletion for safety.

3. **Review Elastic IP charges from Step 3**: If EIPs are unassociated, they incur hourly charges without providing value. If EIPs were recently unassociated, they may be needed soon. If EIPs have been unassociated for 30+ days, release them.

4. **Cross-reference with failed stacks from Step 8**: If CloudFormation stacks failed to delete, investigate and manually clean up resources. If stacks are in rollback state, they may contain orphaned resources. If stacks have deletion protection, verify if still needed.

5. **Assess cost impact from Step 6**: Quantify costs of unused resources to prioritize cleanup. If costs are significant, implement immediate cleanup. If costs are minimal, schedule for regular cleanup cycle.

If the above analysis is inconclusive: Check resource tags for owner and project information. Query CloudTrail for any recent API activity against resources. Verify resources are not part of disaster recovery or backup retention. Contact resource owners before deletion.
