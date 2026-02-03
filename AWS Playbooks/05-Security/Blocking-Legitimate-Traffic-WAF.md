# AWS WAF Blocking Legitimate Traffic

## Meaning

AWS WAF is blocking legitimate traffic (triggering false positives or WAFBlockingLegitimateTraffic alarms) because WAF rules are too restrictive, rule conditions incorrectly match legitimate requests, rule priorities cause incorrect blocking, rate-based rules trigger on normal traffic, IP reputation rules block valid IPs, or WAF rule action overrides allow rules incorrectly. Legitimate user traffic is blocked, WAF rules cause false positives, and legitimate requests return 403 Forbidden errors. This affects the security and application access layer and reduces application availability, typically caused by rule misconfiguration, condition threshold issues, or priority conflicts; if using WAF with CloudFront vs Application Load Balancer, rule behavior may differ and applications may experience false positive blocking.

## Impact

Legitimate user traffic is blocked; WAF rules cause false positives; legitimate requests return 403 Forbidden errors; user access is denied incorrectly; WAF blocking alarms fire; application availability is impacted; security rules are too aggressive; user experience is degraded. WAFBlockingLegitimateTraffic alarms may fire; if using WAF with CloudFront vs Application Load Balancer, rule behavior may differ; applications may experience errors or performance degradation due to blocked legitimate traffic; user-facing services may become inaccessible.

## Playbook

1. Verify WAF Web ACL `<web-acl-id>` exists and AWS service health for WAF in region `<region>` is normal.
2. Retrieve the WAF Web ACL `<web-acl-id>` in region `<region>` and inspect its rule configurations, rule priorities, rule actions, and rule conditions, verifying rule evaluation order.
3. Query CloudWatch Logs for log groups containing WAF logs and filter for blocked request patterns, 403 error patterns, or false positive indicators related to Web ACL `<web-acl-id>`, including blocking reason details.
4. Retrieve CloudWatch metrics for WAF Web ACL `<web-acl-id>` including BlockedRequests and AllowedRequests over the last 1 hour to identify blocking patterns, analyzing blocking frequency.
5. List WAF rule evaluation results for Web ACL `<web-acl-id>` and check rule match patterns, blocking reasons, and request characteristics, analyzing rule matches.
6. Query CloudWatch Logs for log groups containing application access logs and filter for legitimate requests that were blocked by WAF, including request details.
7. Retrieve the WAF Web ACL `<web-acl-id>` default action and verify default action configuration, checking if default action affects legitimate traffic.
8. Retrieve the WAF Web ACL `<web-acl-id>` associated resource (CloudFront distribution or ALB) and verify WAF association, checking if association affects rule evaluation.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for WAF rule or Web ACL modification events related to `<web-acl-id>` within the last 24 hours, checking for rule changes.

## Diagnosis

1. Analyze CloudWatch Logs containing WAF logs (from Playbook step 3) to identify blocked request patterns, including the specific rules that triggered blocks and request characteristics. If logs show a specific rule consistently blocking legitimate requests, that rule's conditions need adjustment. If multiple rules are blocking, examine rule priority order.

2. Review CloudWatch metrics for WAF BlockedRequests and AllowedRequests (from Playbook step 4) to establish baseline blocking patterns. If blocked request count suddenly increased, correlate the timestamp with recent rule modifications. If blocking pattern changed gradually, the issue may be related to traffic pattern changes or managed rule updates.

3. Examine WAF rule evaluation results (from Playbook step 5) to understand which specific rule conditions are matching legitimate requests. If rule conditions use overly broad patterns (e.g., regex matching common request strings), the conditions need refinement. If rate-based rules are triggering, verify threshold values against normal traffic volumes.

4. Compare WAF logs with application access logs (from Playbook step 6) to confirm blocked requests are truly legitimate. If blocked requests contain expected user-agent strings, valid source IPs, and proper request formats, the WAF rules are too restrictive.

5. Correlate CloudTrail events (from Playbook step 9) with blocking increase timestamps within 5 minutes to identify any WAF rule or Web ACL modifications. If rule changes coincide with increased blocking, those changes introduced overly restrictive conditions.

6. Analyze WAF rule configuration (from Playbook step 2) including rule priorities, actions, and conditions. If managed rules conflict with custom rules or if rule priorities cause incorrect evaluation order, legitimate traffic may be blocked before allow rules are evaluated.

7. If rate-based rules are involved, compare current traffic volume against rate-based rule thresholds. If normal traffic patterns exceed thresholds, increase the threshold values or add exceptions for known legitimate traffic sources.

If no correlation is found within the specified time windows: extend timeframes to 7 days, review alternative evidence sources including IP reputation data and request pattern analysis, check for gradual issues like rule condition threshold changes or IP reputation list updates, verify external dependencies like threat intelligence feed updates or rule condition evaluation logic, examine historical patterns of false positives, check for WAF rule action override issues, verify WAF custom rule vs managed rule conflicts. False positives may result from rule condition threshold issues, IP reputation list inaccuracies, rate-based rule misconfiguration, WAF rule action overrides, or WAF custom rule vs managed rule conflicts rather than immediate WAF rule changes.
