---
title: Kube Deployment Replicas Mismatch
weight: 20
---

# KubeDeploymentReplicasMismatch

## Meaning

Deployment has not matched the expected number of replicas (triggering KubeDeploymentReplicasMismatch alerts) because the current number of ready replicas does not match the desired replica count, indicating that pods cannot be created, scheduled, or become ready. Deployments show replica count mismatches in kubectl, pods remain in Pending or NotReady state, and deployment events show FailedCreate or FailedScheduling errors. This affects the workload plane and indicates scheduling constraints, resource limitations, or pod health issues preventing deployment from achieving desired state, typically caused by cluster capacity limitations, resource quota constraints, or persistent scheduling issues; applications run with insufficient capacity and may show errors.

## Impact

KubeDeploymentReplicasMismatch alerts fire; service degradation or unavailability; deployment cannot achieve desired replica count; current replicas mismatch desired replicas; applications run with insufficient capacity; rolling updates may be blocked; replica counts do not match desired state. Deployments show replica count mismatches indefinitely; pods remain in Pending or NotReady state; applications run with insufficient capacity and may experience errors or performance degradation.

## Playbook

1. Describe deployment <deployment-name> in namespace <namespace> to see:
   - Replicas status (desired/current/ready/available)
   - Conditions showing why replicas mismatch
   - Events showing FailedCreate, FailedScheduling, or ReplicaSetCreateError errors

2. List events in namespace <namespace> filtered by involved object name <deployment-name> and sorted by last timestamp to see the sequence of replica mismatch issues.

3. List ReplicaSet resources in namespace <namespace> with label app=<app-label> and check ReplicaSet status and replica counts to verify replica distribution.

4. List pods in namespace <namespace> with label app=<app-label> and describe pod <pod-name> to identify pods in Pending, CrashLoopBackOff, or NotReady states.

5. Retrieve deployment <deployment-name> in namespace <namespace> in YAML format to verify resource requests, node selectors, tolerations, and affinity rules in the pod template.

6. Describe nodes to check allocated resources and verify capacity availability across the cluster for scheduling additional pods.

## Diagnosis

1. Analyze deployment events from Playbook steps 1-2 to identify the primary failure reason. Events showing "FailedScheduling" indicate resource or scheduling constraints. Events showing "FailedCreate" indicate ReplicaSet creation issues. Events showing "BackOff" or "CrashLoopBackOff" indicate pod crash loops. Events showing "Unhealthy" or "FailedReadiness" indicate readiness probe failures.

2. If events indicate scheduling failures (FailedScheduling with messages like "Insufficient cpu" or "Insufficient memory"), correlate pod pending timestamps from Playbook step 4 with node capacity data from Playbook step 6 to confirm resource exhaustion as root cause. Verify which resource (CPU, memory, or both) is constrained and on which nodes.

3. If events indicate resource quota issues (messages containing "exceeded quota" or "forbidden: exceeded quota"), verify quota status from namespace resource quotas and compare with deployment resource requests from Playbook step 5 to confirm quota as the blocking factor.

4. If events indicate pod crashes (CrashLoopBackOff, Error, or OOMKilled), analyze pod describe output from Playbook step 4 to identify container exit codes and termination reasons. Exit code 137 indicates OOMKilled, exit code 1 indicates application error.

5. If events indicate image pull failures (ErrImagePull, ImagePullBackOff), verify image name and tag from deployment spec in Playbook step 5 and check for registry connectivity or authentication issues.

6. If events indicate readiness probe failures, analyze pod conditions and probe configuration from Playbook step 4 to identify application-level issues preventing replicas from becoming ready.

7. If events indicate node affinity or taint issues (messages containing "didn't match node selector" or "node(s) had taints"), compare deployment tolerations and affinity rules from Playbook step 5 with available node labels and taints from Playbook step 6.

8. If events are inconclusive or show only generic errors, compare ReplicaSet status from Playbook step 3 to verify replica distribution across generations and identify if mismatch is due to stuck rollout versus scaling failure.

**If no clear failure reason is identified from events**: Review deployment modification history to identify recent changes, check for HPA conflicts if autoscaling is configured, verify pod disruption budgets are not blocking scaling, and examine historical deployment patterns. Replica mismatch may result from cumulative resource pressure or intermittent scheduling constraints.
