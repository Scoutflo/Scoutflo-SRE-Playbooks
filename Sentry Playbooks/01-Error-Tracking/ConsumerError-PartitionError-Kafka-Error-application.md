# ConsumerError-PartitionError-Kafka-Error-application

## Meaning

Kafka consumer error occurs (triggering Sentry error issue with exception type ConsumerError) because Kafka partition error exists, causing event processing and message queue operations to fail when attempting to consume from unavailable or misconfigured partitions. Error events display in Sentry Issue Details page with error message patterns "partition", "partition error", "partition not found", stack traces show Kafka consumer layer (sentry/utils/kafka.py or sentry/consumers/synchronized.py), and error levels indicate Error or Fatal severity. This affects the message queue and event processing layer and indicates Kafka partition configuration issues typically caused by partition deletion, partition rebalancing, or Kafka broker configuration problems; event processing fails.

## Impact

Sentry error issue alerts fire; Kafka consumer operations fail; event processing stops; message queue operations fail; users affected; issues remain in New or Ongoing status; error levels show Error or Fatal severity; stack traces indicate Kafka partition failures; error events display in Sentry Issue Details page. Event processing pipeline breaks; downstream services affected; affected user count grows; error count increases continuously; issues show High priority in Sentry dashboard; application functionality degrades. Kafka errors increase; event backlog forms; data pipeline interruptions occur.

## Playbook

1. Inspect available issue details including issue type (`metadata.type`), priority (`priority`), affected users (`userCount`), and error message (`metadata.value`) to verify ConsumerError with "partition", "partition error", or "partition not found" pattern.

2. List events for issue `<issue-id>` and analyze event patterns:
   - Retrieve most recent event to inspect stack trace frames (`entries[].data.values[].stacktrace.frames[]`) and identify affected Kafka consumer files
   - Analyze event frequency over last 24 hours (constant, spike, gradual increase) and check user impact distribution (all users vs specific segments) from event data

3. Extract Kafka partition details from error message (`metadata.value`) including topic name and partition number to identify affected partition.

4. Compare release timeline from issue details (firstRelease vs lastRelease if available) to check if issue correlates with deployments.

5. If `firstRelease.lastCommit` is populated, extract repository name from `firstRelease.versionInfo.package` or use service mapping, then retrieve GitHub commit details and check if commit is in PR. If PR found, retrieve PR diff to analyze Kafka partition configuration changes.

6. If error context from Sentry is insufficient, search ELK logs for service around error timestamp to identify Kafka consumer logs, partition assignment errors, and broker connection issues.

7. List similar issues for project `<project-name>` and check if they share common release or deployment timestamps to identify broader incidents.

8. List tags for issue `<issue-id>` to check for additional context such as environment, deployment, or Kafka-related tags that may provide insights into the partition issue.

## Diagnosis

1. Analyze error event patterns from Playbook step 2 to identify the error trend. If events show sudden spike correlating with deployment, this indicates deployment-related partition configuration change. If errors are constant, this indicates persistent partition missing or deleted. If errors are intermittent, this indicates partition rebalancing or broker availability issues.

2. If error spike correlates with deployment (from Playbook step 4 release timeline), compare `firstRelease` timestamp with error onset to confirm deployment as trigger. If `firstRelease` and `lastRelease` differ, analyze whether partition errors started with initial release or appeared with subsequent releases.

3. If `firstRelease.lastCommit` is populated and events indicate code-related issue (from Playbook step 5), analyze GitHub commit changes to identify specific Kafka partition configuration changes, topic subscription modifications, or consumer group assignment changes causing the error.

4. If events indicate infrastructure dependency issues (partition not found, broker unavailable from Playbook step 3), search ELK logs (from Playbook step 6) for correlated Kafka partition deletion events, partition rebalancing operations, or broker configuration changes around the error timestamps from Sentry events.

5. If no clear deployment or infrastructure correlation, analyze affected user patterns from Playbook step 2 event data. If all users affected, likely cluster-wide partition issue. If specific segments affected, likely consumer group or partition assignment configuration issue.

6. If similar issues exist (from Playbook step 7) with shared release timestamps, this indicates broader deployment incident affecting Kafka partition configuration across multiple services.
