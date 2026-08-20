#!/usr/bin/env python3
"""Rewrite starters: LPTHW → type-yourself comments; priority tracks → Chinese notes."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "content" / "tracks"

LPTHW_HEADER = """\
# =============================================================================
# 自己动手敲（笨方法）：
# 1) 把下面「已注释」的代码亲手输入到编辑器（或去掉行首的 # ）
# 2) 删掉最底部的占位 print
# 3) 保存并运行（⌘/Ctrl+Enter）
# 对照书本完成本课；不要复制粘贴完事。
# =============================================================================
"""

LPTHW_FOOTER = """
# =============================================================================
# 写完练习后，删除下面这行占位再运行：
print("(请在上方自行输入代码)")
"""


def comment_out_python(src: str) -> str:
    """Comment executable lines; keep existing comments; add type-yourself banner."""
    if "自己动手敲" in src:
        return src
    lines = src.splitlines()
    out: list[str] = [LPTHW_HEADER.rstrip(), ""]
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            out.append("")
            continue
        # already a full-line comment
        if stripped.startswith("#"):
            out.append(line)
            continue
        # preserve indentation, comment the code
        leading = line[: len(line) - len(line.lstrip(" \t"))]
        code = line[len(leading) :]
        out.append(f"{leading}# {code}")
    out.append(LPTHW_FOOTER)
    return "\n".join(out).rstrip() + "\n"


def annotate_priority(src: str, title: str, track: str) -> str:
    """Prepend Chinese teaching comments; keep code runnable."""
    if "【优先课注释】" in src:
        return src
    track_hint = {
        "async-llm": "Async / LLM 落地",
        "pytorch": "PyTorch",
        "llm-from-scratch": "LLMFromScratch（附录 A）",
        "mit-python": "MIT-Python",
        "mit-llm": "MIT-LLM",
    }.get(track, track)
    header = f'''\
# 【优先课注释】{track_hint}
# 课题：{title}
# 建议：先通读注释 → 运行看输出 → 改一处参数再跑 → 对照书本加深。
# ---------------------------------------------------------------------------

'''
    # Light inline section markers before top-level defs/classes/imports blocks
    lines = src.splitlines()
    annotated: list[str] = []
    seen_import_note = False
    for i, line in enumerate(lines):
        s = line.strip()
        if not seen_import_note and (s.startswith("import ") or s.startswith("from ")):
            annotated.append("# --- 导入依赖 ---")
            seen_import_note = True
        if s.startswith("def ") and not s.startswith("def _"):
            name = s[4:].split("(")[0].strip()
            annotated.append(f"# --- 函数 {name}：读参数与返回值，想清楚谁调用它 ---")
        if s.startswith("class "):
            name = s[6:].split("(")[0].split(":")[0].strip()
            annotated.append(f"# --- 类 {name}：关注 __init__ / forward 或核心方法 ---")
        if s.startswith("async def "):
            name = s[10:].split("(")[0].strip()
            annotated.append(f"# --- 异步函数 {name}：注意 await 点，勿在此写阻塞 IO ---")
        if s.startswith("if __name__"):
            annotated.append("# --- 脚本入口：从这里开始执行 ---")
        annotated.append(line)
    return header + "\n".join(annotated).rstrip() + "\n"


def process_lesson(path: Path, mode: str, track: str) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    starters = data.get("starterFiles") or {}
    changed = False
    title = data.get("title", path.stem)
    for name, content in list(starters.items()):
        if not name.endswith(".py"):
            continue
        if mode == "lpthw":
            new = comment_out_python(content)
        else:
            new = annotate_priority(content, title, track)
        if new != content:
            starters[name] = new
            changed = True
    if changed:
        # nudge body
        body = data.get("body") or ""
        if mode == "lpthw" and "自己动手敲" not in body:
            data["body"] = (
                body.rstrip()
                + "\n\n## 动手要求\n"
                + "- 起始代码已用注释标出：**请自行输入**（或去掉 `#`），再删除占位 `print`。\n"
                + "- 少复制粘贴，多手敲；敲错再改，是笨方法的核心。\n"
            )
        if mode == "priority" and "优先课注释" not in body:
            data["body"] = (
                body.rstrip()
                + "\n\n## 注释\n"
                + "- 代码里带有 **【优先课注释】** 与分段说明，先读注释再跑。\n"
            )
        data["starterFiles"] = starters
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    n = 0
    for p in sorted((TRACKS / "lpthw").glob("ex*.json")):
        if process_lesson(p, "lpthw", "lpthw"):
            n += 1
    for track in ("async-llm", "pytorch", "llm-from-scratch", "mit-python", "mit-llm"):
        folder = TRACKS / track
        if not folder.is_dir():
            continue
        for p in sorted(folder.glob("*.json")):
            if process_lesson(p, "priority", track):
                n += 1
    print(f"updated {n} lessons")


if __name__ == "__main__":
    main()
