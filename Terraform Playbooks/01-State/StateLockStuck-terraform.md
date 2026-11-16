# Terraform State Lock Stuck

## Meaning

`terraform plan` or `apply` fails with "Error acquiring the state lock" and the output shows Lock Info (ID, Operation, Who, Created). Another run holds the lock, or a previous run crashed, was cancelled, or lost network access before releasing it. Common causes: a CI job still running or killed mid-apply, an engineer's laptop session interrupted, an expired backend lease (S3 + DynamoDB item, GCS lock object, Azure blob lease, Terraform Cloud run), or two pipelines targeting the same state.

## Impact

Nobody can plan or apply against that state, so infrastructure changes and rollbacks are blocked. During an incident this delays remediation that depends on Terraform. Forcing the unlock while a real apply is still running can corrupt state or cause concurrent changes, so the lock must be verified before it is removed.

## Playbook

### For AI Agents (NLP)

1. Capture the full lock error and record the Lock Info fields: lock `ID`, `Operation`, `Who`, `Created`, and `Path` for workspace `<workspace>` in directory `<terraform-dir>`.
2. Determine whether the lock holder is still active: check running CI/CD jobs and pipelines for `<terraform-dir>`, and ask the person in `Who` whether a run is in progress.
3. Compare `Created` with the current time. A lock older than the longest expected apply duration with no active job is likely stale.
4. Identify the backend type (S3, GCS, azurerm, Terraform Cloud, local) from the backend configuration and inspect the lock record in that backend.
5. Check backend health and permissions: confirm the identity running Terraform can read and write the lock table, object or lease.
6. Only after confirming no apply is running, release the lock using the lock `ID` from step 1. This is a state-changing action and needs approval.
7. Re-run `terraform plan` to confirm the lock is released and the state is readable, and compare the plan with what the interrupted run intended.

### For DevOps/SREs (CLI)

1. Reproduce with a short wait so you get the Lock Info without hanging:
   ```bash
   terraform plan -input=false -lock-timeout=5s
   ```

2. Check for running pipelines or Terraform processes:
   ```bash
   ps aux | grep -i "[t]erraform"
   gh run list --status in_progress --limit 10    # GitHub Actions example
   ```

3. Inspect the lock record (pick your backend):
   ```bash
   # S3 backend with DynamoDB locking
   aws dynamodb get-item --table-name <lock-table> --region <region> \
     --key '{"LockID":{"S":"<bucket>/<key-path>"}}'
   # S3 backend with native locking (use_lockfile = true)
   aws s3api head-object --bucket <bucket> --key <key-path>.tflock --region <region>
   # GCS backend
   gcloud storage ls gs://<bucket>/<prefix>/*.tflock
   # Local backend
   cat <terraform-dir>/.terraform.tfstate.lock.info
   ```

4. Confirm the state is readable and not corrupted:
   ```bash
   terraform state list
   ```

5. Release the stale lock (state-changing, needs approval; only if no apply is running):
   ```bash
   terraform force-unlock <LOCK-ID>
   ```

6. Verify:
   ```bash
   terraform plan -input=false -lock-timeout=30s
   ```

## Diagnosis

1. If `Created` is recent and a CI job or engineer's session for `<terraform-dir>` is still running, the lock is legitimate: wait for it to finish or cancel that job cleanly, and do not force-unlock.
2. If `Created` is older than the longest normal apply and no process or pipeline is running, the lock is stale from a crashed or cancelled run; plan a force-unlock with the exact lock ID after the state is confirmed readable.
3. If `terraform force-unlock` reports "not locked", the lock was already released and the earlier failure was a race or a different workspace; re-run the plan.
4. If the error is a permissions or network error rather than Lock Info (for example AccessDenied on the lock table or bucket), fix the identity or connectivity first; the lock itself is not the problem.
5. If the same lock reappears right after unlocking, two pipelines are targeting the same state; serialise them or give them separate states or workspaces.
6. If `terraform state list` fails or returns an unexpectedly small state after an interrupted apply, restore the state from the backend's version history before applying anything.

Inline references:
- [Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking)
- [terraform force-unlock](https://developer.hashicorp.com/terraform/cli/commands/force-unlock)
