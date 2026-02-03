# Automation Coverage

## Meaning

Automation coverage indicates that automation coverage is incomplete or automation gaps are detected (triggering alarms like AutomationCoverageIncomplete or AutomationGapDetected) because automation is missing for services, automation scripts are incomplete, automation coverage analysis tools fail, automation gap monitoring indicates problems, or automation quality is insufficient. Automation coverage gaps are detected, automation is missing, automation scripts are incomplete, and automation coverage analysis fails. This affects the operational readiness layer and automation capability, typically caused by automation creation failures, automation script gaps, automation coverage analysis tool failures, or automation gap monitoring issues; if automation coverage affects container workloads, container automation may be incomplete and applications may experience manual operational overhead.

## Impact

AutomationCoverageIncomplete alarms fire; AutomationGapDetected alarms fire; automation coverage is incomplete; automation gaps are detected; manual operational overhead may increase; operational efficiency may be reduced. Automation coverage gaps are detected; if automation coverage affects container workloads, container automation may be incomplete, pod automation may be missing, and container applications may experience manual operational overhead; applications may experience automation coverage gaps or operational efficiency failures.

## Playbook

1. List Systems Manager automation documents in region `<region>` and verify automation coverage for services to identify services without automation, checking automation coverage gaps.
2. Retrieve Systems Manager automation document `<document-name>` content and verify automation step completeness and script quality, checking automation step coverage.
3. Compare automation coverage analysis results with service deployment timestamps and verify whether new services have automation created upon deployment, using service configuration data as supporting evidence.
4. Query CloudWatch Logs for log groups containing automation execution events and filter for automation execution failures or incomplete automation patterns within the last 30 days.
5. Retrieve Systems Manager automation execution history for document `<document-name>` and verify automation execution success rates to identify incomplete automation, checking automation execution coverage.
6. List CloudWatch alarms for services in region `<region>` and verify alarm-to-automation mapping coverage to identify alarms without associated automation, checking alarm automation coverage.
7. Retrieve automation coverage analysis results and verify automation coverage metrics to identify services with incomplete automation coverage, checking automation completeness metrics.
8. Compare automation update timestamps with service configuration change timestamps within 7 days and verify whether automation is updated when services change, using Systems Manager document data as supporting evidence.

## Diagnosis

1. **Analyze automation inventory from Step 1**: If services have no automation documents, prioritize automation creation for those services. If automation exists but is incomplete from Step 2, complete the missing steps. If automation count is low relative to service count, systematic coverage gaps exist.

2. **Evaluate automation execution success from Step 5**: If automation execution success rate is low, automation has bugs or dependencies are missing. If specific steps consistently fail, focus remediation on those steps.

3. **Review alarm-to-automation mapping from Step 6**: If alarms have no associated automation, incidents require manual remediation. If automation exists but is not triggered by alarms, integrate automation with alarm actions.

4. **Cross-reference with service changes from Step 8**: If services changed but automation was not updated, automation may be outdated. If automation updates fail during changes, investigate automation deployment process.

5. **Assess execution patterns from Step 4**: If automation execution failures are increasing, automation quality is degrading. If failures occur for specific services, investigate those service configurations.

If the above analysis is inconclusive: Define automation standards for each service type. Implement automation testing as part of deployment. Review incident history to identify manual tasks that should be automated. Consider AWS Systems Manager OpsCenter for automation gap visibility.
