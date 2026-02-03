# VPC Peering Not Working

## Meaning

VPC peering connections fail to route traffic between VPCs (triggering network connectivity errors or VPCPeeringConnectionFailed alarms) because peering connection is not in Active state, route tables lack routes for peered VPC, security groups or network ACLs block inter-VPC traffic, DNS resolution is disabled for private IP addresses, connectivity tests fail between instances, or CIDR block overlaps prevent peering. Inter-VPC communication fails, services in different VPCs cannot communicate, and network connectivity errors occur. This affects the networking layer and blocks cross-VPC communication, typically caused by peering configuration issues, route table problems, or security group restrictions; if using AWS Organizations, cross-account peering may require additional configuration and applications may experience cross-VPC service failures.

## Impact

Inter-VPC communication fails; services in different VPCs cannot communicate; VPC peering routes are ineffective; network connectivity errors occur; cross-VPC resource access is blocked; application integrations between VPCs fail; data replication between VPCs stops; service dependencies break. VPCPeeringConnectionFailed alarms fire; if using AWS Organizations, cross-account peering may fail; applications may experience errors or performance degradation due to missing cross-VPC connectivity; service-to-service communication between VPCs is blocked.

## Playbook

1. Verify VPC peering connection `<peering-connection-id>` exists and both VPCs exist, and AWS service health for VPC in region `<region>` is normal.
2. Retrieve the VPC Peering Connection `<peering-connection-id>` and verify it is in "Active" state, inspect connection status, and verify peering connection is accepted by both VPC owners, ensuring peering is accepted by both VPCs and checking acceptance status for cross-account peering.
4. Retrieve the Route Table `<route-table-id>` for VPC `<vpc-id>` and check if routes include routes for the peered VPC CIDR blocks, verifying route destination matches peered VPC CIDR.
5. Retrieve the Route Table `<route-table-id>` for both VPCs and verify routes exist in both directions, checking bidirectional routing.
6. Retrieve the Security Group `<security-group-id>` and Network ACL `<nacl-id>` for instances in both VPCs and verify rules allow traffic between the VPCs, checking source and destination CIDR blocks.
7. Retrieve the VPC Peering Connection `<peering-connection-id>` DNS settings and verify DNS resolution is enabled for private IP addresses, checking DNS resolution configuration.
8. Retrieve the VPC `<vpc-id>` CIDR blocks for both VPCs and verify CIDR blocks do not overlap, checking for CIDR block conflicts.
9. Retrieve CloudWatch metrics for VPC peering connection `<peering-connection-id>` if available and verify traffic flow metrics, checking if traffic is being routed through peering connection.
10. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for blocked traffic between VPCs, checking flow log analysis.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify VPC service availability in the region. If service health indicates issues, peering failures may be AWS-side requiring monitoring rather than configuration changes.

2. If peering connection state from Playbook step 2 is not "active", the peering is non-functional. States like "pending-acceptance" indicate the peer VPC owner has not accepted; "failed" or "rejected" indicate configuration or permission issues.

3. If CIDR blocks from Playbook step 8 show overlapping IP ranges between the two VPCs, peering is not possible. Overlapping CIDRs prevent route table entries from distinguishing between local and peered traffic.

4. If route tables from Playbook steps 4-5 lack routes for the peered VPC CIDR blocks pointing to the peering connection (pcx-*), traffic has no path to the peer VPC. Verify bidirectional routes exist in both VPCs.

5. If security groups from Playbook step 6 do not allow traffic from the peer VPC CIDR range, inter-VPC communication is blocked. Verify source CIDR blocks include the peer VPC address space.

6. If Network ACLs from Playbook step 6 contain Deny rules for the peer VPC CIDR or lack explicit Allow rules, NACL is blocking traffic. NACLs require bidirectional rules for stateless filtering.

7. If DNS resolution settings from Playbook step 7 show DNS resolution is disabled, instances cannot resolve private DNS hostnames across the peering connection. This is required for hostname-based connectivity.

8. If VPC Flow Logs from Playbook step 10 show REJECT actions for traffic between VPCs, identify the rejecting component and specific rule causing the block.

9. If peering metrics from Playbook step 9 show no traffic flow, verify that applications are using the correct IP addresses (private IPs, not public IPs) for cross-VPC communication.

If no correlation is found from the collected data: extend VPC Flow Log query timeframes to 1 hour, verify cross-account peering acceptance in AWS Organizations, check for Transit Gateway route table conflicts, and examine IPv6 peering configuration if applicable. Connectivity failures may result from asymmetric routing, CIDR overlap with other peering connections, or cross-account IAM permission issues.

