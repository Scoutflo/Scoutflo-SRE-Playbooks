# Network Security Audit

## Meaning

Network security audit indicates that network security configurations may be misconfigured, overly permissive, or violate security best practices (triggering alerts like NetworkSecurityAuditFailed or OverlyPermissiveNetworkConfig) because network policies show violations, network security configurations are misconfigured, network security policies are not enforced, network traffic patterns indicate suspicious activity, or network security audit findings indicate policy violations. Network security configurations show violations, network traffic patterns indicate suspicious activity, network policies are misconfigured, and network security audit findings indicate policy violations. This affects the security layer and network access control, typically caused by misconfigured network security settings, lack of network security monitoring, or security policy violations; if network security protects container workloads, container network policies may be misconfigured and applications may experience security risks.

## Impact

NetworkSecurityAuditFailed alerts fire; OverlyPermissiveNetworkConfig alerts fire; network access is overly permissive; security policies are violated; suspicious network traffic is detected; network security monitoring fails. Network security configurations show violations; if network security protects container workloads, container network policies may be misconfigured, pod network access may be overly permissive, and container applications may experience security risks; applications may experience security vulnerabilities or unauthorized network access risks.

## Playbook

1. Describe network policy <policy-name> in namespace <namespace> to inspect network policy rules, ingress rules, and egress rules, verifying network security configuration.
2. List recent events in namespace <namespace> sorted by timestamp to identify recent network policy events and security-related issues.
3. Retrieve network policies in namespace <namespace> with YAML output to analyse network policy rule configurations and identify overly permissive or misconfigured rules.
4. List services in namespace <namespace> with wide output to retrieve service network configurations and identify insecure network settings or misconfigured services.
5. Retrieve logs from network policy controller pods and filter for suspicious traffic patterns including unauthorized access attempts or port scans within the last 7 days.
6. Retrieve security audit findings for network security compliance checks and filter for findings with severity 'HIGH' or 'CRITICAL' related to network security misconfigurations.
7. Retrieve Prometheus metrics for network traffic including allowed_traffic and denied_traffic over the last 7 days to identify network traffic patterns.
8. Compare network security configuration change timestamps with security policy violation timestamps within 24 hours and verify whether network changes violate security policies, using network policy events as supporting evidence.

## Diagnosis

1. Review the network policy configurations from Steps 1 and 3. If policies allow ingress from any source or unrestricted egress, these represent high-priority security concerns. Identify which rules need tightening.

2. Analyze the security audit findings from Step 6. If HIGH or CRITICAL findings relate to network security, prioritize remediation. If findings show policy violations, identify the specific resources and namespaces affected.

3. If Step 5 network policy controller logs show suspicious traffic patterns or unauthorized access attempts, then security monitoring is detecting potential threats. Investigate source and destination of flagged traffic.

4. Review the network traffic metrics from Step 7. If allowed_traffic patterns show unexpected access paths, verify these are intentional. If denied_traffic is high, legitimate traffic may be blocked by overly restrictive policies.

5. If Step 8 configuration change timestamps correlate with security violations, then recent changes introduced the issue. Focus remediation on reverting or correcting those changes.

If analysis is inconclusive: Examine events from Step 2 for recent network policy events. Determine whether security violations are concentrated in specific namespaces (suggesting localized misconfiguration) or distributed (suggesting policy template issues). Verify that network security monitoring is correctly configured to detect and alert on violations.
