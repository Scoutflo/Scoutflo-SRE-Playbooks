# Terraform Remote State Access Denied

## Meaning

`terraform init`, `plan` or `apply` fails while reading or writing the remote backend with errors such as "AccessDenied", "403", "NoSuchBucket", "Error loading state", "failed to retrieve state" or "Error refreshing state: ... terraform_remote_state". The identity Terraform runs as cannot read or write the state object or lock table, the backend configuration points to the wrong bucket/key/region/account, a bucket policy or KMS key policy changed, or a `terraform_remote_state` data source references a state this identity may not read.

## Impact

No plan or apply can run for the stack, and stacks that read its outputs through `terraform_remote_state` fail too. Retrying with other credentials risks writing state into the wrong account or workspace.

## Playbook

### For AI Agents (NLP)

1. Capture the exact error text and whether it occurred in the main `backend` block or in a `terraform_remote_state` data source, and record the backend type, bucket/container, key/prefix, region and workspace.
2. Verify which identity Terraform is using (account/project/subscription and principal) and that it matches the intended environment for `<environment>`.
3. Check that the backend target exists and is in the expected account and region; a typo or a wrong profile usually shows as NoSuchBucket or a region redirect.
4. Check whether the identity can list and read the state object and, for locking, read and write the lock table or lockfile.
5. If the bucket or state is encrypted with KMS, check the identity is allowed to use the key.
6. Check recent changes to bucket policy, IAM policies, role trust policies, SSO assignments or key policies around the time errors began.
7. Fix the access path with approval (correct profile/role, add the narrowly scoped permission), then re-run `terraform init` and `plan` and confirm it reads the expected state.

### For DevOps/SREs (CLI)

1. Show the backend configuration Terraform is using:
   ```bash
   cat .terraform/terraform.tfstate | jq '.backend'
   grep -n -A8 'backend "' *.tf
   ```

2. Verify the active identity (S3 example; use the equivalent for GCS/Azure):
   ```bash
   aws sts get-caller-identity --profile <profile> --region <region>
   ```

3. Check the state bucket exists, region and access:
   ```bash
   aws s3api head-bucket --bucket <state-bucket> --profile <profile> --region <region>
   aws s3api head-object --bucket <state-bucket> --key <state-key> --profile <profile> --region <region>
   ```

4. Check the lock table (DynamoDB locking) is readable:
   ```bash
   aws dynamodb describe-table --table-name <lock-table> --profile <profile> --region <region> --query 'Table.TableStatus'
   ```

5. Check the bucket policy and the KMS key policy:
   ```bash
   aws s3api get-bucket-policy --bucket <state-bucket> --profile <profile> --region <region> --query Policy --output text | jq .
   aws kms describe-key --key-id <key-id-or-alias> --profile <profile> --region <region>
   ```

6. Re-initialise against the correct backend once access is fixed (state-changing for local setup only, no remote writes):
   ```bash
   terraform init -reconfigure -input=false
   terraform state list | head
   ```

## Diagnosis

1. If `get-caller-identity` shows a different account or role than intended, fix the profile or role first; this is the most common cause and must be corrected before any apply.
2. If `head-bucket` returns 404 or a redirect, the bucket name or region in the backend block is wrong, or it lives in another account.
3. If `head-bucket` succeeds but `head-object` returns 403, the identity lacks `s3:GetObject`/`s3:ListBucket` on the key prefix: add the specific permission or fix the bucket policy.
4. If reads succeed but locking fails with AccessDenied on DynamoDB, the identity lacks the lock table permissions (`GetItem`, `PutItem`, `DeleteItem`).
5. If errors mention KMS `AccessDeniedException`, add the identity to the key policy (or key grants) for `Decrypt`, `GenerateDataKey`.
6. If only a `terraform_remote_state` data source fails, grant read access to that other state or replace it with a narrower data source or published outputs.
7. If errors began right after a role, SSO or policy change, review the change history and restore the permission rather than switching to broader credentials.

Inline references:
- [S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)
- [terraform_remote_state](https://developer.hashicorp.com/terraform/language/state/remote-state-data)
