# Terraform Provider Authentication Failure

## Meaning

`terraform init`, `plan` or `apply` fails with errors such as "No valid credential sources found", "AccessDenied", "invalid_grant", "could not find default credentials", "AuthorizationFailed" or "401/403" from a provider or backend. Terraform is running as an identity that is missing, expired, pointed at the wrong account/project/subscription, or lacks permission. Common causes: expired SSO or OIDC token in CI, wrong profile or environment variables, assumed-role session expiry, stale cached credentials, a rotated service-account key, or a role trust-policy change.

## Impact

All plans and applies using that provider fail, blocking infrastructure changes and CI pipelines. The bigger risk is running with the wrong credentials: an apply could succeed against an unintended account or project, so identity must be confirmed before any retry.

## Playbook

### For AI Agents (NLP)

1. Capture the exact error text, the provider involved (aws, google, azurerm, kubernetes, ...) and whether it happened during `init` (backend/registry), `plan` (read) or `apply` (write).
2. Identify which credential source Terraform is using: provider block settings, environment variables, shared config profile, instance/pod role, or CI OIDC.
3. Verify the identity that source resolves to (account/project/subscription and principal) and compare it with the intended target for `<environment>`.
4. Check whether credentials are expired or revoked (session token expiry, rotated key, disabled service account).
5. Check whether the principal has the permissions the failing call needs, and whether a role trust policy or condition changed recently.
6. Re-run with debug logging for a single plan to see which call is denied, without printing secrets into shared logs.
7. Fix the credential source (refresh, re-assume role, correct profile), then re-run the plan and confirm it targets the intended account before any apply.

### For DevOps/SREs (CLI)

1. Show which providers and versions the configuration needs:
   ```bash
   terraform providers
   ```

2. Verify the identity Terraform will use (run the one for your cloud, with the same profile/environment as Terraform):
   ```bash
   aws sts get-caller-identity --profile <profile> --region <region>
   gcloud auth list --configuration=<configuration>
   az account show
   ```

3. Check which credential-related environment variables are set (names only, never values):
   ```bash
   env | grep -E '^(AWS_|GOOGLE_|ARM_|TF_VAR_.*(token|key|secret))' | cut -d= -f1 | sort
   ```

4. Capture a debug trace for one failing plan (review before sharing; it may contain request details):
   ```bash
   TF_LOG=debug terraform plan -input=false 2> terraform-debug.log
   grep -i -E "denied|unauthorized|forbidden|expired|invalid_grant|credential" terraform-debug.log | head -20
   ```

5. If the backend is failing, test access to it directly (S3 example):
   ```bash
   aws s3api head-bucket --bucket <state-bucket> --profile <profile> --region <region>
   ```

6. Refresh or re-assume credentials per your setup (for example `aws sso login --profile <profile>`), then re-run:
   ```bash
   terraform plan -input=false
   ```

## Diagnosis

1. If the identity check fails or shows an expired-token error, the credentials expired: refresh SSO/OIDC/session credentials and re-run.
2. If the identity succeeds but shows a different account, project or subscription than intended, stop: the wrong profile or environment is active, so fix it before any apply.
3. If the identity is correct but a specific call returns AccessDenied/403, the principal lacks that permission or a policy condition blocks it: compare the denied action in the debug log with the role's policies and any recent trust-policy or IAM changes.
4. If the failure is only in CI and works locally, the CI OIDC trust condition (branch, repo, environment) or secret injection likely changed.
5. If only `terraform init` fails with registry or checksum errors rather than credential errors, it is a network, proxy or lock-file problem, not authentication.
6. If errors started right after a key or service-account rotation, update the stored secret in the CI system and remove stale cached credentials.

Inline references:
- [Debugging Terraform](https://developer.hashicorp.com/terraform/internals/debugging)
- [AWS provider authentication](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication-and-configuration)
