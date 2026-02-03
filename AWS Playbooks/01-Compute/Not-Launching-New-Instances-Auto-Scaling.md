# EC2 Auto Scaling Not Launching New Instances

## Meaning

An Auto Scaling Group fails to launch new instances (triggering alarms like AutoScalingGroupDesiredCapacityNotMet or EC2AutoScalingLaunchFailure) because launch template or configuration errors prevent instance launches, AMI validation fails, account instance limits are reached, subnet or IP address availability constraints exist, IAM role permissions are insufficient for instance launch, or Auto Scaling Group launch configuration is invalid. Auto Scaling cannot add capacity, desired capacity cannot be met, and applications cannot scale. This affects the compute and scaling layer and prevents service scaling, typically caused by launch configuration issues, capacity constraints, or permission problems; if instances host container workloads, Auto Scaling failures may affect container orchestration and applications may experience scaling delays.

## Impact

Auto Scaling cannot add capacity; desired capacity cannot be met; applications cannot scale; service availability degrades; AutoScalingGroupDesiredCapacityNotMet alarms fire; load cannot be distributed across additional instances; scaling policies fail to execute; capacity constraints prevent service scaling. EC2AutoScalingLaunchFailure alarms may fire; if instances host container workloads, Auto Scaling failures may affect container orchestration and applications may experience scaling delays; service capacity remains insufficient; user-facing services experience performance degradation.

## Playbook

1. Verify Auto Scaling Group `<asg-name>` exists and AWS service health for EC2 and Auto Scaling in region `<region>` is normal.
2. Retrieve the Auto Scaling Group `<asg-name>` in region `<region>` and inspect its desired capacity, current capacity, launch template configuration, and scaling activity history, verifying desired vs current capacity mismatch.
3. Retrieve the Launch Template `<launch-template-id>` referenced by Auto Scaling Group `<asg-name>` and inspect its AMI ID, instance type, IAM role, and security group configuration, verifying launch template validity.
4. List EC2 instances in region `<region>` launched by Auto Scaling Group `<asg-name>` and check their states to identify launch failures, analyzing instance state patterns.
5. Query CloudWatch Logs for log groups containing Auto Scaling events and filter for launch failure events or error patterns related to Auto Scaling Group `<asg-name>`, including failure reason details.
6. Retrieve the IAM role `<role-name>` attached to Launch Template `<launch-template-id>` and inspect its policy permissions for EC2 launch capabilities, verifying IAM permissions.
7. Retrieve CloudWatch metrics for EC2 account limits and verify instance limits, checking if account limits are reached preventing launches.
8. Retrieve the Auto Scaling Group `<asg-name>` subnet configuration and verify subnet IP address availability, checking if subnet capacity constraints prevent launches.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Auto Scaling Group or launch template modification events related to `<asg-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze Auto Scaling Group activity history (from Playbook step 2) to identify when launch failures first appeared. The scaling activity failure timestamps and error messages establish the correlation baseline.

2. If Auto Scaling events (from Playbook step 5) show "Failed to launch instance" with AMI-related errors, verify AMI validity (from Playbook step 3). The AMI may be deregistered, corrupted, or unavailable in the target availability zone.

3. If CloudTrail shows launch template modifications (from Playbook step 9) around the failure timestamp, compare template versions. Invalid configurations (instance type, security groups, IAM role) cause launch failures.

4. If EC2 account limits (from Playbook step 7) show approaching or exceeded limits, instance limits are preventing launches. Request limit increases or use different instance types.

5. If subnet configuration (from Playbook step 8) shows low available IP addresses around failure timestamps, IP exhaustion is preventing instance launches. Expand subnet CIDR or use additional subnets.

6. If IAM role permissions (from Playbook step 6) were modified around the failure time, missing EC2 launch permissions (ec2:RunInstances, iam:PassRole) are blocking instance creation.

7. If launch failures are intermittent (from Playbook step 4 comparison with similar instances), capacity constraints in specific availability zones may be causing failures during peak demand.

If no correlation is found: extend analysis to 2 hours, review AMI availability across regions, check regional capacity constraints, verify security group configuration, examine mixed instance policy settings, and check for instance refresh operation conflicts.
