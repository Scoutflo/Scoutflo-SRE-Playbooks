# AttributeError-MissingAttribute-Error-application

## Meaning

Missing attribute error occurs (triggering Sentry error issue with exception type AttributeError) because application attempts to access non-existent attribute, causing application operations to fail when object does not have expected attribute. Error events display in Sentry Issue Details page with error message patterns "attribute error", "has no attribute", stack traces show application code layers, and error levels indicate Error or Warning severity. This affects the application layer and indicates object attribute issues typically caused by missing object attributes, incorrect object types, or attribute access errors; application operations fail; if errors correlate with code changes, object structure problems may be visible in code modification history.

## Impact

Sentry error issue alerts fire; missing attribute errors occur; application operations fail; applications return attribute errors; users affected; issues remain in New or Ongoing status; error levels show Error or Warning severity; stack traces indicate attribute access failures; error events display in Sentry Issue Details page. Object attribute access fails; affected user count grows; error count increases continuously; issues show Medium or Low priority in Sentry dashboard; application functionality degrades; attribute errors occur. Attribute errors increase; object structure problems occur; if errors correlate with code changes, object structure problems may cause application failures.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify AttributeError with "attribute error" or "has no attribute" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected application files and attribute access location
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract attribute name from error message (`metadata.value`) matching pattern "has no attribute [attribute_name]" to identify missing object attribute and the object type that should have it.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

## Diagnosis

1. Analyze the stack trace frames from the most recent event (`entries[].data.values[].stacktrace.frames[]`) and error message (`metadata.value`) matching pattern "has no attribute [attribute_name]" to identify the object type and missing attribute. If the stack trace shows the error originates from accessing attributes on external API response objects or deserialized data, the issue is likely data structure changes. If the stack trace shows direct class method or property access, the issue is likely a code refactoring error or incorrect object type.

2. Compare the event's `firstSeen` timestamp with `firstRelease` deployment time from issue details. If the AttributeError first appeared within 30 minutes after a release deployment, the root cause is likely a code change that removed or renamed an attribute, changed class inheritance, or modified object initialization. If the error predates recent releases, investigate dependency updates, external API changes, or data model modifications.

3. Examine event frequency patterns and affected code paths from event data. If errors occur consistently across all users and code paths since a specific timestamp, a code or dependency change is the likely cause. If errors are intermittent and occur only in specific code branches, the issue correlates with conditional object creation paths, None object access, or polymorphic type mismatches where different object types are used interchangeably.