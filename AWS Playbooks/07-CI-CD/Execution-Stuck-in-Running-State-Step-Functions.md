# AWS Step Functions Execution Stuck in Running State

## Meaning

AWS Step Functions execution is stuck in running state (triggering workflow failures or StepFunctionsExecutionStuck alarms) because execution is waiting for task token, Lambda function timeout prevents completion, state machine definition has errors, execution input is invalid, Step Functions service encounters errors during execution, or Step Functions execution time limit is exceeded. Step Functions executions are stuck, workflow automation is blocked, and execution state transitions fail. This affects the workflow orchestration and serverless layer and blocks workflow execution, typically caused by state machine definition issues, Lambda function problems, or task token failures; if using Step Functions with Express workflows vs Standard workflows, execution behavior differs and applications may experience execution delays.

## Impact

Step Functions executions are stuck; workflow automation is blocked; execution state transitions fail; workflow processes cannot complete; execution automation is ineffective; state machine executions hang; workflow reliability is compromised; execution monitoring shows stuck states. StepFunctionsExecutionStuck alarms may fire; if using Step Functions with Express workflows vs Standard workflows, execution behavior differs; applications may experience errors or performance degradation due to stuck workflows; workflow automation may be completely blocked.

## Playbook

1. Verify Step Functions execution `<execution-arn>` exists and AWS service health for Step Functions in region `<region>` is normal.
2. Retrieve the Step Functions Execution `<execution-arn>` in region `<region>` and inspect its execution status, execution history, current state, and execution input, verifying execution is in "RUNNING" state.
3. Retrieve the Step Functions State Machine `<state-machine-arn>` for execution `<execution-arn>` and inspect its state machine definition, state configurations, and error handling settings, verifying state machine definition.
4. Query CloudWatch Logs for log groups containing Step Functions execution logs and filter for execution stuck patterns, state transition errors, or timeout events, including error message details.
5. Retrieve CloudWatch metrics for Step Functions State Machine `<state-machine-arn>` including ExecutionsFailed and ExecutionsTimedOut over the last 24 hours to identify execution patterns, analyzing execution metrics.
6. List Step Functions execution events for execution `<execution-arn>` and check execution event history, state transitions, and error events, analyzing event chronology.
7. Retrieve the Step Functions Execution `<execution-arn>` task token status and verify task token callback status, checking if task token callbacks are pending.
8. Retrieve the Lambda Function `<function-name>` if execution involves Lambda tasks and verify Lambda function execution status, checking if Lambda timeouts affect execution.
9. Query CloudWatch Logs for log groups containing CloudTrail events and filter for Step Functions state machine definition or execution modification events related to `<execution-arn>` within the last 24 hours, checking for configuration changes.

## Diagnosis

1. **Analyze CloudWatch Logs and Execution Events from Steps 4 and 6**: Review Step Functions execution logs for the current state and any error patterns. If CloudWatch Logs from Step 4 indicate the execution is waiting on a specific task state, identify the task type. If execution events from Step 6 show the last transition was to a "Task" state with no subsequent events, then the execution is waiting for task completion. If logs show timeout warnings, continue to step 2.

2. **Check Task Token Status from Step 7**: If the execution involves `.waitForTaskToken` tasks and Step 7 shows pending task tokens without callbacks, then missing task token callbacks are causing the stuck state. Verify the external system responsible for sending `SendTaskSuccess` or `SendTaskFailure` is operational. If task tokens are not involved, continue to step 3.

3. **Evaluate Lambda Function Status from Step 8**: If the stuck state involves Lambda invocation, check Lambda function status from Step 8. If CloudWatch Logs show Lambda function timeouts or cold start issues correlating within 5 minutes of the execution getting stuck, then Lambda performance is the root cause. Review Lambda timeout configuration against state machine timeout settings from Step 3. If Lambda is healthy, continue to step 4.

4. **Review State Machine Definition from Step 3**: If the state machine definition from Step 3 contains infinite loops, missing error handling, or states without proper transition definitions, then definition errors are causing the stuck state. Check CloudTrail events from Step 9 - if definition modifications occurred within 30 minutes of the execution starting, then recent changes may have introduced issues.

5. **Analyze Execution Metrics from Step 5**: If CloudWatch metrics show ExecutionsTimedOut increasing or ExecutionsFailed patterns correlating with the stuck execution, then systematic issues are affecting the state machine. Compare execution patterns across state machines - if multiple state machines show similar issues, then account-wide Step Functions service issues may be the cause.

**If no correlation is found**: Extend analysis to 30 days using execution status data. For Express workflows, check the 5-minute execution limit. For Standard workflows, verify the 1-year execution limit is not approaching. Review Lambda function execution logs for unhandled exceptions and verify task token callback delivery mechanisms are functioning correctly.
