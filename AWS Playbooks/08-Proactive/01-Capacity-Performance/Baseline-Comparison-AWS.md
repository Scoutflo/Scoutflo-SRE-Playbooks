# Baseline Comparison

## Meaning

Baseline comparison indicates that performance baseline comparisons cannot be performed or baseline comparison failures are detected (triggering alarms like BaselineComparisonFailed or BaselineUnavailable) because performance baselines are unavailable, baseline comparison tools fail, baseline comparison results show failures, baseline configuration is missing, or baseline comparison monitoring indicates problems. Baseline comparisons show failures, performance baselines are unavailable, baseline comparison tools fail, and baseline comparison monitoring indicates problems. This affects the performance monitoring layer and baseline management, typically caused by baseline data unavailability, baseline comparison tool failures, baseline configuration issues, or baseline comparison monitoring failures; if baseline comparison affects container workloads, container performance baselines may be unavailable and applications may experience baseline comparison failures.

## Impact

BaselineComparisonFailed alarms fire; BaselineUnavailable alarms fire; baseline comparisons cannot be performed; baseline comparison failures are detected; performance analysis may be limited; baseline management may be compromised. Baseline comparisons show failures; if baseline comparison affects container workloads, container performance baselines may be unavailable, pod baseline comparisons may fail, and container applications may experience baseline comparison failures; applications may experience baseline comparison gaps or performance analysis limitations.

## Playbook

1. Retrieve performance baseline configuration for service `<service-name>` and verify baseline data availability and baseline threshold settings, checking baseline configuration.
2. Retrieve CloudWatch metrics for service `<service-name>` including baseline metrics and current performance metrics over the last 30 days to compare with baselines.
3. Query CloudWatch Logs for log groups containing baseline comparison events and filter for baseline comparison failures or baseline unavailability patterns within the last 7 days.
4. Compare baseline comparison failure timestamps with baseline data update timestamps within 1 hour and verify whether baseline updates affect comparison results, using baseline configuration data as supporting evidence.
5. Retrieve baseline comparison tool execution results and verify tool availability and comparison completion status, checking baseline comparison tool health.
6. Compare baseline configuration change timestamps with baseline comparison failure timestamps within 1 hour and verify whether configuration changes cause comparison failures, using baseline configuration data as supporting evidence.
7. Retrieve performance baseline history for service `<service-name>` and verify baseline data completeness and baseline calculation accuracy, checking baseline data quality.
8. List CloudWatch alarms for service `<service-name>` and verify alarm baseline configuration to identify alarms without baselines, checking alarm baseline coverage.

## Diagnosis

1. **Analyze baseline availability from Step 1 and Step 7**: If baseline data is missing, baselines have not been established. If baseline exists but is outdated, recalculate baselines with recent data. If baseline configuration is incorrect, correct the threshold settings.

2. **Evaluate current vs. baseline metrics from Step 2**: If current metrics deviate significantly from baseline, investigate the cause of deviation. If metrics are within baseline ranges, performance is normal. If metrics consistently exceed baseline, baseline may need updating.

3. **Review comparison tool health from Step 5**: If comparison tools are failing, troubleshoot tool configuration. If tools are healthy but comparison fails, input data may be incomplete.

4. **Cross-reference with configuration changes from Step 6**: If baseline changes correlate with comparison failures, recent configuration changes caused issues. If no changes were made but failures occur, investigate data collection.

5. **Assess alarm baseline coverage from Step 8**: If alarms lack baseline configuration, anomaly detection is limited. If alarms have outdated baselines, false positives or negatives may occur. If baselines are current, anomaly detection is effective.

If the above analysis is inconclusive: Use CloudWatch Anomaly Detection for automatic baseline management. Review metric resolution for baseline accuracy. Consider seasonal adjustments to baselines. Implement baseline version history for comparison.
