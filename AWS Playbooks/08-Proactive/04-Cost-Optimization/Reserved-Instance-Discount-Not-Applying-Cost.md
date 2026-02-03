# Reserved Instance Discount Not Applying

## Meaning

Reserved Instance discount is not applying (triggering billing inaccuracies or ReservedInstanceDiscountMissing alarms) because Reserved Instance does not match instance usage, Reserved Instance scope is incorrect, instance type or platform mismatch exists, Reserved Instance is not active, billing system discount calculation fails, or Reserved Instance term has expired. Reserved Instance discounts are not applied, expected cost savings are not realized, and billing charges are higher than expected. This affects the cost management and billing layer and reduces cost optimization, typically caused by Reserved Instance matching issues, scope problems, or billing calculation errors; if using Reserved Instances with different instance families or platforms, matching behavior may differ and applications may experience billing inaccuracies.

## Impact

Reserved Instance discounts are not applied; expected cost savings are not realized; billing charges are higher than expected; Reserved Instance benefits are lost; discount application automation fails; cost optimization objectives are not met; billing accuracy is compromised. ReservedInstanceDiscountMissing alarms may fire; if using Reserved Instances with different instance families or platforms, matching behavior may differ; applications may experience unexpected costs; cost optimization benefits may not be realized.

## Playbook

1. Verify EC2 Reserved Instance exists and AWS service health for EC2 and Billing in region `<region>` is normal.
2. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Reserved Instance purchase events, instance usage events, or billing-related API calls, checking for Reserved Instance purchases.
3. Retrieve CloudWatch metrics for EC2 instance usage including instance type, platform, and region usage over the last 30 days to compare with Reserved Instance attributes, analyzing usage patterns.
4. List EC2 Reserved Instances and check Reserved Instance status, instance type, platform, scope, and active status, verifying Reserved Instance configuration.
5. List EC2 instance usage for Reserved Instance eligible instance types and check instance type, platform, and region matching against Reserved Instances, analyzing matching patterns.
6. Query CloudWatch Logs for log groups containing billing events and filter for Reserved Instance discount application patterns or billing calculation errors, checking billing details.
7. Retrieve the EC2 Reserved Instance `<reserved-instance-id>` term and expiration date and verify Reserved Instance is active, checking if expiration affects discount.
8. Retrieve CloudWatch metrics for EC2 instance usage including instance family and platform and verify instance family and platform matching, checking if platform differences affect matching.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for EC2 instance type or platform modification events within the last 30 days, checking for instance changes.

## Diagnosis

1. **Analyze CloudWatch Metrics from Step 3**: Review EC2 instance usage patterns against Reserved Instance attributes. If CloudWatch metrics show instances running with different instance types, platforms (Linux vs Windows), or tenancy (default vs dedicated) than the Reserved Instance from Step 4, then attribute mismatch is preventing discount application. Compare exact instance type (e.g., m5.large vs m5.xlarge) and platform. If attributes appear matched, continue to step 2.

2. **Check Reserved Instance Status from Steps 4 and 7**: If Reserved Instance from Step 4 shows status other than "active", then the reservation is not applying discounts. If term and expiration from Step 7 show the Reserved Instance has expired or is not yet active, then lifecycle status is the issue. New Reserved Instances typically become active within 24 hours of purchase. If status is active, continue to step 3.

3. **Evaluate Scope Configuration from Step 4**: If Reserved Instance scope is "Availability Zone" but instances run in different AZs within the region, then scope limitation is preventing matching. Regional scope provides flexibility to match instances anywhere in the region. Verify the scope matches your instance deployment pattern. If scope appears correct, continue to step 4.

4. **Review Instance Family Flexibility from Step 8**: If using size-flexible Reserved Instances (regional scope), verify instance family matches (e.g., m5 family). Size flexibility allows matching within the same family. If instances are in a different family than the reservation, then no size flexibility applies. Compare CloudWatch metrics from Step 8 for family matching.

5. **Correlate with Instance Changes from Step 9**: If CloudTrail events from Step 9 show instance type modifications, platform changes, or tenancy changes within 30 days, then instance changes may have broken Reserved Instance matching. Compare instance attributes before and after changes to identify the mismatch.

**If no correlation is found**: Extend analysis to 180 days using billing data from Step 6. Check billing details for Reserved Instance utilization rates - if utilization is below 100%, then usage does not fully match reservation capacity. Verify billing system has processed correctly. Review whether capacity reservations affect matching. Check for Reserved Instance expiration approaching.
