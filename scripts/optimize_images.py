#!/usr/bin/env python3
"""Generate WebP copies of blog images and point post bodies at them.

Usage (from the repo root):
    python3 scripts/optimize_images.py            # convert + rewrite
    python3 scripts/optimize_images.py --dry-run  # report only

What it does
- For every PNG/JPG in assets/images, writes a sibling .webp (quality 80,
  width capped at 1600px). Originals are left untouched: they are still used
  for og:image / JSON-LD, where WebP support is uneven.
- A .webp is kept only when it is smaller than the original.
- In _posts/*.md bodies (never the front matter), rewrites references to an
  image that has a .webp sibling so they load the .webp.

The post layout and the homepage pick up the cover's .webp on their own (they
look for the sibling file at build time), so `image:` in front matter stays a
PNG/JPG. Safe to re-run: existing up-to-date .webp files are skipped.

Requires `cwebp` (brew install webp).
"""
import concurrent.futures
import glob
import os
import re
import struct
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images")
MAX_WIDTH = 1600
QUALITY = "80"
DRY = "--dry-run" in sys.argv


def png_width(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">I", head[16:20])[0]


def image_width(path):
    if path.lower().endswith(".png"):
        width = png_width(path)
        if width:
            return width
    out = subprocess.run(["sips", "-g", "pixelWidth", path], capture_output=True, text=True).stdout
    match = re.search(r"pixelWidth:\s*(\d+)", out)
    return int(match.group(1)) if match else 0


def convert(src):
    dst = os.path.splitext(src)[0] + ".webp"
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return "skip", src, 0, 0
    if DRY:
        return "would-convert", src, os.path.getsize(src), 0
    cmd = ["cwebp", "-quiet", "-mt", "-q", QUALITY]
    if image_width(src) > MAX_WIDTH:
        cmd += ["-resize", str(MAX_WIDTH), "0"]
    cmd += [src, "-o", dst]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.exists(dst):
        if os.path.exists(dst):
            os.remove(dst)
        return "failed", src, 0, 0
    before, after = os.path.getsize(src), os.path.getsize(dst)
    if after >= before:
        os.remove(dst)
        return "not-smaller", src, before, after
    return "converted", src, before, after


def main():
    sources = []
    for ext in ("png", "PNG", "jpg", "JPG", "jpeg", "JPEG"):
        sources += glob.glob(os.path.join(IMG_DIR, "*." + ext))
    # Two sources that differ only by extension would share one .webp: skip both.
    stems = {}
    for src in sources:
        stems.setdefault(os.path.splitext(src)[0], []).append(src)
    sources = [paths[0] for paths in stems.values() if len(paths) == 1]
    counts, saved_from, saved_to = {}, 0, 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for status, src, before, after in pool.map(convert, sorted(set(sources))):
            counts[status] = counts.get(status, 0) + 1
            if status == "converted":
                saved_from += before
                saved_to += after
            elif status == "failed":
                print("FAILED:", os.path.basename(src))
    print("images:", counts)
    if saved_from:
        print("converted set: %.1f MB -> %.1f MB" % (saved_from / 1e6, saved_to / 1e6))

    have_webp = {os.path.basename(p) for p in glob.glob(os.path.join(IMG_DIR, "*.webp"))}
    pattern = re.compile(r"(/assets/images/)([^)\"'\s]+?)\.(png|PNG|jpg|JPG|jpeg|JPEG)(?=[)\"'\s])")
    changed_files = changed_refs = 0
    for post in glob.glob(os.path.join(ROOT, "_posts", "*.md")):
        text = open(post, encoding="utf-8").read()
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue

        def swap(match):
            nonlocal changed_refs
            if match.group(2) + ".webp" in have_webp:
                changed_refs += 1
                return match.group(1) + match.group(2) + ".webp"
            return match.group(0)

        body = pattern.sub(swap, parts[2])
        if body != parts[2]:
            changed_files += 1
            if not DRY:
                open(post, "w", encoding="utf-8").write(parts[0] + "---" + parts[1] + "---" + body)
    print("post bodies: %d references in %d files %s" % (changed_refs, changed_files, "(dry run)" if DRY else "rewritten"))


if __name__ == "__main__":
    main()
