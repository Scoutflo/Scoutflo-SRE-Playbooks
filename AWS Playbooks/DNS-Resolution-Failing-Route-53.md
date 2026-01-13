# Route 53 DNS Resolution Failing

## Meaning

Route 53 DNS resolution fails or returns incorrect results (triggering DNS resolution errors or Route53DNSResolutionFailed alarms) because hosted zone is incorrectly configured, DNS records (A, AAAA, CNAME) are incorrectly set up, name servers are incorrectly configured for the domain, DNS resolution tests fail, Route 53 health checks indicate issues, TTL settings affect propagation, or routing policies are misconfigured. DNS queries fail, domain names cannot resolve, and DNS resolution errors occur. This affects the DNS and service discovery layer and blocks domain resolution, typically caused by DNS configuration issues, health check failures, or routing policy problems; if using Route 53 with CloudFront or Global Accelerator, DNS configuration may differ and applications may experience domain resolution failures.

## Impact

DNS queries fail; domain names cannot resolve; applications cannot connect to services; DNS resolution errors occur; service endpoints become unreachable; DNS propagation issues may occur; health check failures may trigger; user-facing services become inaccessible; service discovery fails. Route53DNSResolutionFailed alarms fire; if using Route 53 with CloudFront, alias records may behave differently; applications may experience errors or performance degradation due to DNS resolution failures; service-to-service communication may be blocked.

## Playbook

1. Verify Route 53 hosted zone `<hosted-zone-id>` exists and domain is registered, and AWS service health for Route 53 in region `<region>` is normal.
2. Retrieve the Route 53 Hosted Zone `<hosted-zone-id>` and verify hosted zone is correctly configured and DNS records (A, AAAA, CNAME) are correctly set up, checking hosted zone status and record types and values.
3. Retrieve the Route 53 Hosted Zone `<hosted-zone-id>` name server configuration and ensure name servers are correctly configured for the domain, checking name server delegation.
4. Retrieve the Route 53 Hosted Zone `<hosted-zone-id>` TTL settings and verify TTL values are appropriate, checking TTL configuration.
5. Retrieve the Route 53 Hosted Zone `<hosted-zone-id>` routing policy configuration and verify routing policies (Simple, Weighted, Latency, Failover) are correctly configured, checking policy settings.
6. Retrieve Route 53 health checks associated with hosted zone `<hosted-zone-id>` and check health check status if configured, verifying health check results.
7. Retrieve the Route 53 Hosted Zone `<hosted-zone-id>` alias record configuration and verify alias records point to correct resources, checking alias target configuration.
8. Query CloudWatch Logs for log groups containing Route 53 query logs or CloudFront logs and filter for DNS resolution failures or issues related to hosted zone `<hosted-zone-id>`, checking query log and CloudFront access log analysis.

## Diagnosis

1. Compare hosted zone configuration change timestamps with DNS resolution failure timestamps within 5 minutes and verify whether resolution failures began after hosted zone changes, using Route 53 configuration events as supporting evidence.
2. Correlate DNS record modification timestamps with resolution error timestamps and verify whether resolution errors occurred after record changes, using Route 53 record change events as supporting evidence.
3. Compare name server configuration change timestamps with DNS resolution failure timestamps within 24 hours and verify whether name server changes caused resolution failures, using domain registration events as supporting evidence.
4. Compare Route 53 health check failure timestamps with DNS resolution failure timestamps within 5 minutes and verify whether health check failures affected DNS resolution, using Route 53 health check events as supporting evidence.
5. Analyze DNS resolution failure frequency over the last 15 minutes to determine if failures are constant (configuration issue) or intermittent (propagation delays).

If no correlation is found within the specified time windows: extend timeframes to 48 hours for DNS propagation, review alternative evidence sources including DNS query logs and resolver logs, check for gradual issues like TTL expiration, verify external dependencies like domain registrar configuration, examine historical patterns of DNS resolution, check for Route 53 CloudFront alias configuration issues, verify Route 53 Global Accelerator integration. Resolution failures may result from DNS propagation delays, TTL caching issues, external DNS resolver problems, Route 53 health check failures, CloudFront distribution issues, or Global Accelerator routing problems rather than immediate Route 53 configuration changes.

