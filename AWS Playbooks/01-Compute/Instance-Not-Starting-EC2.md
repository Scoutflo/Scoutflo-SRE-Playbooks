# EC2 Instance Not Starting

## Meaning

An EC2 instance fails to reach the running state (triggering alarms like EC2InstanceStatusCheckFailed or EC2InstanceSystemStatusCheckFailed) because instance launch fails due to insufficient capacity, IAM role attachment issues, security group misconfiguration, instance type limits, the instance cannot pass system status checks, instance profile is missing, EBS volume attachment fails, or user data script errors prevent startup. New instances cannot launch, Auto Scaling cannot add capacity, and instance status checks fail. This affects the compute layer and blocks instance deployment, typically caused by capacity constraints, configuration issues, or system check failures; if instances host container workloads, container orchestration may fail and applications may experience deployment delays.

## Impact

New instances cannot launch; Auto Scaling cannot add capacity; applications remain unavailable; services cannot scale; capacity constraints prevent instance deployment; EC2InstanceStatusCheckFailed alarms fire; instances remain in pending or stopped state; launch template or AMI issues prevent instance startup; desired capacity cannot be met. EC2InstanceSystemStatusCheckFailed alarms fire; if instances host container workloads, container orchestration may fail, pod scheduling may be blocked, and container applications may experience deployment delays; applications may experience errors or performance degradation due to missing instance capacity.

## Playbook

1. Verify instance `<instance-id>` exists and is not terminated, and AWS service health for EC2 in region `<region>` is normal.
2. Retrieve the EC2 Instance `<instance-id>` in region `<region>` and inspect its state, status checks, and instance type configuration, verifying instance state transitions.
3. Retrieve the EC2 Instance `<instance-id>` account limits and list EC2 instances in region `<region>` with the same instance type to verify instance type availability and account quotas, checking for capacity constraints and analyzing capacity metrics.
4. Verify IAM role permissions for the instance by retrieving the IAM role `<role-name>` attached to instance `<instance-id>` and checking its policy permissions, verifying instance profile.
5. Retrieve the EC2 Instance `<instance-id>` instance profile configuration and verify instance profile is attached, checking instance profile attachment timing (can only attach at launch).
6. Retrieve the EC2 Instance `<instance-id>` spot instance configuration if using spot instances and verify spot instance interruption status, checking spot instance availability.
7. Query CloudWatch Logs for log group containing system logs for instance `<instance-id>` and filter for boot errors, initialization failures, or system log entries indicating startup issues, including user data script errors.
8. Retrieve the EBS volume `<volume-id>` attached to instance `<instance-id>` and inspect its state and attachment configuration, verifying volume availability.
9. Retrieve the EC2 Instance `<instance-id>` launch template configuration and verify launch template is valid, checking template syntax and parameters.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify EC2 service availability in the region. If service health indicates regional capacity issues or service degradation, launch failures may be AWS-side requiring monitoring or region/AZ change.

2. If instance state from Playbook step 2 shows the instance is stuck in "pending" state or transitions to "stopped" immediately, examine instance events for the specific failure reason (InsufficientInstanceCapacity, InvalidParameterValue, etc.).

3. If account limits from Playbook step 3 show the instance type quota is reached, new instances of that type cannot launch. Request a quota increase or use an alternative instance type.

4. If IAM role and instance profile from Playbook steps 4-5 show configuration issues (missing instance profile, role not attached, incorrect permissions), instance launch may fail or instances may launch without expected permissions.

5. If spot instance configuration from Playbook step 6 shows the instance was a spot instance that was terminated or spot capacity is unavailable, spot interruption or capacity constraints are the cause. Consider on-demand instances or diversified spot pools.

6. If system logs from Playbook step 7 show boot errors, kernel panics, or user data script failures, the instance launched but failed during initialization. Examine specific error messages for root cause.

7. If EBS volume from Playbook step 8 shows volume state is not "available" or "in-use", volume issues prevent instance startup. Check for volume corruption, snapshot availability, or encryption key access issues.

8. If launch template from Playbook step 9 contains invalid parameters (non-existent AMI, invalid instance type for the selected region, incompatible configurations), the launch fails before instance creation.

If no correlation is found from the collected data: extend CloudWatch Logs query timeframes to 1 hour, verify AMI exists and is available in the target region, check for placement group constraints, examine dedicated host availability if using dedicated tenancy, and verify VPC subnet has available IP addresses. Launch failures may result from Elastic IP limits, ENI limits in the subnet, or Auto Scaling group configuration issues.

