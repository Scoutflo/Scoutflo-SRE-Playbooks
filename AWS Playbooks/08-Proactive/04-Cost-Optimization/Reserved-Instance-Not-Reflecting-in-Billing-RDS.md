# RDS Reserved Instance Not Reflecting in Billing

## Meaning

RDS Reserved Instance discount is not reflecting in billing (triggering billing inaccuracies or RDSReservedInstanceDiscountMissing alarms) because Reserved Instance does not match RDS instance usage, Reserved Instance scope is incorrect, database engine or instance class mismatch exists, Reserved Instance is not active, billing system discount calculation fails, or Reserved Instance term has expired. RDS Reserved Instance discounts are not applied, expected cost savings are not realized, and billing charges are higher than expected. This affects the cost management and billing layer and reduces cost optimization, typically caused by Reserved Instance matching issues, scope problems, or billing calculation errors; if using RDS Multi-AZ vs Single-AZ, Reserved Instance matching may differ and applications may experience billing inaccuracies.

## Impact

RDS Reserved Instance discounts are not applied; expected cost savings are not realized; billing charges are higher than expected; Reserved Instance benefits are lost; discount application automation fails; cost optimization objectives are not met; billing accuracy is compromised. RDSReservedInstanceDiscountMissing alarms may fire; if using RDS Multi-AZ vs Single-AZ, Reserved Instance matching may differ; applications may experience unexpected costs; cost optimization benefits may not be realized.

## Playbook

1. Verify RDS Reserved Instance exists and AWS service health for RDS and Billing in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing CloudTrail events and filter for RDS Reserved Instance purchase events, RDS instance usage events, or billing-related API calls, checking for Reserved Instance purchases.
3. Retrieve CloudWatch metrics for RDS instance usage including instance class, database engine, and region usage over the last 30 days to compare with Reserved Instance attributes, analyzing usage patterns.
4. List RDS Reserved Instances and check Reserved Instance status, instance class, database engine, scope, and active status, verifying Reserved Instance configuration.
5. List RDS instance usage for Reserved Instance eligible instance classes and check instance class, database engine, and region matching against Reserved Instances, analyzing matching patterns.
6. Query CloudWatch Logs for log groups containing billing events and filter for RDS Reserved Instance discount application patterns or billing calculation errors, checking billing details.
7. Retrieve the RDS Reserved Instance `<reserved-instance-id>` term and expiration date and verify Reserved Instance is active, checking if expiration affects discount.
8. Retrieve CloudWatch metrics for RDS instance usage including Multi-AZ configuration and verify Multi-AZ vs Single-AZ usage, checking if Multi-AZ affects matching.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for RDS instance type or database engine modification events within the last 30 days, checking for instance changes.

## Diagnosis

1. **Analyze RDS Usage Metrics from Step 3**: Review RDS instance usage patterns against Reserved Instance attributes. If CloudWatch metrics show RDS instances running with different instance classes, database engines, or in different regions than the Reserved Instance from Step 4, then attribute mismatch is preventing discount application. Compare instance class (e.g., db.r5.large vs db.r5.xlarge) and database engine (e.g., MySQL vs PostgreSQL) exactly. If attributes appear matched, continue to step 2.

2. **Check Reserved Instance Status and Terms from Steps 4 and 7**: If Reserved Instance from Step 4 shows status other than "active", then the reservation is not applying. If term and expiration from Step 7 show the Reserved Instance has expired or is not yet active (payment pending), then lifecycle status is the issue. New Reserved Instances may take up to 24 hours to become active after purchase. If status is active, continue to step 3.

3. **Evaluate Multi-AZ Configuration from Step 8**: If CloudWatch metrics show Multi-AZ deployment but the Reserved Instance was purchased for Single-AZ (or vice versa), then deployment type mismatch exists. Multi-AZ Reserved Instances cost approximately 2x Single-AZ - ensure the reservation matches actual deployment configuration. If Multi-AZ configuration matches, continue to step 4.

4. **Review Instance Matching Patterns from Step 5**: If instance usage from Step 5 shows instances that should match but are not receiving discounts, verify the Reserved Instance scope (regional vs AZ-specific). If scope is AZ-specific but instances run in different AZs, then scope limitation is preventing matching. Regional scope provides more flexibility. If scope appears correct, continue to step 5.

5. **Correlate with Instance Changes from Step 9**: If CloudTrail events from Step 9 show RDS instance modifications (instance class changes, engine upgrades, Multi-AZ enablement) within 30 days, then instance changes may have broken Reserved Instance matching. Compare instance attributes before and after changes to identify the mismatch.

**If no correlation is found**: Extend analysis to 180 days using billing data from Step 6. Check billing details for Reserved Instance utilization rates. Verify billing system has processed the reservation correctly. Review whether size-flexible reservations (if purchased) are applying to appropriately sized instances. Check for Reserved Instance expiration or approaching term end.
