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

1. Analyze AWS service health from Playbook step 1 to verify EC2 service availability in the region. If service health indicates issues or the instance is not in "running" state, the instance-level issue must be resolved first.

2. If security group inbound rules from Playbook step 2 do not allow SSH (port 22) from the client IP address or CIDR block, network access is blocked at the security group level. Verify the source IP is explicitly permitted.

3. If instance configuration from Playbook step 3 shows no public IP or Elastic IP and the instance is in a private subnet, SSH is only possible via bastion host, VPN, or Systems Manager Session Manager.

4. If route table from Playbook step 8 lacks a route to an internet gateway (0.0.0.0/0 -> igw-*), instances in public subnets cannot receive inbound internet traffic including SSH.

5. If Network ACL from Playbook step 8 contains Deny rules for port 22 or ephemeral ports (1024-65535), NACL rules are blocking SSH traffic. NACLs are stateless and require both inbound and outbound rules.

6. If key pair from Playbook step 4 does not match the key pair used for connection attempts, authentication will fail with "Permission denied" errors rather than timeouts.

7. If IMDSv2 configuration from Playbook step 5 shows IMDSv2 is required with a hop limit of 1, and SSH is attempted through a proxy or bastion, metadata service requests may fail affecting instance configuration.

8. If VPC Flow Logs from Playbook step 9 show REJECT actions for traffic to instance port 22, identify the rejecting component (security group shows as REJECT, NACL shows as REJECT with explicit rule number).

9. If serial console output from Playbook step 7 shows boot failures or SSH daemon errors, the instance-level SSH service is not running properly.

If no correlation is found from the collected data: extend VPC Flow Log query timeframes to 30 minutes, verify client-side firewall rules, check for instance-level iptables/firewalld rules, and examine SSH daemon configuration. Connection failures may result from host-based firewalls, SSH service crashes, or disk full conditions preventing SSH daemon operation.
