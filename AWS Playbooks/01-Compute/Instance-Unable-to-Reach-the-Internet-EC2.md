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

1. Analyze AWS service health from Playbook step 1 to verify EC2 and VPC service availability in the region. If service health indicates issues or the instance is not in "running" state, address the instance-level issue first.

2. If instance configuration from Playbook step 2 shows no public IP or Elastic IP, the instance cannot communicate with the internet directly. For instances in public subnets, a public IP or EIP is required.

3. If route table from Playbook step 4 lacks a route to an Internet Gateway (0.0.0.0/0 -> igw-*), there is no path for internet traffic. Verify the route exists and targets an attached Internet Gateway.

4. If Internet Gateway from Playbook step 5 is not attached to the VPC or shows a state other than "attached", internet connectivity is impossible. Check the attachment timestamp and state.

5. If security group outbound rules from Playbook step 6 do not allow the required egress traffic (typically 0.0.0.0/0 or specific destinations), security group is blocking outbound connections. Verify egress rules permit internet access.

6. If Network ACL from Playbook step 7 contains Deny rules for outbound traffic or lacks Allow rules for ephemeral return ports (1024-65535 inbound), NACL is blocking traffic. NACLs are stateless and require explicit bidirectional rules.

7. If NetworkOut metrics from Playbook step 8 show zero bytes, the instance is not sending any traffic. This may indicate instance-level issues (OS firewall, DNS failure, or application misconfiguration).

8. If VPC Flow Logs from Playbook step 9 show REJECT actions for outbound traffic, identify the specific component rejecting traffic (security group, NACL, or route) based on the flow log details.

If no correlation is found from the collected data: extend VPC Flow Log query timeframes to 1 hour, verify DNS resolution within the instance, check for instance-level firewall rules (iptables, Windows Firewall), and examine VPC endpoint policies that may restrict traffic. Connectivity failures may result from MTU issues, DNS configuration problems, or Transit Gateway routing conflicts.

