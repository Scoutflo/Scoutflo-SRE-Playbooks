# X-Ray Traces Missing in Application Logs

## Meaning

X-Ray traces are missing in application logs (triggering distributed tracing gaps or XRayTracesMissing alarms) because X-Ray daemon is not running, X-Ray SDK is not configured, IAM permissions are insufficient for trace submission, X-Ray sampling rules filter out traces, X-Ray service encounters errors during trace ingestion, or X-Ray trace sampling rate is too low. X-Ray traces are not collected, distributed tracing fails, and trace-based analysis is unavailable. This affects the observability and distributed tracing layer and reduces application visibility, typically caused by X-Ray configuration issues, daemon problems, or sampling rule misconfiguration; if using X-Ray with different services or sampling configurations, trace collection behavior may differ and applications may experience tracing gaps.

## Impact

X-Ray traces are not collected; distributed tracing fails; trace-based analysis is unavailable; application trace visibility is lost; X-Ray trace sampling is ineffective; trace-based debugging fails; observability is compromised; distributed system analysis is limited. XRayTracesMissing alarms may fire; if using X-Ray with different services or sampling configurations, trace collection behavior may differ; applications may experience reduced observability; distributed tracing may be ineffective.

## Playbook

1. Verify X-Ray service access and AWS service health for X-Ray in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing application logs and filter for X-Ray trace ID patterns or trace submission error messages, including trace error details.
3. Retrieve CloudWatch metrics for X-Ray service including TracesReceived and TracesProcessed over the last 24 hours to identify trace ingestion patterns, analyzing trace ingestion.
4. Retrieve the IAM role `<role-name>` used by application for X-Ray trace submission and inspect its policy permissions for X-Ray operations including PutTraceSegments, verifying IAM permissions.
5. List X-Ray sampling rules and check sampling rule configurations, sampling rates, and rule applicability to application traces, verifying sampling configuration.
6. Query CloudWatch Logs for log groups containing X-Ray daemon logs and filter for daemon errors, trace submission failures, or daemon connectivity issues, including daemon error details.
7. Retrieve the X-Ray service sampling configuration and verify sampling rate settings, checking if sampling rate is too low affecting trace collection.
8. Retrieve CloudWatch metrics for X-Ray daemon if available and verify daemon status, checking if daemon is running and processing traces.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for X-Ray SDK configuration or IAM role policy modification events within the last 24 hours, checking for configuration changes.

## Diagnosis

1. **Check IAM Permissions from Step 4 First**: If trace submission requires IAM permissions, verify the IAM role from Step 4 has `xray:PutTraceSegments` and `xray:PutTelemetryRecords` permissions. If application logs from Step 2 show "AccessDeniedException" or permission errors, then insufficient permissions are blocking trace submission. If permissions appear correct, continue to step 2.

2. **Analyze CloudWatch Metrics from Step 3**: Review X-Ray trace ingestion metrics. If CloudWatch metrics show TracesReceived at 0, then no traces are reaching X-Ray service. If some traces are received but fewer than expected, sampling may be filtering traces. Compare with expected trace volume based on application request rate. If metrics show traces are being received, continue to step 3.

3. **Check X-Ray Daemon Status from Steps 6 and 8**: If daemon logs from Step 6 show errors, connectivity issues, or the daemon is not running, then traces cannot be forwarded to X-Ray service. Verify daemon is running and can reach X-Ray endpoints. If using containerized applications, ensure daemon sidecar is properly configured. If daemon is healthy, continue to step 4.

4. **Review Sampling Rules from Steps 5 and 7**: If sampling rules from Step 5 have very low sampling rates (e.g., 0.01 = 1%) or rules exclude your application's traffic patterns, then most traces are being dropped by design. Verify reservoir size and fixed rate settings. If you need 100% of traces, adjust sampling rules accordingly. If sampling appears correct, continue to step 5.

5. **Correlate with Configuration Changes from Step 9**: If CloudTrail events from Step 9 show X-Ray configuration changes, IAM role modifications, or sampling rule updates within 30 minutes of traces disappearing, then recent changes caused the issue. Review the specific modifications to identify the breaking change.

**If no correlation is found**: Extend analysis to 30 days using trace patterns from Step 3. Verify X-Ray SDK is properly integrated in application code and instrumentation is active. Check application logs from Step 2 for SDK initialization errors. For Lambda functions, verify active tracing is enabled. For containers, ensure X-Ray daemon is accessible from the application container.
