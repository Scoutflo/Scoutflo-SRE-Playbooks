# Policy Compliance Verification

## Meaning

Policy compliance verification indicates that policy compliance cannot be verified or policy compliance violations are detected (triggering alarms like PolicyComplianceViolation or PolicyComplianceVerificationFailed) because policy compliance checks fail, policy compliance violations are detected, policy compliance monitoring indicates problems, policy compliance configuration is missing, or policy compliance verification tools fail. Policy compliance verification shows failures, policy compliance violations are detected, policy compliance monitoring indicates problems, and policy compliance verification fails. This affects the compliance layer and policy adherence, typically caused by policy compliance configuration failures, policy compliance verification tool failures, policy violation detection issues, or policy compliance monitoring gaps; if policy compliance affects container workloads, container policy compliance may be violated and applications may experience policy adherence risks.

## Impact

PolicyComplianceViolation alarms fire; PolicyComplianceVerificationFailed alarms fire; policy compliance cannot be verified; policy compliance violations are detected; policy adherence may be compromised; policy risks may exist. Policy compliance verification shows failures; if policy compliance affects container workloads, container policy compliance may be violated, pod policy adherence may be at risk, and container applications may experience policy adherence risks; applications may experience policy compliance violations or policy adherence failures.

## Playbook

1. Retrieve Security Hub findings in region `<region>` and filter for findings with compliance status 'FAILED' related to policy compliance violations.
2. List Config rules in region `<region>` and retrieve Config rule evaluation results to identify rules with compliance status 'NON_COMPLIANT' related to policy violations.
3. Retrieve IAM policy compliance check results for account `<account-id>` and verify IAM policy compliance with security policies and least privilege principles.
4. Query CloudWatch Logs for log groups containing Config or Security Hub policy compliance events and filter for policy compliance violation patterns within the last 7 days.
5. Compare policy compliance verification failure timestamps with policy configuration change timestamps within 24 hours and verify whether policy changes introduce compliance violations, using Config rule evaluation results as supporting evidence.
6. Retrieve Security Hub finding details for policy compliance violations and inspect violation descriptions, affected policies, and remediation recommendations, checking violation severity.
7. List resource policies in region `<region>` and verify policy compliance with resource policy standards and security best practices, checking resource policy compliance.
8. Compare policy compliance violation remediation timestamps with violation detection timestamps over the last 30 days and verify whether violations are remediated promptly, using Security Hub finding history as supporting evidence.

## Diagnosis

1. **Analyze Security Hub findings from Step 1 and Step 6**: If CRITICAL/HIGH findings exist, prioritize remediation by severity. If finding provides remediation guidance, follow recommendations. If multiple policies have same finding, address the common pattern.

2. **Evaluate Config rule status from Step 2**: If specific rules show NON_COMPLIANT, identify the affected policies. If rules are correctly configured, violations are real policy issues. If rules have errors, fix rule configuration.

3. **Review IAM policy compliance from Step 3**: If IAM policies violate least privilege, narrow permissions. If policies have wildcards, replace with specific resources. If policies lack conditions, add appropriate constraints.

4. **Cross-reference with policy changes from Step 5**: If violations correlate with recent policy changes, those changes introduced non-compliance. If no changes correlate, existing policies were non-compliant before monitoring.

5. **Assess remediation timeliness from Step 8**: If violations persist for extended periods, remediation processes are ineffective. If violations are quickly remediated, compliance processes are working.

If the above analysis is inconclusive: Implement policy-as-code for compliance enforcement. Use IAM Access Analyzer for policy validation. Consider preventive controls (SCPs) over detective controls. Automate policy remediation where possible.
