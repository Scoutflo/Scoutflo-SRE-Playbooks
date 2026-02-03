# NACL Blocking Expected Traffic

## Meaning

Network ACL (NACL) rules block expected traffic (triggering connectivity failures or VPCTrafficBlocked alarms) because NACL inbound or outbound rules deny required traffic, rule order prevents traffic flow, ephemeral port ranges are not allowed, NACL rule changes restrict network access, or subnet association changes affect traffic flow. Network traffic is blocked, connectivity between resources fails, and applications cannot communicate. This affects the networking layer and blocks service communication, typically caused by NACL rule misconfiguration, rule order issues, or missing ephemeral port rules; if NACLs are used with security groups, rule evaluation order may affect traffic and applications may experience connectivity failures.

## Impact

Network traffic is blocked; connectivity between resources fails; applications cannot communicate; NACL rules deny expected traffic; network access is restricted; service-to-service communication fails; user-facing connectivity errors occur; network security misconfiguration impacts functionality. VPCTrafficBlocked alarms may fire; if NACLs are used with security groups, rule evaluation order may affect traffic; applications may experience errors or performance degradation due to blocked connectivity; service-to-service communication may be completely blocked.

## Playbook

1. Verify Network ACL `<nacl-id>` exists and AWS service health for VPC in region `<region>` is normal.
2. Retrieve the Network ACL `<nacl-id>` in region `<region>` and inspect its inbound and outbound rules, rule order, and rule actions (allow/deny), verifying rule evaluation order.
3. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for denied traffic patterns related to Network ACL `<nacl-id>`, including denied traffic source and destination.
4. Retrieve CloudWatch metrics for VPC subnet associated with Network ACL `<nacl-id>` including packet drop metrics over the last 1 hour to identify blocked traffic patterns, analyzing drop patterns.
5. List VPC subnets associated with Network ACL `<nacl-id>` and check subnet routing and security group configurations that may interact with NACL rules, verifying subnet associations.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for NACL rule modification events related to Network ACL `<nacl-id>`, checking for rule changes.
7. Retrieve the Network ACL `<nacl-id>` subnet associations and verify which subnets use this NACL, checking if subnet association changes affected traffic.
8. Retrieve CloudWatch metrics for VPC subnet including packet counts and verify traffic flow patterns, checking if traffic is being blocked at NACL level.
9. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for allowed traffic patterns to verify if traffic matches expected patterns, checking rule effectiveness.

## Diagnosis

1. Analyze VPC Flow Logs (from Playbook step 3) to identify when traffic denials first appeared. The timestamps of REJECT actions establish when blocking began and which traffic patterns are affected.

2. If CloudTrail shows NACL rule modifications (from Playbook step 6) around the denial timestamp, those rule changes are the likely root cause. Compare before and after rule configurations.

3. If NACL rules (from Playbook step 2) show a Deny rule with lower rule number than an Allow rule for the same traffic, rule order is preventing traffic. NACLs evaluate rules in ascending order and stop at first match.

4. If outbound traffic is blocked but inbound rules appear correct, check ephemeral port configuration. Return traffic uses ephemeral ports (1024-65535) and requires explicit outbound Allow rules in NACLs.

5. If denial patterns (from Playbook step 3) affect specific subnets, check subnet associations (from Playbook step 7). Recent subnet association changes may have applied a different NACL than expected.

6. If Flow Logs (from Playbook step 9) show allowed traffic for some flows but denied for others with similar patterns, examine specific source/destination combinations. The NACL may be correctly blocking unexpected traffic while also blocking legitimate traffic.

7. If packet drop metrics (from Playbook step 4 and step 8) correlate with denial patterns, confirm the NACL is the blocking layer rather than security groups or route tables.

If no correlation is found: extend analysis to 4 hours, review security group rules for additional restrictions, check route table configurations for routing issues, verify NAT gateway or internet gateway connectivity, and examine NACL rule quota limits.
