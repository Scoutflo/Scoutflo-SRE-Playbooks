# Trace Coverage Issues

## Meaning

Trace coverage issues indicate that distributed tracing coverage is incomplete or trace coverage gaps are detected (triggering alarms like TraceCoverageIncomplete or TraceCollectionGapDetected) because X-Ray tracing is not enabled for services, trace sampling rates are too low, trace collection agents are not installed, trace coverage analysis tools fail, or trace coverage monitoring indicates gaps. Trace coverage gaps are detected, X-Ray tracing is not enabled, trace sampling rates are low, and trace coverage analysis fails. This affects the observability layer and distributed tracing coverage, typically caused by trace configuration failures, trace collection agent installation issues, trace coverage analysis tool failures, or trace coverage monitoring gaps; if trace coverage affects container workloads, container traces may not be collected and applications may experience trace monitoring blind spots.

## Impact

TraceCoverageIncomplete alarms fire; TraceCollectionGapDetected alarms fire; distributed tracing coverage is incomplete; trace coverage gaps are detected; trace monitoring may be insufficient; distributed system analysis may be difficult. Trace coverage gaps are detected; if trace coverage affects container workloads, container traces may not be collected, pod traces may be missing, and container applications may experience trace monitoring blind spots; applications may experience trace coverage gaps or trace collection failures.

## Playbook

1. Retrieve X-Ray trace data coverage for services in region `<region>` and verify tracing enablement status to identify services without tracing, checking trace coverage gaps.
2. List Lambda functions in region `<region>` and verify X-Ray tracing enablement status and trace sampling rate configuration, checking Lambda trace coverage.
3. List ECS services in region `<region>` and verify X-Ray daemon configuration and container trace collection settings, checking container trace coverage.
4. Retrieve X-Ray trace sampling configuration for services in region `<region>` and verify sampling rates are appropriate for trace coverage, checking trace sampling coverage.
5. Query X-Ray trace data for service `<service-name>` and verify trace availability over the last 7 days to identify missing traces or trace collection failures, checking trace collection health.
6. Compare trace coverage analysis results with service deployment timestamps and verify whether new services have X-Ray tracing enabled upon deployment, using service configuration data as supporting evidence.
7. Retrieve X-Ray daemon status for ECS services in region `<region>` and verify daemon health and trace collection status, checking trace daemon coverage.
8. List X-Ray trace groups and verify trace group coverage for services to identify services without trace groups, checking trace group coverage gaps.

## Diagnosis

1. **Analyze trace enablement from Step 1 and Step 2**: If services have X-Ray tracing disabled, enable tracing for those services. If Lambda tracing is disabled, enable active tracing in function configuration. If tracing is enabled but no traces appear, SDK integration is missing.

2. **Evaluate X-Ray daemon status from Step 3 and Step 7**: If X-Ray daemon is not running, container traces cannot be collected. If daemon is running but unhealthy, troubleshoot daemon configuration. If daemon is healthy but traces are missing, application SDK may not be instrumented.

3. **Review sampling configuration from Step 4**: If sampling rate is too low, traces may be missing due to sampling. If sampling rate is 100% but traces are missing, collection is failing. If sampling rate is appropriate, sampling is not the issue.

4. **Cross-reference with deployments from Step 6**: If newly deployed services lack tracing, deployment automation does not include X-Ray configuration. If tracing was enabled but stopped, investigate configuration drift.

5. **Assess trace availability from Step 5**: If traces show gaps, collection was interrupted. If specific services are missing from traces, those services lack instrumentation. If trace segments are incomplete, context propagation is failing.

If the above analysis is inconclusive: Review X-Ray SDK integration in application code. Check IAM roles for X-Ray write permissions. Verify VPC endpoints if tracing from private subnets. Consider AWS Distro for OpenTelemetry for unified tracing.
