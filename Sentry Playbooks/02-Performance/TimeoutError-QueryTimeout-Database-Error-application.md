# TimeoutError-QueryTimeout-Database-Error-application

## Meaning

Database query timeout error occurs (triggering Sentry error issue with exception type TimeoutError) because database query execution times out, causing database operations to fail when attempting to execute long-running queries within timeout period. Error events display in Sentry Issue Details page with error message patterns "query timeout", "database timeout", stack traces show database execution layer (sentry/db/postgres/base.py or similar), and error levels indicate Error or Fatal severity. This affects the database layer and indicates database performance issues typically caused by slow queries, database server overload, or query timeout configuration problems; database operations fail.

## Impact

Sentry error issue alerts fire; database query timeouts occur; database operations fail; applications return database errors; users affected; issues remain in New or Ongoing status; error levels show Error or Fatal severity; stack traces indicate database query timeout failures; error events display in Sentry Issue Details page. Database query performance degrades; affected user count grows; error count increases continuously; issues show High or Medium priority in Sentry dashboard; application functionality degrades; response times increase. Database errors increase; slow queries accumulate.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify TimeoutError with "query timeout" or "database timeout" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected database files
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract database query details from error message (`metadata.value`) or stack trace context including table name and timeout duration to identify slow-running query.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. If `firstRelease.lastCommit` is populated, extract repository name from `firstRelease.versionInfo.package` or use service mapping, then retrieve GitHub commit details and check if commit is in PR. If PR found, retrieve PR diff to analyze database query or timeout setting changes.

6. If error context from Sentry is insufficient, search ELK logs for service around error timestamp to identify slow query logs, database performance issues, and query execution patterns.

7. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

## Diagnosis

1. Analyze error event patterns from Playbook step 2 to identify the error trend. If events show sudden spike correlating with deployment, this indicates deployment-related query change or timeout configuration modification. If errors are constant, this indicates persistent slow query or inefficient query logic. If errors are intermittent, this indicates load-dependent query performance or database contention issues.

2. If error spike correlates with deployment (from Playbook step 4 release timeline), compare `firstRelease` timestamp with error onset to confirm deployment as trigger. If `firstRelease` and `lastRelease` differ, analyze whether query timeout errors started with initial release or increased with subsequent releases.

3. If `firstRelease.lastCommit` is populated and events indicate code-related issue (from Playbook step 5), analyze GitHub commit changes to identify specific query modifications, missing indexes, or inefficient ORM queries causing slow performance.

4. If events indicate infrastructure dependency issues (database overload, query contention from Playbook step 3), search ELK logs (from Playbook step 6) for correlated slow query logs, database CPU/memory spikes, or lock contention events around the error timestamps from Sentry events.

5. If no clear deployment or infrastructure correlation, analyze affected user patterns from Playbook step 2 event data. If all users affected, likely database-wide performance issue or missing index. If specific segments affected, likely specific query or data patterns causing slow performance.

6. If similar issues exist (from Playbook step 7) with shared release timestamps, this indicates broader deployment incident where query changes were deployed without proper performance testing.
