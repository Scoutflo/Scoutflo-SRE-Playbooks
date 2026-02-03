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

1. Analyze AWS service health from Playbook step 1 to verify Route 53 service availability. Route 53 is a global service; check for worldwide service health issues.

2. If hosted zone configuration from Playbook step 2 shows the hosted zone does not exist or DNS records are missing/incorrect, resolution fails at the authoritative level. Verify A, AAAA, or CNAME records exist for the queried domain.

3. If name server configuration from Playbook step 3 shows the domain's registered name servers do not match the Route 53 hosted zone name servers, DNS queries are sent to wrong authoritative servers. This is the most common cause of resolution failures for new hosted zones.

4. If TTL settings from Playbook step 4 show very long TTL values, DNS changes may not propagate for the duration of the TTL. Previous incorrect records may be cached by resolvers.

5. If routing policy from Playbook step 5 shows weighted, latency, failover, or geolocation routing with no healthy endpoints or misconfigured weights (all zero), no responses are returned.

6. If health checks from Playbook step 6 show all health checks for failover or weighted records are unhealthy, Route 53 may not return any records. Verify health check endpoints are accessible and returning expected responses.

7. If alias record configuration from Playbook step 7 points to a non-existent or unhealthy target (ELB, CloudFront, S3 website), resolution fails for the alias. Verify the alias target exists and is healthy.

8. If Route 53 query logs or CloudFront logs from Playbook step 8 show NXDOMAIN or SERVFAIL responses, identify the specific query patterns and response codes to diagnose the failure type.

If no correlation is found from the collected data: extend analysis timeframes to 48 hours to account for DNS propagation delays, verify domain registration is active and not expired, check for DNSSEC validation failures if DNSSEC is enabled, and test resolution from multiple geographic locations. Resolution failures may result from domain expiration, registrar lock, DNSSEC signature expiration, or ISP resolver caching issues.

