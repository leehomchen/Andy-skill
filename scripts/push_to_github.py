#!/usr/bin/env python3
"""一键把本 skill 推送到你的 GitHub 仓库（在你自己电脑上、网络正常时运行）

用法：
  export GH_TOKEN="你的令牌"
  python3 push_to_github.py

也可把令牌作为第 1 个参数传入：
  python3 push_to_github.py ghp_xxxx
"""
import os, sys, base64, json, urllib.request, urllib.error

TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_TOKEN")
if not TOKEN:
    sys.exit("请先设置环境变量 GH_TOKEN 或把令牌作为第1个参数传入")

REPO = os.environ.get("REPO", "leehomchen/Andy-skill")
BRANCH = os.environ.get("BRANCH", "main")
# 本脚本位于 <skill>/scripts/ 下，仓库根目录是上级目录
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = [
    "README.md", "SKILL.md",
    "scripts/tts.py", "scripts/subtitle.py", "scripts/compose.py",
    "references/script-template.md", "references/style-guide.md", "references/ffmpeg-recipes.md",
    "examples/sample-project.md",
]

def req(url, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "andy-skill-push",
    })
    with urllib.request.urlopen(r, timeout=30) as resp:
        return resp.status, json.load(resp)

def get_sha(path):
    try:
        _, d = req(f"https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}")
        return d.get("sha")
    except Exception:
        return None

print(f"目标仓库: {REPO} (分支 {BRANCH})")
for rel in FILES:
    with open(os.path.join(SRC, rel), "rb") as f:
        content = base64.b64encode(f.read()).decode()
    sha = get_sha(rel)
    payload = {"message": ("update " if sha else "add ") + rel, "content": content, "branch": BRANCH}
    if sha:
        payload["sha"] = sha
    try:
        status, _ = req(f"https://api.github.com/repos/{REPO}/contents/{rel}", "PUT", payload)
        print(f"[{status}] {rel}")
    except urllib.error.HTTPError as e:
        print(f"[失败 {e.code}] {rel}: {e.read().decode()[:200]}")
print("完成！")
