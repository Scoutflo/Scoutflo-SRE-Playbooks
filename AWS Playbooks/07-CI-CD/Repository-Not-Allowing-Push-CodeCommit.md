# CodeCommit Repository Not Allowing Push

## Meaning

CodeCommit repository is not allowing push operations (triggering access denied errors or CodeCommitPushDenied alarms) because IAM permissions are insufficient, repository branch protection rules block pushes, repository access policy restricts operations, Git credentials are invalid, repository state prevents writes, or CodeCommit repository branch is locked. CodeCommit push operations fail, code changes cannot be committed, and repository access is denied. This affects the source control and CI/CD layer and blocks code updates, typically caused by permission issues, branch protection problems, or credential failures; if using CodeCommit with pull request workflows, branch protection may differ and applications may experience push failures.

## Impact

CodeCommit push operations fail; code changes cannot be committed; repository access is denied; Git push errors occur; source control operations are blocked; repository write permissions are insufficient; development workflows are interrupted; code updates cannot be pushed. CodeCommitPushDenied alarms may fire; if using CodeCommit with pull request workflows, branch protection may differ; applications may experience errors or performance degradation due to blocked code updates; development workflows may be completely blocked.

## Playbook

1. Verify CodeCommit repository `<repository-name>` exists and AWS service health for CodeCommit in region `<region>` is normal.
2. Retrieve the CodeCommit Repository `<repository-name>` in region `<region>` and inspect its repository access policy, branch protection rules, and repository state, verifying repository state.
3. Retrieve the IAM user `<user-name>` or IAM role `<role-name>` attempting to push and inspect its policy permissions for CodeCommit repository operations, verifying IAM permissions.
4. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CodeCommit API call failures or access denied events related to repository `<repository-name>`, including access denied details.
5. Retrieve CloudWatch metrics for CodeCommit Repository `<repository-name>` including RepositoryTriggersFailed over the last 24 hours to identify access-related error patterns, analyzing error metrics.
6. List CodeCommit repository branches for repository `<repository-name>` and check branch protection rules and push permission settings, verifying branch protection configuration.
7. Retrieve the CodeCommit Repository `<repository-name>` Git credential configuration and verify Git credentials are valid, checking if credential expiration affects access.
8. Query CloudWatch Logs for log groups containing CloudTrail events and filter for CodeCommit repository access policy or branch protection modification events related to repository `<repository-name>` within the last 24 hours, checking for configuration changes.
9. Retrieve CloudWatch metrics for CodeCommit including API call errors and verify CodeCommit service health, checking if service issues affect push operations.

## Diagnosis

1. Analyze CloudWatch Logs containing CloudTrail events (from Playbook step 4) to identify specific push failure error messages. If errors indicate "AccessDenied" or "GitPush failed", proceed immediately to IAM permission verification. If errors indicate "Branch is locked" or "Protected branch", branch protection rules are blocking the push.

2. For access-denied errors, verify IAM permissions (from Playbook step 3) for the user or role attempting to push. The IAM entity must have codecommit:GitPush permission for the repository. If permissions were recently modified, that change is likely the cause.

3. Review branch protection rules (from Playbook step 6) to verify if the target branch has protection rules that block direct pushes. If branch protection requires pull requests or restricts push access to specific users, direct pushes will be denied.

4. Verify repository access policy (from Playbook step 2) to ensure the repository policy does not restrict push operations. If repository-level policies deny push access to certain IAM entities, pushes will fail.

5. Check Git credential configuration (from Playbook step 7) to verify credentials are valid and not expired. If using HTTPS Git credentials, tokens may have expiration dates. If using SSH keys, verify the key is properly configured in IAM.

6. Correlate CloudTrail events (from Playbook step 8) with push failure timestamps within 5 minutes to identify any IAM policy, branch protection, or repository access policy modifications. If permission changes coincide with when pushes started failing, those changes are the likely cause.

7. Compare push failure patterns across different branches within 1 hour. If failures are branch-specific, the issue is likely branch protection rules on that branch. If failures affect all branches in the repository, the issue is IAM permissions or repository-wide access policies.

8. Review CloudWatch metrics for CodeCommit (from Playbook steps 5 and 9) to verify if there are broader service issues affecting the repository. If metrics show elevated error rates, there may be CodeCommit service issues.

9. Analyze push failure frequency over the last 24 hours. If failures are constant, the issue is likely permissions or branch protection. If failures are intermittent, credentials or service availability may be the cause.

If no correlation is found within the specified time windows: extend timeframes to 7 days, review alternative evidence sources including Git credential expiration and repository trigger configuration, check for gradual issues like IAM permission drift or branch protection rule updates, verify external dependencies like Git credential service availability or repository service health, examine historical patterns of push failures, check for CodeCommit repository branch lock status, verify CodeCommit Git credential service token expiration. Push failures may result from Git credential expiration, repository trigger failures, CodeCommit service issues, CodeCommit repository branch lock status, or CodeCommit Git credential service token expiration rather than immediate repository configuration changes.
