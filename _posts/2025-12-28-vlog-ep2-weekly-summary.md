---
layout: post
title: "VLog EP2｜12/22-12/27 週報：AI 記憶突破、企業落地、法規合規"
date: 2025-12-28 10:00:00 +0800
permalink: /vlog-ep2-weekly-summary/
image: /assets/images/vlog-ep2-cover.jpg
description: "VLog 第二期週報。這週發佈 6 篇文章：Google Nested Learning 記憶突破、Gemini Flash 霸榜真相、企業地端 LLM 架構、Excel AI 混淆方案、台灣 AI 基本法解讀、AI Agent 完整指南。"
---

## VLog EP2｜本週文章總結（12/22-12/27）

<iframe width="560" height="315" src="https://www.youtube.com/embed/XnwRcF5FqYY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

這週我發佈了 6 篇文章，主題涵蓋 AI 記憶突破、企業落地實戰、法規合規，以及一張聖誕卡。

### 技術前沿

**[Google Nested Learning](/nested-learning-ai-memory/)** 是這週最重量級的技術解讀。Google 在 NeurIPS 2025 發表的這個研究，試圖讓 LLM 像人類大腦一樣擁有多層記憶系統——不是靠擴大 context window，而是重新定義「什麼是模型」。我在文中用「睡眠記憶鞏固」來類比，說明為何這可能是 Agent 時代最需要的底層能力。

**[Gemini 3.0 Flash 霸榜真相](/gemini-flash-evolution-path/)** 解析了一個反直覺的現象：為何「較弱」的 Flash 模型在多項測試中贏過 Pro？答案是 Flash 不是 Pro 的簡化版，而是另一條進化路線——專注於長上下文場景中「會抓重點、會用記憶」的能力。

### 企業落地

**[企業地端 LLM 架構藍圖](/local-llm-enterprise-architecture/)** 是一篇「很無聊但很實用」的架構文，完整解析 Auth Gateway 權限控管、Orchestrator 任務協調、Python 沙盒安全執行、雙層 Log 審計架構，附 Ollama + LiteLLM + Langfuse 實例。

**[企業 Excel AI 混淆方案](/excel-ai-obfuscation/)** 解決一個真實痛點：企業不允許上傳敏感資料，但又想用 AI 做 Excel 分析。我提出的解法是「混淆」——把部門名稱變成亂碼中文，但保持數據結構不變，這樣 AI 還是能做分析，但看不懂你在算什麼。

### 法規與 Agent 整合

**[台灣人工智慧基本法解讀](/taiwan-ai-basic-act-engineering-perspective/)** 從 IT 主管角度分析 12/23 三讀通過的 AI 基本法，提供 RBAC、Audit Trail、Prompt Injection 防護等 Quick Win 清單。

**[AI Agent 完整指南](/ai-agent/)** 是這週的整合性大作，把過去幾個月的 Agent 系列文整理成完整導覽，涵蓋架構選擇、安全威脅（94.4% 攻擊成功率）、企業落地三大主題。

### 輕鬆一下

**[聖誕賀卡製作過程](/christmas-card-gemini-nanobanana-2025/)**——用 Gemini 寫提示詞、NanoBanana 產圖，10 分鐘完成專屬賀卡。完整記錄了「AI 協作創作」的真實體驗。

---

## 本週文章連結

**技術前沿**
- [Google Nested Learning：AI 終於可以「記住」東西了？](/nested-learning-ai-memory/)
- [Gemini 3.0 Flash 不講理霸榜的真相](/gemini-flash-evolution-path/)

**企業落地**
- [企業級地端 LLM 架構完整藍圖](/local-llm-enterprise-architecture/)
- [都要 2026 年了，企業 AI Excel 還是這麼難搞](/excel-ai-obfuscation/)

**法規與 Agent**
- [台灣人工智慧基本法｜IT 主管必讀](/taiwan-ai-basic-act-engineering-perspective/)
- [AI Agent 完整指南｜架構、安全與企業落地](/ai-agent/)

**輕鬆一下**
- [祝大家聖誕快樂（Gemini + NanoBanana 製圖過程）](/christmas-card-gemini-nanobanana-2025/)
