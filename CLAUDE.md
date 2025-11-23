# Jekyll Blog 部署指南

本文件記錄 Jekyll 部署流程與注意事項。

## 部署位置

**主要部署目標：** `/Users/wisely.chen/Desktop/cc/blog-migration/jekyll_site`

**線上網址：** https://thegiive.github.io
**Git Repository：** git@github.com:thegiive/thegiive.github.io.git
**部署分支：** `main`

## 部署流程

### 1. 文章更新流程

當在 `/Users/wisely.chen/Desktop/cc/blog-content/content/` 更新文章時：

```bash
# Step 1: 更新 markdown 文章（在 blog-content）
cd /Users/wisely.chen/Desktop/cc/blog-content
git add content/<article-name>.md
git commit -m "Update article: <description>"
git push origin topic-multitasking

# Step 2: 複製到 Jekyll 網站並部署
cd /Users/wisely.chen/Desktop/cc/blog-migration/jekyll_site
# 複製更新的文章到 _posts/
# 複製相關圖片到 assets/images/
git add _posts/ assets/images/
git commit -m "Deploy: <description>"
git push origin main
```

### 2. 圖片處理流程

**來源位置：** 通常在 `~/Desktop/` 或 `blog-content/content/images/`

**目標位置：**
- Jekyll: `/Users/wisely.chen/Desktop/cc/blog-migration/jekyll_site/assets/images/`
- Blog content: `/Users/wisely.chen/Desktop/cc/blog-content/content/images/`

**圖片引用格式：**
- Jekyll 文章中：`![Alt text](/assets/images/image-name.png)`
- Blog content 中：`![Alt text](images/image-name.png)`

**流程範例：**
```bash
# 複製圖片到兩個位置
cp ~/Desktop/image-name.png /Users/wisely.chen/Desktop/cc/blog-content/content/images/
cp ~/Desktop/image-name.png /Users/wisely.chen/Desktop/cc/blog-migration/jekyll_site/assets/images/

# 更新 blog-content
cd /Users/wisely.chen/Desktop/cc/blog-content
git add content/images/image-name.png content/article.md
git commit -m "Add image to article"
git push origin topic-multitasking

# 部署到 Jekyll
cd /Users/wisely.chen/Desktop/cc/blog-migration/jekyll_site
git add assets/images/image-name.png _posts/article.md
git commit -m "Deploy: Add image to article"
git push origin main
```

## 目錄結構

### Jekyll Site 結構
```
jekyll_site/
├── _config.yml           # Jekyll 配置
├── _includes/            # 可重用的 HTML 片段
├── _layouts/             # 頁面模板
│   ├── default.html
│   └── post.html
├── _posts/               # 博客文章（markdown）
│   └── YYYY-MM-DD-title.md
├── assets/               # 靜態資源
│   ├── images/          # 圖片資源
│   └── css/             # 樣式文件
├── index.html           # 首頁
├── about.html           # 關於頁面
└── CNAME                # 自訂網域設定
```

### Blog Content 結構
```
blog-content/
├── content/             # 原始 markdown 文章
│   ├── *.md            # 文章檔案
│   └── images/         # 文章圖片
├── pages/              # GitHub Pages HTML 版本（已棄用）
└── topic_discussion/   # 選題討論資料夾
```

## 文章命名規則

### Jekyll 文章命名
- **格式：** `YYYY-MM-DD-title-in-pinyin.md`
- **範例：** `2025-11-19-fde-continuous-experiment.md`

### Blog Content 命名
- **格式：** `title-in-pinyin.md`
- **範例：** `fde-continuous-experiment.md`

## Front Matter 設定

Jekyll 文章必須包含 Front Matter：

```yaml
---
layout: post
title: "文章標題"
date: 2025-11-19 07:21:00 +0800
permalink: /article-url/
image: /assets/images/featured-image.jpg
description: "文章摘要說明"
---
```

## 部署檢查清單

發布文章前確認：

- [ ] 文章已複製到 `jekyll_site/_posts/`
- [ ] 文章檔名符合 `YYYY-MM-DD-title.md` 格式
- [ ] Front Matter 設定完整
- [ ] 圖片已複製到 `assets/images/`
- [ ] 圖片路徑使用 `/assets/images/` 格式
- [ ] 提交訊息清晰描述變更內容
- [ ] 推送到 `main` 分支

## 常見問題

### Q: 為什麼要維護兩個 repository？

**A:**
- `blog-content` - 內容開發與版本控制（工作分支）
- `jekyll_site` - 生產環境部署（GitHub Pages）

### Q: 圖片路徑為什麼不同？

**A:**
- Blog content 使用相對路徑 `images/`（因為文章在 `content/` 目錄）
- Jekyll 使用絕對路徑 `/assets/images/`（符合 Jekyll 慣例）

### Q: 如何驗證部署成功？

**A:**
```bash
# 檢查 GitHub Actions 部署狀態
# 訪問 https://github.com/thegiive/thegiive.github.io/actions

# 或直接訪問網站
# https://thegiive.github.io/article-url/
```

### Q: 部署失敗怎麼辦？

**A:**
1. 檢查 GitHub Actions 日誌
2. 確認 Front Matter 格式正確
3. 確認圖片路徑存在
4. 檢查 Jekyll 語法是否正確

## 相關資源

- **Jekyll 文檔：** https://jekyllrb.com/docs/
- **GitHub Pages 文檔：** https://docs.github.com/en/pages
- **部署腳本：** `/Users/wisely.chen/Desktop/cc/blog-migration/jekyll_site/deploy.sh`

## 維護記錄

- **2025-11-20：** 建立此文件，記錄標準部署流程
  - 明確部署目標為 `jekyll_site`
  - 記錄圖片處理流程
  - 記錄兩個 repository 的關係

---

**重要提醒：** 所有文章發布都必須推送到 `jekyll_site` 才會在 https://thegiive.github.io 上線！
