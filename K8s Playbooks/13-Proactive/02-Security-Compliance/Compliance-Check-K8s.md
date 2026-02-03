# Compliance Check

## Meaning

Compliance check indicates that Kubernetes resources or configurations violate compliance requirements, security standards, or regulatory policies (triggering alerts like ComplianceViolation or SecurityComplianceFailed) because security audit findings indicate compliance failures, compliance checks fail, security standards are violated, regulatory requirements are not met, or compliance status indicates policy violations. Compliance check results show violations, security audit findings indicate non-compliance, compliance checks show failures, and compliance status indicates policy violations. This affects the security layer and compliance posture, typically caused by misconfigured security settings, non-compliant resource configurations, compliance policy violations, or compliance monitoring failures; if compliance affects container workloads, container security configurations may violate policies and applications may experience compliance risks.

## Impact

ComplianceViolation alerts fire; SecurityComplianceFailed alerts fire; compliance requirements are violated; security standards are not met; regulatory requirements are not satisfied; compliance posture is degraded. Compliance check results show violations; if compliance affects container workloads, container security configurations may violate policies, pod security contexts may be non-compliant, and container applications may experience compliance risks; applications may experience compliance violations or regulatory non-compliance.

## Playbook

1. Retrieve pods in namespace <namespace> with YAML output to identify pods and their security context settings for compliance review.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent security policy violations or compliance issues.

3. Describe pod <pod-name> in namespace <namespace> to inspect security context configurations and identify non-compliant settings.

4. List pod security policies and network policies in namespace <namespace> to review configured security policies.

5. Retrieve logs from security audit pods with label app=security-audit in namespace <namespace> and filter for compliance violation patterns.

6. Retrieve security compliance standards status including Pod Security Standards, CIS Kubernetes, or regulatory compliance status to identify standard-specific violations.

7. Retrieve security audit finding details for compliance violations and inspect violation descriptions, affected resources, and remediation recommendations, checking violation severity.

8. List roles and rolebindings in namespace <namespace> and verify compliance with RBAC security best practices and least privilege principles.

## Diagnosis

1. Review the pod security contexts from Steps 1 and 3. If pods are running as root, with privileged containers, or without security contexts, these are common compliance violations. Identify and remediate the most severe violations first.

2. Analyze the security policy configurations from Step 4. If pod security policies or network policies are missing or misconfigured, then security enforcement is incomplete.

3. If Step 5 security audit logs show violation patterns, identify whether violations are concentrated in specific namespaces or distributed. Concentrated violations suggest localized misconfiguration; distributed violations suggest policy template issues.

4. Review the compliance standards status from Step 6. If specific standards (Pod Security Standards, CIS Kubernetes) show violations, prioritize remediation based on standard criticality and audit requirements.

5. If Step 8 RBAC analysis shows violations of least privilege principles, then access control compliance needs attention alongside workload compliance.

If analysis is inconclusive: Examine events from Step 2 for security policy violations. Review the violation severity from Step 7 to prioritize remediation. Determine whether violations are increasing (suggesting compliance posture degradation) or stable (suggesting known accepted risks that need documentation).
