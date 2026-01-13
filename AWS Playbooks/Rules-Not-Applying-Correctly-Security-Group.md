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

1. Compare security group rule modification timestamps with connection failure timestamps within 5 minutes and verify whether connection failures began shortly after rule changes, using security group configuration data as supporting evidence.
2. Correlate security group association change timestamps with traffic blocking timestamps and verify whether traffic blocking occurred after security group association changes, using EC2 instance events as supporting evidence.
3. Compare IP address or CIDR block restriction change timestamps with connection failure timestamps within 5 minutes and verify whether rule restrictions blocked legitimate traffic, using security group rule events as supporting evidence.
4. Compare AWS WAF rule modification timestamps with connection failure timestamps and verify whether WAF rules blocked traffic before security groups, using WAF rule events as supporting evidence.
5. Analyze connection failure frequency over the last 15 minutes to determine if failures are constant (rule configuration issue) or intermittent (network routing).

If no correlation is found within the specified time windows: extend timeframes to 30 minutes, review alternative evidence sources including network ACL rules and instance-level firewall rules, check for gradual issues like rule evaluation order, verify external dependencies like source IP address changes, examine historical patterns of security group rule effectiveness, check for AWS Shield DDoS protection interactions, verify IPv6 security group rule configuration. Connection failures may result from network ACL rule conflicts, instance-level firewall rules, source IP address changes, AWS WAF rule interactions, or security group rule propagation delays rather than immediate security group rule changes.
