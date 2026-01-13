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
7. Retrieve the EC2 Instance `<instance-id>` spot instance configuration if using spot instances and verify spot instance interruption status, checking spot instance availability.
8. Query CloudWatch Logs for log group containing system logs for instance `<instance-id>` and filter for boot errors, initialization failures, or system log entries indicating startup issues, including user data script errors.
9. Retrieve the EBS volume `<volume-id>` attached to instance `<instance-id>` and inspect its state and attachment configuration, verifying volume availability.
10. Retrieve the EC2 Instance `<instance-id>` launch template configuration and verify launch template is valid, checking template syntax and parameters.

## Diagnosis

1. Compare EC2 instance state change timestamps with IAM role attachment timestamps within 5 minutes and verify whether instance launch failures began shortly after IAM role changes, using instance configuration data as supporting evidence.
2. Correlate instance launch failure timestamps with instance type availability timestamps and verify whether failures consistently occur when instance types are unavailable, using EC2 instance listing data as supporting evidence.
3. Compare system log error timestamps with instance launch timestamps within 5 minutes and verify whether boot errors or initialization failures occurred during instance startup, using CloudWatch Logs as supporting evidence.
4. Compare EBS volume state change timestamps with instance launch timestamps within 10 minutes and verify whether volume attachment or corruption issues prevented instance startup, using volume events as supporting evidence.
5. Analyze instance state transition frequency over the last 15 minutes to determine if launch failures are constant (configuration issue) or intermittent (capacity constraints).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including CloudWatch metrics and instance events, check for gradual issues like regional capacity constraints, verify external dependencies like AMI availability, examine historical patterns of similar launch failures, check for EC2 instance tenancy issues, verify EC2 instance placement group constraints. Instance launch failures may result from regional capacity issues, AMI corruption, instance type unavailability, EBS snapshot issues, EC2 instance dedicated host requirements, or user data script failures rather than immediate configuration changes.

