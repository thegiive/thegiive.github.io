---
layout: post
title: "\"Barclays Dissected the AI Profit Chain: For Every $100, Cloud Takes $35-40 and Inference Margins Hit 65%\""
date: 2026-08-31 09:00:00 +0800
permalink: /barclays-ai-profit-chain-cloud-tax-inference-margin-en/
tags: [Barclays, AI profit, profit chain, cloud providers, inference margin, AWS, Azure, Google Cloud, Goldman Sachs, token economics, NVIDIA]
categories: [AI Industry Analysis]
image: /assets/images/barclays-ai-profit-chain-cover.png
description: "\"Barclays' August 28 research note — 'A Primer on AI Lab & AI Hyperscaler Unit Economics' — traces a complete AI profit chain: for every $100 an AI lab earns, $35-40 flows to the Big Three clouds, which pocket $10-20 in operating profit at 34-47% margins. The real surprise is on the model side — paid inference margins jumped from low-teens in 2025 to 48-65% in 2026, with API inference exceeding 80%. But add training costs back, and most labs are barely breaking even or still losing money. Goldman Sachs' July report on Chinese AI labs shows EBIT of -30% to -39%. This piece lays both ledgers side by side.\""
author: Wisely Chen
---

In 2024, AI labs globally generated $7 billion in revenue, and the industry was still debating whether AI could make money at all.

