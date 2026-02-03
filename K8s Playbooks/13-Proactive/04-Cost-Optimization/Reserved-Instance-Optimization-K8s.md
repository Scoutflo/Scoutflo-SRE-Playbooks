# Reserved Instance Optimization

## Meaning

Reserved instance optimization indicates that node reservation coverage is insufficient, reserved nodes are underutilized, or node reservation purchase opportunities are missed (triggering alerts like ReservedNodeUnderutilized or ReservedNodeCoverageLow) because reserved node utilization is below thresholds, reserved node coverage does not match on-demand usage, reserved node purchase recommendations are not implemented, reserved node expiration is approaching, or reserved node exchange opportunities are missed. Reserved node utilization metrics show low usage, reserved node coverage metrics indicate gaps, reserved node purchase recommendations are available, and reserved node expiration warnings are present. This affects the cost management layer and node reservation lifecycle management, typically caused by reserved node purchase misalignment, reserved node utilization tracking failures, or reserved node lifecycle management issues; if reserved nodes host container workloads, container compute costs may not be optimized and applications may experience unnecessary cost overhead.

## Impact

ReservedNodeUnderutilized alerts fire; ReservedNodeCoverageLow alerts fire; cost optimization opportunities are missed; reserved node utilization is inefficient; reserved node coverage gaps exist; reserved node purchase recommendations are not implemented. Reserved node utilization metrics show low usage; if reserved nodes host container workloads, container compute costs may not be optimized, node reservation benefits may be missed, and container applications may experience unnecessary cost overhead; applications may experience cost inefficiencies or missed savings opportunities.

## Playbook

1. List all nodes with wide output and labels to identify node types, labels, and reservation status.
2. List recent events across all namespaces sorted by timestamp and filtered by reason NodeNotReady and NodeReady to identify recent node-related events that may affect reserved instance utilization.
3. Describe node <node-name> to inspect node capacity, allocatable resources, and current utilization for reserved instance analysis.
4. Retrieve Prometheus metrics for node utilization including CPU utilization and memory utilization over the last 30 days and compare with on-demand node usage to identify utilization gaps.
5. Retrieve node reservation coverage data for cluster over the last 30 days and compare reserved node coverage with on-demand node usage to identify coverage gaps.
6. Retrieve node reservation purchase recommendations for cluster and verify recommendation details including node type, term, and payment option recommendations.
7. Retrieve logs from cluster monitoring pods and filter for reserved node utilization warnings or expiration alerts within the last 7 days.
8. Retrieve Prometheus metrics for reserved node utilization including utilization_percentage and coverage_percentage over the last 30 days to identify utilization trends.

## Diagnosis

1. Review the node utilization metrics from Steps 3-4. If reserved nodes show consistently low utilization (e.g., <50%), then reserved capacity is being wasted. If utilization is high, then reserved nodes are being used effectively.

2. Analyze the coverage comparison from Step 5. If reserved node coverage is low relative to on-demand usage, then cost optimization opportunities exist by purchasing additional reservations. If coverage is high but utilization is low, then over-reservation occurred.

3. If Step 6 purchase recommendations exist, evaluate whether recommendations align with current workload patterns. If workloads have changed since reservations were purchased, recommendations may need reassessment.

4. Review the reservation expiration alerts from Step 7. If reserved nodes are approaching expiration with low utilization, consider not renewing. If utilization is high, renew or purchase replacements.

5. If Step 8 utilization trends show declining usage patterns, then reserved capacity may no longer match workload needs. If utilization is stable, then current reservations are appropriate for the workload.

If analysis is inconclusive: Examine events from Step 2 for node-related issues affecting reserved instance utilization. Determine whether underutilization affects specific node types (suggesting workload migration opportunities) or all reserved nodes (suggesting overall capacity reduction needs). Verify that reserved node utilization tracking accurately captures actual usage.
