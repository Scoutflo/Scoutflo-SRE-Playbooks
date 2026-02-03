# ConnectionError-ConnectionRefused-Database-Error-application

## Meaning

Database connection error occurs (triggering Sentry error issue with exception type ConnectionError) because database server connection is refused, causing database operations to fail when attempting to connect to database server. Error events display in Sentry Issue Details page with error message patterns "connection refused", "cannot connect to database", stack traces show database connection layer (sentry/db/postgres/base.py or similar), and error levels indicate Error or Fatal severity. This affects the database layer and indicates database connectivity issues typically caused by database service down, network connectivity problems, or database configuration errors; database operations fail.

## Impact

Sentry error issue alerts fire; database connection fails; database operations fail; applications return database errors; users affected; issues remain in New or Ongoing status; error levels show Error or Fatal severity; stack traces indicate connection failures; error events display in Sentry Issue Details page. Database unavailability causes complete application failure; affected user count grows; error count increases continuously; issues show High priority in Sentry dashboard; application functionality degrades completely. Database errors increase; all database-dependent operations fail.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify ConnectionError with "connection refused" pattern and database component (filename contains "db", "postgres", "mysql", "database").

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected database connection files
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract database connection details from error message (`metadata.value`) including host, port, and database name to identify target database instance.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. If `firstRelease.lastCommit` is populated, extract repository name from `firstRelease.versionInfo.package` or use service mapping, then retrieve GitHub commit details and check if commit is in PR. If PR found, retrieve PR diff to analyze database configuration changes.

6. If error context from Sentry is insufficient, search ELK logs for service around error timestamp to identify database connection attempts, connection failures, and network errors.

7. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

8. List tags for issue `<issue-id>` to check for additional context such as environment, deployment, or database-related tags that may provide insights into the connection issue.

## Diagnosis

1. Analyze error event patterns from Playbook step 2 to identify the error trend. If events show sudden spike correlating with deployment, this indicates deployment-related configuration change. If errors are constant, this indicates persistent database service down or unreachable. If errors are intermittent, this indicates network connectivity or database availability issues.

2. If error spike correlates with deployment (from Playbook step 4 release timeline), compare `firstRelease` timestamp with error onset to confirm deployment as trigger. If `firstRelease` and `lastRelease` differ, analyze whether connection errors started with initial release or increased with subsequent releases.

3. If `firstRelease.lastCommit` is populated and events indicate code-related issue (from Playbook step 5), analyze GitHub commit changes to identify specific database connection string changes, host/port configuration modifications, or connection pool settings causing the error.

4. If events indicate infrastructure dependency issues (connection refused, service unavailable from Playbook step 3), search ELK logs (from Playbook step 6) for correlated database service failures, network connectivity errors, or database restart events around the error timestamps from Sentry events.

5. If no clear deployment or infrastructure correlation, analyze affected user patterns from Playbook step 2 event data. If all users affected, likely database service completely down. If specific segments affected, likely connection pool exhaustion or regional network issue.

6. If similar issues exist (from Playbook step 7) with shared release timestamps, this indicates broader deployment incident affecting database connectivity across multiple services.
