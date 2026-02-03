# Policy Compliance Verification

## Meaning

Policy compliance verification indicates that policy compliance cannot be verified or policy compliance violations are detected (triggering alerts like PolicyComplianceViolation or PolicyComplianceVerificationFailed) because policy compliance checks fail, policy compliance violations are detected, policy compliance monitoring indicates problems, policy compliance configuration is missing, or policy compliance verification tools fail. Policy compliance verification shows failures, policy compliance violations are detected, policy compliance monitoring indicates problems, and policy compliance verification fails. This affects the compliance layer and policy adherence, typically caused by policy compliance configuration failures, policy compliance verification tool failures, policy violation detection issues, or policy compliance monitoring gaps; if policy compliance affects container workloads, container policy compliance may be violated and applications may experience policy adherence risks.

## Impact

PolicyComplianceViolation alerts fire; PolicyComplianceVerificationFailed alerts fire; policy compliance cannot be verified; policy compliance violations are detected; policy adherence may be compromised; policy risks may exist. Policy compliance verification shows failures; if policy compliance affects container workloads, container policy compliance may be violated, pod policy adherence may be at risk, and container applications may experience policy adherence risks; applications may experience policy compliance violations or policy adherence failures.

## Playbook

1. Describe namespace <namespace> to inspect namespace labels, annotations, and resource quotas that may be subject to policy compliance requirements.
2. List recent events in namespace <namespace> sorted by timestamp to identify recent events related to policy enforcement or compliance violations.
3. Retrieve security audit findings for namespace `<namespace>` and filter for findings with compliance status 'FAILED' related to policy compliance violations.
4. Retrieve rolebindings and clusterrolebindings in namespace <namespace> with YAML output to verify compliance with security policies and least privilege principles.
5. Retrieve logs from compliance monitoring pods and filter for policy compliance violation patterns within the last 7 days.
6. Compare policy compliance verification failure timestamps with policy configuration change timestamps within 24 hours and verify whether policy changes introduce compliance violations, using security audit findings as supporting evidence.
7. Retrieve security audit finding details for policy compliance violations and inspect violation descriptions, affected policies, and remediation recommendations, checking violation severity.
8. Compare policy compliance violation remediation timestamps with violation detection timestamps over the last 30 days and verify whether violations are remediated promptly, using security audit finding history as supporting evidence.

## Diagnosis

1. Review the security audit findings from Step 3. If findings show compliance status FAILED, identify the specific policies violated and affected resources. Prioritize remediation based on policy criticality.

2. Analyze the RBAC configurations from Step 4. If rolebindings or clusterrolebindings violate security policies or least privilege principles, these are high-priority compliance issues.

3. If Step 5 compliance monitoring logs show violation patterns, identify whether violations are concentrated in specific namespaces or distributed. Concentrated violations suggest localized misconfiguration; distributed violations suggest systemic policy gaps.

4. Review the violation remediation analysis from Step 8. If violations are not being remediated promptly after detection, then remediation processes need improvement. If remediations are occurring but new violations appear, then prevention measures are insufficient.

5. If Step 6 configuration change analysis shows compliance violations introduced by recent changes, focus on improving change review processes to prevent future violations.

If analysis is inconclusive: Examine events from Step 2 for policy enforcement issues. Review compliance standards status from Step 7 to identify which specific standards are failing. Determine whether violations are increasing over time (suggesting compliance posture degradation) or stable (suggesting known accepted risks).
