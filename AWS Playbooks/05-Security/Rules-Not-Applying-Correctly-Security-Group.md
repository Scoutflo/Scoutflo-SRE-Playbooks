# Security Group Rules Not Applying Correctly

## Meaning

Security group rules fail to allow expected traffic (triggering connection timeout errors or SecurityGroupRuleNotEffective alarms) because incorrect ports are open, conflicting inbound and outbound rules block traffic, security groups are not associated with correct instances, rules restrict IP addresses or CIDR blocks incorrectly, connectivity tests fail, security group rule evaluation order affects access, or rule quotas are reached. Expected network traffic is blocked, connection timeouts occur, and security group rules are ineffective. This affects the security and networking layers and blocks network access, typically caused by rule configuration issues, evaluation order problems, or quota limits; if using AWS WAF, WAF rules may interact with security groups and applications may experience network access failures.

## Impact

Expected network traffic is blocked; connection timeouts occur; security group rules are ineffective; application communication fails; service endpoints become unreachable; connection refused errors appear; network access is denied; firewall rules do not work as expected; operational tasks requiring network access fail. SecurityGroupRuleNotEffective alarms fire; if using AWS WAF, WAF rules may interact with security groups; applications may experience errors or performance degradation due to network access failures; service-to-service communication may be blocked.

## Playbook

1. Verify Security Group `<security-group-id>` and EC2 instance `<instance-id>` exist, and AWS service health for EC2 and VPC in region `<region>` is normal.
2. Retrieve the Security Group `<security-group-id>` associated with EC2 instance `<instance-id>` and verify correct ports (e.g., 22 for SSH, 80 for HTTP) are open in inbound rules, checking port ranges and protocols.
3. Retrieve the Security Group `<security-group-id>` and check for conflicting inbound and outbound rules that could block traffic, verify rule evaluation logic (explicit deny wins), and review rules restricting IP addresses or CIDR blocks, verifying rule evaluation order and source CIDR blocks.
4. Verify the Security Group `<security-group-id>` is associated with the correct instances by retrieving instance security group associations for instance `<instance-id>`, checking multiple security group associations.
5. Retrieve the Security Group `<security-group-id>` rule quotas and verify security group rule limits are not exceeded, checking rule count against quotas.
6. Retrieve CloudWatch metrics for instance `<instance-id>` including NetworkIn and NetworkOut to verify network activity, checking if traffic is reaching the instance.
7. Query CloudWatch Logs for log groups containing VPC Flow Logs or WAF logs and filter for blocked traffic related to security group `<security-group-id>`, checking flow log and WAF rule evaluation.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify EC2 and VPC service availability in the region. If service health indicates issues, rule application failures may be AWS-side requiring monitoring rather than configuration changes.

2. If security group inbound rules from Playbook step 2 do not include the required port (22 for SSH, 80 for HTTP, 443 for HTTPS), traffic on that port is blocked. Security groups are deny-by-default for inbound traffic.

3. If security group rules from Playbook step 3 show conflicting configurations, remember that security groups only have Allow rules (no explicit Deny). If traffic is blocked, it is because no matching Allow rule exists. Check for overly restrictive CIDR blocks or security group references.

4. If security group association from Playbook step 4 shows the security group is not attached to the target instance, or multiple security groups are attached with conflicting intent, verify the correct security groups are associated. Multiple security groups are evaluated with OR logic (any Allow permits traffic).

5. If rule quota from Playbook step 5 shows the security group has reached its rule limit (default 60 inbound + 60 outbound), additional rules cannot be added. Check current rule count against quota.

6. If NetworkIn/NetworkOut metrics from Playbook step 6 show traffic is reaching the instance, the issue may be at the application layer rather than security group. Verify the application is listening on the expected port.

7. If VPC Flow Logs or WAF logs from Playbook step 7 show REJECT actions, identify the rejecting layer. Security group rejections appear in Flow Logs with a specific action type; WAF rejections appear in WAF logs with rule IDs.

If no correlation is found from the collected data: extend VPC Flow Log query timeframes to 30 minutes, verify Network ACL rules are not blocking traffic (NACLs are evaluated before security groups), check for instance-level firewall rules (iptables, Windows Firewall), and examine source IP address changes. Connection failures may result from security group propagation delays (typically seconds), client-side NAT IP changes, or AWS Shield DDoS protection activations.

