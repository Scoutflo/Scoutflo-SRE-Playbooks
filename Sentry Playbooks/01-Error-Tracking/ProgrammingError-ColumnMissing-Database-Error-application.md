# ProgrammingError-ColumnMissing-Database-Error-application

## Meaning

Database programming error occurs (triggering Sentry error issue with exception type ProgrammingError) because database schema column is missing from the table, causing SQL queries to fail when attempting to access non-existent columns. Error events display in Sentry Issue Details page with error message patterns "column does not exist", stack traces show database execution layer (sentry/db/postgres/base.py or similar), and error levels indicate Error or Fatal severity. This affects the database layer and indicates database schema issues typically caused by missing migrations, incomplete schema updates, or database synchronization failures; database queries fail.

## Impact

Sentry error issue alerts fire; database queries fail; applications return database errors; users affected; issues remain in New or Ongoing status; error levels show Error or Fatal severity; stack traces indicate database execution failures; error events display in Sentry Issue Details page. Database operations fail; affected user count grows; error count increases continuously; issues show High priority in Sentry dashboard; application functionality degrades; data access operations fail. Database errors increase; database queries cannot complete.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify ProgrammingError with "column does not exist" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected database files
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract column name from error message (`metadata.value`) matching pattern "column [column_name] does not exist" and table name from stack trace or error context to identify missing database schema element.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. If `firstRelease.lastCommit` is populated, extract repository name from `firstRelease.versionInfo.package` or use service mapping, then retrieve GitHub commit details and check if commit is in PR. If PR found, retrieve PR diff to analyze database migration or schema changes.

6. Search ELK logs around the error timestamp for:
   - Database migration execution logs (search for "migrate", "alembic", "flyway", or your migration tool)
   - Application startup logs that may indicate schema initialization failures
   - Database connection or query logs showing the failing SQL statement
   - Deployment logs that may show incomplete migration runs

7. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

8. List tags for issue `<issue-id>` to check for additional context such as environment, deployment, or database-related tags that may provide insights into the schema mismatch.

## Diagnosis

1. Analyze error event patterns from Playbook step 2 to identify the error trend. If events show sudden spike correlating with deployment, this indicates deployment-related schema change without corresponding migration. If errors are constant, this indicates persistent schema mismatch. If errors are intermittent, this indicates partial migration rollout or environment-specific schema differences.

2. If error spike correlates with deployment (from Playbook step 4 release timeline), compare `firstRelease` timestamp with error onset to confirm deployment as trigger. If `firstRelease` and `lastRelease` differ, analyze whether schema errors started with initial release or appeared with subsequent releases.

3. If `firstRelease.lastCommit` is populated and events indicate code-related issue (from Playbook step 5), analyze GitHub commit changes to identify specific database model changes, ORM field additions, or query modifications referencing missing columns without corresponding migration files.

4. If stack trace shows migration-related code or events indicate migration timing issues, search ELK logs (from Playbook step 6) for correlated migration execution logs, migration failures, or database schema initialization errors around the error timestamps from Sentry events.

5. If no clear deployment correlation, analyze affected user patterns from Playbook step 2 event data. If all users affected, likely missing migration in deployment pipeline. If specific segments affected, likely environment-specific schema drift or partial migration execution.

6. If similar issues exist (from Playbook step 7) with shared release timestamps, this indicates broader deployment incident where migration was not applied before application code deployment.
