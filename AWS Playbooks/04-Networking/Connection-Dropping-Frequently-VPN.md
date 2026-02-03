# VPN Connection Dropping Frequently

## Meaning

VPN connection drops frequently (triggering connectivity failures or VPNConnectionDropped alarms) because VPN tunnel stability issues occur, network path changes cause tunnel renegotiation, VPN gateway or customer gateway configuration is incorrect, tunnel authentication fails, network latency causes tunnel timeouts, or VPN gateway resource constraints cause instability. VPN connections drop frequently, remote access is interrupted, and site-to-site connectivity fails. This affects the networking layer and disrupts connectivity, typically caused by tunnel configuration issues, network path problems, or gateway resource constraints; if using AWS Site-to-Site VPN with Direct Connect, routing may affect stability and applications may experience connectivity interruptions.

## Impact

VPN connections drop frequently; remote access is interrupted; site-to-site connectivity fails; VPN tunnel renegotiation occurs; connection stability is compromised; user connectivity is unreliable; VPN connection alarms fire; network reliability degrades. VPNConnectionDropped alarms may fire; if using AWS Site-to-Site VPN with Direct Connect, routing may affect stability; applications may experience errors or performance degradation due to connection interruptions; site-to-site connectivity may be unreliable.

## Playbook

1. Verify VPN connection `<vpn-connection-id>` exists and AWS service health for VPC in region `<region>` is normal.
2. Retrieve the VPN Connection `<vpn-connection-id>` in region `<region>` and inspect its tunnel status, connection state, and tunnel configuration, verifying tunnel states.
3. Query CloudWatch Logs for log groups containing VPN connection logs and filter for tunnel down events, renegotiation patterns, or connection failure messages, including tunnel state transitions.
4. Retrieve CloudWatch metrics for VPN Connection `<vpn-connection-id>` including TunnelState, TunnelDataIn, and TunnelDataOut over the last 1 hour to identify connection drop patterns, analyzing drop frequency.
5. Retrieve CloudWatch alarms associated with VPN Connection `<vpn-connection-id>` and check for alarms in ALARM state related to tunnel status, verifying alarm configurations.
6. List VPN connection events for connection `<vpn-connection-id>` and check tunnel state change timestamps and renegotiation frequency, analyzing connection stability.
7. Retrieve the VPN Connection `<vpn-connection-id>` customer gateway configuration and verify customer gateway IP address and routing configuration, checking gateway configuration.
8. Retrieve CloudWatch metrics for VPN Connection `<vpn-connection-id>` including TunnelState and verify tunnel up/down patterns, checking if both tunnels are affected.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for VPN connection or customer gateway modification events related to connection `<vpn-connection-id>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. Analyze CloudWatch alarm history (from Playbook step 5) to identify when VPNConnectionDropped or tunnel state alarms first triggered. This timestamp establishes when connection instability began.

2. If CloudWatch metrics (from Playbook step 4) show TunnelState transitions (up to down) around the alarm time, examine whether both tunnels or only one tunnel is affected. Single tunnel issues suggest tunnel-specific configuration; both tunnels suggest gateway or network issues.

3. If VPN connection logs (from Playbook step 3) show renegotiation patterns or authentication failures around drop timestamps, IKE Phase 1 or Phase 2 negotiation issues are causing drops during rekey operations.

4. If TunnelDataIn/TunnelDataOut metrics (from Playbook step 4 and step 8) show traffic stops before drops, DPD (Dead Peer Detection) timeouts may be triggering tunnel teardown due to idle periods.

5. If CloudTrail shows VPN configuration changes (from Playbook step 9) around drop timestamps, those modifications may have caused tunnel renegotiation or incompatible settings.

6. If customer gateway configuration (from Playbook step 7) shows recent IP address or routing changes, verify the customer gateway matches AWS VPN tunnel configuration requirements.

7. If connection event history (from Playbook step 6) shows periodic drops at consistent intervals, DPD timeout or rekey timer misconfiguration is likely causing predictable tunnel cycling.

If no correlation is found: extend analysis to 24 hours, review customer gateway logs for authentication failures, check for Direct Connect routing conflicts affecting VPN failover, verify internet path stability between customer gateway and AWS endpoints, and examine VPN gateway resource constraints.
