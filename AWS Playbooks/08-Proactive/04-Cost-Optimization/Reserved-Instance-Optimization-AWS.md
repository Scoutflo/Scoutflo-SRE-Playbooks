# Reserved Instance Optimization

## Meaning

Reserved Instance optimization indicates that Reserved Instance coverage is insufficient, Reserved Instances are underutilized, or Reserved Instance purchase opportunities are missed (triggering alarms like ReservedInstanceUnderutilized or ReservedInstanceCoverageLow) because Reserved Instance utilization is below thresholds, Reserved Instance coverage does not match on-demand usage, Reserved Instance purchase recommendations are not implemented, Reserved Instance expiration is approaching, or Reserved Instance exchange opportunities are missed. Reserved Instance utilization metrics show low usage, Reserved Instance coverage metrics indicate gaps, Reserved Instance purchase recommendations are available, and Reserved Instance expiration warnings are present. This affects the cost management layer and Reserved Instance lifecycle management, typically caused by Reserved Instance purchase misalignment, Reserved Instance utilization tracking failures, or Reserved Instance lifecycle management issues; if Reserved Instances protect container workloads, container compute costs may not be optimized and applications may experience unnecessary cost overhead.

## Impact

ReservedInstanceUnderutilized alarms fire; ReservedInstanceCoverageLow alarms fire; cost optimization opportunities are missed; Reserved Instance utilization is inefficient; Reserved Instance coverage gaps exist; Reserved Instance purchase recommendations are not implemented. Reserved Instance utilization metrics show low usage; if Reserved Instances protect container workloads, container compute costs may not be optimized, node reservation benefits may be missed, and container applications may experience unnecessary cost overhead; applications may experience cost inefficiencies or missed savings opportunities.

## Playbook

1. Retrieve Cost Explorer Reserved Instance utilization data for region `<region>` over the last 30 days and compare Reserved Instance utilization with on-demand instance usage to identify utilization gaps.
2. List Reserved Instances in region `<region>` and retrieve Reserved Instance utilization metrics including utilization percentage and expiration dates to identify underutilized or expiring Reserved Instances.
3. Retrieve Cost Explorer Reserved Instance coverage data for region `<region>` over the last 30 days and compare Reserved Instance coverage with on-demand instance usage to identify coverage gaps.
4. Retrieve Cost Explorer Reserved Instance purchase recommendations for region `<region>` and verify recommendation details including instance type, term, and payment option recommendations.
5. Query CloudWatch Logs for log groups containing Cost Explorer or billing events and filter for Reserved Instance utilization warnings or expiration alerts within the last 7 days.
6. Retrieve CloudWatch metrics for EC2 Reserved Instance utilization including UtilizationPercentage and CoveragePercentage over the last 30 days to identify utilization trends.
7. Compare Reserved Instance expiration dates with current date and verify whether Reserved Instances are approaching expiration, using Reserved Instance data as supporting evidence.
8. Retrieve Cost Explorer Reserved Instance exchange opportunities and verify whether exchanges can improve utilization or coverage, checking exchange eligibility.

## Diagnosis

1. **Analyze utilization data from Step 1 and Step 2**: If utilization is below 80%, Reserved Instances are underutilized. If specific instance types show low utilization, workloads have shifted away from those types. If utilization dropped recently, investigate what changed.

2. **Evaluate coverage gaps from Step 3**: If on-demand usage exists for instance types with no Reserved Instance coverage, purchase recommendations from Step 4 are valid. If coverage is high but costs are high, Reserved Instance pricing may not provide savings for that usage pattern.

3. **Review purchase recommendations from Step 4**: If recommendations suggest different instance types than currently reserved, workload patterns have changed. If recommendations suggest larger quantities, demand has increased. If recommendations suggest term changes, evaluate commitment vs. flexibility trade-offs.

4. **Cross-reference with expiration data from Step 7**: If Reserved Instances are expiring soon, decide whether to renew, convert to Savings Plans, or let expire. If expired RIs were well-utilized, renew or replace. If expired RIs were underutilized, reconsider the commitment.

5. **Assess exchange opportunities from Step 8**: If exchanges are available that improve utilization, execute them. If exchanges would align RIs with current workloads, evaluate the exchange value. If no beneficial exchanges exist, consider selling on Reserved Instance Marketplace.

If the above analysis is inconclusive: Compare Reserved Instance strategy with Savings Plans for flexibility. Analyze instance family usage patterns over time. Review Spot Instance usage that could replace on-demand coverage. Consider compute optimizer recommendations for instance type changes.
