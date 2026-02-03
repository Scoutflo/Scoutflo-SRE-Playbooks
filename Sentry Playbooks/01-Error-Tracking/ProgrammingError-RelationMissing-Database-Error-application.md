# ProgrammingError-RelationMissing-Database-Error-application

## Meaning

Database programming error occurs (triggering Sentry error issue with exception type ProgrammingError) because database table or relation is missing from the database schema, causing SQL queries to fail when attempting to access non-existent tables. Error events display in Sentry Issue Details page with error message patterns "relation does not exist", stack traces show database execution layer (sentry/db/postgres/base.py or similar), and error levels indicate Error or Fatal severity. This affects the database layer and indicates database schema issues typically caused by missing migrations, incomplete schema deployments, or database synchronization failures; database queries fail.

## Impact

Sentry error issue alerts fire; database queries fail; applications return database errors; users affected; issues remain in New or Ongoing status; error levels show Error or Fatal severity; stack traces indicate database execution failures; error events display in Sentry Issue Details page. Database operations fail; affected user count grows; error count increases continuously; issues show High priority in Sentry dashboard; application functionality degrades; data access operations fail completely. Database errors increase; database queries cannot execute.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify ProgrammingError with "relation does not exist" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected database files
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract table name from error message (`metadata.value`) matching pattern "relation [table_name] does not exist" to identify missing database table or relation.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. If `firstRelease.lastCommit` is populated, extract repository name from `firstRelease.versionInfo.package` or use service mapping, then retrieve GitHub commit details and check if commit is in PR. If PR found, retrieve PR diff to analyze database migration or schema changes.

6. Search ELK logs around the error timestamp for:
   - Database migration execution logs (search for "migrate", "CREATE TABLE", or schema creation commands)
   - Application startup logs showing database initialization or migration status
   - Deployment logs that may show migration failures or timeouts
   - Database replication logs if tables should be synced from another database

7. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

8. List tags for issue `<issue-id>` to check for additional context such as environment, deployment, or database-related tags that may provide insights into the schema mismatch.

## Diagnosis

1. Analyze error event patterns from Playbook step 2 to identify the error trend. If events show sudden spike correlating with deployment, this indicates deployment-related code referencing non-existent table. If errors are constant, this indicates persistent missing table or migration never applied. If errors are intermittent, this indicates partial migration rollout or environment-specific schema differences.

2. If error spike correlates with deployment (from Playbook step 4 release timeline), compare `firstRelease` timestamp with error onset to confirm deployment as trigger. If `firstRelease` and `lastRelease` differ, analyze whether schema errors started with initial release or appeared with subsequent releases.

3. If `firstRelease.lastCommit` is populated and events indicate code-related issue (from Playbook step 5), analyze GitHub commit changes to identify specific new table references, ORM model additions, or query modifications referencing tables without corresponding migration files creating those tables.

4. If stack trace shows migration-related code or events indicate migration timing issues, search ELK logs (from Playbook step 6) for correlated migration execution logs, CREATE TABLE failures, or database initialization errors around the error timestamps from Sentry events.

5. If no clear deployment correlation, analyze affected user patterns from Playbook step 2 event data. If all users affected, likely missing migration in deployment pipeline. If specific segments affected, likely environment-specific schema drift or database replication lag.

6. If similar issues exist (from Playbook step 7) with shared release timestamps, this indicates broader deployment incident where application code was deployed before database migration creating required tables.
