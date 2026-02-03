# Network Security Audit

## Meaning

Network security audit indicates that network security configurations may be misconfigured, overly permissive, or violate security best practices (triggering alarms like NetworkSecurityAuditFailed or OverlyPermissiveNetworkConfig) because VPC security configurations show violations, network ACLs are misconfigured, route tables allow insecure routing, VPC Flow Logs indicate suspicious traffic patterns, or network security policies are not enforced. Network security configurations show violations, VPC Flow Logs indicate suspicious traffic, network ACLs are misconfigured, and network security audit findings indicate policy violations. This affects the security layer and network access control, typically caused by misconfigured network security settings, lack of network security monitoring, or security policy violations; if network security protects container workloads, container network policies may be misconfigured and applications may experience security risks.

## Impact

NetworkSecurityAuditFailed alarms fire; OverlyPermissiveNetworkConfig alarms fire; network access is overly permissive; security policies are violated; suspicious network traffic is detected; network security monitoring fails. Network security configurations show violations; if network security protects container workloads, container network policies may be misconfigured, pod network access may be overly permissive, and container applications may experience security risks; applications may experience security vulnerabilities or unauthorized network access risks.

## Playbook

1. Retrieve the VPC `<vpc-id>` configuration and inspect its security group associations, network ACL configurations, and route table settings, verifying network security configuration.
2. List network ACLs in VPC `<vpc-id>` and retrieve ACL rule configurations to identify overly permissive or misconfigured rules.
3. List route tables in VPC `<vpc-id>` and retrieve route configurations to identify insecure routing or misconfigured routes.
4. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for suspicious traffic patterns including unauthorized access attempts or port scans within the last 7 days.
5. Retrieve Security Hub findings for network security compliance checks and filter for findings with severity 'HIGH' or 'CRITICAL' related to network security misconfigurations.
6. Retrieve CloudWatch metrics for VPC Flow Logs including AllowedTraffic and DeniedTraffic over the last 7 days to identify network traffic patterns.
7. Compare network security configuration change timestamps with security policy violation timestamps within 24 hours and verify whether network changes violate security policies, using CloudWatch Logs containing CloudTrail events as supporting evidence.
8. Retrieve the VPC `<vpc-id>` Flow Log configuration and verify whether Flow Logs are enabled and configured correctly, checking network security monitoring.

## Diagnosis

1. **Analyze Security Hub findings from Step 5**: If HIGH/CRITICAL findings identify specific network misconfigurations, address these first. If findings indicate missing VPC Flow Logs, enable them immediately from Step 8. If findings indicate insecure routing, review route tables from Step 3.

2. **Evaluate VPC Flow Logs from Step 4**: If suspicious traffic patterns are detected (port scans, unusual source IPs), investigate the source. If flow logs show high volumes of denied traffic, security controls are working but attack surface exists. If flow logs show unexpected allowed traffic, rules are too permissive.

3. **Review network ACL rules from Step 2**: If ACLs allow all traffic from 0.0.0.0/0, they provide no security value - all filtering is done by security groups. If ACLs have deny rules that conflict with expected traffic, connectivity issues may result. If ACL rule numbers are improperly ordered, unexpected behavior occurs.

4. **Cross-reference route tables from Step 3**: If routes direct traffic to unknown or suspicious targets, investigate. If routes bypass security controls (NAT Gateway, firewall), this is a security risk. If routes to internet gateway are broader than necessary, restrict to specific subnets.

5. **Assess configuration changes from Step 7**: If network changes correlate with security violations, recent modifications introduced vulnerabilities. If changes are authorized, verify implementation matches intended configuration.

If the above analysis is inconclusive: Verify AWS Network Firewall or third-party firewall configurations. Check Transit Gateway routing if multi-VPC architecture. Review VPC peering connections for unexpected access paths. Examine PrivateLink endpoints for service exposure.
