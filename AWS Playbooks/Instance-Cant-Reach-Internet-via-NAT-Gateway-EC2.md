# EC2 Instance Can't Reach Internet via NAT Gateway

## Meaning

EC2 instances in private subnets cannot reach the internet via NAT Gateway (triggering network connectivity errors or EC2InstanceNATConnectivityFailed alarms) because instances are not in private subnets, NAT Gateway is not associated with a public subnet, route tables lack routes to NAT Gateway, security groups or network ACLs block outbound traffic, NAT Gateway state is unavailable, connectivity tests fail, or NAT Gateway Elastic IP is not associated. Instances in private subnets cannot access internet, software updates fail, and external API calls timeout. This affects the networking layer and blocks outbound internet access, typically caused by NAT Gateway configuration issues, route table problems, or security group restrictions; if using AWS Direct Connect or VPN, routing may differ and applications may experience external dependency failures.

## Impact

Instances in private subnets cannot access internet; software updates fail; external API calls timeout; outbound connectivity is blocked; NAT Gateway routing fails; network connectivity errors occur; application dependencies on external services fail; security patches cannot be downloaded; service integrations break. EC2InstanceNATConnectivityFailed alarms fire; if using AWS Direct Connect or VPN, routing conflicts may occur; applications may experience errors or performance degradation due to missing external dependencies; container images cannot be pulled from public registries.

## Playbook

1. Verify instance `<instance-id>` and NAT Gateway `<nat-gateway-id>` exist, and AWS service health for EC2 and VPC in region `<region>` is normal.
2. Retrieve the EC2 Instance `<instance-id>` and verify it is in a private subnet by checking subnet configuration and route table association, verifying subnet is not public.
3. Retrieve the NAT Gateway `<nat-gateway-id>` and verify it is associated with a public subnet and check NAT Gateway state and subnet association, ensuring gateway is in "available" state.
4. Retrieve the NAT Gateway `<nat-gateway-id>` Elastic IP association and verify Elastic IP is associated with NAT Gateway, checking EIP association status.
5. Retrieve the Route Table `<route-table-id>` for the private subnet containing instance `<instance-id>` and verify it has a route to the NAT Gateway (0.0.0.0/0 → nat-gateway-id), checking route table association.
6. Retrieve the Security Group `<security-group-id>` and Network ACL `<nacl-id>` for instance `<instance-id>` and check outbound rules allowing internet access, verifying egress rules.
7. Retrieve the Route Table `<route-table-id>` for the public subnet containing NAT Gateway and verify public subnet has route to internet gateway, checking internet gateway route.
8. Retrieve CloudWatch metrics for NAT Gateway `<nat-gateway-id>` including BytesOutToDestination, BytesInFromDestination, and bandwidth utilization to verify traffic flow and check if NAT Gateway is processing traffic and not at capacity limits.
9. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for blocked outbound traffic from instance `<instance-id>`, checking flow log analysis.

## Diagnosis

1. Compare instance subnet assignment change timestamps with internet connectivity failure timestamps within 10 minutes and verify whether connectivity failures began when instance subnet changed, using EC2 instance events as supporting evidence.
2. Correlate NAT Gateway state change timestamps with routing failure timestamps and verify whether connectivity failures occurred when NAT Gateway became unavailable, using NAT Gateway events as supporting evidence.
3. Compare route table modification timestamps with internet access failure timestamps within 10 minutes and verify whether route table changes removed NAT Gateway routes, using route table events as supporting evidence.
4. Compare NAT Gateway Elastic IP association change timestamps with connectivity failure timestamps and verify whether EIP disassociation caused routing failures, using NAT Gateway EIP events as supporting evidence.
5. Analyze connectivity failure frequency over the last 15 minutes to determine if failures are constant (configuration issue) or intermittent (NAT Gateway availability).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including VPC flow logs and network ACL rules, check for gradual issues like NAT Gateway capacity limits, verify external dependencies like internet gateway attachment, examine historical patterns of NAT Gateway connectivity, check for AWS Direct Connect or VPN routing conflicts, verify NAT Gateway high availability configuration. Connectivity failures may result from NAT Gateway capacity issues, elastic IP attachment problems, subnet-level routing conflicts, AWS Direct Connect routing priorities, or VPN routing conflicts rather than immediate route table changes.

