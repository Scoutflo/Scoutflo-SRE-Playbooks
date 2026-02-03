# Access Review

## Meaning

Access review indicates that access permissions cannot be reviewed or excessive access permissions are detected (triggering alerts like ExcessiveAccessDetected or AccessReviewFailed) because access review tools fail, access permissions are not reviewed, excessive access permissions are detected, access review monitoring indicates problems, or access review configuration is missing. Access reviews show failures, access permissions are not reviewed, excessive access permissions are detected, and access review fails. This affects the compliance layer and access management, typically caused by access review configuration failures, access review tool failures, access permission analysis issues, or access review monitoring gaps; if access review affects container workloads, container access permissions may be excessive and applications may experience access management risks.

## Impact

ExcessiveAccessDetected alerts fire; AccessReviewFailed alerts fire; access permissions cannot be reviewed; excessive access permissions are detected; access management may be compromised; security risks may exist. Access reviews show failures; if access review affects container workloads, container access permissions may be excessive, pod access controls may be misconfigured, and container applications may experience access management risks; applications may experience access review gaps or security risks.

## Playbook

1. Describe rolebindings and clusterrolebindings in namespace <namespace> to understand current access bindings and their configurations.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent RBAC changes or access issues.

3. List all service accounts in namespace <namespace> to identify all identities that may have permissions.

4. For each service account, check permissions for service account <sa-name> in namespace <namespace> by listing all allowed actions to see what each account can do.

5. Describe role <role-name> in namespace <namespace> or describe clusterrole <role-name> to identify overly permissive rules including wildcards and broad verbs.

6. Verify if service account <sa-name> in namespace <namespace> can create pods and perform similar tests for sensitive resources including secrets, configmaps, and exec operations.

7. List clusterrolebindings and identify all subjects bound to cluster-admin or admin roles.

8. Compare service accounts in namespace <namespace> with pod service account references to identify unused service accounts.

## Diagnosis

1. Review the permission checks from Step 6. If service accounts can perform sensitive actions (create pods, access secrets, exec into containers) beyond documented requirements, these represent excessive access requiring remediation.

2. Analyze the role definitions from Step 5. If roles contain wildcards on resources or verbs, these are overly permissive and should be tightened to specific required permissions.

3. If Step 7 clusterrolebindings show identities bound to cluster-admin without documented justification, these are high-priority findings. Verify each admin binding has a legitimate business requirement.

4. Review the service account comparison from Step 8. If service accounts exist that are not referenced by any pods, they may be unused and candidates for removal. If used by pods, verify their permissions match pod requirements.

5. If Step 4 permission analysis shows service accounts can perform actions not required by their associated workloads, then right-sizing is needed.

If analysis is inconclusive: Examine events from Step 2 for recent RBAC changes that may have introduced permission creep. Review whether excessive access is concentrated in specific namespaces (suggesting localized configuration issues) or cluster-wide (suggesting policy gaps). Verify that periodic access review processes exist and are being followed.
