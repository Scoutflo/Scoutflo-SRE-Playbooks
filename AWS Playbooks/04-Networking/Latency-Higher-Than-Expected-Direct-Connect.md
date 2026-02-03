# Direct Connect Latency Higher Than Expected

## Meaning

Direct Connect latency is higher than expected (triggering performance issues or DirectConnectHighLatency alarms) because network path is suboptimal, Direct Connect virtual interface configuration is incorrect, BGP routing issues cause path inefficiencies, network congestion occurs, cross-connect configuration has problems, or Direct Connect link utilization is high causing congestion. Direct Connect latency increases, network performance degrades, and application response times increase. This affects the networking and connectivity layer and impacts application performance, typically caused by routing issues, congestion problems, or configuration errors; if using Direct Connect with VPN backup, routing behavior may differ and applications may experience latency issues.

## Impact

Direct Connect latency increases; network performance degrades; application response times increase; user experience is impacted; network throughput is reduced; latency-sensitive applications fail; network performance does not meet SLA requirements; connectivity quality degrades. DirectConnectHighLatency alarms may fire; if using Direct Connect with VPN backup, routing behavior may differ; applications may experience errors or performance degradation due to increased latency; latency-sensitive workloads may fail.

## Playbook

1. Verify Direct Connect virtual interface `<virtual-interface-id>` exists and AWS service health for Direct Connect in region `<region>` is normal.
2. Retrieve CloudWatch metrics for Direct Connect Virtual Interface `<virtual-interface-id>` including Latency and PacketLoss over the last 1 hour to identify latency patterns, analyzing latency trends.
3. Retrieve the Direct Connect Virtual Interface `<virtual-interface-id>` in region `<region>` and inspect its BGP configuration, virtual interface state, and connection status, verifying BGP status.
4. Query CloudWatch Logs for log groups containing Direct Connect events and filter for latency-related events or performance degradation patterns, including performance event details.
5. Retrieve CloudWatch metrics for network performance including round-trip time and packet loss over the last 1 hour to identify network path issues, analyzing network metrics.
6. List Direct Connect connection events for virtual interface `<virtual-interface-id>` and check connection state changes and performance metrics, analyzing connection health.
7. Retrieve CloudWatch metrics for Direct Connect Virtual Interface `<virtual-interface-id>` including BytesIn and BytesOut and verify link utilization, checking if high utilization causes congestion.
8. Retrieve the Direct Connect Virtual Interface `<virtual-interface-id>` BGP routes and verify route advertisements, checking if BGP routing affects latency.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Direct Connect virtual interface or BGP configuration modification events related to `<virtual-interface-id>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch metrics for Direct Connect virtual interface (from Playbook step 2) including Latency and PacketLoss over the last hour to identify latency patterns. If latency suddenly increased, correlate the timestamp with BGP or configuration changes. If latency is consistently high, the issue may be network path or capacity-related.

2. Review network performance metrics (from Playbook step 5) including round-trip time and packet loss. If packet loss is elevated, this directly causes latency increases due to retransmissions. If round-trip time increased without packet loss, the network path may have changed.

3. Examine Direct Connect virtual interface state and BGP status (from Playbook step 3) to verify the connection is up and BGP sessions are established. If BGP state is not Established, traffic may be routing through backup paths, causing increased latency.

4. Review link utilization metrics (from Playbook step 7) including BytesIn and BytesOut. If link utilization is approaching capacity (above 80%), congestion may be causing latency. If utilization recently increased, this correlates with latency increases.

5. Analyze BGP route configuration (from Playbook step 8) to verify route advertisements are optimal. If BGP routes changed or suboptimal routes are being preferred, traffic may take longer paths, increasing latency.

6. Review CloudWatch Logs containing Direct Connect events (from Playbook step 4) to identify any performance-related events or connection state changes.

7. Correlate CloudTrail events (from Playbook step 9) with latency increase timestamps within 5 minutes to identify any virtual interface or BGP configuration modifications. If configuration changes coincide with latency increases, those changes are the likely cause.

8. Compare latency patterns across different virtual interfaces within 1 hour. If latency is interface-specific, focus on that interface's configuration and BGP settings. If latency is connection-wide affecting all virtual interfaces, the issue is at the physical connection or carrier network level.

9. Analyze latency trends over the last 4 hours. If high latency is constant, the issue is configuration or capacity-related. If high latency is intermittent and correlates with specific times, network congestion during peak usage is likely.

If no correlation is found within the specified time windows: extend timeframes to 24 hours, review alternative evidence sources including BGP route advertisements and cross-connect configuration, check for gradual issues like network path changes or BGP route optimization, verify external dependencies like on-premises network configuration or carrier network performance, examine historical patterns of latency, check for Direct Connect link utilization affecting latency, verify Direct Connect jumbo frame configuration. High latency may result from BGP routing inefficiencies, cross-connect configuration issues, carrier network problems, Direct Connect link utilization congestion, or Direct Connect jumbo frame configuration rather than immediate Direct Connect configuration changes.
