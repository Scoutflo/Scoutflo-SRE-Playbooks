# AWS WAF Rules Causing False Positives

## Meaning

AWS WAF rules are causing false positives (triggering incorrect blocking or WAFFalsePositive alarms) because WAF rules are too restrictive, rule conditions incorrectly match legitimate requests, rule priorities cause incorrect blocking, rate-based rules trigger on normal traffic, IP reputation rules block valid IPs, or WAF rule action overrides allow rules incorrectly. Legitimate user traffic is blocked, WAF rules cause false positives, and legitimate requests return 403 Forbidden errors. This affects the security and application access layer and reduces application availability, typically caused by rule misconfiguration, condition threshold issues, or priority conflicts; if using WAF with CloudFront vs Application Load Balancer, rule behavior may differ and applications may experience false positive blocking.

## Impact

Legitimate user traffic is blocked; WAF rules cause false positives; legitimate requests return 403 Forbidden errors; user access is denied incorrectly; WAF blocking alarms fire; application availability is impacted; security rules are too aggressive; user experience is degraded. WAFFalsePositive alarms may fire; if using WAF with CloudFront vs Application Load Balancer, rule behavior may differ; applications may experience errors or performance degradation due to blocked legitimate traffic; user-facing services may become inaccessible.

## Playbook

1. Verify WAF Web ACL `<web-acl-id>` exists and AWS service health for WAF in region `<region>` is normal.
2. Retrieve the WAF Web ACL `<web-acl-id>` in region `<region>` and inspect its rule configurations, rule priorities, rule actions, and rule conditions, verifying rule evaluation order.
3. Query CloudWatch Logs for log groups containing WAF logs and filter for blocked request patterns, 403 error patterns, or false positive indicators related to Web ACL `<web-acl-id>`, including blocking reason details.
4. Retrieve CloudWatch metrics for WAF Web ACL `<web-acl-id>` including BlockedRequests and AllowedRequests over the last 24 hours to identify blocking patterns, analyzing blocking frequency.
5. List WAF rule evaluation results for Web ACL `<web-acl-id>` and check rule match patterns, blocking reasons, and request characteristics, analyzing rule matches.
6. Query CloudWatch Logs for log groups containing application access logs and filter for legitimate requests that were blocked by WAF, including request details.
7. Retrieve the WAF Web ACL `<web-acl-id>` default action and verify default action configuration, checking if default action affects legitimate traffic.
8. Retrieve the WAF Web ACL `<web-acl-id>` associated resource (CloudFront distribution or ALB) and verify WAF association, checking if association affects rule evaluation.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for WAF rule or Web ACL modification events related to `<web-acl-id>` within the last 24 hours, checking for rule changes.

## Diagnosis

1. **Analyze WAF Logs from Steps 3 and 5**: Review WAF logs for blocked request patterns and the specific rules causing blocks. If WAF logs from Step 3 identify specific rule IDs consistently blocking legitimate traffic, then those rules need adjustment. Extract the `terminatingRuleId` and request characteristics from blocked requests. If logs show multiple rules blocking, continue to step 2.

2. **Evaluate Blocking Metrics from Step 4**: If CloudWatch metrics from Step 4 show BlockedRequests spiking at specific times or correlating with legitimate traffic patterns (e.g., business hours, deployments), then traffic pattern changes are triggering overly sensitive rules. Compare BlockedRequests to AllowedRequests ratio - if blocking rate exceeds expected baseline, then rule sensitivity is too high. Continue to step 3.

3. **Review Rule Configuration from Step 2**: If the blocking rules from Step 2 contain overly broad regex patterns, low rate-based thresholds, or aggressive SQL injection/XSS detection, then rule conditions need refinement. Check rule priorities - if a blocking rule has higher priority than an allow rule that should whitelist the traffic, then priority misconfiguration exists. If rules appear correct, continue to step 4.

4. **Check Application Access Patterns from Step 6**: If application logs from Step 6 show legitimate requests being blocked with 403 errors, correlate request characteristics with WAF rule conditions. If legitimate requests contain patterns matching security rules (e.g., code snippets, special characters), then rule exceptions or custom rules are needed. Compare blocked request User-Agents, IPs, and paths to identify patterns.

5. **Correlate with Rule Modifications from Step 9**: If CloudTrail events from Step 9 show WAF rule or Web ACL modifications within 5 minutes before false positives began, then recent changes introduced the issue. Review managed rule group updates - if AWS Managed Rules were updated, then new signatures may be causing false positives.

**If no correlation is found**: Extend analysis to 30 days using WAF logs. Check rate-based rule thresholds against normal traffic volumes from Step 4 metrics. Verify IP reputation lists are not blocking legitimate traffic. For managed rules causing issues, consider using rule action overrides to count instead of block, or add specific exceptions. Review custom rule conflicts with managed rules.
