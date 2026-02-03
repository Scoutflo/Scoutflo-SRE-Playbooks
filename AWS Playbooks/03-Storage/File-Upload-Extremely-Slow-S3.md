# S3 File Upload Extremely Slow

## Meaning

S3 file uploads are extremely slow (triggering performance issues or S3UploadSlow alarms) because network bandwidth is constrained, S3 transfer acceleration is not enabled, multipart upload configuration is suboptimal, object size exceeds optimal thresholds, regional network latency is high, or S3 request throttling affects upload performance. S3 upload performance degrades, file transfer times increase significantly, and application upload operations timeout. This affects the storage and data transfer layer and impacts user experience, typically caused by network issues, transfer configuration problems, or throttling; if using S3 with Transfer Acceleration, configuration may differ and applications may experience upload performance issues.

## Impact

S3 upload performance degrades; file transfer times increase significantly; application upload operations timeout; user experience is impacted; upload throughput is reduced; large file transfers fail; upload operations consume excessive time; application performance is severely affected. S3UploadSlow alarms may fire; if using S3 with Transfer Acceleration, configuration may differ; applications may experience errors or performance degradation due to slow uploads; user-facing upload functionality may be unusable.

## Playbook

1. Verify S3 bucket `<bucket-name>` exists and AWS service health for S3 in region `<region>` is normal.
2. Retrieve CloudWatch metrics for S3 Bucket `<bucket-name>` including BytesUploaded and PutRequests over the last 1 hour to identify upload performance patterns, analyzing upload throughput.
3. Retrieve the S3 Bucket `<bucket-name>` in region `<region>` and inspect its transfer acceleration configuration, request metrics configuration, and bucket location, verifying transfer acceleration status.
4. Query CloudWatch Logs for log groups containing S3 server access logs and filter for slow upload patterns or timeout events related to bucket `<bucket-name>`, including upload duration patterns.
5. Retrieve CloudWatch metrics for network performance including network latency and bandwidth utilization over the last 1 hour to identify network constraints, analyzing network metrics.
6. List S3 upload operations for bucket `<bucket-name>` and analyze upload duration patterns and object size distributions, checking if large objects affect performance.
7. Retrieve CloudWatch metrics for S3 Bucket `<bucket-name>` including ThrottledRequests if available and verify if request throttling affects uploads, checking for throttling patterns.
8. Retrieve the S3 Bucket `<bucket-name>` request metrics configuration and verify request metrics are enabled, checking if metrics provide upload performance insights.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for S3 transfer acceleration or request metrics configuration modification events related to bucket `<bucket-name>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch metrics for S3 bucket uploads (from Playbook step 2) including BytesUploaded and PutRequests to identify upload throughput patterns over the last hour. If throughput suddenly decreased, correlate the timestamp with network or configuration changes. If throughput has been consistently low, the issue is likely a persistent configuration problem.

2. Review network performance metrics (from Playbook step 5) including network latency and bandwidth utilization. If network latency is high or bandwidth is constrained, this directly impacts upload performance. If network metrics appear normal, the issue is likely S3 configuration or client-side.

3. Examine S3 server access logs (from Playbook step 4) to analyze upload duration patterns and identify slow upload events. If logs show specific patterns like timeouts or retries, network instability may be causing upload performance issues.

4. Verify S3 transfer acceleration configuration (from Playbook step 3) to determine if acceleration is enabled for the bucket. If uploading from geographic locations far from the bucket's region, enabling transfer acceleration can significantly improve upload speeds.

5. Analyze object size distributions (from Playbook step 6) to determine if large objects are being uploaded. For objects larger than 100MB, multipart uploads should be used. If large objects are uploaded as single requests, upload performance will be poor and timeouts are more likely.

6. Check for S3 request throttling (from Playbook step 7) by examining ThrottledRequests metrics if available. If the bucket is receiving very high request volumes (especially with common prefixes), S3 may throttle requests, causing slowdowns.

7. Review S3 request metrics configuration (from Playbook step 8) to verify detailed metrics are enabled for performance analysis. If request metrics are not configured, enable them for better visibility into upload performance.

8. Correlate CloudTrail events (from Playbook step 9) with upload slowdown timestamps within 30 minutes to identify any transfer acceleration or bucket configuration modifications that may have affected performance.

9. Compare upload performance trends over the last 4 hours. If slow performance is constant, focus on configuration issues like transfer acceleration or multipart settings. If slow performance is intermittent, focus on network issues or request throttling.

If no correlation is found within the specified time windows: extend timeframes to 24 hours, review alternative evidence sources including multipart upload configuration and client-side upload settings, check for gradual issues like network congestion or regional capacity constraints, verify external dependencies like internet connectivity or VPN tunnel performance, examine historical patterns of upload performance, check for S3 request throttling affecting uploads, verify S3 multipart upload part size configuration. Slow uploads may result from multipart upload misconfiguration, network path issues, client-side upload optimization problems, S3 request throttling, or S3 multipart upload part size configuration rather than immediate S3 bucket configuration changes.
