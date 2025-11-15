#!/bin/bash

# 快速部署腳本 - 將 Jekyll 網站推送到 GitHub Pages

echo "======================================"
echo "Jekyll 網站部署到 GitHub Pages"
echo "======================================"

# 檢查是否已經 git init
if [ ! -d ".git" ]; then
  echo "初始化 Git repository..."
  git init
  echo "✅ Git 初始化完成"
fi

# 檢查是否有遠端倉庫
REMOTE=$(git remote -v | grep origin)
if [ -z "$REMOTE" ]; then
  echo ""
  echo "請輸入你的 GitHub repository URL："
  echo "範例: git@github.com:username/username.github.io.git"
  read -p "URL: " REPO_URL

  if [ -z "$REPO_URL" ]; then
    echo "❌ 錯誤：未輸入 repository URL"
    exit 1
  fi

  git remote add origin "$REPO_URL"
  echo "✅ 已添加遠端倉庫: $REPO_URL"
fi

# 提交所有變更
echo ""
echo "準備提交變更..."
git add .

# 詢問 commit message
read -p "Commit message (預設: Update blog): " COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-"Update blog"}

git commit -m "$COMMIT_MSG"
echo "✅ Commit 完成: $COMMIT_MSG"

# 確認要推送的分支
BRANCH=$(git branch --show-current)
if [ -z "$BRANCH" ]; then
  BRANCH="main"
  git branch -M main
fi

echo ""
echo "準備推送到分支: $BRANCH"
read -p "確定要推送嗎？(y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
  echo "❌ 取消推送"
  exit 0
fi

# 推送到 GitHub
echo ""
echo "正在推送到 GitHub..."
git push -u origin $BRANCH

if [ $? -eq 0 ]; then
  echo ""
  echo "======================================"
  echo "✅ 部署成功！"
  echo "======================================"
  echo ""
  echo "下一步："
  echo "1. 前往 GitHub Repository → Settings → Pages"
  echo "2. Source 選擇: Deploy from a branch"
  echo "3. Branch 選擇: $BRANCH, 目錄選擇: / (root)"
  echo "4. 點擊 Save"
  echo ""
  echo "等待 1-2 分鐘，你的網站就會上線！"
  echo ""
else
  echo ""
  echo "❌ 推送失敗，請檢查錯誤訊息"
  exit 1
fi
