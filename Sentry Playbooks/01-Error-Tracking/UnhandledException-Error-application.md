# UnhandledException-Error-application

## Meaning

Unhandled exception occurs (triggering Sentry error issue) because application code raises an exception that is not caught by exception handlers, causing application operations to fail when unexpected errors occur during execution. Error events display in Sentry Issue Details page with various exception types, stack traces show application code layers, and error levels indicate Error or Fatal severity. This affects the application layer and indicates application code issues typically caused by unhandled error conditions, missing exception handling, or unexpected runtime errors; application operations fail.

## Impact

Sentry error issue alerts fire; unhandled exceptions occur; application operations fail; applications return errors; users affected; issues remain in New or Ongoing status; error levels show Error or Fatal severity; stack traces indicate unhandled exception failures; error events display in Sentry Issue Details page. Application functionality degrades; affected user count grows; error count increases continuously; issues show High or Medium priority in Sentry dashboard; user-facing errors occur; application crashes may occur. Application errors increase; exception handling gaps exist.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify unhandled exception type and error pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected application files and exception location
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract exception details from error message (`metadata.value`) and stack trace including exception type, error message, and file location to identify root cause.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. If `firstRelease.lastCommit` is populated, extract repository name from `firstRelease.versionInfo.package` or use service mapping, then retrieve GitHub commit details and check if commit is in PR. If PR found, retrieve PR diff to analyze code changes that may have introduced the exception.

6. If error context from Sentry is insufficient, search ELK logs for service around error timestamp to identify application logs, exception context, and runtime conditions leading to the unhandled exception.

7. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

## Diagnosis

1. Analyze error event patterns from Playbook step 2 to identify the error trend. If events show sudden spike correlating with deployment, this indicates deployment-related code change introducing the exception. If errors are constant, this indicates persistent code logic issue or edge case not handled. If errors are intermittent, this indicates specific input data or user actions triggering the exception.

2. If error spike correlates with deployment (from Playbook step 4 release timeline), compare `firstRelease` timestamp with error onset to confirm deployment as trigger. If `firstRelease` and `lastRelease` differ, analyze whether unhandled exceptions started with initial release or increased with subsequent releases.

3. If `firstRelease.lastCommit` is populated and events indicate code-related issue (from Playbook step 5), analyze GitHub commit changes to identify specific code modifications, missing null checks, or exception handling gaps causing the unhandled exception.

4. If stack trace shows external dependency interactions or events indicate runtime condition issues, search ELK logs (from Playbook step 6) for correlated request context, input parameters, or environmental conditions triggering the exception around the error timestamps from Sentry events.

5. If no clear deployment correlation, analyze affected user patterns from Playbook step 2 event data. If all users affected, likely fundamental code logic issue. If specific segments affected, likely specific input patterns, user permissions, or data conditions triggering the exception.

6. If similar issues exist (from Playbook step 7) with shared release timestamps, this indicates broader deployment incident where code changes were deployed without proper exception handling or testing.
