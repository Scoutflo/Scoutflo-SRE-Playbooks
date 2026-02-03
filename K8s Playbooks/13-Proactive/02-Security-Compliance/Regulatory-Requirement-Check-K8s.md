# Regulatory Requirement Check

## Meaning

Regulatory requirement check indicates that regulatory compliance cannot be verified or regulatory requirement violations are detected (triggering alerts like RegulatoryComplianceViolation or RegulatoryRequirementCheckFailed) because regulatory compliance checks fail, regulatory requirement violations are detected, regulatory compliance monitoring indicates problems, regulatory compliance configuration is missing, or regulatory requirement verification tools fail. Regulatory requirement checks show failures, regulatory requirement violations are detected, regulatory compliance monitoring indicates problems, and regulatory requirement check fails. This affects the compliance layer and regulatory adherence, typically caused by regulatory compliance configuration failures, regulatory requirement verification tool failures, regulatory violation detection issues, or regulatory compliance monitoring gaps; if regulatory requirements affect container workloads, container regulatory compliance may be violated and applications may experience regulatory risks.

## Impact

RegulatoryComplianceViolation alerts fire; RegulatoryRequirementCheckFailed alerts fire; regulatory compliance cannot be verified; regulatory requirement violations are detected; regulatory adherence may be compromised; regulatory risks may exist. Regulatory requirement checks show failures; if regulatory requirements affect container workloads, container regulatory compliance may be violated, pod regulatory adherence may be at risk, and container applications may experience regulatory risks; applications may experience regulatory compliance violations or regulatory non-compliance.

## Playbook

1. List pods, deployments, and services in namespace <namespace> with wide output to identify all resources in the namespace subject to regulatory compliance requirements.
2. List recent events in namespace <namespace> sorted by timestamp to identify recent events that may indicate regulatory compliance issues or policy violations.
3. Retrieve compliance standards status including GDPR, HIPAA, PCI-DSS, or SOC 2 compliance status to identify regulatory requirement violations.
4. List secrets in namespace <namespace> to verify secret management practices and identify potential regulatory compliance gaps related to sensitive data handling.
5. Retrieve security audit findings for namespace `<namespace>` and filter for findings with compliance status 'FAILED' related to regulatory compliance violations.
6. Retrieve logs from compliance monitoring pods and filter for regulatory compliance violation patterns within the last 7 days.
7. Compare regulatory requirement check failure timestamps with pod configuration change timestamps within 24 hours and verify whether configuration changes introduce regulatory violations, using security audit findings as supporting evidence.
8. Retrieve security audit finding details for regulatory compliance violations and inspect violation descriptions, affected resources, and remediation recommendations, checking violation severity and regulatory impact.

## Diagnosis

1. Review the compliance standards status from Step 3. If specific regulations (GDPR, HIPAA, PCI-DSS, SOC 2) show violations, identify the specific requirements not being met and the resources causing violations.

2. Analyze the security audit findings from Step 5. If findings show FAILED compliance status, prioritize remediation based on regulatory severity and potential penalties. If findings are clean, regulatory compliance is maintained.

3. If Step 4 secret management practices show gaps (e.g., unencrypted secrets, missing rotation), these may violate data protection regulations. Address secret management as high priority.

4. Review the violation details from Step 8. If violations include specific resources and remediation recommendations, follow the recommendations. If details are insufficient, additional investigation is needed.

5. If Step 7 configuration change analysis shows regulatory violations introduced recently, focus on reversing or correcting those changes to restore compliance.

If analysis is inconclusive: Examine events from Step 2 for compliance-related issues. Review the compliance monitoring logs from Step 6 for violation patterns. Determine whether violations are concentrated in specific compliance frameworks (suggesting framework-specific gaps) or distributed across frameworks (suggesting systemic compliance issues).
