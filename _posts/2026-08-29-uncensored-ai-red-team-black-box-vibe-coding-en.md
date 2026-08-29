---
layout: post
title: "\"One URL, Zero Context — Two Hours of Black-Box Red Teaming with an Uncensored AI\""
date: 2026-08-29 09:00:00 +0800
permalink: /uncensored-ai-red-team-black-box-vibe-coding-en/
tags: [red team, penetration testing, cybersecurity, uncensored LLM, abliteration, guardrail bypass, black box testing, VibeCoding, Qwen3.8-27B, huihui, AI security, offensive security, bug bounty, vulnerability assessment, open source security]
categories: [AI Agent]
image: /assets/images/uncensored-ai-red-team-cover.png
description: "\"A friend's website had been white-box scanned 3-4 times with Claude Code, rescanned with Codex, and a paid security firm was already signed. Before the real audit, he wanted a dress rehearsal with an uncensored AI. Using an RTX 5090 + Qwen3.8-27B huihui (abliterated), given nothing but a URL, I ran a pure black-box red team. Architecture mapped in 3 minutes, first 2 findings in 30 minutes, 10 issues and 2 PoCs in two hours. If you can build a website with AI, someone else can tear it apart with AI.\""
author: Wisely Chen
---

> **Disclaimer:** The testing described in this article was an authorized red team engagement conducted at the explicit invitation of the website owner. Attacking any website without authorization is almost certainly illegal.

## Table of Contents

