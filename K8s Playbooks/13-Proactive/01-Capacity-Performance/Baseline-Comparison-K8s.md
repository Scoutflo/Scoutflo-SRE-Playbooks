# Baseline Comparison

## Meaning

Baseline comparison indicates that performance baseline comparisons cannot be performed or baseline comparison failures are detected (triggering alerts like BaselineComparisonFailed or BaselineUnavailable) because performance baselines are unavailable, baseline comparison tools fail, baseline comparison results show failures, baseline configuration is missing, or baseline comparison monitoring indicates problems. Baseline comparisons show failures, performance baselines are unavailable, baseline comparison tools fail, and baseline comparison monitoring indicates problems. This affects the performance monitoring layer and baseline management, typically caused by baseline data unavailability, baseline comparison tool failures, baseline configuration issues, or baseline comparison monitoring failures; if baseline comparison affects container workloads, container performance baselines may be unavailable and applications may experience baseline comparison failures.

## Impact

BaselineComparisonFailed alerts fire; BaselineUnavailable alerts fire; baseline comparisons cannot be performed; baseline comparison failures are detected; performance analysis may be limited; baseline management may be compromised. Baseline comparisons show failures; if baseline comparison affects container workloads, container performance baselines may be unavailable, pod baseline comparisons may fail, and container applications may experience baseline comparison failures; applications may experience baseline comparison gaps or performance analysis limitations.

## Playbook

1. Describe deployment <deployment-name> in namespace <namespace> to understand current resource configuration and performance settings.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent changes or issues affecting baseline metrics.

3. Retrieve pod resource usage in namespace <namespace> to compare current performance metrics against expected baselines.

4. Retrieve Prometheus metrics for service `<service-name>` including baseline metrics and current performance metrics over the last 30 days to compare with baselines.

5. Retrieve logs from baseline comparison pods with label app=baseline-comparison in namespace <namespace> and filter for baseline comparison failures.

6. Retrieve baseline comparison tool execution results and verify tool availability and comparison completion status, checking baseline comparison tool health.

7. Retrieve performance baseline history for service `<service-name>` and verify baseline data completeness and baseline calculation accuracy, checking baseline data quality.

8. List Prometheus alerts for service `<service-name>` and verify alert baseline configuration to identify alerts without baselines, checking alert baseline coverage.

## Diagnosis

1. Review the current performance metrics from Step 3 and compare with baseline metrics from Step 4. If current metrics significantly exceed baseline thresholds, genuine performance deviations exist. If metrics appear within baseline ranges, then comparison infrastructure may be the issue.

2. Analyze the baseline comparison tool status from Step 6. If tools show failures or incomplete status, then comparison infrastructure is the issue. If tools are healthy, proceed to baseline data quality analysis.

3. If Step 5 baseline comparison logs show failures, identify whether failures are due to missing baseline data, tool misconfiguration, or metric collection issues.

4. Review the baseline history from Step 7. If baseline data is incomplete or calculation accuracy is poor, then baseline establishment needs improvement before meaningful comparisons can occur.

5. If Step 8 alert baseline coverage shows services without baseline configuration, then these services cannot be compared against baselines. Prioritize establishing baselines for critical services.

If analysis is inconclusive: Examine events from Step 2 for changes affecting baseline metrics. Determine whether comparison failures affect all services (suggesting infrastructure issues) or specific services (suggesting service-specific baseline gaps). Verify that baseline data collection covers sufficient timeframes for meaningful comparison.
