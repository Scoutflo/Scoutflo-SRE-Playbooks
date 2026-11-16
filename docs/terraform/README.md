# Terraform Playbooks

> **3 playbooks** for Terraform and IaC incidents. New category, contributions welcome ([issue 13](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/issues/13)).

| Playbook | Description |
|----------|-------------|
| [StateLockStuck](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/Terraform%20Playbooks/01-State/StateLockStuck-terraform.md) | "Error acquiring the state lock": verify the holder, then safely force-unlock |
| [DriftDetected](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/Terraform%20Playbooks/02-Drift/DriftDetected-terraform.md) | Plan shows changes nobody wrote: find the cause, keep or revert |
| [ProviderAuthenticationFailure](https://github.com/Scoutflo/Scoutflo-SRE-Playbooks/blob/master/Terraform%20Playbooks/03-Providers/ProviderAuthenticationFailure-terraform.md) | AccessDenied / expired or wrong credentials during init, plan or apply |
