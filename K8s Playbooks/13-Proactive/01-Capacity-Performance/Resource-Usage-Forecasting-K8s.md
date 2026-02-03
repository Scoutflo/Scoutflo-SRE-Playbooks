# Resource Usage Forecasting

## Meaning

Resource usage forecasting indicates that future resource needs cannot be accurately predicted or resource capacity planning is insufficient (triggering alerts like ResourceForecastUnavailable or CapacityForecastFailed) because resource usage trends cannot be analyzed, capacity forecasting models fail, resource growth patterns are not identified, capacity planning data is unavailable, or resource usage projections are inaccurate. Resource usage trends show unpredictable patterns, capacity forecasting metrics are unavailable, resource growth projections cannot be calculated, and capacity planning analysis fails. This affects the capacity planning layer and resource provisioning, typically caused by insufficient historical data, forecasting model failures, resource usage pattern changes, or capacity planning tool unavailability; if forecasting affects container workloads, container resource needs may be underestimated and applications may experience capacity constraints.

## Impact

ResourceForecastUnavailable alerts fire; CapacityForecastFailed alerts fire; future resource needs cannot be predicted; capacity planning is insufficient; resource provisioning may be inadequate; capacity constraints may occur unexpectedly. Resource usage forecasting is unavailable; if forecasting affects container workloads, container resource needs may be underestimated, pod scaling may be insufficient, and container applications may experience capacity constraints; applications may experience capacity shortages or unexpected resource exhaustion.

## Playbook

1. List pods in namespace <namespace> with wide output to identify current pod distribution and resource consumption across the namespace.
2. List recent events in namespace <namespace> sorted by timestamp to identify recent events related to resource constraints, scaling, or capacity issues.
3. Describe horizontal pod autoscaler in namespace <namespace> to inspect horizontal pod autoscaler configurations and current scaling status for capacity trend analysis.
4. Retrieve Prometheus metrics for pod CPU utilization and memory utilization over the last 90 days to analyze usage trends and identify growth patterns.
5. Retrieve Prometheus metrics for node CPU utilization and memory utilization over the last 90 days to analyze node usage trends and identify capacity growth patterns.
6. Retrieve resource quota usage data for namespace `<namespace>` over the last 90 days and analyze usage trends to identify growth patterns.
7. Retrieve logs from capacity monitoring pods and filter for patterns indicating usage growth or capacity constraints within the last 90 days.
8. Compare resource usage trend data with capacity forecasting model outputs and verify whether forecasts align with historical trends, using Prometheus metrics as supporting evidence.

## Diagnosis

1. Review the 90-day CPU and memory utilization trends from Steps 4-5. If trends show consistent growth patterns, forecasting should be able to predict future needs. If patterns are highly variable, then reactive scaling with higher headroom may be more appropriate than forecasting.

2. Analyze the HPA configurations from Step 3. If autoscalers are reaching limits frequently, then capacity forecasts may be underestimating demand. If autoscalers rarely trigger, then current capacity is sufficient.

3. If Step 6 resource quota usage shows approaching limits, verify that forecasting has identified this and capacity expansion is planned. If forecasting did not predict approaching limits, then model calibration is needed.

4. Review the capacity monitoring logs from Step 7. If logs show usage growth or constraint patterns, identify which resources are growing fastest and prioritize capacity planning for those resources.

5. If Step 8 forecast model outputs diverge significantly from actual trends, then model parameters need adjustment based on current usage patterns.

If analysis is inconclusive: Examine events from Step 2 for resource constraints or scaling issues that indicate forecasting gaps. Determine whether forecast inaccuracies are clustered around specific timeframes (suggesting pattern recognition issues) or random (suggesting fundamental model problems). Verify that sufficient historical data exists for meaningful trend analysis.
