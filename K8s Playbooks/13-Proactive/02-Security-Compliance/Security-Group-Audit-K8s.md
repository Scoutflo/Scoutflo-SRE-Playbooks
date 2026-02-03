# Network Policy Audit

## Meaning

Network policy audit indicates that network policies may be overly permissive, misconfigured, or violate security best practices (triggering alerts like OverlyPermissiveNetworkPolicy or NetworkPolicyAuditFailed) because network policies allow overly broad access, unused network policies exist, network policy rules violate least privilege principles, network policy ingress rules allow access from all sources, or network policy egress rules are unrestricted. Network policies show overly permissive rules, network policy audit findings indicate violations, unused network policies are detected, and network policy configurations violate security policies. This affects the security layer and network access control, typically caused by misconfigured network policy rules, lack of network policy lifecycle management, or security policy violations; if network policies protect container workloads, container network access may be overly permissive and applications may experience security risks.

## Impact

NetworkPolicyAuditFailed alerts fire; OverlyPermissiveNetworkPolicy alerts fire; network access is overly permissive; security policies are violated; unused network policies consume resources; network policy rules violate least privilege principles. Network policy configurations show overly permissive rules; if network policies protect container workloads, container network access may be overly permissive, pod network policies may be misconfigured, and container applications may experience security risks; applications may experience security vulnerabilities or unauthorized access risks.

## Playbook

1. List all network policies in namespace <namespace> with wide output to retrieve their configurations including pod selectors and policy types.
2. List recent events in namespace <namespace> sorted by timestamp to identify network policy violations, security warnings, or policy-related errors.
3. Describe network policy <network-policy-name> in namespace <namespace> to inspect the network policy configuration including ingress and egress rules, pod selectors, and rule restrictiveness.
4. List pods in namespace `<namespace>` and verify network policy attachments to identify unused network policies not attached to any pods.
5. Retrieve logs from network policy controller pods and filter for traffic patterns indicating overly permissive network policy rules within the last 7 days.
6. Retrieve security audit findings for network policy compliance checks and filter for findings with severity 'HIGH' or 'CRITICAL' related to network policy misconfigurations.
7. Compare network policy rule modification timestamps with security policy change timestamps within 24 hours and verify whether network policy changes violate security policies, using network policy events as supporting evidence.
8. Retrieve the NetworkPolicy `<network-policy-name>` rule usage metrics and verify whether rules are actively used or unused, checking rule utilization patterns.

## Diagnosis

1. Review the network policy configurations from Steps 3-4. If policies allow ingress from all namespaces or all pods, or if egress is unrestricted, these represent the highest-priority security concerns requiring immediate tightening.

2. Analyze the pod-to-policy mapping from Step 4. If network policies are not attached to any pods, they are unused and should be reviewed for removal or proper pod selector configuration.

3. If Step 5 network policy controller logs show traffic patterns indicating overly permissive rules being actively used for unintended access, then policy rules need immediate restriction. If logs show denied traffic that should be allowed, then policies may be too restrictive.

4. Review security audit findings from Step 6. If HIGH or CRITICAL findings relate to network policy misconfigurations, prioritize these for remediation. If findings are lower severity, schedule remediation as part of regular maintenance.

5. If Step 8 rule usage metrics show rules that are never matched, these rules may be redundant or incorrectly configured. If rules are heavily matched, verify the traffic patterns are intentional.

If analysis is inconclusive: Examine events from Step 2 for recent network policy modifications that may have introduced violations. Determine whether overly permissive configurations are concentrated in specific namespaces (suggesting localized misconfiguration) or distributed (suggesting policy template issues). Verify that network policy lifecycle management processes exist for ongoing policy maintenance.
