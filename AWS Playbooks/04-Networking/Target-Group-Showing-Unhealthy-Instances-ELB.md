# Target Group in ELB Showing Unhealthy Instances

## Meaning

Target group instances show unhealthy status (triggering alarms like UnhealthyTargetCount) because target instances fail health checks, security groups or network ACLs block health check traffic, listener configurations are incorrect, instances are not properly registered, health check path or protocol is misconfigured, or CloudWatch metrics indicate health check pattern issues. Target instances are marked unhealthy, load balancer stops routing traffic to unhealthy targets, and health check failures increase. This affects the load balancing layer and reduces service capacity, typically caused by health check configuration issues, network blocking, or application health problems; if using different load balancer types (ALB, NLB, CLB), health check behavior differs and applications may experience traffic routing failures.

## Impact

Target instances are marked unhealthy; load balancer stops routing traffic to unhealthy targets; service capacity decreases; UnhealthyTargetCount alarms fire; application availability is reduced; health check failures increase; user requests may timeout; service degradation occurs; automatic scaling may be triggered. Load balancer cannot route requests; if using different load balancer types (ALB vs NLB vs CLB), health check behavior differs; applications may experience errors or performance degradation due to reduced capacity; target group cross-zone load balancing may be affected.

## Playbook

1. Verify target group `<target-group-name>` exists and load balancer `<load-balancer-name>` is active, and AWS service health for ELB in region `<region>` is normal.
2. Retrieve the Target Group `<target-group-name>` and check health status of target instances and inspect health check configuration, including health check path, protocol, port, timeout, interval, and healthy/unhealthy thresholds.
3. Retrieve the Target Group `<target-group-name>` target type configuration and verify target type (instance vs IP), checking if target type matches instance registration.
4. Retrieve the Security Group `<security-group-id>` associated with target instances and check security groups allowing health check traffic to and from the load balancer, verifying source security groups.
5. Retrieve the Load Balancer `<load-balancer-name>` listener configuration and type (ALB, NLB, or CLB) and verify listeners are configured properly (e.g., HTTP/HTTPS on correct ports) for health checks and load balancer type configuration, checking type-specific health check behavior.
7. Verify proper instance registration in target group `<target-group-name>` by retrieving target group targets and checking instance registration status, verifying target port matches health check port.
8. Retrieve CloudWatch metrics for Target Group `<target-group-name>` including healthy host count, unhealthy host count, and target response time to identify health check patterns.
9. Retrieve the Target Group `<target-group-name>` health check path and verify health check path exists and returns 200 status code.
10. Query CloudWatch Logs for log groups containing application logs and filter for health check endpoint errors or application errors affecting health checks.

## Diagnosis

1. Analyze AWS service health from Playbook step 1 to verify ELB service availability in the region. If service health indicates issues, health check failures may be AWS-side requiring monitoring rather than configuration changes.

2. If target health status from Playbook step 2 shows specific failure reasons (e.g., "Health checks failed", "Connection timeout", "HTTP 5xx"), use these reasons to guide investigation. Each failure type indicates a different root cause.

3. If target type from Playbook step 3 is "instance" but targets were registered by IP, or vice versa, registration type mismatch causes health check failures. Verify target type matches registration method.

4. If security group from Playbook step 4 does not allow inbound traffic from the load balancer security group on the health check port, health checks cannot reach targets. Verify the load balancer security group is an allowed source.

5. If listener configuration from Playbook step 5 shows health check settings (path, port, protocol) that differ from application expectations, health checks fail. For HTTP health checks, verify the health check path returns 200 status code.

6. If target registration from Playbook step 7 shows targets in "draining" state, they are being deregistered and will appear unhealthy temporarily. If in "unused" state, no listeners are routing to the target group.

7. If CloudWatch metrics from Playbook step 8 show HealthyHostCount dropped suddenly, correlate the timestamp with deployment events, instance state changes, or security group modifications.

8. If health check path from Playbook step 9 does not exist on the target application or returns non-200 responses, the application is not properly responding to health probes. Verify application health check endpoint implementation.

9. If application logs from Playbook step 10 show errors correlating with health check timestamps, application-level issues are causing health check failures. Examine error patterns for root cause.

If no correlation is found from the collected data: extend application log query timeframes to 30 minutes, verify instance-level resource utilization (CPU, memory, disk), check for application dependency failures, and examine target group connection draining settings. Unhealthy instances may result from application crashes, memory exhaustion, disk full conditions, or dependency service outages.

