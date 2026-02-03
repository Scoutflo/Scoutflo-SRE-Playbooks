# ProgrammingError-ConstraintViolation-Database-Error-application

## Meaning

Database programming error occurs (triggering Sentry error issue with exception type ProgrammingError) because database constraint violation exists, causing SQL operations to fail when attempting to insert or update data that violates database constraints such as foreign keys, unique constraints, or check constraints. Error events display in Sentry Issue Details page with error message patterns "constraint violation", "foreign key", "unique constraint", stack traces show database execution layer (sentry/db/postgres/base.py or similar), and error levels indicate Error or Fatal severity. This affects the database layer and indicates data integrity issues typically caused by invalid data relationships, duplicate key violations, or constraint enforcement failures; database operations fail.

## Impact

Sentry error issue alerts fire; database operations fail; data integrity violations occur; users affected; issues remain in New or Ongoing status; error levels show Error or Fatal severity; stack traces indicate database constraint failures; error events display in Sentry Issue Details page. Database write operations fail; affected user count grows; error count increases continuously; issues show High priority in Sentry dashboard; application functionality degrades; data consistency problems occur. Database errors increase; data operations cannot complete.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify ProgrammingError with "constraint violation", "foreign key", or "unique constraint" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected database files
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract constraint details from error message (`metadata.value`) including constraint name, table name, and constraint type (foreign key, unique, check) to identify violated database constraint.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. If `firstRelease.lastCommit` is populated, extract repository name from `firstRelease.versionInfo.package` or use service mapping, then retrieve GitHub commit details and check if commit is in PR. If PR found, retrieve PR diff to analyze database constraint or data model changes.

6. Search ELK logs around the error timestamp for:
   - Database constraint modification logs (search for "ALTER TABLE", "ADD CONSTRAINT", or DDL operations)
   - Batch import or data migration logs that may have introduced violating data
   - Application logs showing the data values that caused the constraint violation
   - Database replication or sync logs if data comes from external sources

7. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

8. List tags for issue `<issue-id>` to check for additional context such as environment, deployment, or database-related tags that may provide insights into the constraint violation.

## Diagnosis

1. Analyze error event patterns from Playbook step 2 to identify the error trend. If events show sudden spike correlating with deployment, this indicates deployment-related code change violating existing constraints. If errors are constant, this indicates persistent data integrity issue in application logic. If errors are intermittent, this indicates specific user data or input patterns triggering constraint violations.

2. If error spike correlates with deployment (from Playbook step 4 release timeline), compare `firstRelease` timestamp with error onset to confirm deployment as trigger. If `firstRelease` and `lastRelease` differ, analyze whether constraint errors started with initial release or appeared with subsequent releases.

3. If `firstRelease.lastCommit` is populated and events indicate code-related issue (from Playbook step 5), analyze GitHub commit changes to identify specific data model changes, insert/update logic modifications, or constraint additions that cause the violation.

4. If stack trace shows batch import or data migration code, or events indicate external data source issues, search ELK logs (from Playbook step 6) for correlated batch import logs, data migration execution, or external data sync operations around the error timestamps from Sentry events.

5. If no clear deployment correlation, analyze affected user patterns from Playbook step 2 event data. If all users affected, likely application logic issue with data validation. If specific segments affected, likely specific data patterns or user inputs triggering constraint violations.

6. If similar issues exist (from Playbook step 7) with shared release timestamps, this indicates broader deployment incident where new constraint was added without data cleanup or code was deployed without proper data validation.
