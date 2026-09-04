---
layout: post
title: "Claude First, Grok Seconds Later, ChatGPT an Hour Behind: The September 3 AI Outage and the Assumption Nobody Checked"
date: 2026-09-05 05:10:49 +0800
permalink: /ai-triple-outage-shared-failure-domain-en/
image: /assets/images/ai-triple-outage-shared-failure-domain-cover.png
description: "**Date:** 2026-09-05"
---

**Date:** 2026-09-05

![SpaceXAI official post acknowledging Memphis compute center outage](/assets/images/ai-triple-outage-shared-failure-domain-cover.png)

On the morning of September 3, Eastern Time, Anthropic's status page lit up first. Around 9:41 AM, Claude went down — Mythos, Fable, and Opus were all on the affected list. Grok degraded almost simultaneously. ChatGPT followed about an hour later. Gemini had no official outage report the entire time. Cursor, which has no frontier models of its own and relies on upstream APIs, went down with them.

Downdetector peaked between 10:30 and 11:00 AM ET: over 35,000 reports for ChatGPT, roughly 1,400 for Claude, and about 1,200 for Grok ([Karmactive](https://www.karmactive.com/chatgpt-claude-grok-simultaneous-ai-outage-september-2026/)). All three services were fully restored by 12:38 PM PT.

Someone sent me an analysis with two hypotheses and three exclusion items. The hypotheses were solid — I thought they were reasonable at first glance. But after spending half a day tracing every source, my conclusion was: the real thing that needed rewriting wasn't the hypotheses. It was **exclusion item number three**.

## 30-Second Overview

| Item | Detail |
|------|--------|
| Date | 2026-09-03 |
| Sequence | Claude (~09:41 ET) → Grok (near-simultaneous) → ChatGPT (~1 hour later) |
| Unaffected | Gemini (no official outage report) |
| Collateral | Cursor (upstream API dependency) |
| Official root cause | No unified cross-company statement; OpenAI spokesperson cited routing error; SpaceXAI acknowledged Memphis compute center outage |
| Named hardware failure | SpaceXAI acknowledged Memphis outage; Grok account confirmed Anthropic's leased capacity was affected |
| Official denial | Cloudflare explicitly denied any significant service disruption |

## Hypothesis 1: Cloudflare Ingress Layer

This was the loudest answer on X in the first hour. The logic was intuitive: all three services rely heavily on Cloudflare for frontend ingress, DNS, and DDoS protection. If Cloudflare hiccups, users can't even reach the backend — no amount of healthy GPU compute matters.

And Cloudflare's status page did show two ongoing issues at the time: an HTTP/3 problem with R2 custom domains, and incorrect geolocation for some WARP users. For anyone looking to close the case quickly, these two items looked like evidence.

The problem is Cloudflare shut this down hard. Their statement to The Register:

> Cloudflare is not experiencing any significant service disruptions at this time. Our services are operating normally, and any reporting that deviates from this is incorrect.

In plain English: not just "we're fine," but "any reporting that says otherwise is wrong." That's an unusually strong denial for a vendor statement.

The timeline doesn't fit either. A pure CDN global failure produces simultaneous, widespread errors — not Claude going down first with ChatGPT following an hour later. The R2 HTTP/3 issue affected a small slice of object storage, not global API endpoints.

My read: this hypothesis should have been retired on the day it happened. It lasted as long as it did because it was the easiest story to tell — Cloudflare has had several major outages in the past two years, and everyone's muscle memory was still there.

## Hypothesis 2: Traffic Cascade

The second hypothesis was cascading overload. Claude goes down first; users, automation scripts, and API clients fail and auto-retry, while humans manually switch to Grok and ChatGPT. The sudden traffic surge exceeds the other two providers' rate-limiting thresholds, sequentially crushing their ingress layers. Client-side infinite retries amplify another round, creating a self-reinforcing traffic flood.

This hypothesis has one strong piece of evidence: **the time gap**. ChatGPT went down about an hour later — exactly the shape you'd expect from "one goes down, traffic migrates, migration overwhelms the next one." If it were a shared upstream failure, all three should have gone down simultaneously.

It also has one strong counterpoint: **Grok went down almost simultaneously with Claude**. There wasn't enough time for traffic migration. Users switching from Claude to Grok need minutes to tens of minutes of diffusion, not seconds.

So hypothesis two explains the third domino but not the second.

## The Real Problem Was in the Exclusion Items

The analysis listed three exclusion items. The first two I had no issue with:

1. Not a model code bug — the probability of multiple independent models having core bugs simultaneously is vanishingly small.
2. Not a cyberattack — no status page disclosed a DDoS event.

The third one read: not a unified cloud datacenter power failure, because the three providers' compute infrastructure runs on Azure, AWS, and self-built clusters respectively — their underlying datacenters are independent.

This stopped being true in May 2026.

In May 2026, Anthropic signed a deal with SpaceX to take full exclusive use of Colossus 1 — 222,000 NVIDIA GPUs (H100/H200/GB200 mix), 300+ MW of power, at $1.25 billion per month, with a contract running to May 2029, total value exceeding $40 billion.

Colossus 1 is in Memphis. It went operational between July and September 2024. It was originally built by xAI to train Grok. xAI's own training has since moved to the larger Colossus 2 (2 GW, 555,000 GPUs). Colossus 1 — the entire facility — was leased to Grok's direct competitor.

That evening, the official SpaceXAI account posted:

> We are sorry for the issues you may have experienced with Grok following an outage at our Memphis compute center this morning. We'd also like to apologize to our impacted compute partners.

As of the morning of September 4, this post had accumulated roughly 10,000 likes, 1.43 million views, and 478 replies ([original post](https://x.com/SpaceXAI/status/2095597264043717014) — the cover image of this article is a screenshot of it).

The key is the last sentence. They didn't just apologize for Grok — they apologized to their "impacted compute partners." This is the only company in this entire incident to name a specific hardware failure and explicitly say external customers were affected.

Shortly after, Grok's official account went further, confirming that the Memphis outage hit "Grok and Anthropic's leased capacity there (Claude)." SpaceXAI's post only said "compute partners" — Grok named names. This was the first time any official source directly linked Anthropic to the Memphis failure.

Put it all together: Memphis went down. Anthropic leases nearly all of Memphis's compute capacity. An official source confirmed Anthropic's leased capacity was affected. Claude and Grok degraded almost simultaneously. The question about the second domino disappears — those two dominoes may have been the same one all along.

## What About ChatGPT?

This is where I'm not going to force-fit the thesis. OpenAI has no known relationship with Memphis. ChatGPT went down an hour later. A shared failure domain doesn't explain it.

An OpenAI spokesperson told [Newsweek](https://www.newsweek.com/outages-openai-chatgpt-grok-claude-gemini-downdetector-12401012): "A routing error starting around 7:43 a.m. PT made ChatGPT and Codex unavailable for some users across platforms." They mentioned only a routing error — no mention of Memphis, no connection to the other providers. Notably, OpenAI's own status page said only "investigating the issue" and "applied mitigation." The term "routing error" appeared only in the spokesperson's response to media.

Some outlets pointed to Azure East US, claiming all three providers were in the same cloud failure domain and that Gemini survived because it runs on Google Cloud. But [Quartz's reporting](https://qz.com/chatgpt-claude-grok-simultaneous-outages-090326) explicitly stated that no official confirmation tied an Azure failure to this incident, nor was any shared infrastructure failure verified.

My read is a two-layer chain of causation:

- **Layer 1 (physical)**: Memphis compute center failure, simultaneously taking down Claude and Grok. This layer is supported by official posts, Grok's account naming Anthropic, and the lease agreement.
- **Layer 2 (traffic)**: With two providers down simultaneously, retry storms plus manual user switching pushed load toward OpenAI, exceeding thresholds about an hour later. OpenAI's own "routing error" is consistent with a routing layer suddenly absorbing millions of additional users.

An incident doesn't have to have a single root cause. This one looks more like the physical layer opened a hole, and the traffic layer tore it wider.

## Charles Hoskinson's Third Version

Worth mentioning: there was also a high-visibility version from Cardano founder Charles Hoskinson:

> It looks like a national state brought down Claude, ChatGPT, and Grok

His evidence was that Gemini was unaffected:

> They all use Nvidia chips. Google doesn't.

The observation itself is correct — Google uses its own TPUs while the other three use Nvidia. But the leap from "shared chip vendor" to "nation-state attack" skips too many steps. The same observation has a far more mundane explanation: shared chips often mean shared datacenters, shared power supply, shared cooling design — in other words, shared failure modes. No attacker needed; one building losing power is enough.

I include this not to mock, but because it demonstrates something: **when companies don't provide a root cause, the market fills the gap** — and what gets filled in is usually more dramatic than the facts.

## This Corrects Something I Wrote Before

When Cloudflare had a major outage in November 2025, I wrote about how Andrew Ng's team used AI Coding to quickly build minimal Cloudflare backup components, surviving the outage. The thesis: AI Coding can serve as a new kind of BCP (Business Continuity Plan).

That article had an unwritten assumption: **AI is an always-online repair tool**.

September 3 punctured that assumption. When what goes down is AI itself, AI Coding can't be your BCP. For those three hours, your repair tool was lying flat right alongside the thing you needed to repair.

This doesn't mean that article was wrong — it means its applicability boundary needs an addendum: AI Coding as BCP works only when the failure domain doesn't include the AI provider itself. When Cloudflare went down, that premise held. This time it didn't.

## Who This Changes What For

**Enterprise CTOs.** The previous procurement logic was "we've got three providers, they can't all go down." After this, contract negotiations need one more question: which physical datacenter does your inference run in, and does it overlap with my other two providers?

That question is hard to get answered right now, because compute lease relationships are mostly not public — I found the Anthropic–Colossus 1 deal on Wikipedia, not from any procurement document. But the inability to get an answer is itself information: your multi-provider strategy might just be three logos hung on one failure domain.

**Individual developers.** The previous fallback path was: Claude goes down, switch to Codex; Codex goes down, switch to Grok. This time, all three paths broke simultaneously for about three hours.

The only effective fallbacks left are two kinds: an on-premises machine that can run models, or a work mode that can continue offline (reading code, writing specs, running tests). When I tested on-prem models on my RTX Pro 6000 setup, the motivation was privacy and cost. After September 3, there's a third reason: **on-prem's failure domain doesn't overlap with the cloud**.

## To Be Honest

The core inference of this article — that the Memphis failure simultaneously took down Claude and Grok — is currently **inference, not a confirmed root cause**.

Specifically, three gaps remain:

First, SpaceXAI's "compute partners" wasn't named explicitly, though Grok's official account subsequently confirmed the affected parties included "Anthropic's leased capacity." However, the Grok account generates AI responses — it's not equivalent to an official xAI PR statement, so its authority is discounted.

Second, Anthropic's use of Colossus 1 has not been publicly specified. Large GPU cluster leases are often for training; a training cluster going down doesn't necessarily take down inference services. If Anthropic's inference runs elsewhere, this line of reasoning breaks.

Third, I cannot explain why Anthropic made no mention of Memphis in their own incident reports. It could be that they hadn't finished investigating, that their contract prohibits disclosure, or that it's simply unrelated.

So this should be read as a hypothesis, standing in the same lineup as the two I dismantled above — except I believe its evidence is stronger, because it has at least one company's official post and a public lease agreement. The other two hypotheses currently have only the shape of the timeline.

If an official root cause report comes out and proves me wrong, I'll come back and revise this article.

## Key Insight

**Failure domains follow physical location, not vendor logos.**

For the past two years, the industry's redundancy playbook has been "connect to multiple providers." That playbook rests on a premise that was true in 2023 but no longer holds in 2026: different AI companies run on different machines.

When frontier labs start leasing compute from each other — one builds a datacenter, another rents the entire thing — vendor-level diversification no longer equals infrastructure-level diversification. You think you have three providers. At the physical layer, you might have one and a half.

To verify this, the only tool you have is: ask your provider where inference runs, and see whether they're willing to answer.

---

## FAQ

**Q: Has an official root cause been published for the September 3, 2026 AI outage?**

No unified cross-company root cause statement exists as of this writing. SpaceXAI officially acknowledged a Memphis compute center failure and apologized to "impacted compute partners." Grok's official account further confirmed that those affected included Anthropic's leased capacity. An OpenAI spokesperson told Newsweek that ChatGPT's failure was a routing error, with no mention of Memphis or shared infrastructure. Anthropic made no mention of Memphis in their incident reports. Cloudflare explicitly denied any significant service disruption.

**Q: What is a Failure Domain, and how is it different from a multi-provider strategy?**

A failure domain is the smallest unit that "breaks together" — the same machine, the same rack, the same datacenter, the same power feed. A multi-provider strategy diversifies commercial contract relationships; failure domain diversification targets physical and infrastructure relationships. The two are often treated as the same thing, but when Provider A leases compute to Provider B, two logos land in the same failure domain. Anthropic agreeing to lease nearly all of xAI's Memphis Colossus 1 capacity in May 2026 is exactly this situation.

**Q: Why was Gemini unaffected while the other three went down?**

Gemini had no official outage report throughout September 3. Two explanations circulated in the community: one was that Google uses its own TPUs while the other three use Nvidia GPUs — cited by Cardano founder Charles Hoskinson as evidence of a nation-state attack. The other was that Google's inference runs on its own Google Cloud, sharing no datacenters with other labs. The second explanation requires no assumption of an attacker and can explain the same phenomenon with much lower evidentiary requirements.

**Q: Why did Cursor go down too?**

Cursor has no frontier models of its own. Its core functionality is calling upstream provider APIs from OpenAI, Anthropic, and others. When upstream returns errors, Cursor has no local inference to fall back on, so it becomes unavailable in lockstep. This is the structural risk of pure API-relay products: your availability ceiling equals your upstream's availability, and you can't even issue outage notifications until upstream goes first.

**Q: How should individual developers prepare for the next time all three go down simultaneously?**

Cross-cloud provider switching was ineffective this time — Claude, Grok, and ChatGPT had roughly an hour of overlapping unavailability, with all three fully restored at 12:38 PM PT. The only effective preparations fall into two categories: on-premises models that can run locally, whose failure domain doesn't overlap with the cloud; and pre-planned offline work modes (reading existing code, writing spec documents, running test suites) that turn a three-hour outage into something other than a three-hour standstill.

---

## Sources

- [9to5Google: ChatGPT, Claude, Grok simultaneous outages (with recovery time updates)](https://9to5google.com/2026/09/03/chatgpt-claude-grok-outages/)
- [The Register: All three down simultaneously, including Cloudflare statement](https://www.theregister.com/ai-and-ml/2026/09/03/chatgpt-claude-and-grok-all-had-outages-at-the-same-time/)
- [Quartz: ChatGPT, Claude, Grok simultaneous outages, root cause unconfirmed](https://qz.com/chatgpt-claude-grok-simultaneous-outages-090326)
- [Karmactive: Downdetector data compilation](https://www.karmactive.com/chatgpt-claude-grok-simultaneous-ai-outage-september-2026/)
- [SpaceXAI official post: Memphis compute center outage](https://x.com/SpaceXAI/status/2095597264043717014)
- [Wikipedia: Colossus (supercomputer)](https://en.wikipedia.org/wiki/Colossus_(supercomputer))
- [Newsweek: OpenAI spokesperson confirms routing error](https://www.newsweek.com/outages-openai-chatgpt-grok-claude-gemini-downdetector-12401012)
- [OpenAI Status Page: ChatGPT/Codex incident record](https://status.openai.com/incidents/01M1KWEDH417T2CF44YYHZDFCR)
- [Charles Hoskinson's nation-state attack theory](https://bitcoinethereumnews.com/tech/charles-hoskinson-has-a-theory-for-ai-outage-affecting-chatgpt-claude-and-grok/)
