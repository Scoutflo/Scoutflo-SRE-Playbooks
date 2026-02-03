# PrivateLink Endpoint Not Working

## Meaning

VPC PrivateLink endpoint is not working (triggering connectivity failures or VPCEndpointConnectionFailed alarms) because endpoint service is unavailable, endpoint policy restricts access, security group rules block traffic, route table configuration is incorrect, endpoint service acceptance is pending, or VPC endpoint DNS resolution fails. PrivateLink endpoint connectivity fails, private service access is blocked, and endpoint connections cannot be established. This affects the networking and service access layer and blocks private service connectivity, typically caused by endpoint configuration issues, policy restrictions, or service availability problems; if using PrivateLink with multiple services, endpoint configuration may differ and applications may experience service access failures.

## Impact

PrivateLink endpoint connectivity fails; private service access is blocked; endpoint connections cannot be established; service-to-service communication fails; endpoint status shows failures; private network access is unavailable; application integration fails. VPCEndpointConnectionFailed alarms may fire; if using PrivateLink with multiple services, endpoint configuration may differ; applications may experience errors or performance degradation due to blocked service access; service-to-service communication may be completely blocked.

## Playbook

1. Verify VPC endpoint `<vpc-endpoint-id>` exists and AWS service health for VPC in region `<region>` is normal.
2. Retrieve the VPC Endpoint `<vpc-endpoint-id>` in region `<region>` and inspect its endpoint status, service name, endpoint policy, and connection state, verifying endpoint is in "available" state.
3. Query CloudWatch Logs for log groups containing VPC endpoint logs and filter for endpoint failure events, connection errors, or policy denial patterns, including failure reason details.
4. Retrieve CloudWatch metrics for VPC Endpoint `<vpc-endpoint-id>` including BytesIn and BytesOut over the last 1 hour to identify connectivity patterns, analyzing traffic flow.
5. Retrieve the Security Group `<security-group-id>` associated with VPC Endpoint `<vpc-endpoint-id>` and inspect its inbound and outbound rules for endpoint traffic, verifying security group rules.
6. List route table entries for subnets containing VPC Endpoint `<vpc-endpoint-id>` and check routing configuration for endpoint traffic, verifying route table associations.
7. Retrieve the VPC Endpoint Service `<service-name>` configuration and verify endpoint service acceptance status, checking if endpoint service acceptance is pending.
8. Retrieve the VPC Endpoint `<vpc-endpoint-id>` DNS configuration and verify DNS resolution for endpoint, checking if DNS resolution is configured correctly.
9. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for blocked traffic to or from VPC endpoint `<vpc-endpoint-id>`, checking flow log analysis.

## Diagnosis

1. Analyze VPC endpoint status (from Playbook step 2) to identify when the endpoint entered a failed or unavailable state. Check connection state and verify endpoint is in "available" status.

2. If endpoint status shows "pendingAcceptance" (from Playbook step 7), the endpoint service provider has not accepted the connection request. This requires action from the service provider.

3. If endpoint is "available" but traffic fails, examine security group rules (from Playbook step 5). If security groups do not allow traffic to/from the endpoint on required ports, traffic is blocked at the security group level.

4. If security groups are correct, check VPC Flow Logs (from Playbook step 9) for blocked traffic patterns. Flow Logs show whether traffic reaches the endpoint or is blocked by network controls.

5. If endpoint policy (from Playbook step 2) has been modified recently (check Playbook step 3 logs), restrictive policies may be denying access to specific services or actions.

6. If DNS resolution (from Playbook step 8) does not return private IP addresses for the endpoint, Private DNS may not be enabled or may be misconfigured.

7. If CloudWatch metrics (from Playbook step 4) show zero BytesIn/BytesOut, traffic is not reaching the endpoint at all. Check route table associations (from Playbook step 6) for correct routing to the endpoint.

If no correlation is found: extend analysis to 24 hours, verify endpoint service provider configuration, check DNS resolution from consumer VPC, examine route table entries for endpoint routing, and verify endpoint policy size limits are not exceeded.
