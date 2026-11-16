# SQS Queue Backlog and Dead-Letter Queue Growth

## Meaning

The number of visible messages (`ApproximateNumberOfMessagesVisible`) or the age of the oldest message (`ApproximateAgeOfOldestMessage`) in an SQS queue keeps rising, or messages are accumulating in its dead-letter queue (DLQ). Consumers (Lambda, ECS/EKS workers, EC2) are not keeping up or are failing: messages are received but not deleted, the visibility timeout is shorter than processing time so messages reappear, handlers throw errors until `maxReceiveCount` sends them to the DLQ, Lambda concurrency or event-source scaling is throttled, or producers suddenly send more than usual.

## Impact

Delayed processing of orders, events or jobs, growing latency for downstream systems, and risk of data loss if messages expire before they are processed (retention period) or DLQ messages are never replayed. A DLQ that fills silently hides failures.

## Playbook

### For AI Agents (NLP)

1. Retrieve the queue attributes for `<queue-url>` and its DLQ in region `<region>`: visible, in-flight and delayed message counts, `VisibilityTimeout`, `MessageRetentionPeriod` and the `RedrivePolicy` (`maxReceiveCount`, DLQ ARN).
2. Retrieve CloudWatch metrics for the last 6 hours for the queue: `NumberOfMessagesSent`, `NumberOfMessagesReceived`, `NumberOfMessagesDeleted`, `ApproximateNumberOfMessagesVisible`, `ApproximateAgeOfOldestMessage`, and DLQ visible messages, to decide whether the problem is producer surge, slow consumers, or failing consumers.
3. Identify the consumer (Lambda event source mapping, ECS/EKS service, EC2 workers) and check its health, error rate, throttles/concurrency and recent deployments.
4. Compare consumer processing time with the queue `VisibilityTimeout`; if processing exceeds it, messages become visible again and are processed repeatedly.
5. Sample a few messages from the DLQ without deleting them, and read the consumer logs for the matching errors to find the failure cause.
6. For Lambda consumers, check the event source mapping state, batch size, maximum concurrency and function throttles/reserved concurrency.
7. After the cause is fixed, redrive DLQ messages back to the source queue (state-changing, needs approval) and watch the backlog drain.

### For DevOps/SREs (CLI)

1. Get queue attributes (replace the queue URL; look up with `aws sqs get-queue-url --queue-name <queue-name>`):
   ```bash
   aws sqs get-queue-attributes --queue-url <queue-url> --attribute-names All \
     --profile <profile> --region <region>
   ```

2. Find the DLQ and its depth:
   ```bash
   aws sqs list-dead-letter-source-queues --queue-url <dlq-url> --profile <profile> --region <region>
   aws sqs get-queue-attributes --queue-url <dlq-url> \
     --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible \
     --profile <profile> --region <region>
   ```

3. Check backlog age over the last 6 hours (portable time bounds):
   ```bash
   START=$(date -u -d '6 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-6H +%Y-%m-%dT%H:%M:%SZ)
   END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
   aws cloudwatch get-metric-statistics --namespace AWS/SQS --metric-name ApproximateAgeOfOldestMessage \
     --dimensions Name=QueueName,Value=<queue-name> --start-time "$START" --end-time "$END" \
     --period 300 --statistics Maximum --profile <profile> --region <region>
   ```

4. Check Lambda consumers (event source mappings and throttles):
   ```bash
   aws lambda list-event-source-mappings --function-name <function-name> --profile <profile> --region <region>
   aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Throttles \
     --dimensions Name=FunctionName,Value=<function-name> --start-time "$START" --end-time "$END" \
     --period 300 --statistics Sum --profile <profile> --region <region>
   ```

5. Peek at DLQ messages without deleting them (they return after the short visibility timeout):
   ```bash
   aws sqs receive-message --queue-url <dlq-url> --max-number-of-messages 5 \
     --visibility-timeout 5 --attribute-names All --message-attribute-names All \
     --profile <profile> --region <region>
   ```

6. After fixing the consumer, redrive the DLQ to its source (state-changing, needs approval):
   ```bash
   aws sqs start-message-move-task --source-arn <dlq-arn> --profile <profile> --region <region>
   aws sqs list-message-move-tasks --source-arn <dlq-arn> --profile <profile> --region <region>
   ```

## Diagnosis

1. If `NumberOfMessagesSent` jumped while consumer throughput is flat, a producer surge is the cause: scale consumers or throttle the producer.
2. If messages are received but `NumberOfMessagesDeleted` is much lower, consumers are failing or timing out: read their logs and fix the handler error before anything else.
3. If processing time exceeds `VisibilityTimeout`, messages reappear and are duplicated or sent to the DLQ: raise the visibility timeout above the worst-case processing time (for Lambda, at least six times the function timeout).
4. If a Lambda consumer shows throttles or the mapping is disabled/erroring, fix concurrency limits or re-enable the mapping.
5. If the DLQ grows only for specific messages, they are poison messages (bad payload): fix the handler or discard after review; redrive only after the fix.
6. If `ApproximateAgeOfOldestMessage` approaches `MessageRetentionPeriod`, messages are about to be lost: increase retention immediately and prioritise draining.

Inline references:
- [Amazon SQS dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
- [DLQ redrive](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html)
