# Elastic Load Balancer (ELB) Not Routing Traffic

## Meaning

Elastic Load Balancer fails to route traffic to target instances (triggering alarms like UnhealthyTargetCount or TargetResponseTime) because target instances are unhealthy, security groups or network ACLs block traffic, listener configurations are incorrect, instances are not properly registered in target groups, load balancer scheme is misconfigured, listener rules prevent routing, or CloudWatch metrics indicate traffic pattern issues. Load balancer cannot route requests, applications receive no traffic, and health checks fail. This affects the load balancing layer and blocks service access, typically caused by target health issues, network blocking, or listener configuration problems; if using different load balancer types (ALB, NLB, CLB), routing behavior differs and applications may experience traffic routing failures.

## Impact

Load balancer cannot route requests; applications receive no traffic; services become unavailable; health checks fail; UnhealthyTargetCount alarms fire; target response time increases; user requests timeout; service endpoints become unreachable; high availability is compromised. TargetResponseTime alarms fire; if using different load balancer types (ALB vs NLB vs CLB), routing behavior differs; applications may experience errors or performance degradation due to missing traffic; service capacity is effectively zero.

## Playbook

1. Verify Load Balancer `<load-balancer-name>` and target group `<target-group-name>` exist, and AWS service health for ELB in region `<region>` is normal.
2. Retrieve the Target Group `<target-group-name>` associated with Load Balancer `<load-balancer-name>` and check health status of target instances, verifying target health state.
3. Retrieve the Load Balancer `<load-balancer-name>` type (ALB, NLB, or CLB) and verify load balancer type configuration, checking type-specific routing behavior.
4. Retrieve the Load Balancer `<load-balancer-name>` scheme (internet-facing vs internal) and verify load balancer scheme matches requirements, checking scheme configuration.
5. Retrieve the Security Group `<security-group-id>` associated with Load Balancer `<load-balancer-name>` and check security groups allowing traffic to and from the load balancer, verifying security group rules.
6. Retrieve the Load Balancer `<load-balancer-name>` listener configuration and listener rules and verify listeners are configured properly (e.g., HTTP/HTTPS on correct ports) and listener rules are correctly configured for routing, checking listener rules, rule priority, and conditions.
8. Verify proper instance registration in target group `<target-group-name>` by retrieving target group targets and checking instance registration status, verifying target port.
9. Retrieve CloudWatch metrics for Load Balancer `<load-balancer-name>` including request count, target response time, and healthy host count to identify traffic patterns, analyzing metrics.
10. Query CloudWatch Logs for log groups containing application logs and filter for load balancer access log errors or routing issues, checking access logs.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify ELB service availability in the region. If service health indicates issues, routing failures may be AWS-side requiring monitoring rather than configuration changes.

2. If target health status from Playbook step 2 shows all targets as "unhealthy", the load balancer has no healthy backends to route traffic to. Examine the health check failure reasons (timeout, connection refused, HTTP error codes) for each target.

3. If load balancer type from Playbook step 3 differs from application requirements (ALB for HTTP/HTTPS, NLB for TCP/UDP, CLB for legacy), the load balancer type may not support the required routing behavior.

4. If load balancer scheme from Playbook step 4 is "internal" but clients are attempting to connect from the internet, the load balancer is not internet-accessible. Verify scheme matches access requirements.

5. If security group from Playbook step 5 does not allow inbound traffic on listener ports or outbound traffic to target ports, network access is blocked. Verify both directions are permitted.

6. If listener configuration from Playbook step 6 shows incorrect port, protocol, or routing rules, traffic is not being directed to targets properly. Verify listener rules match expected routing behavior and check rule priority order.

7. If target registration from Playbook step 8 shows instances are not registered or are in "draining" state, targets are not available for traffic. Verify target port matches application listening port.

8. If CloudWatch metrics from Playbook step 9 show zero RequestCount but HealthyHostCount is greater than zero, clients may not be reaching the load balancer (DNS, client-side issues, or network path problems).

9. If access logs from Playbook step 10 show 5xx errors, examine the error patterns to distinguish between load balancer issues (502, 503, 504) and backend issues (500, 501).

If no correlation is found from the collected data: extend access log query timeframes to 30 minutes, verify DNS resolution of load balancer endpoint, check for AWS WAF rules blocking traffic, and examine AWS Global Accelerator routing configurations. Routing failures may result from SSL/TLS certificate issues, target group connection draining, or DDoS protection activations.

