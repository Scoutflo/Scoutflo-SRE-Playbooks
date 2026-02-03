# KeyError-MissingKey-Error-application

## Meaning

Missing key error occurs (triggering Sentry error issue with exception type KeyError) because application attempts to access non-existent dictionary key, causing application operations to fail when dictionary does not contain expected key. Error events display in Sentry Issue Details page with error message patterns "key error", "key not found", stack traces show application code layers, and error levels indicate Error or Warning severity. This affects the application layer and indicates dictionary key issues typically caused by missing dictionary keys, incorrect key names, or key access errors; application operations fail; if errors correlate with data changes, dictionary structure problems may be visible in data modification history.

## Impact

Sentry error issue alerts fire; missing key errors occur; application operations fail; applications return key errors; users affected; issues remain in New or Ongoing status; error levels show Error or Warning severity; stack traces indicate key access failures; error events display in Sentry Issue Details page. Dictionary key access fails; affected user count grows; error count increases continuously; issues show Medium or Low priority in Sentry dashboard; application functionality degrades; key errors occur. Key errors increase; dictionary structure problems occur; if errors correlate with data changes, dictionary structure problems may cause application failures.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify KeyError with "key error" or "key not found" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected application files and key access location
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract key name from error message (`metadata.value`) or stack trace context to identify missing dictionary key and the expected data structure.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

## Diagnosis

1. Analyze stack trace frames from the most recent event (`entries[].data.values[].stacktrace.frames[]`) to identify the exact code location and dictionary access pattern causing the KeyError. If the stack trace shows the error originates from code accessing external API responses or database results, the issue is likely data-dependent. If the stack trace shows direct dictionary literal access, the issue is likely a code typo or refactoring error.

2. Compare the event's `firstSeen` timestamp with `firstRelease` deployment time from issue details. If the KeyError first appeared within 30 minutes after a release deployment, the root cause is likely a code change introducing incorrect key access or removing expected dictionary keys. If the error predates recent releases, investigate data source changes or upstream API modifications.

3. Examine event frequency patterns and affected user distribution from event data. If errors occur consistently across all users since a specific timestamp, a code or configuration change is the likely cause. If errors are intermittent and affect specific user segments, the issue correlates with particular data patterns such as missing optional fields or edge-case dictionary structures.