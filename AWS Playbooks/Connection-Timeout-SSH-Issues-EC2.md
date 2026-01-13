# EC2 Instance Connection Timeout (SSH Issues)

## Meaning

EC2 instance SSH connections timeout or fail (triggering alarms like EC2InstanceStatusCheckFailed or connection timeout errors) because security group rules block SSH access, the instance lacks a public IP address, key pair mismatches occur, network connectivity issues prevent SSH access, or Systems Manager Session Manager is not configured. Users experience "Connection timed out" or "Connection refused" errors when attempting SSH access, instances show "running" state but status checks may indicate failures in AWS console, and security group rules may block port 22 access. This affects the compute layer and prevents remote access, typically caused by security group restrictions, missing public IP addresses, network connectivity issues, or IMDSv2 enforcement blocking access; if instances host container workloads, pod troubleshooting may be blocked and container orchestration tasks may fail.

## Impact

EC2InstanceStatusCheckFailed alarms may fire; administrators cannot access instances; SSH connection timeout errors occur; "Connection timed out" or "Connection refused" messages appear in logs; instance remains inaccessible; remote management fails; troubleshooting is blocked. Instance shows "running" state in AWS console but status checks indicate failures; manual intervention required; operational tasks delayed; users cannot perform administrative actions; configuration changes cannot be applied. Instance health appears degraded in CloudWatch dashboards; Auto Scaling may mark instance as unhealthy; if instances host container workloads, pod scheduling may fail, containers may be unable to start, or cluster connectivity issues may occur; container orchestration tasks may show failures; applications may experience errors or performance degradation.

## Playbook

1. Verify instance `<instance-id>` is in "running" state and AWS service health for EC2 in region `<region>` is normal.
2. Retrieve the Security Group `<security-group-id>` associated with EC2 instance `<instance-id>` and inspect inbound rules for SSH port 22 access, verifying source IP addresses or CIDR blocks.
3. Retrieve the EC2 Instance `<instance-id>` in region `<region>` and verify public IP address or Elastic IP assignment, checking if instance is in a public subnet with internet gateway route.
4. Verify the key pair `<key-pair-name>` matches the key pair assigned to instance `<instance-id>` by retrieving instance key pair configuration.
5. Retrieve the EC2 Instance `<instance-id>` metadata service configuration and verify IMDSv2 enforcement settings.
6. Retrieve the EC2 Instance `<instance-id>` IAM role configuration and verify instance profile is attached, checking IAM role association.
7. Retrieve CloudWatch Logs for EC2 serial console output for instance `<instance-id>` and filter for connection errors or authentication failures.
8. Retrieve the Route Table `<route-table-id>` and Network ACL `<nacl-id>` for subnet containing instance `<instance-id>` and verify route to internet gateway (0.0.0.0/0 → igw-id) exists and inbound and outbound rules allow SSH traffic (port 22 TCP).
9. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for blocked traffic to instance `<instance-id>` on port 22.

## Diagnosis

1. Compare security group rule modification timestamps with SSH connection failure timestamps within 5 minutes and verify whether connection failures began after security group changes, using security group configuration data as supporting evidence.
2. Correlate instance public IP assignment timestamps with SSH connection attempt timestamps and verify whether connection failures occur when instances lack public IP addresses, using instance configuration events as supporting evidence.
3. Compare key pair assignment timestamps with SSH authentication failure timestamps within 5 minutes and verify whether authentication failures began after key pair changes, using instance metadata as supporting evidence.
4. Compare IMDSv2 enforcement change timestamps with SSH connection failure timestamps within 5 minutes and verify whether IMDSv2 enforcement blocked access, using instance metadata service configuration as supporting evidence.
5. Analyze SSH connection failure frequency over the last 15 minutes to determine if failures are constant (configuration issue) or intermittent (network connectivity).

If no correlation is found within the specified time windows: extend timeframes to 30 minutes, review alternative evidence sources including network ACL rules and route table configurations, check for gradual issues like security group rule drift, verify external dependencies like internet gateway connectivity and AWS service health, examine historical patterns of SSH access. SSH connection failures may result from network-level blocking, VPC routing issues, instance-level firewall rules, IMDSv2 enforcement, or AWS service health issues rather than immediate security group changes.
