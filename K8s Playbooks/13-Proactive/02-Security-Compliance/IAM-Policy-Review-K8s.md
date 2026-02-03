# RBAC Policy Review

## Meaning

RBAC policy review indicates that RBAC policies may be overly permissive, misconfigured, or violate least privilege principles (triggering alerts like OverlyPermissiveRBACPolicy or RBACPolicyAuditFailed) because RBAC policies grant excessive permissions, unused RBAC roles exist, RBAC policies violate least privilege principles, RBAC role bindings allow wildcard resources, or RBAC policy conditions are missing or misconfigured. RBAC policies show overly permissive statements, RBAC policy audit findings indicate violations, unused RBAC roles are detected, and RBAC policy configurations violate security policies. This affects the security layer and access control, typically caused by misconfigured RBAC policies, lack of RBAC role lifecycle management, or security policy violations; if RBAC policies protect container workloads, container service account permissions may be overly permissive and applications may experience security risks.

## Impact

RBACPolicyAuditFailed alerts fire; OverlyPermissiveRBACPolicy alerts fire; access permissions are overly permissive; security policies are violated; unused RBAC roles consume resources; RBAC policies violate least privilege principles. RBAC policy configurations show overly permissive statements; if RBAC policies protect container workloads, container service account permissions may be overly permissive, pod RBAC role permissions may be misconfigured, and container applications may experience security risks; applications may experience security vulnerabilities or unauthorized access risks.

## Playbook

1. List roles and rolebindings in namespace <namespace> with wide output and list clusterroles and clusterrolebindings with wide output to identify all roles and their bindings in the environment.

2. List recent events across all namespaces sorted by timestamp and filtered by involved object kind Role and ClusterRole to identify recent RBAC modifications.

3. Retrieve roles in namespace <namespace> with YAML output and analyse for wildcard permissions on resources or verbs that indicate overly permissive configurations.

4. Describe role <role-name> in namespace <namespace> to see its full rule set and check for overly broad permissions on resources or verbs.

5. Check permissions for service account <sa-name> in namespace <namespace> by listing all allowed actions to verify what the role permits.

6. Retrieve clusterroles with YAML output and analyse for dangerous permissions including access to secrets, pods/exec, or wildcard resources.

7. List rolebindings in namespace <namespace> with wide output and list clusterrolebindings with wide output to see which identities have which roles.

8. Verify permissions against least-privilege requirements by checking if service account <sa-name> in namespace <namespace> can perform sensitive actions including creating secrets, configmaps, pods/exec, and accessing nodes.

## Diagnosis

1. Review the role and clusterrole configurations from Steps 3 and 6. If wildcard permissions on resources or verbs are present, these represent the highest-priority security concerns requiring immediate remediation.

2. Analyze the permission checks from Step 8. If service accounts can perform sensitive actions (create secrets, pods/exec, access nodes) beyond their operational requirements, then least privilege principles are being violated.

3. If Step 4 role rules show overly broad permissions, identify whether these were intentionally configured or result from template/default configurations. If permissions exceed documented requirements, then role right-sizing is needed.

4. Compare rolebindings from Step 7 with active pod usage. If identities are bound to roles but not actively using those permissions, then unused role bindings exist that should be reviewed for removal.

5. If cluster-admin or admin bindings are identified in Step 7, verify each subject has a documented business justification. If justification is missing, then privilege escalation risks exist.

If analysis is inconclusive: Review the RBAC events from Step 2 to identify recent modifications that may have introduced permission creep. Examine whether overly permissive policies are concentrated in specific namespaces (suggesting localized misconfiguration) or widespread (suggesting systemic policy issues). Check for RBAC role lifecycle management processes and verify that periodic access reviews are being conducted.
