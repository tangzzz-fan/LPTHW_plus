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

PKG_FILE_HEADER = """\
# =============================================================================
# 包支持文件（{rel}）：必须保持可被 import。
# 主练习在入口脚本里手敲；本文件请直接阅读/微调，不要改成只剩占位 print。
# =============================================================================
"""


def _looks_like_python(code: str) -> bool:
    s = code.strip()
    if not s:
        return False
    prefixes = (
        '"""',
        "'''",
        "def ",
        "class ",
        "import ",
        "from ",
        "return ",
        "async ",
        "if ",
        "elif ",
        "else:",
        "for ",
        "while ",
        "try:",
        "except",
        "finally:",
        "with ",
        "@",
        "pass",
        "raise ",
        "yield ",
        "assert ",
        "print(",
        "__all__",
        "VERSION",
    )
    if any(s.startswith(p) for p in prefixes):
        return True
    if s[0] in "\"'([{":
        return True
    # simple assignment: NAME = ...
    if "=" in s and not s.startswith("="):
        left = s.split("=", 1)[0].strip()
        if left.isidentifier():
            return True
    return False


def _uncomment_hand_typed(src: str) -> str:
    """Best-effort undo of comment_out_python (for repairing package files)."""
    lines_out: list[str] = []
    for line in src.splitlines():
        s = line.strip()
        if not s:
            lines_out.append("")
            continue
        if "请在上方自行输入" in s:
            continue
        if s.startswith("# ==="):
            continue
        if any(
            k in s
            for k in (
                "自己动手敲",
                "删掉最底部",
                "保存并运行",
                "对照书本",
                "写完练习后",
                "包支持文件",
                "必须保持可被 import",
                "主练习在入口",
                "把下面",
                "不要改成只剩",
            )
        ):
            continue
        # Drop already-broken instruction lines like "1) 把下面..."
        if len(s) >= 2 and s[0].isdigit() and s[1] == ")":
            continue
        if s.startswith("#"):
            # Only uncomment real code lines, never instructional Chinese comments
            if s.startswith("# "):
                leading = line[: len(line) - len(line.lstrip(" \t"))]
                rest = line.lstrip()[2:]
                if _looks_like_python(rest):
                    lines_out.append(f"{leading}{rest}")
            continue
        if _looks_like_python(s) or s.startswith(")") or s.startswith("]") or s.startswith("}"):
            lines_out.append(line)
            continue
        # drop leftover junk
    text = "\n".join(lines_out)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip() + "\n"


def keep_package_module(src: str, rel_path: str) -> str:
    """Package modules (__init__.py / pkg/*.py) must stay importable."""
    rel = rel_path.replace("\\", "/")
    needs_repair = (
        "自己动手敲" in src
        or 'print("(请在上方自行输入代码)")' in src
        or any(
            ln.strip()[:2].isdigit() and ")" in ln.strip()[:4]
            for ln in src.splitlines()
            if ln.strip()
        )
        or (
            "必须保持可被 import" in src
            and not _looks_like_python(
                next(
                    (
                        ln
                        for ln in src.splitlines()
                        if ln.strip() and not ln.strip().startswith("#")
                    ),
                    "",
                )
            )
        )
    )
    if "必须保持可被 import" in src and not needs_repair:
        return src
    raw = _uncomment_hand_typed(src) if needs_repair or "自己动手敲" in src else src
    # Always rebuild header for repaired files
    body = raw
    if "必须保持可被 import" in body:
        body = _uncomment_hand_typed(body)
    return PKG_FILE_HEADER.format(rel=rel) + "\n" + body.lstrip()


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
    """Prepend Chinese teaching comments; keep code runnable (may be commented out later)."""
    if "【优先课注释】" in src:
        # Refresh stale guidance line if present.
        return src.replace(
            "# 建议：先通读注释 → 运行看输出 → 改一处参数再跑 → 对照书本加深。",
            "# 建议：先通读注释 → 按注释自己手敲（或去掉行首 #）→ 删占位 print 再跑。",
        )
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
# 建议：先通读注释 → 按注释自己手敲（或去掉行首 #）→ 删占位 print 再跑。
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
    entry = data.get("entry") or ""
    for name, content in list(starters.items()):
        if not name.endswith(".py"):
            continue
        if mode == "lpthw":
            rel = name.replace("\\", "/")
            # Package modules must stay importable (Ex46 skeleton etc.)
            is_pkg_support = rel.endswith("__init__.py") or (
                "/" in rel and rel != entry
            )
            if is_pkg_support:
                new = keep_package_module(content, rel)
            else:
                new = comment_out_python(content)
        else:
            # mit-python / mit-llm: keep hand-type code; only add priority header if missing.
            if "自己动手敲" in content:
                new = annotate_priority(content, title, track)
            else:
                new = annotate_priority(content, title, track)
                new = comment_out_python(new)
        if new != content:
            starters[name] = new
            changed = True
    if not changed:
        return False
    body = data.get("body") or ""
    if mode == "lpthw" and "自己动手敲" not in body:
        data["body"] = (
            body.rstrip()
            + "\n\n## 动手要求\n"
            + "- 起始代码已用注释标出：**请自行输入**（或去掉 `#`），再删除占位 `print`。\n"
            + "- 包内 `__init__.py` 等需保持可导入；不要改成只剩占位 print。\n"
            + "- 少复制粘贴，多手敲；敲错再改，是笨方法的核心。\n"
        )
    if mode == "priority" and "## 本题任务" not in body and "优先课注释" not in body:
        data["body"] = (
            (data.get("body") or body).rstrip()
            + "\n\n## 注释\n"
            + "- 代码里带有 **【优先课注释】**；先读左侧题目文档中的关键概念再手敲。\n"
        )
    data["starterFiles"] = starters
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def main() -> None:
    n = 0
    for p in sorted((TRACKS / "lpthw").glob("ex*.json")):
        if process_lesson(p, "lpthw", "lpthw"):
            n += 1
    # mit-* already ship mit-python style from gen_mit_tracks; only light priority tag if missing.
    # async/pytorch/lfs are upgraded by scripts/upgrade_tracks_mit_style.py (rich body + mit starter).
    for track in ("mit-python", "mit-llm"):
        folder = TRACKS / track
        if not folder.is_dir():
            continue
        for p in sorted(folder.glob("*.json")):
            if process_lesson(p, "priority", track):
                n += 1
    print(f"updated {n} lessons")
    print("note: async-llm/pytorch/llm-from-scratch → run scripts/upgrade_tracks_mit_style.py")


if __name__ == "__main__":
    main()
