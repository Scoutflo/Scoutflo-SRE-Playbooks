# On-call Readiness

## Meaning

On-call readiness indicates that on-call procedures are incomplete or on-call readiness gaps are detected (triggering alarms like OnCallReadinessIncomplete or OnCallProcedureGapDetected) because on-call procedures are missing, on-call escalation paths are not defined, on-call tools are not configured, on-call readiness monitoring indicates problems, or on-call training is insufficient. On-call readiness gaps are detected, on-call procedures are missing, on-call escalation paths are undefined, and on-call readiness analysis fails. This affects the operational readiness layer and incident response capability, typically caused by on-call procedure creation failures, on-call tool configuration issues, on-call readiness monitoring gaps, or on-call training deficiencies; if on-call readiness affects container workloads, container on-call procedures may be incomplete and applications may experience incident response delays.

## Impact

OnCallReadinessIncomplete alarms fire; OnCallProcedureGapDetected alarms fire; on-call readiness is incomplete; on-call readiness gaps are detected; incident response may be delayed; on-call effectiveness may be reduced. On-call readiness gaps are detected; if on-call readiness affects container workloads, container on-call procedures may be incomplete, pod on-call escalation may be undefined, and container applications may experience incident response delays; applications may experience on-call readiness gaps or incident response failures.

## Playbook

1. Retrieve on-call procedure documentation and verify on-call procedure coverage for services in region `<region>` to identify services without on-call procedures, checking on-call procedure coverage.
2. Retrieve on-call escalation path configuration and verify escalation path definitions for services to identify missing escalation paths, checking on-call escalation coverage.
3. List on-call management tools and verify on-call tool configuration for services to identify services without on-call tools, checking on-call tool coverage.
4. Query CloudWatch Logs for log groups containing on-call incident events and filter for on-call procedure execution failures or escalation failures within the last 30 days.
5. Compare on-call readiness analysis results with service deployment timestamps and verify whether new services have on-call procedures defined upon deployment, using service configuration data as supporting evidence.
6. Retrieve on-call incident response metrics and verify on-call response times and escalation effectiveness to identify on-call readiness issues, checking on-call effectiveness coverage.
7. List CloudWatch alarms for services in region `<region>` and verify alarm-to-on-call mapping coverage to identify alarms without on-call assignments, checking alarm on-call coverage.
8. Compare on-call procedure update timestamps with service configuration change timestamps within 7 days and verify whether on-call procedures are updated when services change, using on-call procedure documentation data as supporting evidence.

## Diagnosis

1. **Analyze on-call procedure coverage from Step 1**: If services have no on-call procedures, prioritize procedure creation for critical services. If procedures exist but are incomplete from Step 2, define missing escalation paths. If procedure count is low relative to service count, systematic gaps exist.

2. **Evaluate escalation path definitions from Step 2**: If escalation paths are undefined, incidents cannot be properly escalated. If paths exist but are outdated, escalation may reach wrong contacts. If paths are correctly defined, escalation readiness is complete.

3. **Review alarm-to-on-call mapping from Step 7**: If alarms have no on-call assignments, alerts may not reach responders. If mappings exist but are incorrect, wrong teams are notified. If mappings are current, notification readiness is complete.

4. **Cross-reference with incident metrics from Step 6**: If response times are high, on-call procedures are ineffective. If escalation success rate is low, escalation paths are not working. If metrics are healthy, on-call processes are effective.

5. **Assess procedure maintenance from Step 8**: If procedures are outdated compared to service changes, responders have incorrect information. If procedures are regularly updated, on-call documentation is maintained.

If the above analysis is inconclusive: Conduct on-call drills to test procedure effectiveness. Review historical incidents for on-call response patterns. Implement on-call procedure templates for consistency. Consider automated on-call scheduling tools.