In 2026, Barclays estimates that number at $137 billion. Their [research note published August 28](https://cryptobriefing.com/barclays-ai-revenue-cloud-providers/) — titled "A Primer on AI Lab & AI Hyperscaler Unit Economics" — doesn't dissect any single company's financials. It traces a complete profit chain: for every $100 an AI model company earns, how does the money flow between layers, and what margin does each layer capture?

The conclusion is blunt: every layer is making money. More than anyone expected in 2024.

---

## The Profit Map: How $100 Splits

Barclays models two hypothetical frontier labs: Lab A is API-heavy (70% of revenue), Lab B is subscription-heavy (80% of revenue). Here's the split:

| Item | Lab A (API-driven) | Lab B (Subscription-driven) |
|------|:--:|:--:|
| Lab revenue | $100 | $100 |
| Flows to cloud (AWS/Azure/GCP) | $35 | $41 |
| Cloud operating profit | $11.80 | $19.10 |
| Cloud margin | 34% | 47% |

For every $100 an AI lab earns, $35-40 goes to the Big Three — AWS, Azure, Google Cloud.

The clouds pocket $10-20 in operating profit, at margins of 34% to 47%. That's after power costs, GPU depreciation, everything. Subscription models (Lab B) let clouds earn more because stable inference workloads push infrastructure utilization higher.

An analogy: the Big Three are the water meters behind the AI industry. The more inference a model company runs, the faster the meter spins. And the meter's gross margin is close to 50%.

---

## The Real Surprise Is on the Model Side

Clouds making money is no surprise — selling shovels during a gold rush has always worked. What makes this profit chain exceed expectations is the model layer itself.

Barclays' numbers: paid inference margins jumped from low-teens in 2025 to 48-65% in a single year.

The breakdown is even more striking:

| Product Type | 2025 Inference Margin | 2026 Inference Margin |
|---------|:--:|:--:|
| Subscription | Low teens | ~70% |
| Direct API | Low teens | >80% |

API inference margins exceed 80%.

This means every time Anthropic's Claude or OpenAI's GPT processes an API call, after deducting cloud fees and compute costs, over 80% of revenue is profit. A year ago, that number was in the low teens.

Barclays attributes the margin jump to five forces hitting simultaneously:

1. **Demand pull**: Enterprise customers and agentic workflows became "must-haves," driving inference volume up
2. **API price increases**: Frontier labs are raising prices, not cutting them
3. **Token efficiency gains**: Completing the same task requires fewer tokens
4. **Inference infrastructure optimization**: Quantization, speculative decoding, and next-gen hardware keep pushing per-inference costs down
5. **Scale effects**: Revenue growing from $7B to $137B dilutes fixed costs

The first two are the revenue story (selling more, selling higher). The last three are the cost story (spending less). All five pushing at once is how margins jump from the teens to the sixties.

---

## The Scale of the Flywheel

High margins are only half the story. The other half is scale.

| Year | Global AI Lab Revenue | Training Spend as % of Revenue |
|------|:--:|:--:|
| 2024 | $7B | 96% |
| 2026 | $137B (est.) | 48% |
| 2028 | $690B (proj.) | 30% |

In 2024, training consumed 96% of revenue — nearly every dollar went to training the next model. By 2026, that ratio drops to 48%. Not because training got cheaper, but because inference revenue grew too fast.

Barclays estimates annualized recurring revenue at roughly $200 billion by end of 2026. Adjusted gross margins increased 30-50 percentage points year over year.

One sentence: training is capex, inference is the money printer. The printer is now running.

---

## Goldman Sachs' Other Ledger: Same Industry, Opposite Numbers

If you only read Barclays, the story is "AI is printing money everywhere." But Goldman Sachs' report from last month paints a completely different picture.

[Goldman's Ronald Keung team published a 50-page deep dive on Chinese AI models in July](/goldman-sachs-china-ai-moe-token-price-war-agent-coding/), estimating: Chinese top-tier model EBIT at -30% for agentic scenarios, -39% for coding. Goldman projects breakeven no earlier than 2030.

Barclays says 65% margins. Goldman says -30% margins.

Both numbers are true at the same time, because they're measuring different populations.

Barclays is measuring frontier labs — Anthropic, OpenAI, Google DeepMind — companies running inference on the Big Three clouds, selling API and subscriptions at prices that include profit. Claude API charges $10-50 per million output tokens depending on model tier. The pricing itself contains margin.

Goldman is measuring Chinese model companies — DeepSeek, Zhipu, Tongyi. Their strategy is the exact opposite: lose money on pricing to win market share. DeepSeek V4 Flash API output costs $0.28 per million tokens — less than one-tenth of Anthropic's cheapest model. Chinese models captured [85% of agent tokens and 89% of coding tokens on OpenRouter](/goldman-sachs-china-ai-moe-token-price-war-agent-coding/), at the cost of losing $0.30-0.40 for every dollar of revenue.

**Profit didn't disappear from AI — it concentrated in the hands of those with pricing power.** Those with pricing power are frontier labs. Those without are buying market share with losses. Laid side by side, global AI profit distribution is far more extreme than any single report shows.

---

## But Are Frontier Labs Actually Profitable? Add Training Back

Inference margins of 48-65% sound like a money printer. But Barclays' inference margin deducts cloud costs and compute — **it doesn't deduct training**.

Training spend as a percentage of revenue is 48% in 2026. Add it back, and the math changes:

| | Adjusted Gross Margin | Less: Training % of Revenue | Net per $100 |
|---|:--:|:--:|:--:|
| Lab A (API-driven) | ~55% | 48% | ~$7 |
| Lab B (Subscription-driven) | ~38% | 48% | ~-$10 |
| Big Three Clouds | 34-47% | 0% | $10-20 |

Lab A earns $100, deducts cloud fees, inference costs, and training, and has about $7 left. Lab B is still negative — training consumes all gross margin and then some.

The Big Three don't train models. They don't bear R&D risk. They collect water fees. Whether model companies profit or bleed, the meter keeps spinning.

**Who's making money, who's losing:**

- **Big Three Clouds: Steady profit.** $10-20 per $100, at 34-47% margins, and this profit is independent of which model generation wins — the next model still runs on their infrastructure.
- **Frontier labs (API-driven): Barely breaking even.** Inference prints money, but training burns most of it. Lab A's $7 profit is paper-thin — one training budget expansion could wipe it out.
- **Frontier labs (Subscription-driven): Still losing.** Subscriptions let clouds extract more (47% vs 34%), leaving less gross margin for the lab. After training, it's negative.
- **Chinese model companies: Deep losses.** Goldman estimates EBIT -30% to -39%, breakeven projected for 2030. They're losing money on inference alone, let alone training.

The frontier lab strategy is to use inference profits to subsidize training — training went from 96% of revenue in 2024 to 48% in 2026, not because training got cheaper, but because inference revenue grew too fast. But "inference subsidizes training" and "overall profitability" are two different things. The inference side is printing money. The training side is burning it. Net: Lab A barely breaks even, Lab B is still in the red.

**The real winner across the entire profit chain is the cloud.** They don't need to bet on which model wins. They don't bear the risk of a failed training run. As long as AI inference keeps running on their infrastructure, the meter keeps spinning.

---

## Behavioral Evidence: Industry-Wide Pricing Migration — Kill Subscriptions, Push Token Billing

If Barclays' profit model is right — API billing (Lab A) gross margin 55%, subscription (Lab B) only 38% — then the rational move for model companies is to push customers from subscriptions to API billing as hard as possible.

Over the past year, that's exactly what they did.

| Company | Product | Date | Change |
|---------|--------|------|--------|
| Anthropic | Enterprise Claude | 2025/11 → 2026/04 | Bundled tokens → [seat fee + per-token](https://www.theregister.com/2026/04/16/anthropic_ejects_bundled_tokens_enterprise/), no flat-fee for 150+ seats |
| OpenAI | ChatGPT / Codex | 2026/04/02 | Per-message → [token credit billing](https://lilting.ch/en/articles/openai-codex-token-based-pricing-rate-card), Business seat fee dropped from $25 to $20 |
| GitHub | Copilot | 2026/04 → 06 | Fixed quota → [AI Credits (token billing)](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/) |
| Anthropic | Pro / Max (consumer) | [2026/05/13 announced (6/15 paused)](https://www.techtimes.com/articles/317625/20260602/anthropic-ends-subscription-subsidy-agents-june-15-credit-pool-replaces-flat-rate-access.htm) | Flat-rate → credit pool + per-token |
| Google | Gemini Notebook (fmr. NotebookLM) | [2026/08/28 announced](https://9to5google.com/2026/08/28/gemini-notebook-usage-limits/), effective 9/2 | Daily fixed quota → compute-based, 5-hour rolling window + weekly cap |

**Five companies made the same move in the same quarter.** Direction entirely consistent: seat fees and monthly plans become entry tickets; real revenue shifts to per-token or per-compute. This isn't coincidence — it's the inevitable result of profit structure. Barclays' numbers explain why. API billing leaves $17 more gross margin per $100 than subscriptions. At $137 billion in revenue, 17 percentage points is over $20 billion.

---

## The Counter-Case: How Long Can These Margins Last?

Barclays' numbers are a 2026 snapshot. At least five forces push against this being the new normal:

**One: Open-source is closing on the frontier.** [Kimi K3 and GLM-5.3 score 60 on the Artificial Analysis Intelligence Index; Fable 5 scores 62](/not-your-weights-not-your-product-en/). The gap is 2 points. When open-source models approach closed-model capability, enterprise CTOs get alternatives. The day alternatives appear, pricing power starts eroding.

**Two: Chinese models' loss-leader pricing won't last forever, but it'll lower global price expectations before it ends.** DeepSeek V4 Flash's $0.28/M tokens has already anchored agent and coding pricing. Even if Chinese models raise prices later, the market's expectation of "fair token pricing" has been permanently pulled down.

**Three: On-premise inference is pushing marginal cost toward zero.** This blog [covered the Beijing AGI Bar case](/agi-bar-free-token-dgx-spark-inference-infrastructure/): two DGX Sparks ($9,400 total) running V4 Flash, annualized cost ~$3,500, after which only electricity remains. When hardware is amortized once and per-token marginal cost approaches zero, cloud API profit faces structural pressure.

**Four: Frontier labs are leaving the cloud.** Barclays assumes $35-40 flows to the Big Three, but frontier labs can read the same ledger — losing $35-40 to clouds that earn 34-47% margin while you're left with $7 or -$10. The rational response is to build your own data centers. OpenAI launched [Project Camellia (Georgia, 3.2GW)](https://builtin.com/articles/openai-cloud-deals) plus Stargate (7GW, $4,000B+), with infra budget reaching $750B through 2030. Anthropic signed a [$50B Fluidstack data center deal](https://www.techcrunch.com/2025/11/12/anthropic-announces-50-billion-data-center-plan/) and in August 2026 formed the [Theseus Infrastructure JV](https://enterprisedna.co/resources/news/anthropic-theseus-infrastructure-macquarie-gic-data-centers-2026/) with Macquarie and GIC. xAI built from scratch — Memphis Colossus is at 1GW, 550,000 GPUs. Google DeepMind runs on Google's own TPUs. Meta trains all Llama models in its own facilities. The cloud's water-meter business is good for now, but its biggest customers are installing their own pipes.

**But the clouds aren't sitting still — they have a three-layer defense.**

The first layer is **equity lock-in**. Amazon has invested [$33B in Anthropic](https://www.forbes.com/sites/jonmarkman/2026/04/22/amazon-33-billion-anthropic-deal-and-the-limits-of-ai-infrastructure/). Microsoft has put $13B+ into OpenAI and locked in [$250B in Azure commitments](https://techcrunch.com/2026/07/29/microsoft-is-openly-competing-with-openai-anthropic-more-than-ever/) through 2032. Even if frontier labs build their own data centers, clouds profit as shareholders. Investment isn't just a cloud play — it's a hedge.

The second layer is **custom chip migration costs**. AWS Trainium has [$20B in annualized revenue](https://cryptobriefing.com/amazon-trainium-chip-20b-revenue/) and over $225B in committed revenue. Anthropic and OpenAI both signed multi-year contracts. Google has sold 1 million TPUs to Anthropic; Gemini trains entirely on TPUs. Models trained on Trainium/TPU face enormous switching costs — it's not just moving data, it's re-adapting the entire training stack.

The third layer is **building their own models**. Microsoft [gained the freedom to build its own models](https://www.cnbc.com/2026/06/02/microsoft-unveils-new-ai-models-lessen-reliance-on-openai-lower-costs.html) in September 2025 and in 2026 launched MAI-Code-1-Flash, MAI-Thinking-1, and other in-house models. Amazon's AGI team has been tasked with building models that surpass Claude. Google's Gemini was always their own. The Big Three's message is clear: you won't run on my cloud? I have my own models.

Add multi-model platforms — Bedrock, Vertex AI, Azure Foundry — hosting Claude, Llama, Gemini, Mistral simultaneously. Enterprises can switch models without switching clouds. That's a retention mechanism by itself.

None of these five forces has yet broken frontier labs' margins. But they're all pushing in the same direction at once. Barclays' 65% is the margin right now, not a floor. And the clouds' 34-47% margin is not steady-state either — it's simultaneously threatened by customer self-build and protected by three layers of defense. The fight is still in progress.

---

## Reality Check

This report has several limitations worth knowing.

**Barclays' unit economics model is hypothetical, not any company's actual financials.** Lab A and Lab B are stylized archetypes, not Anthropic or OpenAI's real cost structures. The real numbers aren't public — these companies haven't IPO'd. So the 34% and 47% cloud margins are estimates, not audited figures.

**"$137 billion global AI lab revenue" has unclear boundaries.** Which companies are included? How is "AI lab" defined? Does Google Cloud's AI revenue count? Microsoft Copilot? Internal AI inference that doesn't touch external APIs? The secondary reporting doesn't specify. $7B to $137B may be directionally right, but definitional boundaries significantly affect the scale impression.

**Inference margins of 48-65% are an industry median, not universal.** Frontier labs selling API may exceed 80%, but smaller model companies or those with aggressive pricing strategies could have much lower margins. Medians hide distributions.

But it gets one thing right: **for the first time, it breaks AI profit down from "are model companies profitable?" to "how much does each layer earn?"** Everyone has been watching training costs for three years. Inference economics are only now being laid open. Knowing that clouds extract $35-40 from every $100 and earn close to 50% on it — that's useful arithmetic for anyone deciding between self-hosting and API.

---

## Key Takeaways

**One: AI industry profit structure is now calculable.** In 2024, only training costs were knowable; revenue was guesswork. In 2026, inference revenue, cloud commissions, and per-layer margins all have estimation frameworks. Disagree with Barclays' numbers if you want — what matters is you can now plug your own numbers into this framework to calculate how much of your API bill is cloud profit, how much is model profit, and how much room self-hosting could save.

**Two: The cloud tax is real, and subscriptions pay more of it.** Lab B's (subscription-heavy) cloud margin is 47%; Lab A's (API-heavy) is 34%. If you're an enterprise CTO using subscription AI products (Copilot, Claude Pro), close to half of what you pay is cloud profit. That number belongs in your build-vs-buy spreadsheet.

**Three: Profit concentrates in those with pricing power.** Barclays' 65% and Goldman's -30% coexist. The difference isn't technology — it's pricing power. Frontier labs with pricing power are printing money. Chinese models without it are buying share with losses. Your decision depends on which inflection point you're betting on: Chinese models reaching breakeven by 2030, or open-source models closing that 2-point gap.

---

## Three-Way Battle Royale, One Arms Dealer

Spread all the moves across the board, and this isn't a single profit chain — it's a three-way battle royale where every player is simultaneously fleeing from and locking in the other two:

**Users** get pushed toward API billing (bigger bills) → respond by going on-premise, embracing open-source and sovereign AI → labs lose pricing power. **Labs** get $35-40 extracted by clouds → push users to API for better margins while building their own data centers to escape cloud fees → but capex explodes and users revolt. **Clouds** carry massive capex for data centers → use custom chips (Trainium, TPU) to lock labs in, equity stakes to hedge defections, own models as plan B → become direct competitors to labs.

Every player's defensive move is a new threat to the other two. The cycle never stops.

But no matter who wins this battle royale, one player is sitting comfortably.

| Player | Position | Margin |
|--------|----------|--------|
| NVIDIA | Sells GPUs to everyone | [~60%+ gross, 80-85% AI chip market share](https://presenc.ai/research/ai-chip-market-share-2026) |
| Cloud | Water meters, three-layer defense | 34-47% |
| Frontier labs (API) | Inference prints but training burns | ~7% net |
| Frontier labs (Subscription) | Squeezed from both sides | -10% net |
| Chinese models | Buying share with losses | -30% to -39% |

Users go on-premise — buy NVIDIA GPUs. Labs build data centers — buy NVIDIA GPUs. Clouds expand — buy NVIDIA GPUs. NVIDIA FY2026 data center revenue: [$193.7B](https://www.datacenterdynamics.com/en/news/nvidia-reports-record-data-center-revenues-of-623bn-up-75-yoy/), Q2 2026 alone $89B, YoY +117%.

And it's not just NVIDIA. OpenAI has purchased tens of thousands of Mac minis and Mac Studios to train Computer-Use Agents via reinforcement learning. Anthropic is renting Mac minis through AWS. Training AI to operate computers requires buying computers first. Apple is also selling shovels.

**The further upstream, the more you earn.** NVIDIA sells shovels, clouds sell water, labs mine gold, Chinese models lose money to acquire users. The only threat to NVIDIA is custom chips — Trainium and TPU have taken 15-20% market share with 40-65% TCO advantages — but those chips are exclusive to the cloud that makes them. For everyone who isn't a hyperscaler, the only option is still NVIDIA.

The shovel sellers don't need to run.

---

## FAQ

**Q: What is the core finding of this Barclays research note?**

Barclays' August 28, 2026 research note — "A Primer on AI Lab & AI Hyperscaler Unit Economics" — traces a complete AI profit chain: for every $100 an AI model company earns, $35-40 flows to the Big Three cloud providers (AWS, Azure, Google Cloud), which pocket $10-20 in operating profit at 34-47% margins. On the model side, paid inference margins jumped from low-teens in 2025 to 48-65% in 2026, with direct API inference exceeding 80%. Global AI lab revenue grew from $7 billion in 2024 to an estimated $137 billion in 2026.

**Q: Why did AI inference margins jump so dramatically in one year?**

Barclays identifies five simultaneous forces. On the revenue side: enterprise customers and agentic workflows became essential, driving inference demand up sharply; meanwhile, frontier labs raised API pricing rather than cutting it. On the cost side: model token efficiency improved so the same task requires fewer tokens; inference infrastructure optimization (quantization, speculative decoding, next-gen hardware) keeps lowering per-inference costs; and scale effects mean global AI lab revenue growing from $7B to $137B in two years dilutes fixed costs across a much larger revenue base. Revenue up, costs down, both at the same time — that's how margins jump from the teens to the sixties.

**Q: Barclays says 65% margins but Goldman Sachs says Chinese models lose 30% — how can both be true?**

They're measuring different populations. Barclays measures frontier labs (Anthropic, OpenAI, Google DeepMind) — companies running inference on the Big Three clouds, selling API and subscriptions at profitable price points. Goldman measures Chinese model companies (DeepSeek, Zhipu, Tongyi) whose strategy is loss-leader pricing for market share — DeepSeek V4 Flash API output costs $0.28 per million tokens, less than one-tenth of Anthropic's cheapest model. Profit didn't disappear from AI — it concentrated in the hands of those with pricing power.

**Q: What does this report mean for enterprises choosing between API and self-hosted inference?**

Barclays' unit economics show that for every $100 spent on AI through API, $35-41 goes to cloud providers, of which nearly half is cloud profit. Subscription models let clouds extract even more (47% vs 34% margin). This means that if an enterprise's AI usage is large enough, self-hosting saves not just the model company's margin but also the cloud layer's ~50% margin. However, self-hosting requires GPUs, an ops team, and ongoing model updates as capex — whether it makes sense depends on usage volume and technical capability.

---

## Sources

- [CryptoBriefing: Barclays report on cloud providers' AI revenue](https://cryptobriefing.com/barclays-ai-revenue-cloud-providers/)
- [AllWeatherFinance: AI profit structure analysis](https://allweatherfinance.com/ai-profit-structure-for-every-100-in-revenue-generated-by-model-companies-35-40-flows-to-cloud-providers-bringing-them-10-20-in-operating-profit/)
