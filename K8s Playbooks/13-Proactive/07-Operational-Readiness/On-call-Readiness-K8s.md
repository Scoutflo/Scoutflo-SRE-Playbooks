# On-call Readiness

## Meaning

On-call readiness indicates that on-call procedures are incomplete or on-call readiness gaps are detected (triggering alerts like OnCallReadinessIncomplete or OnCallProcedureGapDetected) because on-call procedures are missing, on-call escalation paths are not defined, on-call tools are not configured, on-call readiness monitoring indicates problems, or on-call training is insufficient. On-call readiness gaps are detected, on-call procedures are missing, on-call escalation paths are undefined, and on-call readiness analysis fails. This affects the operational readiness layer and incident response capability, typically caused by on-call procedure creation failures, on-call tool configuration issues, on-call readiness monitoring gaps, or on-call training deficiencies; if on-call readiness affects container workloads, container on-call procedures may be incomplete and applications may experience incident response delays.

## Impact

OnCallReadinessIncomplete alerts fire; OnCallProcedureGapDetected alerts fire; on-call readiness is incomplete; on-call readiness gaps are detected; incident response may be delayed; on-call effectiveness may be reduced. On-call readiness gaps are detected; if on-call readiness affects container workloads, container on-call procedures may be incomplete, pod on-call escalation may be undefined, and container applications may experience incident response delays; applications may experience on-call readiness gaps or incident response failures.

## Playbook

1. List deployments and services in namespace <namespace> with wide output to retrieve all services and deployments that require on-call procedure coverage.
2. List recent events in namespace <namespace> sorted by timestamp to identify recent incidents and events that may indicate on-call readiness gaps.
3. Retrieve on-call procedure documentation and verify on-call procedure coverage for services in namespace `<namespace>` to identify services without on-call procedures, checking on-call procedure coverage.
4. Retrieve on-call escalation path configuration and verify escalation path definitions for services to identify missing escalation paths, checking on-call escalation coverage.
5. List on-call management tools and verify on-call tool configuration for services to identify services without on-call tools, checking on-call tool coverage.
6. Retrieve logs from on-call incident pods and filter for on-call procedure execution failures or escalation failures within the last 30 days.
7. Compare on-call readiness analysis results with pod deployment timestamps and verify whether new pods have on-call procedures defined upon deployment, using pod configuration data as supporting evidence.
8. Retrieve on-call incident response metrics and verify on-call response times and escalation effectiveness to identify on-call readiness issues, checking on-call effectiveness coverage.

## Diagnosis

1. Review the on-call procedure coverage from Step 3. If services lack documented on-call procedures, these are the primary readiness gaps. Prioritize creating procedures for critical services.

2. Analyze the escalation path configuration from Step 4. If escalation paths are undefined or incomplete, then incidents may not reach the right responders. Verify escalation paths for all severity levels.

3. If Step 6 on-call incident logs show procedure execution failures or escalation failures, identify whether failures are due to missing procedures, incorrect contact information, or tool issues.

4. Review the on-call response metrics from Step 8. If response times are slow or escalation effectiveness is low, then on-call processes may need improvement even if procedures exist.

5. If Step 7 shows new pods without on-call procedures upon deployment, then deployment automation needs to include on-call procedure creation or linking.

If analysis is inconclusive: Examine events from Step 2 for recent incidents that revealed on-call readiness gaps. Determine whether gaps are concentrated in newly deployed services (suggesting onboarding process issues) or established services (suggesting documentation decay). Verify that on-call training is up to date and team members are familiar with procedures.
