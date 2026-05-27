# AI for everyone - AI Coding Blog

這是一個從 Ghost CMS 遷移到 Jekyll/GitHub Pages 的技術博客。

## 作者

Wisely Chen - AI Coding, ATPM, Vibe Coding 實戰分享

## 內容主題

- **ATPM Framework** - 真實產品環境的 Vibe Coding 流程
- **AI Agent** - AI Agent 落地策略與實戰
- **Vibe Coding** - 前端開發與 AI Coding 實踐
- **FDE 模式** - Field Data Engineer 新模式

## 本地開發

### 安裝依賴

```bash
bundle install
```

### 本地運行

```bash
bundle exec jekyll serve
```

網站將在 `http://localhost:4000` 運行

### 建置靜態網站

```bash
bundle exec jekyll build
```

輸出在 `_site/` 目錄

## 部署到 GitHub Pages

### 方法一：GitHub Pages 自動建置（推薦）

1. 建立 GitHub repository
2. 推送代碼到 `main` 或 `gh-pages` 分支
3. 在 Repository Settings → Pages 中啟用 GitHub Pages
4. 選擇 Source: Deploy from a branch
5. 選擇 Branch: `main` 或 `gh-pages`，目錄選 `/ (root)`

### 方法二：GitHub Actions

在 `.github/workflows/` 建立 workflow 檔案，使用 `actions/jekyll-build-pages`。

## URL 結構

文章 URL 格式保持與原 Ghost 網站一致：`/<slug>/`

例如：
- 原網址：`https://ai-coding.wiselychen.com/atpm-a-real-production-vibe-coding-process/`
- 新網址：`https://your-username.github.io/atpm-a-real-production-vibe-coding-process/`

## 技術細節

- **靜態網站生成器**: Jekyll 4.3.0
- **主題**: 自訂 (基於 minima)
- **插件**:
  - jekyll-feed (RSS)
  - jekyll-seo-tag (SEO)
  - jekyll-sitemap (Sitemap)
  - jekyll-paginate (分頁)

## 文章統計

- 總文章數：19 篇
- 總圖片數：91 張
- 日期範圍：2025-09-16 到 2025-11-01

## 授權

所有文章版權歸 Wisely Chen 所有。

