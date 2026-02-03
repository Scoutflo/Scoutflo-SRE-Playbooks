# Compliance Status Check

## Meaning

Compliance status check indicates that compliance status cannot be verified or compliance violations are detected (triggering alerts like ComplianceViolation or ComplianceStatusCheckFailed) because compliance status checks fail, compliance violations are detected, compliance monitoring indicates problems, compliance configuration is missing, or compliance status data is unavailable. Compliance status checks show failures, compliance violations are detected, compliance monitoring indicates problems, and compliance status check fails. This affects the compliance layer and regulatory adherence, typically caused by compliance configuration failures, compliance monitoring tool failures, compliance violation detection issues, or compliance status check monitoring gaps; if compliance status affects container workloads, container compliance may be violated and applications may experience regulatory risks.

## Impact

ComplianceViolation alerts fire; ComplianceStatusCheckFailed alerts fire; compliance status cannot be verified; compliance violations are detected; regulatory adherence may be compromised; compliance risks may exist. Compliance status checks show failures; if compliance status affects container workloads, container compliance may be violated, pod compliance may be at risk, and container applications may experience regulatory risks; applications may experience compliance violations or regulatory non-compliance.

## Playbook

1. List all resources in namespace <namespace> to identify all resources requiring compliance verification.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent compliance violations or policy issues.

3. Describe pods in namespace <namespace> to inspect security contexts and compliance-relevant settings.

4. List network policies and pod security policies in namespace <namespace> to review policy evaluation status.

5. Retrieve logs from compliance monitoring pods with label app=compliance-monitor in namespace <namespace> and filter for compliance violation patterns.

6. Retrieve compliance standards status including Pod Security Standards, CIS Kubernetes, or regulatory compliance status to identify standard-specific violations.

7. Retrieve security audit finding details for compliance violations and inspect violation descriptions, affected resources, and remediation recommendations, checking violation severity.

8. List roles, rolebindings, clusterroles, and clusterrolebindings in namespace <namespace> and verify compliance with RBAC security best practices.

## Diagnosis

1. Review the resource inventory from Step 1 and pod configurations from Step 3. If pods have security context issues or run with elevated privileges, these are common compliance violations requiring remediation.

2. Analyze the policy configurations from Step 4. If network policies or pod security policies show gaps, then security enforcement is incomplete and compliance status will reflect violations.

3. If Step 5 compliance monitoring logs show violation patterns, identify the specific compliance controls failing and the resources causing violations.

4. Review the compliance standards status from Step 6. If standards show FAILED status, prioritize remediation based on regulatory requirements and audit timelines.

5. If Step 4 remediation tracking shows violations not being addressed promptly, then compliance remediation processes need improvement. If remediations are occurring but new violations appear, then prevention measures are insufficient.

If analysis is inconclusive: Examine events from Step 2 for compliance-related issues. Review the violation severity from Step 7 to prioritize remediation. Verify that compliance monitoring tools are correctly configured and have visibility into all resources requiring compliance verification.
