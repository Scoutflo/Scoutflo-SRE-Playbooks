# ValidationError-DataValidation-Error-application

## Meaning

Data validation error occurs (triggering Sentry error issue with exception type ValidationError) because data validation fails, causing application operations to fail when input data does not meet validation requirements. Error events display in Sentry Issue Details page with error message patterns "validation error", "invalid data", "validation failed", stack traces show application validation layer, and error levels indicate Error or Warning severity. This affects the application layer and indicates data integrity issues typically caused by invalid input data, missing required fields, or validation rule violations; application operations fail; if errors correlate with user input, data quality problems may be visible in user behavior monitoring.

## Impact

Sentry error issue alerts fire; data validation errors occur; application operations fail; applications return validation errors; users affected; issues remain in New or Ongoing status; error levels show Error or Warning severity; stack traces indicate validation failures; error events display in Sentry Issue Details page. User input validation fails; affected user count grows; error count increases continuously; issues show Medium or Low priority in Sentry dashboard; application functionality degrades; user experience issues occur. Validation errors increase; data quality problems occur; if errors correlate with user input, data quality problems may cause user experience degradation.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify ValidationError with "validation error", "invalid data", or "validation failed" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected validation files
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract validation error details from error message (`metadata.value`) including validation field, validation rule violated, and the invalid value received.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

## Diagnosis

1. Analyze the validation error details from event stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and error message (`metadata.value`) to identify the specific validation rule that failed, the field name, and the invalid value received. If the error message indicates a schema validation failure (e.g., missing required field, type mismatch), the issue is likely upstream data quality. If the error indicates a business rule violation (e.g., value out of range), the issue may be user input or validation rule changes.

2. Compare the event's `firstSeen` timestamp with `firstRelease` deployment time from issue details. If the ValidationError first appeared within 30 minutes after a release deployment, the root cause is likely a validation rule change, new required fields, or stricter validation logic introduced in the release. If the error predates recent releases, investigate changes in data sources, user input patterns, or third-party integrations.

3. Examine the affected user distribution and event frequency from event data. If validation errors affect all users uniformly since a specific timestamp, a validation rule or schema change is the likely cause. If errors are concentrated among specific user segments or correlate with particular input sources, the issue relates to data quality from those specific sources or user behaviors.