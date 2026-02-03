# IndexError-IndexOutOfRange-Error-application

## Meaning

Index out of range error occurs (triggering Sentry error issue with exception type IndexError) because application attempts to access list or array element at invalid index, causing application operations to fail when index exceeds list or array bounds. Error events display in Sentry Issue Details page with error message patterns "index error", "index out of range", stack traces show application code layers, and error levels indicate Error or Warning severity. This affects the application layer and indicates array indexing issues typically caused by invalid index values, empty lists, or index calculation errors; application operations fail; if errors correlate with data changes, array size problems may be visible in data modification history.

## Impact

Sentry error issue alerts fire; index out of range errors occur; application operations fail; applications return index errors; users affected; issues remain in New or Ongoing status; error levels show Error or Warning severity; stack traces indicate index access failures; error events display in Sentry Issue Details page. Array index access fails; affected user count grows; error count increases continuously; issues show Medium or Low priority in Sentry dashboard; application functionality degrades; index errors occur. Index errors increase; array size problems occur; if errors correlate with data changes, array size problems may cause application failures.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify IndexError with "index error" or "index out of range" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected application files and index access location
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract index value from error message (`metadata.value`) or stack trace context to identify invalid array index and the expected vs actual array size.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

## Diagnosis

1. Analyze the stack trace frames from the most recent event (`entries[].data.values[].stacktrace.frames[]`) and error message (`metadata.value`) to identify the exact code location, the index value attempted, and the list or array being accessed. If the stack trace shows the error originates from accessing elements in external API responses or database query results, the issue is likely data-dependent with unexpected empty or short collections. If the stack trace shows hardcoded index access, the issue is likely a code assumption error.

2. Compare the event's `firstSeen` timestamp with `firstRelease` deployment time from issue details. If the IndexError first appeared within 30 minutes after a release deployment, the root cause is likely a code change that introduced incorrect index calculations, changed expected array structures, or removed boundary checks. If the error predates recent releases, investigate data source changes or upstream modifications that affect collection sizes.

3. Examine event frequency patterns and affected data contexts from event data. If errors occur consistently across all users since a specific timestamp, a code or configuration change is the likely cause. If errors are intermittent and correlate with specific data patterns, the issue relates to edge cases such as empty result sets, single-element collections accessed with higher indices, or variable-length data where the code assumes fixed-size arrays.
