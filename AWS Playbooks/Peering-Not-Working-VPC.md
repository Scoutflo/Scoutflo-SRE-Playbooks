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

1. Compare VPC peering connection state change timestamps with connectivity failure timestamps within 10 minutes and verify whether connectivity failures began when peering connection changed state, using VPC peering events as supporting evidence.
2. Correlate route table modification timestamps with routing failure timestamps and verify whether connectivity failures occurred after route table changes, using route table events as supporting evidence.
3. Compare security group rule modification timestamps with inter-VPC traffic blocking timestamps within 10 minutes and verify whether security group changes blocked peering traffic, using security group configuration data as supporting evidence.
4. Compare VPC peering connection acceptance timestamps with connectivity failure timestamps and verify whether peering acceptance issues prevented connectivity, using VPC peering acceptance events as supporting evidence.
5. Analyze connectivity failure frequency over the last 15 minutes to determine if failures are constant (configuration issue) or intermittent (network routing fluctuations).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including VPC flow logs and network ACL rules, check for gradual issues like CIDR block conflicts, verify external dependencies like internet gateway routing, examine historical patterns of VPC peering connectivity, check for AWS Organizations cross-account peering issues, verify IPv6 peering configuration. Connectivity failures may result from CIDR block overlaps, network ACL rule conflicts, instance-level firewall rules, AWS Transit Gateway routing conflicts, or cross-account IAM permission issues rather than immediate VPC peering configuration changes.
