# Compliance Check

## Meaning

Compliance check indicates that AWS resources or configurations violate compliance requirements, security standards, or regulatory policies (triggering alarms like ComplianceViolation or SecurityComplianceFailed) because Security Hub findings indicate compliance failures, Config rule evaluations show non-compliance, compliance checks fail, security standards are violated, or regulatory requirements are not met. Compliance check results show violations, Security Hub findings indicate non-compliance, Config rule evaluations show failures, and compliance status indicates policy violations. This affects the security layer and compliance posture, typically caused by misconfigured security settings, non-compliant resource configurations, compliance policy violations, or compliance monitoring failures; if compliance affects container workloads, container security configurations may violate policies and applications may experience compliance risks.

## Impact

ComplianceViolation alarms fire; SecurityComplianceFailed alarms fire; compliance requirements are violated; security standards are not met; regulatory requirements are not satisfied; compliance posture is degraded. Compliance check results show violations; if compliance affects container workloads, container security configurations may violate policies, pod security contexts may be non-compliant, and container applications may experience compliance risks; applications may experience compliance violations or regulatory non-compliance.

## Playbook

1. Retrieve Security Hub findings in region `<region>` and filter for findings with compliance status 'FAILED' or severity 'HIGH' related to compliance violations.
2. List Config rules in region `<region>` and retrieve Config rule evaluation results to identify rules with compliance status 'NON_COMPLIANT'.
3. Retrieve Config compliance summary for account `<account-id>` in region `<region>` and inspect compliance status by resource type and rule, verifying overall compliance posture.
4. Query CloudWatch Logs for log groups containing Config or Security Hub compliance events and filter for compliance violation patterns within the last 7 days.
5. Retrieve Security Hub compliance standards status including CIS AWS Foundations Benchmark, PCI-DSS, or HIPAA compliance status to identify standard-specific violations.
6. Compare Config rule evaluation timestamps with resource configuration change timestamps within 24 hours and verify whether configuration changes introduce compliance violations, using Config rule evaluation results as supporting evidence.
7. Retrieve Security Hub finding details for compliance violations and inspect violation descriptions, affected resources, and remediation recommendations, checking violation severity.
8. List IAM policies in account `<account-id>` and verify compliance with IAM security best practices and least privilege principles, checking IAM policy compliance.

## Diagnosis

1. **Analyze Security Hub findings from Step 1 and Step 7**: If CRITICAL/HIGH findings exist, prioritize remediation by severity. If finding provides remediation guidance, follow the recommendations. If multiple resources have the same finding, address the root cause rather than individual resources.

2. **Evaluate Config rule status from Step 2**: If specific Config rules show NON_COMPLIANT, identify affected resources. If rules were recently deployed and show high non-compliance, resources were already non-compliant. If previously compliant rules show new violations, recent changes caused the issue.

3. **Review compliance standards from Step 5**: If CIS benchmark shows failures, foundational security controls need attention. If PCI-DSS or HIPAA shows failures, regulatory compliance is at risk. If multiple standards fail on the same control, prioritize that control.

4. **Cross-reference with configuration changes from Step 6**: If Config rule violations correlate with recent resource changes, those changes introduced non-compliance. If violations exist without recent changes, resources were always non-compliant or rules were newly applied.

5. **Assess compliance summary from Step 3**: If compliance percentage is declining, drift is occurring. If specific resource types show higher non-compliance, focus remediation there. If non-compliance is widespread, systemic policy or process issues exist.

If the above analysis is inconclusive: Review AWS Config conformance packs for comprehensive compliance coverage. Check if custom Config rules have logic errors. Verify Security Hub integrations are receiving data. Consider AWS Audit Manager for more detailed compliance tracking.
