---
layout: post
title: "NemoClaw 架構拆解：NVIDIA 怎麼把龍蝦鎖進三層安全堡壘"
date: 2026-03-21 13:00:00 +0800
permalink: /nemoclaw-architecture-deep-dive/
image: /assets/images/nemoclaw-slide-cover.png
description: "NemoClaw 不是「OpenClaw 外面包一層 Docker」。它是一整個 K3s Cluster，用 netns + HTTP CONNECT proxy + OPA Policy、seccomp BPF、Landlock LSM 三層安全機制，把 AI Agent 鎖進企業級沙箱裡。這篇拆解架構設計、Trust Boundary、Per-Binary Egress Control，以及代價與價值的取捨。"
---

# NemoClaw 架構拆解

![NemoClaw 企業級 AI 代理架構解析](/assets/images/nemoclaw-slide-cover.png)

> **相關資源：**
> - [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) — 主 repo（Apache 2.0）
> - [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) — 底層 sandbox runtime
> - [NVIDIA Agent Toolkit](https://developer.nvidia.com/agent-toolkit) — NemoClaw 所屬的工具生態

## NemoClaw 的底層：不是「包一層 Docker」，是一整個 K3s Cluster

很多人聽到 NemoClaw 以為只是「OpenClaw 外面包一層安全殼」。不是。

先說結論：**NemoClaw 是把原版龍蝦裝進一個 K3s 控制的 Sandbox 裡面跑。** K3s 不是外掛，是直接嵌在同一個 container image 裡。啟動時走 Blueprint Runner 的 `resolve → verify → plan → apply` 四個階段，確保每次部署都有明確的生命週期。

這跟你自己用 Docker 跑 OpenClaw 完全是兩回事。

![Blueprint Runner 部署生命週期：迷思 vs 架構重構](/assets/images/nemoclaw-slide-blueprint.png)

## 三個核心元件，完全隔離

K3s cluster 裡面跑三個核心元件：

| 元件 | 職責 | 位置 |
|------|------|------|
| **Gateway API** | Control plane，協調一切 | K3s cluster 內 |
| **Policy Engine** | 管理所有安全 policy | K3s cluster 內 |
| **Privacy Router** | 攔截所有往外部 LLM 的 inference 請求，路由至 [NVIDIA NIM](https://build.nvidia.com/) 或本地 vLLM | K3s cluster 內 |

Agent 本身呢？跑在**獨立的 Sandbox Pod** 裡，跟這三個元件完全隔開。

![空間拓撲：控制面與沙盒的徹底切割](/assets/images/nemoclaw-slide-topology.png)

這個設計很關鍵：Agent 看不到 Policy Engine 的資料，摸不到 Gateway API 的控制面。就算 Agent 被 prompt injection 攻破了，它能做的事情被三層安全機制鎖死。

## 安全三層：各自獨立，互相強化

這是 NemoClaw 最值得看的地方。三層安全機制，每一層獨立運作，任何一層被繞過，另外兩層還在。

### 第一層：網路隔離（netns + HTTP CONNECT proxy + OPA Policy）

每個 sandbox pod 有獨立的 [network namespace](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)（veth pair: `10.200.0.1 ↔ 10.200.0.2`）。Agent 發出的**所有 TCP 連線**都被強制導向 HTTP CONNECT proxy，再由 [OPA（Open Policy Agent）](https://www.openpolicyagent.org/) 進行應用層的 policy 判斷。

這比傳統的 iptables 規則更強——不只是網路層的 allow/deny，而是可以根據請求的目標 URL、binary 來源等做**語意級別**的存取控制。

Agent 層面完全感知不到，也沒有辦法繞過——因為 netns 本身就是隔離的網路視角，Agent 看不到 host 的網路介面。

白話講：**Agent 以為自己在上網，其實每個請求都經過一個懂規則的安檢門。**

![第一層防護：語意級網路隔離](/assets/images/nemoclaw-slide-network.png)

### 第二層：系統呼叫封鎖（[seccomp BPF](https://docs.kernel.org/userspace-api/seccomp_filter.html)）

seccomp BPF filter 在 sandbox pod **建立時套用，之後直接鎖死**。具體來說，filter 是在 child process 的 `pre_exec`（`fork()` 之後、`exec()` 之前）階段套用，套用後**不可變更**。

這個 filter 宣告的是 allowlist 模式——針對有安全疑慮的 syscall 封鎖，而且可以針對同一個 syscall 的不同參數做精細控制。

白話講：**Agent 能呼叫的作業系統功能被列清單管控，清單之外的一律拒絕。**

![第二層防護：系統呼叫封鎖 seccomp BPF](/assets/images/nemoclaw-slide-seccomp.png)

### 第三層：檔案系統（[Landlock LSM](https://docs.kernel.org/security/landlock.html)）

[Landlock](https://landlock.io/) 是 Linux Security Module。`openshell-sandbox` supervisor 在 sandbox 啟動時透過 gRPC 向 Policy Engine 動態拿 Landlock policy，套用之後**鎖死，無法修改**。

可讀寫的路徑只有：`/sandbox`、`/tmp`、`/usr`、`/lib`、`/etc` 這些系統路徑。其他路徑對 Agent **完全不可見**。

白話講：**Agent 的世界被縮小到一個房間裡，其他房間的門不是鎖起來——是根本不存在。**

![第三層防護：Landlock LSM 檔案系統隱形](/assets/images/nemoclaw-slide-landlock.png)

## Trust Boundary 設計：Agent 連 Policy 都看不到

這裡有個設計值得特別拿出來講。

Agent 和 Policy Engine 跑在不同的 pod，各自有獨立的：
- **PID namespace**（看不到對方的 process）
- **mount namespace**（看不到對方的檔案系統）
- **network namespace**（看不到對方的網路）

Policy Engine 的資料靠 mount namespace 對 Agent 完全不可見，再加上 Landlock 雙重保護。

這代表什麼？**Agent 即使有辦法逃逸到其他 pod，也無法看到或影響管理自己的 policy。** 不是靠 Prompt 說「不准改 policy」——是架構上做到不可能。

這就是我一直在講的：**Prompt 負責引導，工程負責約束。** NemoClaw 在這個層面做得很到位。

![Trust Boundary：互不相見的隔離空間](/assets/images/nemoclaw-slide-trust-boundary.png)

## 跟 Docker / VM 最大的差異：Per-Binary Egress Control

如果你只用 Docker 跑 OpenClaw（就像我之前做的），你的網路控制粒度是 container 級別——整個容器能不能連外網。

NemoClaw 不一樣。它的 **Network Egress Policy 是 YAML 定義的 allowlist，每個 binary 各自有獨立的對外規則。**

舉例：你可以讓 `curl` 只能連 `api.anthropic.com:443`，但 `node` 只能連 `localhost:11434`（本地 Ollama）。不是容器級別的規則，是**程式級別**的規則。預設的推論模型是 [`nvidia/nemotron-3-super-120b-a12b`](https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b)，透過 Privacy Router 統一路由。

而且 policy 支援 **hot-reload**——不需要中斷 Agent 就可以更新 policy。

（補充：目前 port 8080 還沒有對應的 NetworkPolicy，這是一個已知的 gap。）

![Per-Binary Egress Control](/assets/images/nemoclaw-slide-egress.png)

## 代價：記憶體和複雜度

坦白說，這套架構不是免費的。

K3s cluster + 三層安全機制 + 獨立的 Policy Engine pod = **記憶體消耗會比原版 OpenClaw 高不少**。建議至少 8GB 以上。

如果你只是個人用途、一隻龍蝦、信任自己的網路環境——原版 OpenClaw 可能就夠了。

但如果你是企業，跑多個 Agent、處理敏感資料、需要合規——這個 overhead 完全值得。K3s 的好處是**天生支援 multi-tenant**，多加幾個 Agent 進去不需要動 infrastructure，對平行擴展很方便。Sandbox pod 是透過 [Kubernetes CRD](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) 管理的，在 `agent-sandbox-system` namespace 底下，架構上就是為了多 Agent 而設計。

![架構對決：傳統 Docker vs NemoClaw K3s](/assets/images/nemoclaw-slide-comparison.png)

![代價與價值：企業基礎設施的必然抉擇](/assets/images/nemoclaw-slide-tradeoff.png)

---

## 架構圖速讀

![NemoClaw 縱深防禦全景圖](/assets/images/nemoclaw-slide-defense.png)

![NemoClaw 架構圖](/assets/images/nemoclaw-architecture-diagram.png)

```
User → NemoClaw CLI → Blueprint Runner (resolve → verify → plan → apply)
  ↓
Gateway Docker Container
  ↓ openshell gateway start
K3s Cluster
  ├── Gateway API (control plane)
  ├── Policy Engine ──── allow/deny ────→ Sandbox Pod
  ├── Privacy Router ───────────────────→ NVIDIA Cloud / Local NIM / Local vLLM
  │
  └── Sandbox Pod（隔離）
       ├── netns + HTTP CONNECT proxy + OPA Policy
       ├── seccomp BPF (allowlist)
       ├── Landlock (filesystem)
       │
       └── OpenClaw Agent
            ├── HTTP CONNECT proxy（所有流量經過）
            ├── File System（只能看到 /sandbox, /tmp, /usr, /lib, /etc）
            ├── Network Egress Policy (YAML allowlist, per-binary)
            └── Terminal User Interface (TUI)
```
