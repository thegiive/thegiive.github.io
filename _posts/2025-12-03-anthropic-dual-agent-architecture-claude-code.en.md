---
layout: post
title: "Anthropic Explains: Why Does Claude Code Feel So Good to Use?"
date: 2025-12-03 09:00:00 +0800
lang: en
permalink: /en/anthropic-dual-agent-architecture-claude-code/
image: /assets/images/dual-agent-architecture-logo.png
description: "Anthropic reveals a dual-agent architecture—Initializer Agent + Coding Agent—so long-running tasks don’t rely on brute model power, but on an engineered workflow."
---

![Initializer Agent + Coding Agent Dual-Agent Architecture](/assets/images/dual-agent-architecture-logo.png)

Anthropic’s blog published an engineering approach for [long-running tasks](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents). This isn’t about brute-forcing with a bigger model or longer context. It’s about designing an engineered workflow so that even in multi-window conditions where the agent repeatedly “forgets,” it can still push forward like a human engineer.

I’ve read some reverse-engineering pieces about Claude Code; they’re broadly very similar to this architecture. And since the article mentions it was a collective effort by Anthropic’s RL team and the Claude Code team, we can treat this as a good representation of Claude Code’s design thinking.

=== Why does a single agent fail? ===

I’ve said before: long-running tasks are the holy grail for agents. Long tasks involve dozens to hundreds of features. But the model works within limited context each round—**every run is a “memory reset.”**

A single agent tends to run into two kinds of issues:

**Problem 1: It tries to write everything until it blows up.** The model starts coding at large scale until the context is exhausted, leaving “half code” behind—unfinished, undocumented, untested. When the next round takes over, it can’t tell what progress was made.

**Problem 2: It declares completion too early.** It sees some UI or API and assumes the feature set is complete, then terminates.

The core problem isn’t model capability. It’s the **lack of a structured way of working that can carry task logic across context resets**.

=== Dual-agent architecture: one directs, one iterates ===

Anthropic’s solution is to split long-running tasks into two roles.

**Initializer Agent (principal architect)** is responsible for the first run:
- Break the requirements into a JSON-structured feature list, each with acceptance criteria
- Create a `progress` file to record project status, tracked with git
- Generate an `init.sh` bootstrap script to ensure environment health

**Coding Agent (incremental implementer)** is responsible for subsequent iterations:
- At the start of each round, check the directory, read git history, run init.sh, do end-to-end tests
- Pick one unfinished feature from the list—**do exactly one thing at a time**
- Use Puppeteer to test like a real user; only mark complete and commit after it passes

This rhythm is slower, but extremely reliable. It turns “unattended long-running tasks” into “verifiable development iterations per round.” It’s very similar to what I previously described as Plan, Exec, Critic.

## Implementation details: the JSON manifest structure

The feature list uses JSON, and each feature has explicit acceptance steps:

```json
{
  "category": "functional",
  "description": "New chat button creates a fresh conversation",
  "steps": [
    "Navigate to main interface",
    "Click the 'New Chat' button",
    "Verify a new conversation is created",
    "Check that chat area shows welcome state",
    "Verify conversation appears in sidebar"
  ],
  "passes": false
}
```

Key design: **the agent can only modify the `passes` field**, and cannot delete or edit the tests themselves. This guarantees consistent acceptance criteria.

## How a Coding Agent session typically begins

At the start of each new session, the Coding Agent “onboards” itself:

```
[Assistant] 我將開始了解項目當前狀態
[Tool Use] <bash - pwd>
[Tool Use] <read - claude-progress.txt>
[Tool Use] <read - feature_list.json>
```

That’s why Claude Code often begins by reading CLAUDE.md, checking git logs, and understanding the project structure—**it’s rebuilding context**.

## Common failure modes and solutions

**Problem 1: The agent declares completion too early**
→ Create a 200+ feature checklist and force verification item by item

**Problem 2: Bugs remain unrecorded in the environment**
→ Force writing to git + a progress file

**Problem 3: Features are marked done too early**
→ Require self-verification via Puppeteer before marking complete

**Problem 4: The agent wastes time figuring out how to start the app**
→ Provide an init.sh script for one-command bootstrap

The article specifically mentions: even with the strongest **Claude Opus 4.5**, “out of the box” it still can’t build a production-grade web app across multiple context windows—**unless you adopt this structured approach**.

## Not the model—everything is engineering workflow

When I saw this architecture, my first reaction was: **isn’t this exactly what SDD has always emphasized?**

- Turn vague requirements into a structured feature list → we call it PRD
- Build a state-tracking mechanism → we use git + progress files
- Ensure every round is verifiable → we use QA acceptance flows

The difference is we do it with humans, and they make the AI do it. But the core insight is the same:

**Long-running task success isn’t about how strong the model is, but whether you have a structured workflow that can carry context forward.**


![The Workflow Loop: the Coding Agent iteration process](/assets/images/workflow-loop-diagram.png)

1. The bottleneck of long-running tasks is workflow design, not model capability
2. Dual agents are division of labor: one lays foundations, one iterates
3. Structured state recording is the key to cross-session collaboration
4. End-to-end testing is necessary in every iteration
5. In the future we may see Test Agents, QA Agents, Documentation Agents—forming an “AI engineering team”

In the next agent era, the breakthrough may not be higher model capability, but a breakthrough in **AI agent engineering methodology**. That’s why I’ve been focusing on writing technical articles about agent workflows.
