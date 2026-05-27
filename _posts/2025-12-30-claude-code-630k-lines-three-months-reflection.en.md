---
layout: post
title: "After 630K Lines in Three Months: In the AI Coding Era, What Is an Engineer’s Real Value?"
date: 2025-12-30 10:00:00 +0800
lang: en
permalink: /en/claude-code-630k-lines-three-months-reflection/
image: /assets/images/claude-code-630k-lines-stats.png
description: "Three months. 630,000 lines of code. This isn’t about bragging output—it’s about what matters after code becomes ‘cheap’: humans’ last core value is defining the work (kickoff/specs) and accepting it (review/QA)."
---

Three months. 630,000 lines of code.

That number might sound exaggerated, so let me be clear about what those 630k lines are made of:

- **~5–10%**: production code (customer-facing product code)
- **~90–95%**: one-off scripts, internal data analysis, and batch programs for daily routines

(Since this is a new-company laptop, the folders only contain output from mid-September—when I joined—until now, so I’m pretty confident it’s a three-month number.)

This post isn’t about flexing volume. It’s about sharing this: when code becomes “cheap,” what becomes truly important?



## How I started using Claude Code

### Phase 1: AI Coding reviewer

When I first joined YongLian Logistics, the team mostly used Cursor. I used Claude Code to review [AI Coding](/atpm-a-real-production-vibe-coding-process/) work.

What did that look like?

1. **Scan git to see what everyone wrote**: have Claude Code sweep commits and highlight suspicious areas, then I’d dive deeper
2. **Review Jira workflows**: check whether QA partners were following the right process
3. **Data analysis**: connect via MCP to BigQuery and do ops-optimization analysis

Even then, I felt Claude Code was extremely useful.

### Phase 2: FDE data analysis (world-class e-commerce logistics optimization)

Later, when the [FDE](/fde-continuous-experiment/) team was doing [logistics optimization for a world-class e-commerce company](/notebooklm-trust-fde/), we used Claude Code heavily for data analysis and provided the team with **hundreds of indexes and metrics** for fast validation.

This phase made me realize: Claude Code isn’t just a coding tool—it’s an **accelerator for data exploration**.

### Phase 3: Managing a cross-national team (the NeuroBrain Dynamics period)

After moving to NeuroBrain Dynamics, I led a cross-national team and returned to my IT roots. IT is highly digitized; unlike traditional industries where early-stage work is about “digitization requirements,” we had lots of operational data. Using Claude Code for **team management** work became very natural.

A few concrete examples:

**Performance review**
When I want to review someone’s performance, I use Claude Code to pull up their code first and see whether the work over the past few months shows progress. Then I ask Claude Code for insights, and validate those suggestions with my own judgment.

**Utilization calculation**
If I want to calculate team utilization, I also use Claude Code to do the computations.

**Code review**
Any code that will be delivered to clients, I use Claude Code for code review.

**Life**
And of course, the daily routine of [slow jogging + Claude Code](/vibe-duo-ai-ru-he-zeng-jia-wo-de-sheng-chan-li/) gives me a lot more time to take care of my health while getting things done.

### Phase 4: AI blog author

As an AI blogger, over these three months I’ve also continuously used Claude Code to help with ideation and research.

I use a “[Storm mode agent](/storm-ai-agent-as-expert-editor-team/)” approach—send out lots of subagents to review and collect information from different angles. In the end, I act as the **chief editor**, adding my own signature “salt”: my tone, plus one or two punchlines when inspiration hits.

In these ~100 days, I wrote around 65 posts. That’s why this blog can stay close to daily posting while still preserving my personal style as much as possible.

## Reflections after 630K lines

630K lines may only be the beginning.

As agents are used more and more, code truly becomes cheaper. At that point, code usage splits into two categories:

### Type 1: one-off / daily-routine code

This is what I write most often. Characteristics:
- internal use
- the goal is simply that it’s **correct** and **manageable**
- long-term maintenance isn’t a requirement

### Type 2: customer-facing product code

