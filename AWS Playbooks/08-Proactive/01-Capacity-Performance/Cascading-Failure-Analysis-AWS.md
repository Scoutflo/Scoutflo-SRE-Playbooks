# Cascading Failure Analysis

## Meaning

Cascading failure analysis indicates that cascading failure risks cannot be analyzed or cascading failure patterns are detected (triggering alarms like CascadingFailureDetected or FailureCascadeAnalysisFailed) because cascading failure analysis tools fail, cascading failure patterns are not detected, failure propagation paths are not identified, cascading failure risk assessment is unavailable, or cascading failure monitoring indicates problems. Cascading failure analysis shows failures, cascading failure patterns are detected, failure propagation paths are not identified, and cascading failure risk assessment fails. This affects the dependency management layer and service resilience, typically caused by service dependency failures, failure propagation tracking issues, cascading failure analysis tool failures, or cascading failure monitoring issues; if cascading failures affect container workloads, container service failures may propagate and applications may experience widespread service outages.

## Impact

CascadingFailureDetected alarms fire; FailureCascadeAnalysisFailed alarms fire; cascading failure risks cannot be analyzed; cascading failure patterns are detected; service resilience is compromised; widespread service outages may occur. Cascading failure analysis shows failures; if cascading failures affect container workloads, container service failures may propagate, pod failures may cascade, and container applications may experience widespread service outages; applications may experience service-wide failures or cascading failure propagation.

## Playbook

1. Query CloudWatch Logs for log groups containing service error events and filter for cascading failure patterns or failure propagation patterns within the last 24 hours to identify cascading failures.
2. Retrieve CloudWatch metrics for service error rates including ErrorRate and FailureRate over the last 24 hours to identify failure propagation patterns across services.
3. Retrieve X-Ray trace data for service `<service-name>` and analyze trace error propagation to identify cascading failure paths and downstream service impact.
4. List CloudWatch alarms with state 'ALARM' across multiple services and verify alarm correlation indicates cascading failures, checking alarm-based cascading failure detection.
5. Retrieve the Application Load Balancer `<alb-arn>` target group health status and verify target failures correlate with upstream service failures, checking load balancer-level cascading failures.
6. Compare cascading failure detection timestamps with initial service failure timestamps within 30 minutes and verify whether initial failures trigger cascading failures, using CloudWatch Logs containing service error events as supporting evidence.
7. Retrieve CloudWatch Service Map data for account `<account-id>` in region `<region>` and analyze service dependency paths to identify potential cascading failure propagation routes.
8. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for service-to-service communication failures to identify network-level cascading failures.

## Diagnosis

1. **Analyze X-Ray error propagation from Step 3**: If traces show errors propagating downstream, identify the originating service. If multiple downstream services fail after one upstream fails, cascading pattern is confirmed. If errors are isolated, no cascade is occurring.

2. **Evaluate alarm correlation from Step 4**: If multiple service alarms fire within minutes of each other, correlate the timing to identify the cascade sequence. If alarms fire simultaneously, a common dependency failed. If alarms fire in sequence, the cascade path is visible.

3. **Review Service Map dependencies from Step 7**: If the failed service has many downstream dependencies, impact scope is large. If dependencies have circuit breakers, cascade should be limited. If no resilience patterns exist, cascading failures are expected.

4. **Cross-reference with initial failure from Step 6**: If the initial failure timestamp is identifiable, that service needs immediate remediation. If failures appear to start from multiple services, a common infrastructure issue exists.

5. **Assess target health patterns from Step 5**: If ALB targets fail in sequence matching dependency order, cascading failure is confirmed. If all targets fail simultaneously, the issue is not a cascade but a common cause.

If the above analysis is inconclusive: Implement circuit breakers to prevent future cascades. Review retry logic that may amplify failures. Consider bulkhead patterns to isolate failures. Analyze pre-failure metrics for early warning indicators.
