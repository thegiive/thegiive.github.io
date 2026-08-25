---
layout: post
title: "No Model Swap, No Fine-Tuning: Let Open-Source Models Read Their Own Neural Layers to Self-Verify — LLM-as-a-Verifier"
date: 2026-08-25 12:00:00 +0800
permalink: /verification-scaling-llm-as-a-verifier-terminal-bench-en/
image: /assets/images/verification-scaling-terminal-bench-2-1.png
description: "A Stanford + UC Berkeley paper shows how open-source models can read their own logits to self-verify, jumping DeepSeek V4 Flash from 79% to 88% on Terminal-Bench 2.1. The framework naturally favors on-prem deployment — it needs full logits access and burns 10-15x tokens, making it the sweet spot for open-weight models on your own GPUs."
---

A new paper from Stanford and UC Berkeley — [LLM-as-a-Verifier](https://arxiv.org/abs/2607.05391), authored by Chelsea Finn, Ion Stoica, Azalia Mirhoseini, and others — found a way to push open-source models one notch higher.

No larger model needed. No additional training.

The method: run each problem five times, then look inside the model's brain — read the probability distribution from its neural layers — to self-verify and pick the best answer.

DeepSeek V4 Flash scores 79% on Terminal-Bench 2.1 in a single pass. With five passes plus self-verification, it jumps to 88%. Same model, purely an inference strategy upgrade, nine percentage points gained.

---

## The Numbers

![Terminal-Bench 2.1 cost-efficiency comparison](/assets/images/verification-scaling-terminal-bench-2-1.png)

| Setup | Success Rate | Cost / Task | Agent Harness |
|-------|:------:|:---------:|:----------:|
| DeepSeek V4 Flash x1 + self-verify | ~79% | ~$0.05 | mini-swe-agent |
| DeepSeek V4 Flash x3 + self-verify | ~86% | ~$0.20 | mini-swe-agent |
| DeepSeek V4 Flash x5 + self-verify | ~88% | ~$0.30 | mini-swe-agent |
| GPT-5.6 Luna (Codex) | ~81% | ~$0.50 | Codex |
| GPT-5.6 Terra (Codex) | ~84% | ~$1.00 | Codex |
| Opus 4.8 (Claude Code) | ~80% | ~$1.50 | Claude Code |
| Fable 5 (Claude Code) | ~83% | ~$2.00 | Claude Code |
| GPT-5.6 Sol (Codex) | ~88% | ~$2.00 | Codex |

The 88% beats Fable 5's 83% and matches GPT-5.6 Sol's 88%. But the three groups use different agent harnesses (mini-swe-agent / Codex / Claude Code), so you can't attribute the entire gap to the verification strategy. **Look at the trend within a single model** — the three red dots share the same harness, and the 79% to 86% to 88% climb is solid.

---

## Core Mechanism: Reading Logits from the Neural Layer

Generating multiple candidate solutions is easy. The hard part is knowing which one is best.

The traditional approach, LLM-as-a-Judge, asks the model to score each answer on a 1-5 scale. Problem: on complex coding tasks, over 27% of scores tie. Two solutions of clearly different quality both get a 4. Discrete scales lack the resolution.

LLM-as-a-Verifier takes a different approach. Instead of looking at the token the model outputs, it looks one layer deeper — at the logits.

When an LLM generates each token, it doesn't just "decide to output 7." It first computes a probability distribution over all candidate tokens. When asked "Rate this solution 1-10," the model's internals already have:

> "7" probability 0.35, "8" probability 0.40, "6" probability 0.15, "9" probability 0.05...

That probability table is the logits (technically, the probabilities after softmax).

A traditional judge takes only the highest-probability token (argmax), getting a discrete "8." LLM-as-a-Verifier reads out all scoring-token probabilities and computes a weighted average:

> 0.35 x 7 + 0.40 x 8 + 0.15 x 6 + 0.05 x 9 + 0.03 x 5 = **7.3**

The resolution of 7.3 vs 7.1 is far greater than 7 vs 7 (tie). No additional training required. No stronger model needed as judge.

---

## Why Self-Verification Works

Why can a model judge the quality of its own answers?

Because generation and verification are different cognitive tasks. Generation is divergent — writing a solution from scratch. Verification is convergent — judging an existing solution.

Judging whether an answer is correct is easier than producing the correct answer from zero. This is true for humans, and it's true for LLMs.

The probability distribution at the logits level contains richer information than the single token the model finally outputs. The model's internal judgment of answer quality is actually more nuanced than the number it says out loud. LLM-as-a-Verifier simply extracts that nuance.

---

## Three Scaling Dimensions

Continuous scores alone aren't enough. The paper scales along three axes simultaneously, with independently multiplicative effects:

**Score Granularity.** Expand the rating scale from 1-5 to 1-20, giving the logits distribution more room to spread. On Terminal-Bench V2, the tie rate drops from 27% to near zero.

**Repeated Evaluation.** Run K independent evaluations of the same candidate and average them. Monte Carlo averaging washes out single-evaluation bias. K=1 to K=16 improves accuracy from 74.7% to 77.4%.

**Criteria Decomposition.** Instead of asking "Is this correct?" — a big, blunt question — split it into sub-criteria: "Does it meet the spec?" "Is the output format right?" "Are there error messages?" Score each independently and ensemble. Accuracy goes from 75-76% to 78.3%.

Ranking uses a Probabilistic Pivot Tournament (PPT) that reduces complexity from O(N^2) to O(Nk). All three dimensions combined push Terminal-Bench V2 verification accuracy to 86.5%.

---

## Why This Is Especially Useful for On-Prem

The framework has two hard requirements, and both point straight at on-prem deployment:

**First, it needs logits access.** Self-hosted open-weight models (vLLM / SGLang) give you the full logits vector with no restrictions. OpenAI's API exposes only top-5 logprobs — the paper says it works but with reduced performance. Anthropic's API doesn't expose logprobs at all, so Claude cannot serve as a verifier.

**Second, it burns a lot of tokens.** Five generations plus repeated verification plus multi-criteria scoring easily uses 10-15x the tokens of a single pass. On a cloud API, that bill multiplies directly.

On-prem, neither problem exists. The GPU is already paid for. Marginal token cost approaches zero. Logits are fully transparent. Running five passes just costs more inference time, not more money.

Models like Qwen 3.8 27B or DeepSeek V4 Flash (both Intelligence Index = 52) run on a single GPU. Their single-pass capability genuinely trails Fable 5 or GPT-5.6 Sol. But with five passes plus self-verification, they win on Terminal-Bench. Spare GPU compute converts directly into quality.

Cloud users see "6x the token bill." On-prem users see "a free nine-percentage-point upgrade."

---

## Not Just Coding

The framework generalizes across three entirely different domains without domain-specific fine-tuning:

| Domain | Benchmark | Result | Baseline |
|--------|-----------|:------:|:--------:|
| Coding | Terminal-Bench V2 | 86.5% | 83.1% |
| Coding | SWE-Bench Verified | 78.2% | 76.8% best single model |
| Robotics | RoboRewardBench | 87.4% | 81.4% (trained RoboReward-8B) |
| Medical | MedAgentBench | 73.3% | — |

In robotics, it beats a purpose-trained reward model (87.4% vs 81.4%). A general-purpose verification framework, using logits weighting and three-axis scaling, outperforms a specialist model.

The paper also measures progress tracking: the correlation between verifier scores and task step progression (VOC) reaches 0.966 on successful trajectories. The verifier can track whether an agent is on the right path during execution, not just judge pass/fail at the end.

---

## How to Run It

The code is fully open-sourced on [GitHub](https://github.com/llm-as-a-verifier/llm-as-a-verifier).

### Python SDK

```bash
pip install llm-verifier
```

Three core APIs:

```python
import llm_verifier

result = llm_verifier.select(
    problem=problem,
    candidates=candidates,
    criteria={"Correctness": "Does the code solve the problem?"},
)

# Pairwise comparison
reward_a, reward_b = llm_verifier.compare(
    problem, sol_a, sol_b,
    criteria={"Overall": "Does the code solve the problem?"},
)

# Progress tracking: is the agent on the right path mid-execution?
result = llm_verifier.track(
    problem=problem, steps=steps,
    checkpoint_steps=[1, 2, 3, 4, 5], n_evaluations=4,
)
```

### TurboAgent: Drop-in Proxy

[TurboAgent](https://github.com/llm-as-a-verifier/TurboAgent) is an API proxy that sits between your client and LLM provider, automatically doing generate-then-verify:

```bash
pip install turbo-agent
turbo-agent              # default port 8888
ANTHROPIC_BASE_URL=http://localhost:8888 claude
```

### On-Prem

Serve an open-weight model with vLLM and point TurboAgent at it:

```bash
vllm serve Qwen/Qwen3.8-27B --port 8000
```

Same model as both generator and verifier. Marginal cost: near zero.

---

## Limitations

**Needs clear right/wrong.** Terminal-Bench and SWE-Bench have objective pass criteria. Whether self-verification works for ambiguous judgments ("Is the requirement understood correctly?") remains unproven.

**Latency multiplied by N.** Five candidates means five times the generation time (if not parallelized). Fits batch workloads, not real-time interaction.

**Harness differences matter.** The three groups in the chart use different agent harnesses. Cross-harness comparisons should be taken with a grain of salt. The within-model trend is what counts.

---

## Closing Observation

This paper shows that a model's effective intelligence is not a fixed value — it's a function of inference strategy.

Same DeepSeek V4 Flash: single pass 79%, five passes with self-verification 88%. Not a stronger model. A smarter way to use it.

For on-prem deployment, this may be the most pragmatic capability upgrade available right now. No waiting for the next-generation model. No paying for more expensive APIs. Take the open-weight model and GPU you already have, let the model read its own brain, and let it verify itself.

Try it yourself. After all, the most reliable form of verification is still: run it once and see.
