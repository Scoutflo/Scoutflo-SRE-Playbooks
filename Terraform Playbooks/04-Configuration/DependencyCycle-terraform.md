# Terraform Dependency Cycle

## Meaning

`terraform validate`, `plan` or `apply` fails with "Error: Cycle: <resource>, <resource>...". Two or more resources, modules or outputs reference each other directly or indirectly, so Terraform cannot build an acyclic dependency graph and cannot decide an order. Typical causes: security groups that reference each other inline, IAM role/policy or KMS key/policy documents referencing the resource they protect, `depends_on` combined with a reference in the opposite direction, module outputs fed back into the module's own inputs, or a provider configured from a resource it also manages.

## Impact

No plan or apply is possible for the configuration, so all changes to that stack are blocked, including emergency fixes. The error appears at plan time, so no infrastructure is changed by it.

## Playbook

### For AI Agents (NLP)

1. Capture the full Cycle error from `terraform validate` in `<terraform-dir>` and record every resource or module address listed.
2. Open the configuration for each listed address and map which attribute of one references which attribute of the other (including `depends_on`, module inputs/outputs and provider blocks).
3. Generate the dependency graph with cycles highlighted, if more context is needed.
4. Identify the reference that is not truly required for ordering (for example a rule inline in two security groups, or a policy that only needs a name/ARN string known up front).
5. Propose a break: split inline rules into separate rule resources, build the ARN from known values instead of the resource attribute, move one side into its own resource, or remove an unnecessary `depends_on`.
6. Apply the code change on a branch, run `terraform validate` and `terraform plan`, and confirm the plan has no unintended destroy or replace before any apply.

### For DevOps/SREs (CLI)

1. Reproduce and read the cycle (this is read-only):
   ```bash
   terraform validate
   ```

2. Draw the graph with cycles highlighted (render with Graphviz if installed):
   ```bash
   terraform graph -draw-cycles > graph.dot
   dot -Tsvg graph.dot -o graph.svg
   ```

3. Find the references between the listed resources:
   ```bash
   grep -rn -E "<resource-type>\.<name-a>|<resource-type>\.<name-b>" --include='*.tf' .
   ```

4. After editing the code, confirm the cycle is gone and review the plan:
   ```bash
   terraform validate
   terraform plan -out=fix.tfplan -input=false
   terraform show -json fix.tfplan | jq '[.resource_changes[] | select(.change.actions != ["no-op"]) | {address, actions: .change.actions}]'
   ```

## Diagnosis

1. If the cycle lists two `aws_security_group` resources, each with inline `ingress`/`egress` rules referencing the other, move the rules into separate `aws_security_group_rule` or `aws_vpc_security_group_ingress_rule` resources.
2. If the cycle includes an IAM policy or KMS key policy and the resource it protects, build the ARN from known inputs (name, account ID, region) or use a separate policy attachment resource instead of referencing the resource's own attribute.
3. If `depends_on` appears in the cycle, remove it or the opposite reference: a resource cannot depend on something that already depends on it.
4. If a module is in the cycle, check that its outputs are not fed back into its own inputs, and split the module if two parts need each other.
5. If a provider block references a resource that the same configuration creates, move that resource to a separate root module or stack and read it back through data sources or remote state.
6. If the plan after the fix shows `-/+` replace on stateful resources, stop and review before applying: changing how a reference is built can force replacement.

Inline references:
- [terraform graph](https://developer.hashicorp.com/terraform/cli/commands/graph)
- [Resource dependencies](https://developer.hashicorp.com/terraform/language/resources/behavior#resource-dependencies)
