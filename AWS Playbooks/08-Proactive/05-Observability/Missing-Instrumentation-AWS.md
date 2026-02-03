# Missing Instrumentation

## Meaning

Missing instrumentation indicates that services or resources are not properly instrumented for observability or instrumentation gaps are detected (triggering alarms like InstrumentationMissing or ObservabilityGapDetected) because CloudWatch metrics are not collected, CloudWatch Logs are not configured, X-Ray tracing is not enabled, custom metrics are missing, or instrumentation coverage is incomplete. Instrumentation gaps are detected, CloudWatch metrics are missing, CloudWatch Logs are not configured, and instrumentation coverage is incomplete. This affects the observability layer and monitoring coverage, typically caused by instrumentation configuration failures, monitoring tool unavailability, instrumentation deployment issues, or instrumentation coverage gaps; if missing instrumentation affects container workloads, container observability may be incomplete and applications may experience monitoring blind spots.

## Impact

InstrumentationMissing alarms fire; ObservabilityGapDetected alarms fire; services are not properly instrumented; monitoring coverage is incomplete; observability gaps exist; troubleshooting may be difficult. Instrumentation gaps are detected; if missing instrumentation affects container workloads, container observability may be incomplete, pod metrics may be missing, and container applications may experience monitoring blind spots; applications may experience observability gaps or monitoring failures.

## Playbook

1. List EC2 instances in region `<region>` and verify CloudWatch agent installation status and CloudWatch metrics collection configuration, checking instance-level instrumentation.
2. List Lambda functions in region `<region>` and verify CloudWatch Logs configuration and X-Ray tracing enablement status, checking Lambda instrumentation.
3. List ECS services in region `<region>` and verify CloudWatch Logs configuration and container insights enablement status, checking container instrumentation.
4. Query CloudWatch Logs for log groups and verify log group coverage for services in region `<region>` to identify services without log groups, checking log instrumentation gaps.
5. Retrieve CloudWatch metrics namespace coverage for services in region `<region>` and verify metric collection coverage to identify services without metrics, checking metric instrumentation gaps.
6. Compare instrumentation coverage analysis results with service deployment timestamps and verify whether new services are instrumented upon deployment, using service configuration data as supporting evidence.
7. Retrieve X-Ray trace data coverage for services in region `<region>` and verify tracing enablement status to identify services without tracing, checking trace instrumentation gaps.
8. List CloudWatch alarms for services in region `<region>` and verify alarm coverage to identify services without alarms, checking alarm instrumentation gaps.

## Diagnosis

1. **Analyze EC2 instrumentation from Step 1**: If CloudWatch agent is not installed, both metrics and logs are missing. If agent is installed but partially configured, some telemetry types are missing. If agent is fully configured, EC2 instrumentation is complete.

2. **Evaluate Lambda instrumentation from Step 2**: If X-Ray tracing is disabled, distributed tracing cannot show Lambda in traces. If CloudWatch Logs integration is disabled, function logs are lost. If both are enabled, Lambda instrumentation is complete.

3. **Review ECS instrumentation from Step 3**: If Container Insights is not enabled, detailed container metrics are unavailable. If CloudWatch Logs driver is not configured, container logs are lost. If both are enabled, ECS instrumentation is complete.

4. **Cross-reference with trace coverage from Step 7**: If services appear in logs and metrics but not traces, X-Ray SDK integration is missing. If traces show gaps between services, some services are not propagating trace context.

5. **Assess alarm coverage from Step 8**: If services have metrics and logs but no alarms, monitoring is passive. If critical services lack alarms, incidents may not be detected automatically. If alarm coverage is uneven, prioritize critical services.

If the above analysis is inconclusive: Define instrumentation standards for each service type. Implement instrumentation as code in deployment pipelines. Conduct observability audits regularly. Consider AWS Distro for OpenTelemetry for unified instrumentation.