- [If You Can Build It with AI, Someone Can Break It with AI](#if-you-can-build-it-with-ai-someone-can-break-it-with-ai)
- [Why "Uncensored" Is Non-Negotiable](#why-uncensored-is-non-negotiable)
- [Black-Box Rules: One URL, Nothing Else](#black-box-rules-one-url-nothing-else)
- [The AI Draws the Map First](#the-ai-draws-the-map-first)
- [First Two Meaningful Findings at 30 Minutes](#first-two-meaningful-findings-at-30-minutes)
- [Why Did White-Box Miss These?](#why-did-white-box-miss-these)
- [Human Steps In: Login and Payment](#human-steps-in-login-and-payment)
- [Two Hours: Done](#two-hours-done)
- [Efficiency Breakdown](#efficiency-breakdown)
- [How It Felt: Point and Shoot](#how-it-felt-point-and-shoot)
- [The Unsettling Implication](#the-unsettling-implication)
- [For Anyone Shipping a VibeCoded Product](#for-anyone-shipping-a-vibecoded-product)

## If You Can Build It with AI, Someone Can Break It with AI

Another Saturday security day.

A friend's website was about to go live. He'd actually done a solid job on security prep — last month he used Claude Code to run white-box scans directly against the source code, three or four passes in total. On my suggestion, he also ran Codex for a rescan with a different model, cross-validating with a fresh set of eyes on the same codebase. He'd even signed with a professional security firm for a formal paid penetration test.

Multiple white-box rounds plus a paid engagement on the way — by the standards of projects I've seen, that's genuinely thorough.

Then he saw [the article I published last week](/qwen38-27b-abliteration-three-days-safety-paradox/) — about how the community produced five uncensored versions of Qwen3.8-27B within three days of its open-source release, dropping the refusal rate on 842 harmful prompts to zero. He asked: "Before the real exam, can we do a practice run with an uncensored AI?"

## Why "Uncensored" Is Non-Negotiable

I don't have much red team experience, but I've been very curious about what uncensored AI can actually do. I covered the technical details of abliteration and the safety paradox in [that earlier article](/qwen38-27b-abliteration-three-days-safety-paradox/) — here I'll stick to what's directly relevant to red teaming.

If you ask Claude to "help me attack this website," it will refuse. Not because it lacks the capability — the safety guardrails block it. Commercial models go through RLHF training, and attack-class instructions trigger refusal mechanisms. Even if you prepend "I'm an authorized penetration tester," most of the time it will politely decline.

White-box scanning doesn't have this problem — you're just asking the AI to read code and find bugs; it doesn't need to "attack" anything. But black-box testing is fundamentally about simulating an attacker. You need the AI to actually probe, test, and send malicious payloads. When the guardrails block that, the entire exercise falls apart.

A community contributor named huihui specializes in "abliteration" — using technical methods to strip a model's safety training while preserving its original capabilities. The huihui version of Qwen3.8-27B is the result. The model's reasoning ability is identical to the original; it just won't lecture you when you say "help me test for SQL injection."

The 27B size was chosen because it runs local inference — no need to send anything to a cloud API. Red team logs contain the target's complete architecture and vulnerability details. You don't want any of that passing through a third-party server.

## Black-Box Rules: One URL, Nothing Else

I arranged a time with my friend and asked him to give me a public URL. No information about the framework, language, database, or hosting. Just a URL. Pure black-box.

This is the core of black-box testing — simulating an external attacker who knows nothing about the target. White-box means holding the source code and hunting for bugs. Black-box means standing outside and looking in. The two methods find different things — they're complementary.

My friend sent the URL. I fired up the RTX 5090 + Qwen3.8-27B Huihui edition, pasted the URL into the prompt, and told the AI: Go.

## The AI Draws the Map First

I didn't know what to expect. This was genuinely my first serious red team engagement.

The output in the first three minutes caught me off guard.

The AI mapped out the entire frontend architecture. Not a casual list of pages — a structured breakdown: how many components in each major section, what technology each component used, which third-party SaaS services were integrated, all names identified.

Three minutes. Given nothing but a URL. No source code, no documentation, no internal information whatsoever.

Is it really that easy?

For a human to do the same thing, an experienced pentester would spend fifteen to twenty minutes flipping through the network tab, reading JS bundles, and probing various paths. The AI compressed the entire reconnaissance phase to under three minutes, and the output was structured — ready to drop into a report as-is.

## First Two Meaningful Findings at 30 Minutes

After reconnaissance, the AI began systematically testing the attack surfaces it had identified.

Thirty minutes in, it found two issues I considered worth putting in a formal report. By "meaningful," I mean problems at the level of data theft, DoS, or script ingestion — not "you should add a CSP header."

And both of these had been missed across three to four previous white-box scans.

## Why Did White-Box Miss These?

This left the deepest impression on me. But what I want to say is not "black-box is better than white-box" — that's not the point.

The point is: **white-box and black-box are looking at fundamentally different things.**

White-box is like inspecting every bolt in the factory to make sure it's tight. Black-box is like standing on the street watching the car drive by to see if anything is leaking. They're not examining the same thing, and what they find doesn't overlap.

White-box examines the code: logic errors, hardcoded secrets, insecure dependency versions, race conditions. That's its home turf, and AI reviewing source code line by line is extremely efficient at it.

Black-box examines deployed behavior: server response headers leaking framework versions, API endpoint error handling returning too much information, a SaaS integration with improperly locked permissions, overly permissive CORS settings. These might be perfectly correct in the source code, but once deployed and combined with the real environment, problems emerge. You'll never know unless you hit it from the outside.

So the conclusion isn't "white-box isn't good enough, switch to black-box." It's **do both, because their blind spots are exactly complementary**.

## Human Steps In: Login and Payment

After running the unauthenticated tests, the AI hit a wall: many features required login to access.

This is where my friend and I got involved together. We registered two test accounts on the site so the AI could access authenticated functionality. Then we walked through several business flows — actually completing the full user journey. I even spent 100 TWD (about $3 USD) testing the payment flow.

The AI tested the flow in fine detail. For information it couldn't obtain externally, it asked me to pull data from DevTools. Despite never seeing a single document, within 10 minutes I felt like the AI had figured out exactly how the entire payment pipeline was wired.

Human involvement was needed for practical reasons: the AI can fill forms and send requests on its own, but account registration and payment require a human present to authorize. And some business logic vulnerabilities can only be discovered by actually walking through the complete flow.

## Two Hours: Done

Final tally: 10 issues identified. For the critical ones, I had the AI pick two bugs, execute actual attacks, and leave script ingestion logs on the website. Done.

The whole thing was genuinely entertaining for me.

This step matters. If a red team report only says "there might be a vulnerability here," it has limited persuasive power. You need proof of concept — actual evidence that the vulnerability can be exploited. The AI delivered: it understood how to exploit the vulnerabilities, assembled complete attack chains, and judged what evidence was sufficient to prove the issues existed.

## Efficiency Breakdown

| Phase | Time | Output |
|-------|------|--------|
| Reconnaissance (architecture analysis) | 3 min | Complete frontend architecture map, component inventory, SaaS service identification |
| Unauthenticated testing | 30 min | 2 report-worthy findings |
| Authenticated testing | ~90 min | Business flow testing, payment flow testing |
| PoC validation | Final segment | 2 bugs with actual exploitation + evidence |
| **Total** | **~2 hours** | **10 issues, 2 PoCs with evidence** |

That's one person plus one AI, two hours of work. Compare that to hiring a security firm for the same scope — timelines are typically measured in days.

Of course, a professional pentester's depth and breadth would far exceed what we did here. But as a "practice exam before the real thing," the efficiency exceeded my expectations.

## How It Felt: Point and Shoot

Overall, the AI was highly responsive. Tell it to test API permission controls, it tests them. Tell it to check forms for XSS, it runs through various payloads. On the "getting things done" dimension, its capability was never in question.

But sometimes, after clearly finding a problem, it would just stop.

Not a crash, not a timeout — just sitting there, waiting. I had to give it a push, an explicit instruction, before it would continue.

My sense is that the abliterated model isn't entirely free of hesitation. The moral imprint seems to linger. It's not the guardrails blocking it — more like residual uncertainty about "should I really execute this step." It needs a human to make the call at critical moments.

This actually made me feel more comfortable — at least it's not a completely unrestrained tool.

## The Unsettling Implication

I'm not a security expert. I'm just someone who can code and has a basic understanding of cybersecurity.

My "opponent" was someone who had already white-box scanned their site four or five times with AI. But armed with an uncensored AI and nothing but a URL, I found 10 issues in two hours and left evidence for two.

Flip the perspective: if someone with just a basic CS background can do this, what about an actual attacker?

The emergence of Qwen3.8-27B has dramatically lowered the deployment cost for Opus-tier model capabilities. As uncensored models grow more powerful, VibeCoded websites are probably the easiest targets. VibeCoding's core value proposition is rapid delivery of functional products — security is almost certainly not a consideration for 99% of VibeCoded sites.

I previously wrote about [Mythos using social engineering to attack real humans](/aisi-mythos-social-engineering-github-sock-puppet-attack/) — that was AI autonomously deciding to attack. This time is different — a human directing AI to perform authorized security testing. But the underlying capability is the same toolkit. AI can build, and AI can break. Right now, breaking appears to have a much lower barrier than building.

## For Anyone Shipping a VibeCoded Product

**White-box scanning is table stakes, but it's not enough.** Run at least one black-box pass. You don't need to hire professionals first (though you should eventually) — run an uncensored AI sweep yourself first. Two hours might save you from a critical vulnerability.

**Run uncensored models locally.** Don't send red team prompts and results to any cloud API. Your test logs contain the target's complete architecture and vulnerability inventory — if those leak, they become an attack playbook. A 27B model runs fine on a consumer GPU.

**Find a friend with a CS background to help.** You don't need a security expert. Like my experience here — first time doing it, prompts weren't even optimized, but two hours still turned up findings. AI handles the grunt work; humans provide judgment and direction.

**Do both white-box and black-box — their blind spots are exactly complementary.** White-box finds logic-layer issues. Black-box finds deployment-layer and configuration-layer exposure. The two methods have different blind spots; together they're complete.

---

Pandora's box is already open — open-source, free, runs on a single consumer GPU. Is your VibeCoded website ready?
