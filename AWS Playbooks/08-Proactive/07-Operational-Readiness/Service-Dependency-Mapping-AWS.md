# Service Dependency Mapping

## Meaning

Service dependency mapping indicates that service dependencies cannot be mapped or dependency relationships are not identified (triggering alarms like DependencyMappingFailed or ServiceDependencyUnavailable) because service dependency mapping tools fail, dependency relationships are not discovered, service dependency graphs are unavailable, dependency mapping data is missing, or service dependency analysis cannot be performed. Service dependency mapping shows failures, dependency relationships are not identified, service dependency graphs are unavailable, and service dependency analysis fails. This affects the dependency management layer and service architecture understanding, typically caused by dependency mapping tool failures, service discovery issues, dependency relationship tracking failures, or dependency mapping data collection issues; if dependency mapping affects container workloads, container service dependencies may be unknown and applications may experience dependency-related failures.

## Impact

DependencyMappingFailed alarms fire; ServiceDependencyUnavailable alarms fire; service dependencies cannot be mapped; dependency relationships are not identified; service architecture understanding is limited; dependency-related failures may occur unexpectedly. Service dependency mapping is unavailable; if dependency mapping affects container workloads, container service dependencies may be unknown, pod dependencies may be unmapped, and container applications may experience dependency-related failures; applications may experience service dependency failures or architecture understanding gaps.

## Playbook

1. Query CloudWatch Logs for log groups containing application or service logs and filter for service call patterns or API dependency patterns within the last 7 days to identify service dependencies.
2. Retrieve CloudWatch metrics for service-to-service communication including API call counts and latency metrics over the last 7 days to identify service dependency patterns.
3. Retrieve X-Ray trace data for service `<service-name>` and analyze trace segments to identify downstream service dependencies and dependency relationships.
4. List API Gateway APIs in region `<region>` and retrieve API integration configurations to identify backend service dependencies.
5. Retrieve the Application Load Balancer `<alb-arn>` target group configurations and verify target service dependencies, checking load balancer backend dependencies.
6. Compare service dependency mapping results with service call pattern timestamps and verify whether dependencies are accurately mapped, using CloudWatch Logs containing service logs as supporting evidence.
7. Retrieve CloudWatch Service Map data for account `<account-id>` in region `<region>` and verify service dependency graph availability, checking service map configuration.
8. Query CloudWatch Logs for log groups containing VPC Flow Logs and filter for inter-service communication patterns to identify network-level service dependencies.

## Diagnosis

1. **Analyze X-Ray trace data from Step 3**: If trace segments show downstream services, dependency relationships are visible. If trace segments are incomplete, some services lack X-Ray instrumentation. If specific dependencies are missing, those services need tracing enabled.

2. **Evaluate Service Map data from Step 7**: If Service Map shows complete topology, dependency mapping is working. If map has gaps, verify X-Ray SDK integration in missing services. If map shows outdated dependencies, recent changes have not been traced.

3. **Review network-level data from Step 8**: If VPC Flow Logs show traffic to services not in X-Ray maps, those services need instrumentation. If unexpected traffic patterns exist, undocumented dependencies are present.

4. **Cross-reference with API patterns from Step 1 and Step 2**: If API call logs show services not in dependency maps, correlation is incomplete. If call counts are high but dependencies are unmapped, trace sampling may be too low.

5. **Assess infrastructure dependencies from Step 4 and Step 5**: If API Gateway integrations or ALB targets show services not in maps, add those to the dependency inventory. If configurations have changed, update dependency documentation.

If the above analysis is inconclusive: Enable X-Ray instrumentation for all services systematically. Review trace segment propagation headers. Consider AWS Application Discovery Service for infrastructure discovery. Implement CloudMap for service discovery integration.
