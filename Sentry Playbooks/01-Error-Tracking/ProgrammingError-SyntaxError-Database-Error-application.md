# ProgrammingError-SyntaxError-Database-Error-application

## Meaning

Database programming error occurs (triggering Sentry error issue with exception type ProgrammingError) because SQL syntax error exists in database query, causing SQL queries to fail when executing malformed or invalid SQL statements. Error events display in Sentry Issue Details page with error message patterns "syntax error", "SQL syntax", stack traces show database execution layer (sentry/db/postgres/base.py or similar), and error levels indicate Error or Fatal severity. This affects the database layer and indicates SQL query construction issues typically caused by incorrect query syntax, parameter binding errors, or SQL generation bugs; database queries fail.

## Impact

Sentry error issue alerts fire; database queries fail; applications return database errors; users affected; issues remain in New or Ongoing status; error levels show Error or Fatal severity; stack traces indicate database execution failures; error events display in Sentry Issue Details page. Database operations fail; affected user count grows; error count increases continuously; issues show High priority in Sentry dashboard; application functionality degrades; data access operations fail. Database errors increase; database queries cannot execute.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify ProgrammingError with "syntax error" or "SQL syntax" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected database files
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract SQL query from error message (`metadata.value`) or stack trace context to identify malformed SQL statement causing syntax error.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. If `firstRelease.lastCommit` is populated, extract repository name from `firstRelease.versionInfo.package` or use service mapping, then retrieve GitHub commit details and check if commit is in PR. If PR found, retrieve PR diff to analyze SQL query or ORM code changes.

6. Search ELK logs around the error timestamp for:
   - Database query logs showing the full SQL statement that failed
   - ORM/SQLAlchemy debug logs that may show query construction details
   - Application logs with request context to identify the input that triggered the malformed query
   - Database connection logs showing query execution attempts

7. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

8. List tags for issue `<issue-id>` to check for additional context such as environment, deployment, or database-related tags that may provide insights into the syntax error.

## Diagnosis

1. Analyze error event patterns from Playbook step 2 to identify the error trend. If events show sudden spike correlating with deployment, this indicates deployment-related SQL query change with syntax error. If errors are constant, this indicates persistent malformed query in code. If errors are intermittent, this indicates specific input parameters or data patterns triggering malformed SQL generation.

2. If error spike correlates with deployment (from Playbook step 4 release timeline), compare `firstRelease` timestamp with error onset to confirm deployment as trigger. If `firstRelease` and `lastRelease` differ, analyze whether syntax errors started with initial release or appeared with subsequent releases.

3. If `firstRelease.lastCommit` is populated and events indicate code-related issue (from Playbook step 5), analyze GitHub commit changes to identify specific SQL query modifications, ORM query builder changes, or raw SQL additions containing syntax errors.

4. If stack trace shows dynamic query generation or events indicate parameter-dependent errors, search ELK logs (from Playbook step 6) for correlated database query logs showing the full malformed SQL statement, request context, or input parameters triggering the syntax error around the error timestamps from Sentry events.

5. If no clear deployment correlation, analyze affected user patterns from Playbook step 2 event data. If all users affected, likely static SQL syntax error in code. If specific segments affected, likely dynamic query construction issue with specific input patterns.

6. If similar issues exist (from Playbook step 7) with shared release timestamps, this indicates broader deployment incident where SQL query changes were deployed without proper testing.
