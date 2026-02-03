# AWS Shield Not Mitigating DDoS Attacks

## Meaning

AWS Shield is not mitigating DDoS attacks (triggering protection failures or ShieldMitigationFailed alarms) because Shield is not enabled, Shield Advanced is not subscribed, attack detection thresholds are not met, Shield mitigation rules are misconfigured, Shield service encounters errors during attack mitigation, or Shield protection scope does not cover targeted resources. AWS Shield DDoS protection fails, DDoS attacks are not mitigated, and service availability is compromised. This affects the security and DDoS protection layer and compromises service availability, typically caused by Shield configuration issues, subscription problems, or detection threshold misconfiguration; if using Shield Advanced vs Shield Standard, mitigation capabilities differ and applications may experience DDoS protection failures.

## Impact

AWS Shield DDoS protection fails; DDoS attacks are not mitigated; service availability is compromised; attack traffic reaches resources; Shield protection automation is ineffective; DDoS attack detection fails; service reliability is impacted; security protection is compromised. ShieldMitigationFailed alarms may fire; if using Shield Advanced vs Shield Standard, mitigation capabilities differ; applications may experience errors or performance degradation due to DDoS attacks; service availability may be completely compromised.

## Playbook

1. Verify AWS Shield protection for resource `<resource-arn>` exists and AWS service health for Shield in region `<region>` is normal.
2. Retrieve the AWS Shield protection configuration for resource `<resource-arn>` in region `<region>` and inspect Shield enablement status, Shield Advanced subscription, and protection settings, verifying Shield is enabled.
3. Query CloudWatch Logs for log groups containing Shield events and filter for DDoS attack detection patterns, mitigation events, or protection failure messages, including mitigation error details.
4. Retrieve CloudWatch metrics for Shield protection including AttackCount and MitigatedAttackCount over the last 7 days to identify attack patterns and mitigation effectiveness, analyzing mitigation metrics.
5. List Shield-protected resources and check protection status, attack history, and mitigation configuration, verifying protection scope.
6. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Shield configuration or attack mitigation events, checking for configuration changes.
7. Retrieve the AWS Shield Advanced subscription status and verify Shield Advanced subscription, checking if subscription affects mitigation capabilities.
8. Retrieve CloudWatch metrics for Shield protection including AttackTraffic and verify attack traffic patterns, checking if attack detection thresholds are met.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Shield protection configuration modification events related to resource `<resource-arn>` within the last 7 days, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Metrics from Steps 4 and 8**: Review Shield metrics for attack detection and mitigation patterns. If CloudWatch metrics from Step 4 show AttackCount > 0 but MitigatedAttackCount = 0, then attacks are being detected but not mitigated. If metrics from Step 8 show attack traffic below detection thresholds, then attack volume may not trigger automatic mitigation. If metrics show no attack detection, continue to step 2.

2. **Verify Shield Protection Configuration from Step 2**: If Shield protection from Step 2 shows the resource is not protected or Shield is not enabled, then lack of protection is the root cause. Check Shield Advanced subscription status from Step 7 - if Shield Advanced is required for the attack type but only Standard is enabled, then subscription level is insufficient. If protection is properly configured, continue to step 3.

3. **Check Protection Scope from Step 5**: If the protected resources list from Step 5 does not include the targeted resource, then incomplete protection scope is the issue. Verify that CloudFront distributions, Route 53 hosted zones, ELBs, Elastic IPs, and Global Accelerators are all covered. If scope is complete, continue to step 4.

4. **Review CloudWatch Logs and CloudTrail Events from Steps 3 and 6**: If CloudWatch Logs from Step 3 show Shield mitigation events but with errors or partial mitigation, then mitigation rule configuration may be suboptimal. If CloudTrail events from Step 6 show Shield configuration modifications correlating with mitigation failures, then recent changes affected protection. If logs show protection failures for specific attack vectors, then attack type may not be covered.

5. **Correlate Shield Advanced Features from Step 7**: If using Shield Advanced, verify DDoS Response Team (DRT) engagement and proactive engagement features are configured. If Shield Advanced metrics show lower mitigation rates than expected, then advanced features may not be properly enabled or the attack pattern is novel.

**If no correlation is found**: Extend analysis to 30 days using CloudWatch metrics from Step 4. If mitigation failures are constant, verify Shield is properly enabled for all resources. If failures are intermittent, investigate attack patterns that may evade standard detection. Check CloudTrail events from Step 9 for protection configuration changes and verify Shield service health from Step 1.
