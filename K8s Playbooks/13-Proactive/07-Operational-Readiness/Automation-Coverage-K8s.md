# Automation Coverage

## Meaning

Automation coverage indicates that automation coverage is incomplete or automation gaps are detected (triggering alerts like AutomationCoverageIncomplete or AutomationGapDetected) because automation is missing for services, automation scripts are incomplete, automation coverage analysis tools fail, automation gap monitoring indicates problems, or automation quality is insufficient. Automation coverage gaps are detected, automation is missing, automation scripts are incomplete, and automation coverage analysis fails. This affects the operational readiness layer and automation capability, typically caused by automation creation failures, automation script gaps, automation coverage analysis tool failures, or automation gap monitoring issues; if automation coverage affects container workloads, container automation may be incomplete and applications may experience manual operational overhead.

## Impact

AutomationCoverageIncomplete alerts fire; AutomationGapDetected alerts fire; automation coverage is incomplete; automation gaps are detected; manual operational overhead may increase; operational efficiency may be reduced. Automation coverage gaps are detected; if automation coverage affects container workloads, container automation may be incomplete, pod automation may be missing, and container applications may experience manual operational overhead; applications may experience automation coverage gaps or operational efficiency failures.

## Playbook

1. List cronjobs and jobs in namespace <namespace> to identify configured automation and scheduled tasks in the namespace.

2. List recent events in namespace <namespace> sorted by timestamp to identify any recent automation execution issues or failures.

3. Describe configmap <automation-configmap-name> in namespace <namespace> to verify automation step completeness and script quality.

4. Retrieve logs from automation execution pods with label app=automation in namespace <namespace> and filter for automation execution failures or incomplete patterns.

5. List jobs in namespace <namespace> with wide output to retrieve automation execution history and verify automation execution success rates.

6. List Prometheus alerts for services in namespace `<namespace>` and verify alert-to-automation mapping coverage to identify alerts without associated automation, checking alert automation coverage.

7. Retrieve automation coverage analysis results and verify automation coverage metrics to identify services with incomplete automation coverage, checking automation completeness metrics.

8. Compare automation update timestamps with pod configuration change timestamps within 7 days and verify whether automation is updated when pods change, using automation configuration data as supporting evidence.

## Diagnosis

1. Review the cronjob and job configurations from Step 1 and automation configmap from Step 3. If services lack associated automation, these are the primary coverage gaps. Prioritize automating critical operational tasks.

2. Analyze the automation execution logs from Step 4. If logs show execution failures or incomplete patterns, identify which automation scripts are failing and the failure causes.

3. If Step 5 automation execution history shows low success rates, then existing automation is unreliable. Focus on improving reliability before expanding coverage.

4. Review the alert-to-automation mapping from Step 6. If alerts exist without associated automation, then manual intervention is required for those alert types. Prioritize automating responses to high-frequency alerts.

5. If Step 8 shows automation not updated after pod changes, then automation drift is occurring. Integrate automation updates into deployment pipelines.

If analysis is inconclusive: Examine events from Step 2 for automation execution issues. Review the automation coverage metrics from Step 7 to identify services with incomplete coverage. Determine whether gaps are concentrated in newly deployed services (suggesting onboarding issues) or established services (suggesting automation maintenance decay).
