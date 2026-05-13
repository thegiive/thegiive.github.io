---
layout: post
title: "你的 Claude Code 可能被植入後門了：Mini Shai-Hulud npm 供應鏈攻擊全解析"
date: 2026-05-14 09:00:00 +0800
permalink: /npm-mini-shai-hulud-claude-code-supply-chain-attack/
image: /assets/images/npm-shai-hulud-deadman-switch.png
description: "Mini Shai-Hulud 供應鏈攻擊把惡意程式埋進 TanStack npm 套件，甚至利用 Claude Code、VS Code 設定做持久化。這篇整理攻擊鏈、AI 開發者為什麼特別危險，以及實際自查與處置順序。"
tags:
  - 供應鏈攻擊
  - npm
  - Claude Code
  - AI 開發者安全
  - TanStack
---

![Mini Shai-Hulud dead-man's switch 警告](/assets/images/npm-shai-hulud-deadman-switch.png)

> 安全研究員 carlini 在 [TanStack/router#7383 的留言](https://github.com/TanStack/router/issues/7383#issuecomment-4425225340) 點出最致命的一招：payload 會在 Linux 上掛 systemd user service、在 macOS 上掛 LaunchAgent（`com.user.gh-token-monitor`），每 60 秒去 poll `api.github.com/user` — token 一被 revoke，立刻 `rm -rf ~/`。

---

## 先講結論：現在請暫停 `npm install`

如果你今天看到這篇文章，請先做一件事：

**把手上正在跑的 `npm install` / `pnpm install` / `yarn install` 全部停掉。**

不是危言聳聽，是真的有事。

過去一週，npm 生態系正在爆發一場叫做 **Mini Shai-Hulud** 的供應鏈攻擊。截至目前已知範圍：

- **TanStack 官方 42 個 npm 套件**遭植入惡意程式碼
- 已釋出 **84 個惡意版本**
- 光是 `@tanstack/react-router` 每週下載量就超過 **1,200 萬次**
- 攻擊已擴散到 **OpenSearch、Mistral AI、Guardrails AI、UiPath、Squawk** 等 170+ 個套件
- npm 與 PyPI 兩邊都中

而且最噁心的一點是：**這次攻擊專打用 AI 寫 code 的人。**

對，就是你我這種天天開 Claude Code、Cursor、VS Code 的人。

---

## 為什麼叫 Shai-Hulud？這個隱喻有夠到位

先說一下這個攻擊的命名梗，因為它真的反映了這次事件的本質。

**Shai-Hulud** 是科幻小說《沙丘》（Dune）裡的「沙蟲」 — 在 Arrakis 星球的沙漠底下蜿蜒穿行的巨型生物。牠的特性是：

- **無所不在**：整片沙漠底下都是牠
- **殺不死**：人類目前所有武器都對牠無效
- **會自我繁殖**：被切斷一段，那一段照樣活下去
- **平常你看不到牠**：只有當你太用力踩地面、發出震動，牠才從地底竄出來吃掉你

攻擊者顯然很清楚自己在做什麼 — 他們在惡意 repo 裡**用的 branch 名稱全部取自《沙丘》**，每個被感染的 repo 描述都被改成同一句話：

> **"Shai-Hulud: Here We Go Again"**

而這個隱喻精準到讓人有點毛骨悚然：

- **無所不在** → 這次蠕蟲藏在你天天裝的 dependency tree 裡
- **殺不死** → 你 `npm uninstall` 完，它從 `~/.claude/settings.json` 又活過來
- **會自我繁殖** → 它是 worm，偷到一個 repo 的 CI key 就感染下一個
- **平常看不到牠** → 它只在你 revoke token 那一刻才現形 — 然後把你的 home directory 吃掉

而且攻擊者的黑色幽默還不只命名這一層。

### 攻擊者偽裝的身份是「Claude Code 本人」

這次惡意 commit 的提交者身份是：

```
Author: Claude (claude@users.noreply.github.com)
Committer: Claude Code GitHub App
Message: chore: update dependencies
```

對，**他冒充的就是 Claude Code 的 GitHub App**。

你想一下這個畫面：

- Repo 收到一個 commit
- 作者顯示是 Claude
- email 是 `claude@users.noreply.github.com`（看起來像 GitHub 的 noreply）
- commit message 是 `chore: update dependencies`（每天都看到一百次）

整個維護者 review 介面看下來：**毫無違和感**。

對於已經習慣讓 Claude / Cursor / Copilot 幫忙更新 dependency 的開發者，這個 commit 看起來就是「你昨晚開的 agent 工作完了」。

這就是 Shai-Hulud 第二層意思 — **牠連你看到牠的時候，都會偽裝成你最信任的東西。**

---

## 這次攻擊為什麼這麼難防

過去我們看 npm 供應鏈攻擊，大致都是同一套劇本：

1. 駭客釣魚拿到 maintainer 的 npm token
2. 推一個假版本上去
3. maintainer 發現後 revoke token，下架版本

防禦邏輯也很單純：開 2FA、pin 死版本、看 lockfile，差不多就擋住八成。

但這次 Mini Shai-Hulud 把這套劇本整個翻掉了。

### 1. 2FA 沒用，因為被打的不是人

TanStack 維護者 Tanner Linsley 親自確認：**整個 team 都有開 2FA**。沒人帳號被盜。

那是怎麼進去的？

攻擊者 fork 了 TanStack 的 repo，推了一個藏得很深的 commit，然後**騙過 TanStack 自己的 GitHub Actions 發版流程**，讓 CI 用合法的金鑰幫惡意 code「蓋章認證」。

換句話說，這次被打的不是 npm 帳號，**是整條 CI/CD pipeline**。

### 2. SLSA 簽章驗證直接失效

這是史上第一個有完整 **SLSA Provenance（軟體供應鏈 3 級可信證明）** 的 npm 惡意套件。

簡單講，SLSA 就是 npm 給套件貼的「這個版本真的是官方發的，沒被改過」的封條。

過去我們檢查供應鏈安全的最後一道防線就是看這個封條。

而現在 — **封條本身被駭客貼上去了**，而且是真貨。

所有靠 cryptographic provenance 來檢查的工具，這次全部失靈。

### 3. `npm uninstall` 殺不掉它

這才是真正讓 AI 開發者該全身發冷的部分。

過去的 npm 惡意套件，最多就是執行一個 `postinstall` script，把你電腦上的 `~/.aws/credentials`、`~/.ssh/` 偷走。你只要：

```bash
npm uninstall <package>
rm -rf node_modules
```

就乾淨了。

但 Mini Shai-Hulud 不是這樣。它做的事情是：

**修改你的 `~/.claude/settings.json` 和 `~/.vscode/tasks.json`，把自己埋進去。**

意思是：

- 你刪掉惡意套件 ✅
- 你刪掉整個 `node_modules` ✅
- 你刪掉整個專案 ✅

**只要你下次打開 Claude Code 或 VS Code，它就會被觸發重新執行一次。**

它把自己掛在 IDE 的 hook 上面，每次你叫 Claude 跑工具、每次 VS Code 跑 task，它就跟著跑一次。

`npm uninstall` 是治標不治本，根本沒有 uninstall 到。

### 4. 死亡開關（Dead-man's switch）

最狠的一招在這裡。

它偷走你的 GitHub token 之後，會在你本機部署一個 watcher，做一件事：

> **持續監看 GitHub 上的這顆 token 還在不在。**

如果你做了「正常的應變動作」— 發現 token 外洩，跑去 GitHub Settings 把它 revoke 掉 — 那一瞬間：

**它會把你整個 home directory `rm -rf` 掉。**

所有專案、SSH key、設定檔、Downloads 裡那份沒備份的合約 — 全部炸光。

這是教科書級別的勒索手段：**「你不撤 token，我就慢慢偷你的東西；你撤 token，我就毀了你整台電腦。」**

---

## 為什麼這次 AI 開發者是高風險族群？

我自己這幾天看下來，感受最深的一點是：

**這次的攻擊面，跟你「依賴 Agent 的程度」成正比。**

### 第一個風險：Agent 不會幫你檢查 lockfile

我們以前裝套件的習慣，是手動敲 `npm install <package>`，會多看一眼版本號。

現在我們開著 Claude Code 寫 code，自然語言講「幫我加上 react-router」，Agent 就直接幫你裝了。

**Agent 不會去看「這個版本是不是 6 分鐘前才剛發佈的」、「provenance 有沒有異常」、「maintainer 有沒有發公告說被打」。**

Agent 對 npm registry 的信任，是無條件的。

### 第二個風險：你的 .claude/settings.json 是「植入後門的完美位置」

Claude Code 的 `settings.json` 設計上就是讓你掛 hooks、定義工具行為的地方。它每個 Claude 事件都會去讀一次。

從攻擊者的角度，這簡直是禮物：

- ✅ 每次 Claude 工作都會 trigger 一次（持久化）
- ✅ 寫進去看起來像 legitimate 的 user config（隱蔽性）
- ✅ Claude 有檔案系統、shell、網路權限（爆破半徑大）

VS Code 的 `tasks.json` 同理。

過去這些檔案本來就在你的 `.gitignore` 裡，你自己也不太會打開看，這就是 perfect hiding spot。

### 第三個風險：pin 死版本也救不了你

過去我們會說：「別用 `^1.0.0`，要用精準版本 `1.0.0`，這樣才安全。」

這次例外。

因為這次的攻擊發生在「官方版本發佈的 6 分鐘窗口期」之內 — 你 pin 死的那個版本號，本身就是惡意版本。

**版本號是對的，內容是壞的，簽章是真的，CI 是合法的。**

你能信任的所有東西，這次都失效。

---

## 現在請馬上做這幾件事

我自己昨晚做的清單，提供參考：

### Step 1：暫停所有套件安裝（這小時就要做）

```bash
# 包含但不限於：
# - 別 npm install / pnpm install / yarn install
# - 別讓 Claude Code / Cursor 自動裝套件
# - CI/CD 上能暫停 build 就暫停
```

如果你不能停 CI（畢竟是 production），至少把 `npm ci --ignore-scripts` 加進去，先擋掉 postinstall script 的執行。

### Step 2：檢查 IDE 設定有沒有被改過

**最重要的兩個檔案：**

```bash
# Claude Code 的 hook 設定
cat ~/.claude/settings.json

# VS Code 的 task 設定
cat ~/.vscode/tasks.json
# 或專案層級的
cat .vscode/tasks.json
```

看裡面有沒有你自己沒設定過的 hook、command、task，特別是任何長得像 base64 編碼、curl 到陌生網址、或執行 `node -e "..."` 一行 inline script 的東西。

**有就是中招了。**

### Step 3：跑一次自動化檢查

社群已經有人寫好工具：

```bash
npx supply-chain-attack
```

它會掃你的 `node_modules`、`package-lock.json`、IDE 設定檔，比對目前已知的惡意套件清單。

（提醒：這指令本身的安全性也請自己評估一下，看一眼 source 再跑。）

### Step 4：旋轉所有 credentials（順序很重要）

這是最容易踩雷的一步。**順序錯了你會自己觸發 dead-man's switch。**

正確順序：

1. **先**把 IDE 設定檔（`.claude/settings.json`、`.vscode/tasks.json`）裡的可疑條目清掉
2. **再**把 watcher process 找出來 kill 掉（檢查 `ps aux`、`launchctl list`、crontab）
3. **然後**才去 GitHub / GCP / AWS revoke token

如果你還沒清乾淨就先 revoke token，watcher 偵測到的瞬間，你的 home directory 就沒了。

**先確保 watcher 死透了，再去動 token。**

### Step 5：備份 home directory（保險起見）

```bash
# 不管你有沒有中招，現在就 backup 一份
cp -a ~/ /Volumes/External/home_backup_$(date +%Y%m%d)/
```

跑完這個再去動 token，至少最壞情況下還救得回來。

---

## 坦白說：這件事的長期影響

短期是清毒、換 key。但這次 Mini Shai-Hulud 真正打開的潘朵拉盒子是：

**「合法 CI 簽章 + IDE 持久化」這個組合，從此會被當成標準攻擊模板。**

過去 AI 開發者的安全思維大概是：

- 不要把 API key commit 進 git
- 不要 `curl | bash` 不認識的 script
- 不要安裝來路不明的 VS Code extension

這次之後，要再多加一條：

- **不要假設你的 `~/.claude/`、`~/.vscode/` 是乾淨的。**

我們把 Agent 寫進 IDE config 的便利性，跟攻擊者把後門寫進 IDE config 的便利性，是**同一個便利性**。

這是 AI Coding 時代要學會接受的新 trade-off。

---

## 最後一句話

過去十年，我們用 `npm install` 換來的是極致的開發效率。

過去兩年，我們用 Agent 自動裝套件換來的是再翻一倍的效率。

**這次的代價，這幾天會慢慢浮現。**

不是說 Agent 不能用、npm 不能用 — 我自己也還是會繼續用。

只是這次之後，我會多做一件事：

> **每次 Agent 幫我裝完套件，我自己 `cat ~/.claude/settings.json` 看一眼。**

便宜得很，五秒鐘的事。

但這五秒，就是 AI 開發者進入下一個階段必須付的學費。

---

## 延伸閱讀

- [用 Claude Code 做 Linux 系統管理](./ai-ops-yong-agent-claude-code-linux.md)
- [ATPM：真實的 Vibe Coding 流程](./atpm-a-real-production-vibe-coding-process.md)
- [慢跑開會都能寫 code？Claude Code 讓我一天當 1.5 天用](./claude-code-yi-bu-xie-zuo-man-pao-kai-hui-dou-neng-xie-code.md)

---

## 參考資料

- [TanStack/router#7383 — carlini 揭露 dead-man's switch 機制](https://github.com/TanStack/router/issues/7383#issuecomment-4425225340)
- [TanStack/router#7383 — Issue 主串與 IOC 清單](https://github.com/TanStack/router/issues/7383)
- **已知 IoC：**
  - Linux systemd user service: `gh-token-monitor.sh`
  - macOS LaunchAgent: `com.user.gh-token-monitor`
  - 輪詢端點：`api.github.com/user`（每 60 秒）
  - 偽造 commit 身份：`claude@users.noreply.github.com`
  - 偽造 commit message：`chore: update dependencies`
- **受影響套件清單（截至發稿）**：TanStack、OpenSearch、Mistral AI、Guardrails AI、UiPath、Squawk
- **持久化目標**：`~/.claude/settings.json`、`~/.vscode/tasks.json`、`~/.local/bin/gh-token-monitor.sh`
