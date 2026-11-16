# SNS Delivery Failures

## Meaning

Messages published to an SNS topic do not reach subscribers: the `NumberOfNotificationsFailed` metric rises, subscribers see no messages, or messages arrive late or only for some subscriptions. Common causes: a subscription filter policy that excludes the messages, a pending (unconfirmed) or deleted subscription, an SQS queue or Lambda function whose access policy does not allow `sns.amazonaws.com` to deliver, an encrypted topic or queue whose KMS key policy blocks SNS, an HTTP/S endpoint that is down or returns errors, or throttling at the endpoint.

## Impact

Alerts, notifications and event-driven workflows silently stop. If SNS carries alarm notifications, incidents go unnoticed. Failed deliveries can be lost after retries unless a subscription dead-letter queue is configured.

## Playbook

### For AI Agents (NLP)

1. Retrieve topic `<topic-arn>` attributes and list its subscriptions in region `<region>`, noting each protocol, endpoint and whether the subscription is confirmed.
2. Retrieve CloudWatch metrics for the topic over the last 6 hours: `NumberOfMessagesPublished`, `NumberOfNotificationsDelivered`, `NumberOfNotificationsFailed`, and `NumberOfNotificationsFilteredOut`, to see whether messages are failing, filtered out, or never published.
3. For each failing subscription, read its attributes: `FilterPolicy`, `RedrivePolicy`, `PendingConfirmation`, and delivery policy.
4. For SQS or Lambda subscribers, verify the target resource policy allows `sns.amazonaws.com` with a `SourceArn` condition matching `<topic-arn>`.
5. If topic, queue or function uses KMS encryption, verify the key policy allows SNS to use the key.
6. For HTTP/S endpoints, test the endpoint directly and check its response codes and TLS certificate.
7. Check whether the subscription has a dead-letter queue and inspect it for undelivered messages and error details.
8. Fix the specific cause (policy, filter, confirmation, endpoint) with approval and confirm delivery by publishing a test message to a non-production topic or with a clearly marked test payload.

### For DevOps/SREs (CLI)

1. List the topic's attributes and subscriptions:
   ```bash
   aws sns get-topic-attributes --topic-arn <topic-arn> --profile <profile> --region <region>
   aws sns list-subscriptions-by-topic --topic-arn <topic-arn> --profile <profile> --region <region>
   ```

2. Inspect one subscription (filter policy, redrive policy, pending confirmation):
   ```bash
   aws sns get-subscription-attributes --subscription-arn <subscription-arn> --profile <profile> --region <region>
   ```

3. Check delivered, failed and filtered counts over the last 6 hours:
   ```bash
   START=$(date -u -d '6 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-6H +%Y-%m-%dT%H:%M:%SZ)
   END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
   for m in NumberOfMessagesPublished NumberOfNotificationsDelivered NumberOfNotificationsFailed NumberOfNotificationsFilteredOut; do
     echo "== $m"
     aws cloudwatch get-metric-statistics --namespace AWS/SNS --metric-name $m \
       --dimensions Name=TopicName,Value=<topic-name> --start-time "$START" --end-time "$END" \
       --period 3600 --statistics Sum --profile <profile> --region <region> \
       --query 'Datapoints[].[Timestamp,Sum]' --output text
   done
   ```

4. For an SQS subscriber, check the queue policy allows SNS:
   ```bash
   aws sqs get-queue-attributes --queue-url <queue-url> --attribute-names Policy KmsMasterKeyId \
     --profile <profile> --region <region>
   ```

5. For a Lambda subscriber, check the function's resource policy:
   ```bash
   aws lambda get-policy --function-name <function-name> --profile <profile> --region <region>
   ```

6. Check delivery failure logs, if delivery status logging is enabled for the topic:
   ```bash
   aws logs filter-log-events --log-group-name "sns/<region>/<account-id>/<topic-name>/Failure" \
     --limit 20 --profile <profile> --region <region>
   ```

## Diagnosis

1. If `NumberOfNotificationsFilteredOut` is high and delivered is low, the subscription filter policy is excluding messages: compare the policy with the message attributes (or body, for payload-based filtering) being published.
2. If `PendingConfirmation` is `true`, the subscriber never confirmed: re-send or re-create the subscription and confirm it.
3. If `NumberOfNotificationsFailed` rises for an SQS or Lambda subscriber and the target's resource policy lacks SNS with the right `SourceArn`, add it; if a KMS key is involved, allow SNS in the key policy.
4. If failures are only for an HTTP/S endpoint, the endpoint is down, slow or erroring: check its status, certificate and response codes in the delivery failure logs.
5. If published count itself is zero, the producer is not publishing or lacks `sns:Publish` permission: investigate the producer.
6. If messages are lost after retries and no subscription DLQ exists, configure a DLQ on the subscription so failed messages can be inspected and replayed.

Inline references:
- [Amazon SNS troubleshooting](https://docs.aws.amazon.com/sns/latest/dg/sns-troubleshooting.html)
- [SNS message filtering](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html)
