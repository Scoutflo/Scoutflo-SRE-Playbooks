# Using These Playbooks

Every playbook is written so it works for both people and AI agents.

## For on-call engineers

Open the playbook for your alert or symptom, read **Meaning** and **Impact**, then follow **Playbook → For DevOps/SREs (CLI)** step by step. Use **Diagnosis** to interpret what you see. Steps that change state are marked as needing approval.

> The CLI section currently exists on a growing subset of playbooks (see the [roadmap](/roadmap)). The NLP steps are on all of them.

## For AI agents and automation

The **For AI Agents (NLP)** section is a numbered, tool-agnostic investigation plan with `<placeholders>` for the resource names. Give it to your agent together with the **Diagnosis** section, keep the agent read-only until a human approves any state-changing step, and have it report which diagnosis branch matched.

## With Scoutflo AI SRE

These playbooks are maintained by [Scoutflo](https://scoutflo.com), the team behind Scoutflo AI SRE, and follow the same events-first approach to root-cause analysis: check recent events and changes first, then narrow by symptom. Use them as an open reference for what a good investigation looks like, whether you run it by hand, with your own agent, or with Scoutflo.

## Contribute

Found a wrong command or a missing alert? Open an issue or a PR: see [How to Contribute](/contributing) and the [format guide](/format).
