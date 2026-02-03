# Metric Coverage Gaps

## Meaning

Metric coverage gaps indicate that metric collection coverage is incomplete or metric coverage gaps are detected (triggering alarms like MetricCoverageIncomplete or MetricCollectionGapDetected) because CloudWatch metrics are not collected for services, custom metrics are missing, metric namespaces are not configured, metric collection agents are not installed, or metric coverage analysis indicates gaps. Metric coverage gaps are detected, CloudWatch metrics are not collected, custom metrics are missing, and metric coverage analysis fails. This affects the observability layer and metric monitoring coverage, typically caused by metric configuration failures, metric collection agent installation issues, metric coverage analysis tool failures, or metric coverage monitoring gaps; if metric coverage affects container workloads, container metrics may not be collected and applications may experience metric monitoring blind spots.

## Impact

MetricCoverageIncomplete alarms fire; MetricCollectionGapDetected alarms fire; metric collection coverage is incomplete; metric coverage gaps are detected; metric monitoring may be insufficient; performance analysis may be difficult. Metric coverage gaps are detected; if metric coverage affects container workloads, container metrics may not be collected, pod metrics may be missing, and container applications may experience metric monitoring blind spots; applications may experience metric coverage gaps or metric collection failures.

## Playbook

1. Retrieve CloudWatch metrics namespace coverage for services in region `<region>` and verify metric collection coverage to identify services without metrics, checking metric coverage gaps.
2. List EC2 instances in region `<region>` and verify CloudWatch agent installation status and metric collection configuration, checking instance-level metric coverage.
3. List Lambda functions in region `<region>` and verify CloudWatch metrics configuration and metric namespace association, checking Lambda metric coverage.
4. List ECS services in region `<region>` and verify CloudWatch Container Insights enablement and container metric collection settings, checking container metric coverage.
5. Query CloudWatch metrics for service namespaces and verify metric availability over the last 7 days to identify missing metrics or metric collection failures, checking metric collection health.
6. Compare metric coverage analysis results with service deployment timestamps and verify whether new services have metrics configured upon deployment, using service configuration data as supporting evidence.
7. Retrieve CloudWatch agent status for EC2 instances in region `<region>` and verify agent health and metric collection status, checking metric agent coverage.
8. List CloudWatch custom metrics and verify custom metric coverage for services to identify services without custom metrics, checking custom metric coverage gaps.

## Diagnosis

1. **Analyze metric namespace inventory from Step 1**: If services have no metrics in expected namespaces, metric collection is not configured. If default AWS metrics exist but custom metrics are missing from Step 8, application instrumentation is incomplete.

2. **Evaluate EC2 agent status from Step 2 and Step 7**: If CloudWatch agent is not installed, detailed metrics cannot be collected. If agent is installed but unhealthy, troubleshoot agent configuration. If agent is healthy but metrics are missing, metric configuration may be incorrect.

3. **Review Lambda and ECS metrics from Step 3 and Step 4**: If Lambda metrics are missing, verify function execution is occurring. If Container Insights is not enabled, ECS metrics are limited to basic data. If container metrics are missing, verify task definition logging configuration.

4. **Cross-reference with deployments from Step 6**: If newly deployed services lack metrics, deployment automation does not include metric configuration. If metrics were present but disappeared, investigate configuration drift.

5. **Assess metric availability from Step 5**: If metrics show gaps, collection was interrupted during those periods. If specific metrics are consistently missing, those metrics are not being published. If all metrics are missing for a service, the service may not be running.

If the above analysis is inconclusive: Review CloudWatch agent configuration for metric definitions. Check IAM roles for metric write permissions. Verify custom metric dimensions and namespaces. Consider unified CloudWatch agent for comprehensive coverage.
