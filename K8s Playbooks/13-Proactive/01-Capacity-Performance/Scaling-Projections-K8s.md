# Scaling Projections

## Meaning

Scaling projections indicate that future scaling needs cannot be accurately projected or scaling capacity planning is insufficient (triggering alerts like ScalingProjectionUnavailable or ScalingForecastFailed) because scaling trend analysis fails, scaling projection models are unavailable, scaling growth patterns are not identified, scaling capacity planning data is missing, or scaling projections are inaccurate. Scaling trends show unpredictable patterns, scaling projection metrics are unavailable, scaling growth projections cannot be calculated, and scaling capacity planning analysis fails. This affects the capacity planning layer and auto-scaling configuration, typically caused by insufficient scaling historical data, scaling projection model failures, scaling pattern changes, or scaling planning tool unavailability; if scaling projections affect container workloads, container scaling needs may be underestimated and applications may experience scaling failures.

## Impact

ScalingProjectionUnavailable alerts fire; ScalingForecastFailed alerts fire; future scaling needs cannot be projected; scaling capacity planning is insufficient; auto-scaling may be inadequate; scaling failures may occur unexpectedly. Scaling projections are unavailable; if scaling projections affect container workloads, container scaling needs may be underestimated, pod autoscaling may be insufficient, and container applications may experience scaling failures; applications may experience scaling shortages or unexpected scaling constraints.

## Playbook

1. Retrieve HorizontalPodAutoscaler <hpa-name> in namespace <namespace> with YAML output to inspect its scaling thresholds, target utilization settings, and current scaling status.
2. List recent events in namespace <namespace> sorted by timestamp to identify scaling-related events, scaling failures, or resource constraint warnings.
3. Retrieve Prometheus metrics for horizontal pod autoscaler scaling activity including scale_out_events and scale_in_events over the last 90 days to analyze scaling patterns and identify scaling trends.
4. Retrieve Prometheus metrics for pod scaling including pod creation and termination events over the last 90 days to analyze pod scaling patterns.
5. Retrieve Prometheus metrics for deployment scaling including replica count changes over the last 90 days to analyze deployment scaling patterns.
6. Retrieve logs from autoscaler pods and filter for scaling activity patterns or scaling constraint events within the last 90 days.
7. Compare scaling activity trend data with scaling projection model outputs and verify whether projections align with historical scaling patterns, using Prometheus metrics as supporting evidence.
8. Retrieve Prometheus metrics for scaling capacity including available capacity and scaling rate over the last 90 days to identify scaling capacity trends.
9. Analyze scaling activity distribution patterns over the last 90 days to identify seasonal scaling trends or scaling spikes that affect projections.

## Diagnosis

1. Review the HPA configuration from Step 1 and scaling metrics from Steps 3-5. If historical scaling activity shows consistent patterns over 90 days, then reliable projections should be possible. If patterns are highly variable, then projection accuracy will be limited.

2. Analyze the scaling capacity metrics from Step 8. If available capacity trends are declining while scaling demand is increasing, then capacity expansion is needed. If capacity is stable, then current projections may be adequate.

3. If Step 3 HPA scaling events show frequent scale-out reaching maximum replicas, then current capacity projections are underestimating demand. If scale-out is rare, then current capacity may be sufficient.

4. Review the scaling activity distribution from Step 9. If seasonal patterns or predictable spikes are identified, use these to improve projection models. If activity is unpredictable, then reactive scaling with higher headroom may be more appropriate than projections.

5. If Step 7 projection model outputs significantly differ from actual scaling patterns, then the model parameters need adjustment. If models are not producing outputs, then model configuration or data collection issues exist.

If analysis is inconclusive: Examine events from Step 2 for scaling failures or resource constraint warnings that indicate projection gaps. Determine whether projection inaccuracies are clustered around specific timeframes (suggesting pattern recognition issues) or random (suggesting fundamental model problems). Verify that historical scaling data collection covers sufficient timeframes for meaningful trend analysis.
