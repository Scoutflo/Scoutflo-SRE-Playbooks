# Terraform Drift Detected

## Meaning

`terraform plan` shows changes nobody wrote in code, or a scheduled drift check exits with code 2, because real infrastructure no longer matches the Terraform state or configuration. Typical causes: manual console or CLI edits during an incident, autoscaling or another controller changing managed attributes, a provider upgrade changing defaults, resources changed by another automation, or resources deleted outside Terraform.

## Impact

The next `terraform apply` can silently revert an emergency manual fix, recreate deleted resources, or replace resources (causing downtime). Drift also hides real configuration problems and makes plans noisy and hard to review.

## Playbook

### For AI Agents (NLP)

1. Run a refresh-only plan in `<terraform-dir>` to separate infrastructure drift from configuration changes, and record which resources and attributes differ.
2. For each drifted resource, identify who or what changed it by checking cloud audit logs (CloudTrail, GCP Audit Logs, Azure Activity Log) for the resource and the time window.
3. Classify each difference: intentional emergency change to keep, accidental change to revert, attribute managed by another controller (for example autoscaler-managed counts), or provider default change.
4. Check whether the plan would destroy or replace anything (`-/+` or `-`) and flag those resources as high risk.
5. Decide per resource: update the code to match reality, revert reality to match the code, add `ignore_changes` for externally managed attributes, or import an unmanaged resource.
6. Apply the decision with approval, then re-run the plan to confirm it reports no changes.

### For DevOps/SREs (CLI)

1. Detect drift without proposing config changes (exit code 0 = none, 2 = drift, 1 = error):
   ```bash
   terraform plan -refresh-only -detailed-exitcode -input=false
   ```

2. Save and inspect the full plan as JSON to list exactly what changed:
   ```bash
   terraform plan -out=drift.tfplan -input=false
   terraform show -json drift.tfplan | jq '.resource_changes[] | select(.change.actions != ["no-op"]) | {address, actions: .change.actions}'
   ```

3. Find who changed the resource (AWS example; use the equivalent audit log for GCP/Azure):
   ```bash
   aws cloudtrail lookup-events --region <region> \
     --lookup-attributes AttributeKey=ResourceName,AttributeValue=<resource-id> \
     --max-results 20 \
     --query 'Events[].{time:EventTime,user:Username,event:EventName}'
   ```

4. Look at the recorded state of one resource and compare:
   ```bash
   terraform state show <resource-address>
   ```

5. Accept real-world changes into state without changing infrastructure (state-changing, needs approval):
   ```bash
   terraform apply -refresh-only
   ```

6. Or revert infrastructure to match code after reviewing the plan (state-changing, needs approval):
   ```bash
   terraform apply drift.tfplan
   ```

7. Verify no drift remains:
   ```bash
   terraform plan -detailed-exitcode -input=false; echo "exit=$?"
   ```

## Diagnosis

1. If the refresh-only plan reports changes but the normal plan shows the same changes as a revert, the drift is infrastructure-side: decide whether to keep the manual change (update code) or revert it.
2. If audit logs show a human or console change during a recent incident window, treat it as an intentional emergency change: update the code to match before anyone applies, or the fix will be reverted.
3. If the differing attribute is one an autoscaler or controller updates (desired counts, tags added by another tool), add `lifecycle { ignore_changes = [...] }` for that attribute rather than fighting it.
4. If many resources drift right after a provider version change and audit logs show no changes, a provider default changed: pin the provider version, read its upgrade notes, and set the attribute explicitly.
5. If the plan shows `-/+` replace for a stateful resource (database, volume, load balancer), stop and review the cause (usually an immutable attribute changed) before any apply.
6. If a resource exists in the cloud but not in state, import it rather than letting Terraform try to create a duplicate.

Inline references:
- [Terraform refresh-only mode](https://developer.hashicorp.com/terraform/cli/commands/plan#planning-modes)
- [lifecycle ignore_changes](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#ignore_changes)
