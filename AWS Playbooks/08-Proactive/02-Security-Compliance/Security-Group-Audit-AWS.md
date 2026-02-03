# Security Group Audit

## Meaning

Security group audit indicates that security group rules may be overly permissive, misconfigured, or violate security best practices (triggering alarms like OverlyPermissiveSecurityGroup or SecurityGroupAuditFailed) because security group rules allow overly broad access, unused security groups exist, security group rules violate least privilege principles, security group ingress rules allow access from 0.0.0.0/0, or security group egress rules are unrestricted. Security groups show overly permissive rules, security group audit findings indicate violations, unused security groups are detected, and security group configurations violate security policies. This affects the security layer and network access control, typically caused by misconfigured security group rules, lack of security group lifecycle management, or security policy violations; if security groups protect container workloads, container network access may be overly permissive and applications may experience security risks.

## Impact

SecurityGroupAuditFailed alarms fire; OverlyPermissiveSecurityGroup alarms fire; network access is overly permissive; security policies are violated; unused security groups consume resources; security group rules violate least privilege principles. Security group configurations show overly permissive rules; if security groups protect container workloads, container network access may be overly permissive, pod network policies may be misconfigured, and container applications may experience security risks; applications may experience security vulnerabilities or unauthorized access risks.

## Playbook

1. List security groups in region `<region>` and retrieve security group configurations including ingress and egress rules to identify overly permissive rules.
2. Retrieve the Security Group `<security-group-id>` configuration and inspect its ingress rules for rules allowing access from 0.0.0.0/0 or overly broad CIDR blocks, verifying rule restrictiveness.
3. Retrieve the Security Group `<security-group-id>` configuration and inspect its egress rules for rules allowing unrestricted outbound access, verifying egress rule restrictions.
4. List EC2 instances in region `<region>` and verify security group attachments to identify unused security groups not attached to any resources.
5. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for traffic patterns indicating overly permissive security group rules within the last 7 days.
6. Retrieve Security Hub findings for security group compliance checks and filter for findings with severity 'HIGH' or 'CRITICAL' related to security group misconfigurations.
7. Compare security group rule modification timestamps with security policy change timestamps within 24 hours and verify whether security group changes violate security policies, using CloudWatch Logs containing CloudTrail events as supporting evidence.
8. Retrieve the Security Group `<security-group-id>` rule usage metrics and verify whether rules are actively used or unused, checking rule utilization patterns.

## Diagnosis

1. **Analyze Security Hub findings from Step 6**: If HIGH/CRITICAL findings identify specific security groups with 0.0.0.0/0 ingress, these require immediate remediation. If findings indicate open SSH (port 22) or RDP (port 3389), restrict to specific IP ranges or use bastion hosts. If findings indicate all traffic allowed, implement least privilege rules.

2. **Evaluate unused security groups from Step 4**: If security groups are not attached to any resources, they are candidates for deletion. If security groups are attached but their rules are not used (Step 8), rules may be overly broad or resources are misconfigured.

3. **Review VPC Flow Logs from Step 5**: If flow logs show traffic matching permissive rules, the rules are actively in use. If flow logs show rejected traffic that would be allowed by current rules, rules may be correct but source IPs are blocked elsewhere. If no traffic matches rules, rules may be unnecessary.

4. **Cross-reference recent changes from Step 7**: If security group modifications correlate with security findings, recent changes introduced vulnerabilities. If modifications were authorized change requests, verify they match intended configuration.

5. **Assess egress rules from Step 3**: If egress allows all traffic (0.0.0.0/0 on all ports), consider restricting to necessary destinations. If egress is to known malicious IPs (check threat intelligence), immediate action required.

If the above analysis is inconclusive: Use VPC Reachability Analyzer to understand actual network paths. Review network ACLs for additional controls. Check if security groups are referenced by other security groups creating indirect access. Verify AWS Network Firewall or third-party firewall rules.
