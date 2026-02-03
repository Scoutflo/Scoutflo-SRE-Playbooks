# DynamoDB On-Demand Pricing Higher Than Expected

## Meaning

DynamoDB On-Demand pricing is higher than expected (triggering cost anomalies or DynamoDBOnDemandPricingHigh alarms) because on-demand request pricing increased, data transfer costs spiked, backup and restore costs increased, on-demand capacity units exceeded expectations, pricing model calculations are incorrect, or DynamoDB table usage patterns changed unexpectedly. DynamoDB On-Demand costs increase unexpectedly, on-demand pricing exceeds expectations, and cost optimization objectives are not met. This affects the cost management and database layer and increases costs, typically caused by usage spikes, data transfer increases, or backup cost changes; if using DynamoDB On-Demand with Global Tables, pricing behavior may differ and applications may experience unexpected costs.

## Impact

DynamoDB On-Demand costs increase unexpectedly; on-demand pricing exceeds expectations; cost optimization objectives are not met; budget thresholds may be exceeded; on-demand cost predictability is lost; billing charges are higher than expected; cost management automation is ineffective. DynamoDBOnDemandPricingHigh alarms may fire; if using DynamoDB On-Demand with Global Tables, pricing behavior may differ; applications may experience unexpected costs; cost optimization objectives may not be met.

## Playbook

1. Verify DynamoDB table `<table-name>` exists and AWS service health for DynamoDB and Billing in region `<region>` is normal.
2. Retrieve CloudWatch metrics for DynamoDB table `<table-name>` including ConsumedReadCapacityUnits, ConsumedWriteCapacityUnits, and DataTransferBytes over the last 30 days to identify usage patterns, analyzing usage trends.
3. Query CloudWatch Logs for log groups containing CloudTrail events and filter for DynamoDB API call events, request patterns, or data transfer events related to table `<table-name>`, checking for usage spikes.
4. List DynamoDB table usage patterns for table `<table-name>` and check read request units, write request units, and data transfer volumes, analyzing usage volume.
5. Query CloudWatch Logs for log groups containing billing events and filter for DynamoDB on-demand pricing patterns or unexpected charge events, checking billing details.
6. Retrieve DynamoDB table backup and restore activity for table `<table-name>` and check backup costs and restore operation costs, analyzing backup costs.
7. Retrieve CloudWatch metrics for DynamoDB table `<table-name>` including ItemCount and TableSizeBytes and verify table size trends, checking if table size growth affects costs.
8. Retrieve the DynamoDB Table `<table-name>` Global Tables configuration if applicable and verify Global Tables replication, checking if Global Tables replication affects costs.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for DynamoDB table capacity mode or usage pattern changes within the last 30 days, checking for capacity mode or usage changes.

## Diagnosis

1. **Analyze CloudWatch Metrics from Step 2**: Review DynamoDB usage metrics for cost drivers. If CloudWatch metrics show ConsumedReadCapacityUnits or ConsumedWriteCapacityUnits spiking significantly, then increased request volume is driving costs. On-Demand pricing charges per request - calculate expected cost by multiplying RRU/WRU by pricing rate. If request units correlate with billing increase, usage growth is confirmed. If request patterns are stable, continue to step 2.

2. **Check Data Transfer Metrics from Step 2**: If DataTransferBytes metrics from Step 2 show significant outbound data transfer, then data transfer costs may be contributing. Cross-region data transfer and internet egress are charged separately from request units. If data transfer correlates with cost increase, then data movement patterns are the cause. If data transfer is minimal, continue to step 3.

3. **Review Table Size and Storage from Step 7**: If CloudWatch metrics from Step 7 show ItemCount and TableSizeBytes growing significantly, then storage costs are increasing. DynamoDB charges for storage based on table size. Compare storage growth rate to cost increase rate - if proportional, storage is the driver. If storage is stable, continue to step 4.

4. **Evaluate Backup and Global Tables Costs from Steps 6 and 8**: If backup activity from Step 6 shows frequent on-demand backups or point-in-time recovery enabled, then backup costs contribute to billing. If Global Tables configuration from Step 8 shows cross-region replication enabled, then replication writes double or triple request costs depending on replica count. Calculate replication overhead against billing increase.

5. **Correlate with Usage Changes from Step 9**: If CloudTrail events from Step 9 show capacity mode changes, GSI additions, or application deployment events within 7 days of cost increase, then recent changes drove usage patterns. Compare request patterns before and after changes to quantify impact.

**If no correlation is found**: Extend analysis to 180 days using billing data from Step 5. Check for hot partition issues causing throttling and retries (which increase total requests). Review GSI usage patterns - GSIs consume separate capacity. Verify application retry logic is not amplifying request counts. Consider switching to Provisioned capacity if usage patterns are predictable for cost optimization.
