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

1. Compare target instance health check failure timestamps with instance state change timestamps within 5 minutes and verify whether health check failures began when instances changed state, using target group health check events as supporting evidence.
2. Correlate security group rule modification timestamps with health check failure timestamps and verify whether health check failures occurred after security group changes, using security group configuration data as supporting evidence.
3. Compare health check configuration change timestamps with unhealthy status timestamps within 10 minutes and verify whether health check configuration changes caused instances to become unhealthy, using target group configuration events as supporting evidence.
4. Compare load balancer type change timestamps with health check failure timestamps and verify whether load balancer type changes affected health check behavior, using load balancer configuration events as supporting evidence.
5. Analyze health check failure frequency over the last 15 minutes to determine if failures are constant (configuration issue) or intermittent (application health fluctuations).

If no correlation is found within the specified time windows: extend timeframes to 30 minutes, review alternative evidence sources including application logs and instance system status, check for gradual issues like application performance degradation, verify external dependencies like application dependencies, examine historical patterns of target health, check for load balancer type-specific health check behavior differences, verify target group connection draining configuration. Unhealthy instances may result from application-level issues, resource exhaustion, dependency failures, load balancer type-specific behavior, or target group cross-zone load balancing issues rather than immediate target group configuration changes.
