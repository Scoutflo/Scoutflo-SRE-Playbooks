# Route 53 Latency-Based Routing Not Working

## Meaning

Route 53 latency-based routing is not working (triggering routing failures or Route53LatencyRoutingFailed alarms) because latency-based routing policy is not configured, health checks fail preventing routing, latency records are incorrect, routing policy evaluation fails, endpoint health status prevents routing, or Route 53 health check configuration is incorrect. Route 53 latency-based routing fails, traffic is not routed based on latency, and DNS routing is suboptimal. This affects the DNS and routing layer and reduces routing optimization, typically caused by health check issues, routing policy configuration problems, or endpoint configuration errors; if using Route 53 with weighted routing, routing behavior may differ and applications may experience suboptimal routing.

## Impact

Route 53 latency-based routing fails; traffic is not routed based on latency; DNS routing is suboptimal; latency-based routing policy is ineffective; user requests are not routed to lowest latency endpoints; routing performance degrades; DNS resolution does not optimize for latency. Route53LatencyRoutingFailed alarms may fire; if using Route 53 with weighted routing, routing behavior may differ; applications may experience errors or performance degradation due to suboptimal routing; user-facing latency may increase.

## Playbook

1. Verify Route 53 hosted zone `<hosted-zone-id>` exists and AWS service health for Route 53 in region `<region>` is normal.
2. Retrieve the Route 53 Hosted Zone `<hosted-zone-id>` and inspect its latency-based routing records, record configurations, and routing policy settings, verifying latency-based routing is configured.
3. Retrieve Route 53 health checks for latency-based routing records and inspect health check status, health check configuration, and endpoint health, verifying health checks are passing.
4. Query CloudWatch Logs for log groups containing Route 53 query logs and filter for latency-based routing patterns or routing decision logs, including routing decision details.
5. Retrieve CloudWatch metrics for Route 53 Hosted Zone `<hosted-zone-id>` including HealthCheckStatus over the last 1 hour to identify health check patterns, analyzing health check status.
6. List Route 53 resource record sets with latency-based routing policy and check record configurations, endpoint configurations, and routing policy evaluation, verifying record configuration.
7. Retrieve the Route 53 Hosted Zone `<hosted-zone-id>` latency records and verify latency region mappings, checking if latency regions are correctly configured.
8. Retrieve Route 53 health check configuration and verify health check settings match endpoint requirements, checking if health check configuration affects routing.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Route 53 record or health check modification events related to hosted zone `<hosted-zone-id>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch metrics for Route 53 health checks (from Playbook step 5) including HealthCheckStatus over the last hour to identify endpoint health patterns. If health checks are failing for endpoints, traffic cannot be routed to those endpoints regardless of latency. Resolve health check failures first before investigating latency routing issues.

2. Review Route 53 health check status and configuration (from Playbook step 3) to verify all endpoints associated with latency-based records have passing health checks. If health checks are failing, identify the failure reason (endpoint unreachable, unhealthy responses, or health check misconfiguration).

3. Examine CloudWatch Logs containing Route 53 query logs (from Playbook step 4) to identify routing decision patterns. If logs show traffic consistently routing to a single endpoint regardless of client location, health checks on other endpoints may be failing or latency records may be misconfigured.

4. Verify latency-based routing record configuration (from Playbook step 2) to ensure records are correctly defined with proper latency regions and set identifiers. If latency regions are incorrectly mapped to endpoints, routing will be suboptimal.

5. Review latency record region mappings (from Playbook step 7) to verify each endpoint is associated with the correct AWS region for latency measurement. If region mappings are incorrect, Route 53 cannot accurately measure latency and routing decisions will be suboptimal.

6. Compare routing patterns across different endpoints within 1 hour. If all traffic routes to a single endpoint, either that endpoint has the lowest measured latency from all client locations, or other endpoints are failing health checks. If traffic distribution varies by client location as expected, latency routing is working correctly.

7. Correlate CloudTrail events (from Playbook step 9) with routing failure timestamps within 5 minutes to identify any record or health check modifications. If configuration changes coincide with when routing became suboptimal, those changes are the likely cause.

8. Analyze health check configuration (from Playbook step 8) to verify health check settings match endpoint requirements. If health check paths, ports, or protocols are incorrect, endpoints may incorrectly appear unhealthy.

If no correlation is found within the specified time windows: extend timeframes to 7 days, review alternative evidence sources including endpoint latency measurements and routing policy evaluation logic, check for gradual issues like health check threshold changes or endpoint latency variations, verify external dependencies like endpoint availability or health check service health, examine historical patterns of latency-based routing, check for Route 53 health check probe location issues, verify Route 53 latency record region configuration. Routing failures may result from health check configuration issues, endpoint latency measurement problems, routing policy evaluation errors, Route 53 health check probe location issues, or Route 53 latency record region configuration rather than immediate routing policy changes.