This is a totally different bar:
- others must be able to read it
- it must be maintainable
- it must run long-term

**At this point, the “birth” of code is no longer the point. The point is whether you can write a good PRD, and whether you can write the relevant QA test cases well.**

## My confusion about the Vibe Coding community

Honestly, after listening to many Vibe Coding discussions, people talk about a lot of things—but **very few emphasize how to do QA well**, which really puzzles me.

In ATPM, I’ve repeatedly stressed the importance of [QA](/atpm-qa-ru-he-yan-shou-ai-coding-de-cheng-shi/)—and in practice, I spend about 70% of my time on acceptance/review.

The reason is: in the end, as summarized by Li Muyue in a [Generative AI talk I heard this year](https://live.gaiconf.com?utm_source=chatgpt.com)—

**Humanity’s last value is “the client-side value.”**

What is “client-side value”?

1. **Kickoff / defining the work**: write the specs well and clearly
2. **Acceptance / verification**: quickly review the massive amount of output the AI produces

If all you can do is have AI generate code, but you can’t define specs and can’t verify quality, you’re just “playing” with AI—not “using” AI.

## In the AI Coding era, do engineers still have value?

This is the question I get asked most. My answer: **yes, but the definition of value has changed.**

In the past, an engineer’s value was “being able to write code.” Now AI has drastically lowered that bar. But engineer value hasn’t disappeared—it has shifted upward:

- **understanding business needs**: AI doesn’t know what your customer actually wants
- **architecture decisions**: which stack to choose, how to define system boundaries
- **quality control**: whether AI outputs are correct, good, and usable

Put bluntly, engineers have moved from “producers” to “quality controllers” and “architects.”

## Will AI agents replace engineers?

Not in the short term. But in the long term, **some types of engineers will be replaced**.

Those likely to be replaced:
- people who only write code to spec
- people unwilling to learn how to collaborate with AI
- people who treat “coding” as their only skill

Those unlikely to be replaced:
- people who can define problems
- people who can accept/verify quality
- people who can make architecture decisions
- people who can communicate with stakeholders

That’s why I keep saying: code itself is no longer valuable. What’s valuable is whether you can be a good “client.”

## How should engineers avoid being淘汰 in the AI era?

Based on my three months of hands-on experience, here are some concrete suggestions:

**1. Learn to write good PRDs (Product Requirement Documents)**

The quality of AI output is 80% determined by the input you give it: the [PRD](/atpm-prdde-zhong-yao-xing/). If you can’t even write requirements clearly, AI won’t save you.

**2. Build acceptance/verification skills**

When AI can output thousands of lines of code a day, your bottleneck isn’t generating—it’s reviewing/accepting. The scarce skill is quickly judging code quality and finding potential issues.

**3. Embrace AI tools, but don’t depend on them**

Treat AI as a co-pilot, not autopilot. You still need to know where you’re going and what the road conditions are.

**4. Move upstream**

The closer your work is to the business side and decision-making, the harder it is to be replaced. Coding is downstream; defining requirements is upstream.

## Closing

630K lines sounds like a lot, but honestly, it will become less and less special.

When code becomes cheap, what becomes scarce is:
- people who can define problems well
- people who can verify results well
- people who can judge quality quickly amid massive output

That’s why I emphasize the A (Assessment) and T (Testing) in the ATPM framework—**kickoff** and **acceptance** are humanity’s last core value.


Claude Code is no longer just a tool. Honestly, it’s become like a programming partner, or a great assistant in my management work. It’s a bit rigid and not as “chatty” as pre-5.2 ChatGPT, but it can truly do 70% to 80% of the work I assign. To be honest, even swapping in another person might not be as reliable.

![Slow jogging with Claude Code: health and productivity at the same time](/assets/images/claude-code-slow-jogging.png)

Dear Claude Code—please take care of me in the new year too.


=====

PS. Photo taken this morning at a hotel in Sha Tin, Hong Kong—my “year-end summary” photo with Claude Code.

After annual reviews at foreign companies, don’t we always take a big group photo? XD
