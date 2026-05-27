#!/usr/bin/env python3
"""
SEO Description Scanner for Jekyll Blog Posts
掃描所有文章的 meta description，找出需要改進的項目

Usage:
    python3 check_descriptions.py [--fix] [--min-length 80]

Options:
    --fix           互動式修正模式，逐一修正有問題的 description
    --min-length    最小建議長度（預設 80 字元）
    --json          輸出 JSON 格式
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# 設定
POSTS_DIR = Path(__file__).parent.parent / "_posts"
MIN_DESCRIPTION_LENGTH = 80  # SEO 建議最小長度
MAX_DESCRIPTION_LENGTH = 160  # SEO 建議最大長度

# 問題 description 的特徵
PLACEHOLDER_PATTERNS = [
    r'^章節\.{0,3}$',
    r'^\.{3}$',
    r'^\s*$',
    r'^This post is for subscribers',
    r'^問題：.{0,20}$',  # 太短的問題開頭
]


@dataclass
class PostDescription:
    """文章 description 資訊"""
    filename: str
    title: str
    description: str
    length: int
    status: str  # 'ok', 'empty', 'too_short', 'too_long', 'placeholder'
    issue: Optional[str] = None


def extract_front_matter(content: str) -> dict:
    """從 markdown 內容提取 front matter"""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    front_matter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            front_matter[key] = value

    return front_matter


def check_description(desc: str) -> tuple[str, Optional[str]]:
    """檢查 description 狀態"""
    if not desc or desc.strip() == '':
        return 'empty', '❌ 空白'

    # 檢查是否為佔位符
    for pattern in PLACEHOLDER_PATTERNS:
        if re.match(pattern, desc):
            return 'placeholder', f'⚠️ 佔位符文字'

    length = len(desc)

    if length < MIN_DESCRIPTION_LENGTH:
        return 'too_short', f'⚠️ 過短 ({length} < {MIN_DESCRIPTION_LENGTH})'

    if length > MAX_DESCRIPTION_LENGTH:
        return 'too_long', f'⚠️ 過長 ({length} > {MAX_DESCRIPTION_LENGTH})'

    return 'ok', None


def scan_posts() -> list[PostDescription]:
    """掃描所有文章"""
    results = []

    if not POSTS_DIR.exists():
        print(f"❌ 找不到 _posts 目錄: {POSTS_DIR}")
        sys.exit(1)

    for md_file in sorted(POSTS_DIR.glob("*.md")):
        try:
            content = md_file.read_text(encoding='utf-8')
            front_matter = extract_front_matter(content)

            title = front_matter.get('title', '(無標題)')
            description = front_matter.get('description', '')

            status, issue = check_description(description)

            results.append(PostDescription(
                filename=md_file.name,
                title=title,
                description=description,
                length=len(description),
                status=status,
                issue=issue
            ))
        except Exception as e:
            print(f"⚠️ 讀取失敗: {md_file.name} - {e}")

    return results


def print_report(results: list[PostDescription], show_all: bool = False):
    """輸出報告"""
    total = len(results)
    ok_count = sum(1 for r in results if r.status == 'ok')
    problem_count = total - ok_count

    print("=" * 70)
    print("📊 SEO Description 掃描報告")
    print("=" * 70)
    print(f"📁 掃描目錄: {POSTS_DIR}")
    print(f"📄 總文章數: {total}")
    print(f"✅ 正常: {ok_count}")
    print(f"⚠️  需改進: {problem_count}")
    print(f"📏 建議長度: {MIN_DESCRIPTION_LENGTH}-{MAX_DESCRIPTION_LENGTH} 字元")
    print("=" * 70)

    # 分類統計
    by_status = {}
    for r in results:
        by_status.setdefault(r.status, []).append(r)

    # 顯示有問題的文章
    if problem_count > 0:
        print("\n🔴 需要修正的文章:\n")

        for status in ['empty', 'placeholder', 'too_short', 'too_long']:
            if status in by_status:
                posts = by_status[status]
                status_labels = {
                    'empty': '❌ 空白',
                    'placeholder': '⚠️ 佔位符',
                    'too_short': '📏 過短',
                    'too_long': '📏 過長'
                }
                print(f"\n### {status_labels[status]} ({len(posts)} 篇)\n")

                for p in posts:
                    print(f"  📄 {p.filename}")
                    print(f"     標題: {p.title[:50]}{'...' if len(p.title) > 50 else ''}")
                    print(f"     Description ({p.length} 字): {p.description[:60]}{'...' if len(p.description) > 60 else ''}")
                    print()

    # 顯示所有文章（如果要求）
    if show_all:
        print("\n" + "=" * 70)
        print("📋 所有文章 Description 列表")
        print("=" * 70 + "\n")

        for p in results:
            status_icon = "✅" if p.status == 'ok' else "⚠️"
            print(f"{status_icon} [{p.length:3d}字] {p.filename}")
            print(f"    {p.description[:70]}{'...' if len(p.description) > 70 else ''}")
            print()

    # 長度分佈統計
    print("\n" + "=" * 70)
    print("📊 長度分佈統計")
    print("=" * 70)

    ranges = [
        (0, 0, "空白"),
        (1, 49, "極短 (1-49)"),
        (50, 79, "偏短 (50-79)"),
        (80, 120, "理想 (80-120)"),
        (121, 160, "偏長 (121-160)"),
        (161, float('inf'), "過長 (>160)")
    ]

    for min_len, max_len, label in ranges:
        count = sum(1 for r in results if min_len <= r.length <= max_len)
        bar = "█" * (count * 2)
        if count > 0:
            print(f"  {label:20s} | {bar} {count}")


def output_json(results: list[PostDescription]):
    """輸出 JSON 格式"""
    data = {
        "total": len(results),
        "ok": sum(1 for r in results if r.status == 'ok'),
        "problems": sum(1 for r in results if r.status != 'ok'),
        "posts": [
            {
                "filename": r.filename,
                "title": r.title,
                "description": r.description,
                "length": r.length,
                "status": r.status,
                "issue": r.issue
            }
            for r in results
        ]
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))


def interactive_fix(results: list[PostDescription]):
    """互動式修正模式"""
    problems = [r for r in results if r.status != 'ok']

    if not problems:
        print("✅ 所有文章的 description 都符合標準，無需修正！")
        return

    print(f"\n🔧 互動式修正模式 - 共 {len(problems)} 篇需要修正\n")
    print("指令: [Enter] 跳過 | [q] 結束 | 輸入新 description 直接替換\n")

    modified = 0

    for i, p in enumerate(problems, 1):
        print(f"\n[{i}/{len(problems)}] {p.issue}")
        print(f"📄 檔案: {p.filename}")
        print(f"📝 標題: {p.title}")
        print(f"📏 目前 ({p.length}字): {p.description}")

        new_desc = input("\n新 description (Enter 跳過, q 結束): ").strip()

        if new_desc.lower() == 'q':
            break

        if new_desc:
            # 更新檔案
            file_path = POSTS_DIR / p.filename
            content = file_path.read_text(encoding='utf-8')

            # 替換 description
            old_pattern = f'description: "{p.description}"'
            new_pattern = f'description: "{new_desc}"'

            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                file_path.write_text(content, encoding='utf-8')
                print(f"✅ 已更新！新長度: {len(new_desc)} 字")
                modified += 1
            else:
                # 嘗試其他格式
                old_pattern = f"description: '{p.description}'"
                if old_pattern in content:
                    content = content.replace(old_pattern, f'description: "{new_desc}"')
                    file_path.write_text(content, encoding='utf-8')
                    print(f"✅ 已更新！新長度: {len(new_desc)} 字")
                    modified += 1
                else:
                    print("⚠️ 無法找到原始 description，請手動修改")

    print(f"\n{'=' * 50}")
    print(f"📊 修正完成！共修改 {modified} 篇文章")


def main():
    parser = argparse.ArgumentParser(description='SEO Description Scanner')
    parser.add_argument('--fix', action='store_true', help='互動式修正模式')
    parser.add_argument('--min-length', type=int, default=80, help='最小建議長度')
    parser.add_argument('--json', action='store_true', help='輸出 JSON 格式')
    parser.add_argument('--all', action='store_true', help='顯示所有文章')

    args = parser.parse_args()

    global MIN_DESCRIPTION_LENGTH
    MIN_DESCRIPTION_LENGTH = args.min_length

    results = scan_posts()

    if args.json:
        output_json(results)
    elif args.fix:
        interactive_fix(results)
    else:
        print_report(results, show_all=args.all)


if __name__ == "__main__":
    main()
