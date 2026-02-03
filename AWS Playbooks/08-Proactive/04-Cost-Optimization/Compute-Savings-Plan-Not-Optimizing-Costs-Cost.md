# AWS Compute Savings Plan Not Optimizing Costs

## Meaning

AWS Compute Savings Plan is not optimizing costs (triggering cost optimization failures or ComputeSavingsPlanNotOptimizing alarms) because Savings Plan coverage is insufficient, Savings Plan commitment does not match usage, Savings Plan scope is incorrect, usage patterns changed, Savings Plan utilization is low, or Savings Plan term has expired. Compute Savings Plan benefits are not realized, expected cost savings are not achieved, and Savings Plan utilization is low. This affects the cost management and optimization layer and reduces cost savings, typically caused by Savings Plan coverage gaps, utilization issues, or usage pattern mismatches; if using Compute Savings Plan with different service combinations, optimization behavior may differ and applications may experience suboptimal cost savings.

## Impact

Compute Savings Plan benefits are not realized; expected cost savings are not achieved; Savings Plan utilization is low; cost optimization objectives are not met; Savings Plan coverage is insufficient; billing charges are higher than expected; cost management automation is ineffective. ComputeSavingsPlanNotOptimizing alarms may fire; if using Compute Savings Plan with different service combinations, optimization behavior may differ; applications may experience higher than expected costs; cost optimization benefits may not be realized.

## Playbook

1. Verify AWS Compute Savings Plan exists and AWS service health for Billing in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Compute Savings Plan purchase events, usage events, or billing-related API calls, checking for Savings Plan purchases.
3. Retrieve CloudWatch metrics for EC2, Lambda, and Fargate usage including usage patterns over the last 30 days to compare with Savings Plan coverage, analyzing usage patterns.
4. List AWS Compute Savings Plans and check Savings Plan status, commitment amount, coverage scope, and utilization rates, verifying Savings Plan configuration.
5. List EC2, Lambda, and Fargate usage for Savings Plan eligible services and check usage patterns against Savings Plan coverage, analyzing coverage gaps.
6. Query CloudWatch Logs for log groups containing billing events and filter for Savings Plan discount application patterns or utilization metrics, checking billing details.
7. Retrieve the Compute Savings Plan `<savings-plan-id>` term and expiration date and verify Savings Plan is active, checking if expiration affects optimization.
8. Retrieve CloudWatch metrics for EC2, Lambda, and Fargate service usage including service-specific utilization and verify utilization against Savings Plan coverage, checking if utilization is below commitment.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for service usage pattern changes or instance type modifications within the last 30 days, checking for usage changes.

## Diagnosis

1. **Analyze CloudWatch Usage Metrics from Step 3**: Review EC2, Lambda, and Fargate usage patterns against Savings Plan coverage. If CloudWatch metrics show usage in regions, instance families, or services not covered by the Savings Plan scope from Step 4, then coverage mismatch is the issue. If usage has shifted to different instance types since Savings Plan purchase, then usage pattern changes caused optimization gaps. If usage appears aligned with Savings Plan, continue to step 2.

2. **Check Savings Plan Status and Terms from Steps 4 and 7**: If Savings Plan from Step 4 shows status other than "Active", then the plan is not applying discounts. If the term and expiration from Step 7 show the Savings Plan has expired or is pending activation, then plan lifecycle is the issue. Verify the commitment amount matches current usage levels. If plan status is healthy, continue to step 3.

3. **Evaluate Utilization Rates from Steps 4 and 8**: If utilization rates from Step 4 are below 100%, then Savings Plan commitment exceeds actual usage. If CloudWatch metrics from Step 8 show service usage dropped significantly, then reduced usage is causing low utilization. Compare commitment amount to actual hourly usage - if usage is consistently below commitment, then over-commitment occurred. If utilization should be higher, continue to step 4.

4. **Review Coverage Scope Configuration from Step 5**: If coverage analysis from Step 5 shows gaps between Savings Plan eligible usage and actual coverage, identify which services or instance types are not covered. If using EC2 Instance Savings Plans instead of Compute Savings Plans, then flexibility limitations may cause gaps. Compute Savings Plans should cover EC2, Lambda, and Fargate regardless of instance family, size, or region.

5. **Correlate with Usage Changes from Step 9**: If CloudTrail events from Step 9 show significant service usage pattern changes (new instance types, region migrations, service transitions) within 30 days, then usage evolution has outpaced Savings Plan coverage. Compare usage before and after changes to quantify the coverage gap.

**If no correlation is found**: Extend analysis to 180 days using billing data from Step 6. Check for Savings Plan expiration approaching. Verify the Savings Plan type matches usage patterns - Compute Savings Plans provide flexibility across services while EC2 Instance Savings Plans are instance-family specific. Review whether usage has migrated to services not covered by existing plans.
