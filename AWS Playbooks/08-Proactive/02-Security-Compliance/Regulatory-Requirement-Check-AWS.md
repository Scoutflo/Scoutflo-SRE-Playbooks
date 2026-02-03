# Regulatory Requirement Check

## Meaning

Regulatory requirement check indicates that regulatory compliance cannot be verified or regulatory requirement violations are detected (triggering alarms like RegulatoryComplianceViolation or RegulatoryRequirementCheckFailed) because regulatory compliance checks fail, regulatory requirement violations are detected, regulatory compliance monitoring indicates problems, regulatory compliance configuration is missing, or regulatory requirement verification tools fail. Regulatory requirement checks show failures, regulatory requirement violations are detected, regulatory compliance monitoring indicates problems, and regulatory requirement check fails. This affects the compliance layer and regulatory adherence, typically caused by regulatory compliance configuration failures, regulatory requirement verification tool failures, regulatory violation detection issues, or regulatory compliance monitoring gaps; if regulatory requirements affect container workloads, container regulatory compliance may be violated and applications may experience regulatory risks.

## Impact

RegulatoryComplianceViolation alarms fire; RegulatoryRequirementCheckFailed alarms fire; regulatory compliance cannot be verified; regulatory requirement violations are detected; regulatory adherence may be compromised; regulatory risks may exist. Regulatory requirement checks show failures; if regulatory requirements affect container workloads, container regulatory compliance may be violated, pod regulatory adherence may be at risk, and container applications may experience regulatory risks; applications may experience regulatory compliance violations or regulatory non-compliance.

## Playbook

1. Retrieve Security Hub compliance standards status including GDPR, HIPAA, PCI-DSS, or SOC 2 compliance status to identify regulatory requirement violations.
2. List Config rules in region `<region>` and retrieve Config rule evaluation results to identify rules with compliance status 'NON_COMPLIANT' related to regulatory requirements.
3. Retrieve Security Hub findings in region `<region>` and filter for findings with compliance status 'FAILED' related to regulatory compliance violations.
4. Query CloudWatch Logs for log groups containing Config or Security Hub regulatory compliance events and filter for regulatory compliance violation patterns within the last 7 days.
5. Compare regulatory requirement check failure timestamps with resource configuration change timestamps within 24 hours and verify whether configuration changes introduce regulatory violations, using Config rule evaluation results as supporting evidence.
6. Retrieve Security Hub finding details for regulatory compliance violations and inspect violation descriptions, affected resources, and remediation recommendations, checking violation severity and regulatory impact.
7. List IAM policies in account `<account-id>` and verify compliance with regulatory requirements such as data access controls and encryption requirements, checking IAM regulatory compliance.
8. Compare regulatory compliance violation remediation timestamps with violation detection timestamps over the last 30 days and verify whether violations are remediated promptly, using Security Hub finding history as supporting evidence.

## Diagnosis

1. **Analyze regulatory standards status from Step 1**: If HIPAA shows violations, PHI protection controls need review. If PCI-DSS shows violations, cardholder data protection is at risk. If multiple standards fail on same control, that control is critical.

2. **Evaluate Security Hub findings from Step 3 and Step 6**: If CRITICAL findings exist, regulatory risk is high. If findings provide remediation steps, follow them precisely. If findings affect data handling, prioritize due to regulatory exposure.

3. **Review Config rule evaluations from Step 2**: If rules show increasing non-compliance, configuration drift is occurring. If specific resource types are non-compliant, focus remediation there. If rules are new, existing resources may need updates.

4. **Cross-reference with configuration changes from Step 5**: If regulatory violations correlate with recent changes, those changes introduced non-compliance. If no changes correlate, existing configurations were non-compliant.

5. **Assess remediation timeliness from Step 8**: If regulatory violations persist, audit risk increases. If violations are quickly remediated, compliance processes are effective. If remediation is slow, allocate more resources.

If the above analysis is inconclusive: Engage compliance team for regulatory interpretation. Use AWS Audit Manager for compliance evidence. Consider third-party compliance assessments. Implement compensating controls where direct compliance is difficult.
