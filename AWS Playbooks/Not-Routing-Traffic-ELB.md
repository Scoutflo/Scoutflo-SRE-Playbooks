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

1. Compare target instance health check failure timestamps with traffic routing failure timestamps within 5 minutes and verify whether routing failures began when targets became unhealthy, using target group health check events as supporting evidence.
2. Correlate security group rule modification timestamps with traffic blocking timestamps and verify whether routing failures occurred after security group changes, using security group configuration data as supporting evidence.
3. Compare listener configuration change timestamps with routing failure timestamps within 10 minutes and verify whether listener changes prevented traffic routing, using load balancer configuration events as supporting evidence.
4. Compare load balancer type change timestamps with routing failure timestamps and verify whether load balancer type changes affected routing behavior, using load balancer configuration events as supporting evidence.
5. Analyze traffic pattern frequency over the last 15 minutes to determine if routing failures are constant (configuration issue) or intermittent (target health fluctuations).

If no correlation is found within the specified time windows: extend timeframes to 30 minutes, review alternative evidence sources including VPC flow logs and network ACL rules, check for gradual issues like target capacity exhaustion, verify external dependencies like DNS resolution, examine historical patterns of load balancer traffic, check for AWS Global Accelerator integration issues, verify AWS WAF rule interactions. Routing failures may result from network-level routing issues, DNS resolution problems, application-level health check failures, AWS Global Accelerator routing conflicts, or AWS Shield DDoS protection rather than immediate load balancer configuration changes.
