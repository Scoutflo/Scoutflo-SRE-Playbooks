# Secrets Rotation Status

## Meaning

Secrets rotation status indicates that secrets rotation has not occurred according to schedule or rotation operations fail (triggering alerts like SecretsRotationFailed or SecretsRotationOverdue) because secrets rotation schedules are not met, rotation operations fail, rotation status shows overdue, rotation automation does not trigger, or rotation completion cannot be verified. Secrets show rotation overdue status, rotation operations show failed status, rotation schedules are not met, and rotation automation triggers do not activate. This affects the security layer and secrets management, typically caused by rotation automation failures, rotation schedule misconfigurations, rotation service account permission issues, or rotation service unavailability; if secrets protect container workloads, container secret rotation may fail and applications may experience authentication failures.

## Impact

SecretsRotationFailed alerts fire; SecretsRotationOverdue alerts fire; secrets may become compromised; rotation schedules are not met; rotation automation fails; security policies are violated. Secrets rotation status shows overdue or failed; if secrets protect container workloads, container secret rotation may fail, pod secret updates may not occur, and container applications may experience authentication failures; applications may experience authentication failures or security risks from stale secrets.

## Playbook

1. List all secrets in namespace <namespace> with wide output to retrieve secret metadata including creation timestamps and types.
2. List recent events in namespace <namespace> sorted by timestamp to identify secret rotation failures, permission errors, or secret-related warnings.
3. Describe secret <secret-name> in namespace <namespace> to inspect the secret details including annotations for rotation configuration and last rotation timestamp.
4. List pods in namespace `<namespace>` with automatic secret rotation enabled and verify rotation status and last rotation timestamp.
5. Retrieve logs from secret rotation pods in namespace `<namespace>` and filter for rotation failure patterns or rotation overdue warnings within the last 7 days.
6. Retrieve Prometheus metrics for secret rotation service including rotation_success_rate and rotation_duration over the last 30 days to identify rotation failure patterns.
7. Verify secret rotation service account permissions by retrieving the service account `<service-account-name>` in namespace `<namespace>` attached to secret rotation and checking its role binding permissions, verifying rotation role access.
8. Compare secret rotation schedule timestamps with actual rotation completion timestamps and verify whether rotations occur according to schedule, using secret rotation data as supporting evidence.
9. Retrieve the Secret `<secret-name>` rotation job configuration and verify whether rotation automation is correctly configured, checking rotation job accessibility.

## Diagnosis

1. Review the secret metadata from Steps 1 and 3. If annotations show rotation timestamps significantly older than the rotation schedule requires, then rotations are overdue and immediate rotation is needed.

2. Analyze the rotation pod logs from Step 5. If logs show rotation failure patterns, identify whether failures are due to permissions, network issues, or destination unavailability. If logs show no rotation attempts, then scheduling is the issue.

3. If Step 6 rotation metrics show low success rates, then rotation infrastructure has systemic problems. If success rates are high but specific secrets are overdue, then those secrets may have configuration issues.

4. Review the service account permissions from Step 7. If the rotation service account lacks required permissions, then RBAC configuration needs updating. If permissions are correct, then operational issues are causing failures.

5. If Step 8 schedule comparison shows rotations not occurring at scheduled times, verify that rotation job configurations from Step 9 are correctly configured with appropriate triggers and schedules.

If analysis is inconclusive: Examine events from Step 2 for permission errors or secret-related warnings. Determine whether rotation failures affect all secrets (suggesting infrastructure issues) or specific secrets (suggesting secret-specific configuration problems). Verify that secret rotation automation has necessary network access to downstream systems that consume rotated secrets.
