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

1. Analyze AWS service health from Playbook step 1 to verify EC2 and VPC service availability in the region. If service health indicates issues, connectivity failures may be AWS-side requiring monitoring rather than configuration changes.

2. If NAT Gateway state from Playbook step 3 is not "available", the NAT Gateway is non-functional. Check the state change timestamp to correlate with when connectivity issues began. States like "failed" or "deleted" indicate NAT Gateway problems.

3. If NAT Gateway Elastic IP from Playbook step 4 is not associated, the NAT Gateway cannot route traffic to the internet. Verify EIP association status and association timestamp.

4. If private subnet route table from Playbook step 5 lacks a route to the NAT Gateway (0.0.0.0/0 -> nat-*), outbound internet traffic has no path. Verify the route exists and targets the correct NAT Gateway ID.

5. If instance subnet configuration from Playbook step 2 shows the instance is in a public subnet (not private), it should use an Internet Gateway directly, not NAT Gateway. Verify subnet classification.

6. If public subnet route table from Playbook step 7 lacks a route to an Internet Gateway, the NAT Gateway itself cannot reach the internet. The NAT Gateway requires internet access to function.

7. If security group or NACL from Playbook step 6 blocks outbound traffic from the instance, egress is blocked before reaching NAT Gateway. Verify outbound rules permit the required traffic.

8. If NAT Gateway metrics from Playbook step 8 show BytesOutToDestination is zero or very low, the NAT Gateway is not processing traffic. High ErrorPortAllocation indicates port exhaustion.

9. If VPC Flow Logs from Playbook step 9 show REJECT actions for outbound traffic, identify whether the rejection occurs at security group, NACL, or route level.

If no correlation is found from the collected data: extend VPC Flow Log query timeframes to 1 hour, check for NAT Gateway bandwidth limits, verify no conflicting routes from AWS Direct Connect or VPN, and examine NAT Gateway high availability across multiple AZs. Connectivity failures may result from NAT Gateway port exhaustion, bandwidth throttling, or asymmetric routing configurations.

