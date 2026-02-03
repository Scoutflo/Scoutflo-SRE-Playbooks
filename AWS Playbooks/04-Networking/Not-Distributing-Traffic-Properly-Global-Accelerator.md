# AWS Global Accelerator Not Distributing Traffic Properly

## Meaning

AWS Global Accelerator is not distributing traffic properly (triggering traffic distribution failures or GlobalAcceleratorTrafficDistributionFailed alarms) because accelerator endpoint group configuration is incorrect, health checks fail preventing traffic routing, endpoint weights are misconfigured, traffic dial settings restrict distribution, endpoint health status prevents routing, or Global Accelerator listener configuration is incorrect. Global Accelerator traffic distribution fails, traffic is not routed to healthy endpoints, and traffic distribution is uneven. This affects the networking and global routing layer and reduces traffic optimization, typically caused by endpoint configuration issues, health check problems, or weight misconfiguration; if using Global Accelerator with multiple regions, routing behavior may differ and applications may experience traffic distribution failures.

## Impact

Global Accelerator traffic distribution fails; traffic is not routed to healthy endpoints; traffic distribution is uneven; endpoint group routing is ineffective; user requests are not optimally distributed; traffic dial settings restrict flow; accelerator routing performance degrades; global traffic optimization fails. GlobalAcceleratorTrafficDistributionFailed alarms may fire; if using Global Accelerator with multiple regions, routing behavior may differ; applications may experience errors or performance degradation due to uneven traffic distribution; user-facing services may experience inconsistent performance.

## Playbook

1. Verify Global Accelerator `<accelerator-arn>` exists and AWS service health for Global Accelerator in region `<region>` is normal.
2. Retrieve the Global Accelerator `<accelerator-arn>` in region `<region>` and inspect its endpoint group configurations, endpoint configurations, health check settings, and traffic dial configurations, verifying accelerator configuration.
3. Retrieve Global Accelerator endpoint health status for accelerator `<accelerator-arn>` and check endpoint health, health check results, and endpoint availability, analyzing health status.
4. Query CloudWatch Logs for log groups containing Global Accelerator events and filter for traffic distribution patterns or routing decision logs, including routing error details.
5. Retrieve CloudWatch metrics for Global Accelerator `<accelerator-arn>` including FlowLogs and HealthCheckStatus over the last 1 hour to identify traffic distribution patterns, analyzing traffic flow.
6. List Global Accelerator listeners for accelerator `<accelerator-arn>` and check listener configurations, endpoint group associations, and routing configurations, verifying listener setup.
7. Retrieve the Global Accelerator `<accelerator-arn>` endpoint weights and verify weight configuration, checking if endpoint weights affect distribution.
8. Retrieve the Global Accelerator `<accelerator-arn>` traffic dial settings and verify traffic dial configuration, checking if traffic dial restricts distribution.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Global Accelerator endpoint group or listener modification events related to accelerator `<accelerator-arn>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch metrics for Global Accelerator (from Playbook step 5) including FlowLogs and HealthCheckStatus to identify traffic distribution patterns. If metrics show traffic flowing to only some endpoints, health check failures or weight configuration is the issue. If metrics show no traffic at all, listener or accelerator configuration may be incorrect.

2. Review endpoint health status (from Playbook step 3) to verify all endpoints are healthy. If endpoints show unhealthy status, traffic cannot be routed to them. Identify which specific endpoints are failing health checks and examine their health check configuration.

3. Examine CloudWatch Logs containing Global Accelerator events (from Playbook step 4) to identify routing patterns or error messages. If logs show specific endpoints consistently receiving no traffic, verify their weight configuration and health status.

4. Verify endpoint group configurations (from Playbook step 2) including endpoint weights, traffic dial settings, and health check configurations. If endpoint weights are set to 0 or traffic dial is set to 0%, traffic will not be routed to those endpoints.

5. Review traffic dial settings (from Playbook step 8) to verify traffic is not being restricted. If traffic dial is set below 100%, only a portion of traffic is routed to that endpoint group. If investigating cross-region traffic issues, verify each regional endpoint group's traffic dial setting.

6. Examine listener configurations (from Playbook step 6) to verify port mappings and endpoint group associations are correct. If listener ports do not match application requirements or endpoint groups are not associated with the listener, traffic routing fails.

7. Correlate CloudTrail events (from Playbook step 9) with traffic distribution failure timestamps within 5 minutes to identify any endpoint group, listener, or weight modifications. If configuration changes coincide with when traffic distribution became uneven, those changes are the likely cause.

8. Compare traffic distribution patterns across different endpoint groups within 1 hour. If distribution issues are endpoint group-specific, verify that group's configuration and endpoint health. If distribution issues are accelerator-wide, check the accelerator or listener configuration.

If no correlation is found within the specified time windows: extend timeframes to 24 hours, review alternative evidence sources including endpoint weight configurations and listener routing settings, check for gradual issues like endpoint health degradation or traffic dial adjustments, verify external dependencies like endpoint availability or health check service health, examine historical patterns of traffic distribution, check for Global Accelerator cross-region routing issues, verify Global Accelerator client affinity settings. Distribution failures may result from endpoint weight misconfiguration, health check threshold issues, traffic dial setting problems, Global Accelerator cross-region routing issues, or Global Accelerator client affinity settings rather than immediate accelerator configuration changes.
