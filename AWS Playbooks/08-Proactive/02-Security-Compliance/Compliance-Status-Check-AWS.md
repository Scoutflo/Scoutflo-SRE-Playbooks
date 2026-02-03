# Compliance Status Check

## Meaning

Compliance status check indicates that compliance status cannot be verified or compliance violations are detected (triggering alarms like ComplianceViolation or ComplianceStatusCheckFailed) because compliance status checks fail, compliance violations are detected, compliance monitoring indicates problems, compliance configuration is missing, or compliance status data is unavailable. Compliance status checks show failures, compliance violations are detected, compliance monitoring indicates problems, and compliance status check fails. This affects the compliance layer and regulatory adherence, typically caused by compliance configuration failures, compliance monitoring tool failures, compliance violation detection issues, or compliance status check monitoring gaps; if compliance status affects container workloads, container compliance may be violated and applications may experience regulatory risks.

## Impact

ComplianceViolation alarms fire; ComplianceStatusCheckFailed alarms fire; compliance status cannot be verified; compliance violations are detected; regulatory adherence may be compromised; compliance risks may exist. Compliance status checks show failures; if compliance status affects container workloads, container compliance may be violated, pod compliance may be at risk, and container applications may experience regulatory risks; applications may experience compliance violations or regulatory non-compliance.

## Playbook

1. Retrieve Security Hub compliance findings in region `<region>` and filter for findings with compliance status 'FAILED' or severity 'HIGH' related to compliance violations.
2. Retrieve Config compliance summary for account `<account-id>` in region `<region>` and inspect compliance status by resource type and rule, verifying overall compliance posture.
3. List Config rules in region `<region>` and retrieve Config rule evaluation results to identify rules with compliance status 'NON_COMPLIANT'.
4. Query CloudWatch Logs for log groups containing Config or Security Hub compliance events and filter for compliance violation patterns within the last 7 days.
5. Retrieve Security Hub compliance standards status including CIS AWS Foundations Benchmark, PCI-DSS, or HIPAA compliance status to identify standard-specific violations.
6. Compare compliance status check failure timestamps with resource configuration change timestamps within 24 hours and verify whether configuration changes introduce compliance violations, using Config rule evaluation results as supporting evidence.
7. Retrieve Security Hub finding details for compliance violations and inspect violation descriptions, affected resources, and remediation recommendations, checking violation severity.
8. List IAM policies in account `<account-id>` and verify compliance with IAM security best practices and least privilege principles, checking IAM policy compliance.

## Diagnosis

1. **Analyze Security Hub findings from Step 1 and Step 7**: If CRITICAL/HIGH findings exist, prioritize remediation by severity. If finding provides remediation guidance, follow the recommendations. If multiple resources have the same finding, address the root cause.

2. **Evaluate compliance summary from Step 2**: If compliance percentage is declining, drift is occurring. If specific resource types show higher non-compliance, focus remediation there. If overall compliance is healthy, no immediate action needed.

3. **Review Config rule status from Step 3**: If specific rules show NON_COMPLIANT, identify affected resources. If rules were recently deployed, resources may have been previously non-compliant. If compliance worsened, recent changes caused issues.

4. **Cross-reference with configuration changes from Step 6**: If compliance violations correlate with recent resource changes, those changes introduced non-compliance. If no changes correlate, rules or standards may have been updated.

5. **Assess compliance standards from Step 5**: If CIS benchmark shows failures, foundational security controls need attention. If regulatory standards fail, compliance risk is elevated. If multiple standards fail on same control, prioritize that control.

If the above analysis is inconclusive: Review AWS Config conformance packs for compliance coverage. Check if custom rules have logic errors. Consider AWS Audit Manager for compliance automation. Implement compliance remediation automation.
