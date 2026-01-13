# EC2 Instance Unable to Reach the Internet

## Meaning

EC2 instances cannot reach the internet (triggering network connectivity errors or EC2InstanceInternetConnectivityFailed alarms) because instances lack public IP addresses or are not in public subnets, route tables lack routes to internet gateway, security group rules block outbound traffic, network ACLs block outbound traffic, internet gateway is not attached to VPC, instances are in subnets without internet gateway routes, or internet gateway attachment state is incorrect. Instances cannot access internet, software updates fail, and external API calls timeout. This affects the networking layer and blocks internet access, typically caused by network configuration issues, security group restrictions, or internet gateway problems; if instances host container workloads, container images cannot be pulled and applications may experience dependency failures.

## Impact

Instances cannot access internet; software updates fail; external API calls timeout; outbound connectivity is completely blocked; internet gateway routing fails; network connectivity errors occur; application dependencies on external services fail; security patches cannot be downloaded; DNS resolution may fail for external domains. EC2InstanceInternetConnectivityFailed alarms fire; if instances host container workloads, container images cannot be pulled, pod scheduling may fail, and container orchestration tasks may show network errors; applications may experience errors or performance degradation due to missing external dependencies.

## Playbook

1. Verify instance `<instance-id>` is in "running" state and AWS service health for EC2 and VPC in region `<region>` is normal.
2. Retrieve the EC2 Instance `<instance-id>` and check if instance has a public IP address or Elastic IP association, verifying it is in a public subnet with public IP assignment or EIP association status.
4. Retrieve the Route Table `<route-table-id>` for subnet containing instance `<instance-id>` and verify route table has a route to internet gateway (0.0.0.0/0 → igw-id), checking route table association.
5. Retrieve the Internet Gateway `<igw-id>` attachment state and verify internet gateway is attached to VPC, checking gateway attachment status.
6. Retrieve the Security Group `<security-group-id>` associated with instance `<instance-id>` and check security group rules allow outbound traffic, verifying outbound rule configuration.
7. Retrieve the Network ACL `<nacl-id>` for subnet containing instance `<instance-id>` and verify network ACLs allow outbound traffic, checking both inbound and outbound rules.
8. Retrieve CloudWatch metrics for instance `<instance-id>` including NetworkOut and NetworkIn to verify network activity, checking if outbound traffic is occurring.
9. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for blocked outbound traffic from instance `<instance-id>`, checking flow log analysis.

## Diagnosis

1. Compare instance public IP assignment change timestamps with internet connectivity failure timestamps within 10 minutes and verify whether connectivity failures began when public IP was removed, using EC2 instance events as supporting evidence.
2. Correlate route table modification timestamps with internet gateway route removal timestamps and verify whether connectivity failures occurred after route table changes, using route table events as supporting evidence.
3. Compare security group rule modification timestamps with outbound traffic blocking timestamps within 10 minutes and verify whether security group changes blocked internet access, using security group configuration data as supporting evidence.
4. Compare internet gateway attachment change timestamps with connectivity failure timestamps within 10 minutes and verify whether gateway detachment prevented internet access, using VPC events as supporting evidence.
5. Analyze connectivity failure frequency over the last 15 minutes to determine if failures are constant (configuration issue) or intermittent (internet gateway availability).

If no correlation is found within the specified time windows: extend timeframes to 1 hour, review alternative evidence sources including VPC flow logs and network ACL rules, check for gradual issues like internet gateway capacity limits, verify external dependencies like DNS resolution, examine historical patterns of internet connectivity, check for AWS Direct Connect or VPN routing conflicts, verify AWS Transit Gateway routing issues. Connectivity failures may result from DNS resolution issues, network ACL rule conflicts, instance-level firewall rules, VPC endpoint policy restrictions, or AWS service health issues rather than immediate route table changes.
