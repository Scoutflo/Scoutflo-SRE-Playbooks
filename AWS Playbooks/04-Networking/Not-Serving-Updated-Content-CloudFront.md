# CloudFront Not Serving Updated Content

## Meaning

CloudFront is not serving updated content (triggering cache issues or CloudFrontStaleContent alarms) because cache TTL settings are too long, cache invalidation is not performed, origin cache headers prevent updates, CloudFront distribution cache behavior is misconfigured, origin server returns stale content, or CloudFront cache invalidation is incomplete. CloudFront serves stale cached content, content updates are not reflected, and cache invalidation is ineffective. This affects the content delivery and CDN layer and reduces content freshness, typically caused by cache configuration issues, invalidation problems, or origin header conflicts; if using CloudFront with S3, cache behavior may differ and applications may experience stale content issues.

## Impact

CloudFront serves stale cached content; content updates are not reflected; cache invalidation is ineffective; user-facing content is outdated; CDN cache behavior is incorrect; content refresh fails; cache TTL prevents updates; application content remains stale. CloudFrontStaleContent alarms may fire; if using CloudFront with S3, cache behavior may differ; applications may experience errors or performance degradation due to stale content; user-facing content may be outdated.

## Playbook

1. Verify CloudFront distribution `<distribution-id>` exists and AWS service health for CloudFront in region `<region>` is normal.
2. Retrieve the CloudFront Distribution `<distribution-id>` in region `<region>` and inspect its cache behavior settings, default TTL configuration, and origin cache policy settings, verifying cache configuration.
3. Query CloudWatch Logs for log groups containing CloudFront access logs and filter for cache hit patterns or content age indicators related to distribution `<distribution-id>`, including cache hit/miss patterns.
4. Retrieve CloudFront invalidation history for distribution `<distribution-id>` and check invalidation status, completion times, and invalidation patterns, analyzing invalidation history.
5. Retrieve CloudWatch metrics for CloudFront Distribution `<distribution-id>` including CacheHitRate and BytesDownloaded over the last 24 hours to identify cache behavior patterns, analyzing cache metrics.
6. List CloudFront cache behaviors for distribution `<distribution-id>` and check TTL settings, cache policy configurations, and origin response headers, verifying cache behavior settings.
7. Retrieve the CloudFront Distribution `<distribution-id>` origin configuration and verify origin cache headers, checking if origin headers affect caching.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CloudFront distribution cache policy or invalidation events related to `<distribution-id>` within the last 24 hours, checking for configuration changes.
9. Retrieve CloudFront invalidation status for distribution `<distribution-id>` and verify recent invalidations completed successfully, checking if invalidations are pending.

## Diagnosis

1. Analyze CloudWatch metrics for CloudFront distribution (from Playbook step 5) including CacheHitRate over the last 24 hours to identify caching patterns. If cache hit rate is very high (close to 100%), content is being served from cache rather than fetched from origin. This is expected behavior based on TTL settings.

2. Review cache invalidation history (from Playbook steps 4 and 9) to verify if invalidations have been requested and completed successfully. If invalidations are pending or failed, cached content will not be updated. If invalidations completed but content is still stale, the invalidation paths may not match the affected content paths.

3. Examine CloudFront cache behavior configuration (from Playbook step 6) to verify TTL settings for the affected content paths. If minimum TTL, default TTL, or maximum TTL are set to high values, content will remain cached for extended periods regardless of origin updates.

4. Review CloudFront access logs (from Playbook step 3) to identify cache hit/miss patterns for specific content. If logs show cache hits for content that should be fresh, the cached version is being served. If logs show cache misses but content is still stale, origin may be returning outdated content.

5. Check origin cache headers (from Playbook step 7) to verify the origin server is not sending Cache-Control or Expires headers that override CloudFront's TTL settings. If origin sends long cache lifetimes, CloudFront respects those headers.

6. Correlate CloudTrail events (from Playbook step 8) with stale content reports to identify any cache policy or behavior modifications within the last 24 hours that may have affected caching.

7. Compare stale content patterns across different path patterns. If stale content is path-specific, that path's cache behavior configuration needs adjustment. If stale content is distribution-wide, check default cache behavior and origin configuration.

8. To resolve stale content immediately, create a cache invalidation for the affected paths. If invalidations are already in progress, check invalidation status to confirm completion.

9. For frequently updated content, consider reducing TTL values or implementing versioned URLs (e.g., appending query strings or including version numbers in file names) to ensure fresh content is fetched from origin.

If no correlation is found within the specified time windows: extend timeframes to 30 days, review alternative evidence sources including origin server cache headers and CloudFront edge location cache status, check for gradual issues like cache policy changes or origin response header modifications, verify external dependencies like origin server availability or cache invalidation service health, examine historical patterns of content staleness, check for CloudFront cache invalidation path pattern issues, verify CloudFront origin cache control headers. Stale content may result from origin server cache headers, CloudFront edge location cache persistence, cache invalidation delays, CloudFront cache invalidation path pattern issues, or CloudFront origin cache control headers rather than immediate distribution configuration changes.
