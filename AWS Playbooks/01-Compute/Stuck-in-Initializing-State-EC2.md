# EC2 Instance Stuck in "Initializing" State

## Meaning

An EC2 instance remains in the initializing state (triggering alarms like EC2InstanceStatusCheckFailed or EC2InstanceSystemStatusCheckFailed) because the instance cannot complete its boot process due to CloudWatch metrics indicating high CPU, disk, or memory usage, failing status checks, system log errors, initialization script failures preventing the instance from reaching a ready state, or user data script execution issues. Instances cannot complete startup, applications remain unavailable, and status check failures prevent instance readiness. This affects the compute layer and blocks instance deployment, typically caused by resource constraints, initialization script failures, or AMI configuration issues; if instances host container workloads, container initialization may be blocked and applications may experience deployment delays.

## Impact

Instances cannot complete startup; applications remain unavailable; services cannot initialize; status check failures prevent instance readiness; EC2InstanceStatusCheckFailed alarms fire; instances remain in initializing state indefinitely; boot process hangs; system services fail to start; initialization scripts timeout or fail. EC2InstanceSystemStatusCheckFailed alarms may fire; if instances host container workloads, container initialization may be blocked and applications may experience deployment delays; instance health appears degraded in CloudWatch dashboards; Auto Scaling may mark instance as unhealthy.

## Playbook

1. Verify instance `<instance-id>` exists and is not terminated, and AWS service health for EC2 in region `<region>` is normal.
2. Retrieve CloudWatch metrics for EC2 instance `<instance-id>` including CPUUtilization, DiskReadOps, DiskWriteOps, and MemoryUtilization over the last 1 hour to identify resource constraints, analyzing resource utilization patterns.
3. Retrieve the EC2 Instance `<instance-id>` in region `<region>` and inspect its status checks, instance state, system status check results, and instance state transitions.
4. Query CloudWatch Logs for log groups containing system logs for instance `<instance-id>` and filter for error patterns in `/var/log/messages` or `/var/log/syslog` indicating initialization failures, including user data script execution errors.
5. Retrieve CloudWatch alarms associated with instance `<instance-id>` and check for alarms in ALARM state related to status checks or system health, verifying alarm configurations.
6. Retrieve the EC2 Instance `<instance-id>` user data configuration and verify user data script is executing correctly, checking user data script syntax and execution status.
7. Retrieve the EC2 Instance `<instance-id>` launch template or AMI configuration and verify AMI or launch template is valid, checking for AMI configuration issues.
8. List EC2 instances in region `<region>` with the same instance type and AMI as `<instance-id>` to verify if the issue is instance-specific or affects multiple instances, analyzing instance state patterns.
9. Query CloudWatch Logs for log groups containing EC2 instance serial console output for instance `<instance-id>` and filter for boot errors or initialization failures, checking console output.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when EC2InstanceStatusCheckFailed or EC2InstanceSystemStatusCheckFailed alarms first triggered. This timestamp marks when initialization stalled.

2. If CloudWatch metrics (from Playbook step 2) show high CPUUtilization or DiskReadOps during initialization, resource exhaustion during boot is preventing completion. The instance may be undersized for the boot workload.

3. If status check inspection (from Playbook step 3) shows system status check failures, the issue is at the hypervisor or infrastructure level. If instance status check fails, the issue is within the guest OS.

4. If system logs (from Playbook step 4) contain user data script errors or timeout messages, examine user data configuration (from Playbook step 6). Script execution failures are blocking instance readiness.

5. If comparing with similar instances (from Playbook step 8) shows this instance alone is stuck while others launched from the same AMI succeeded, the issue is instance-specific (placement, availability zone capacity, or ephemeral hardware issue).

6. If multiple instances from the same AMI or launch template (from Playbook step 7) show initialization failures, examine AMI configuration and launch template for systemic issues like incorrect kernel parameters or missing drivers.

7. If serial console output (from Playbook step 9) shows boot errors, kernel panics, or filesystem mount failures, the boot process itself is failing before reaching user data execution.

8. If initialization times exceed normal thresholds compared to historical patterns (from Playbook step 8), EBS volume attachment delays or IMDS connectivity issues may be extending boot time.

If no correlation is found: extend analysis to 2 hours, review EBS volume performance metrics, check network interface configuration, verify placement group constraints, and examine IMDS initialization for connectivity issues.
