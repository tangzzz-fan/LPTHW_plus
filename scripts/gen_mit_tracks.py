#!/usr/bin/env python3
"""Generate MIT-Python (T1–T6) and MIT-LLM (T1–T7) tracks from inbox.

LPTHW style: reference .py fully commented; learners type it themselves.
Does NOT import 密卷 / 批改 / 费曼 / .venv.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "inbox"
OUT = ROOT / "content" / "tracks"

LPTHW_HEADER = """\
# =============================================================================
# 自己动手敲（笨方法 / MIT 代码题）：
# 1) 把下面「已注释」的参考实现亲手输入（或去掉行首 #）
# 2) 删掉最底部的占位 print
# 3) 保存并运行（⌘/Ctrl+Enter）
# 先读讲义任务，再敲代码；不要直接复制粘贴完事。
# =============================================================================
"""

LPTHW_FOOTER = """
# =============================================================================
# 写完练习后，删除下面这行占位再运行：
print("(请在上方自行输入代码)")
"""


def comment_out_python(src: str) -> str:
    if "自己动手敲" in src:
        return src
    lines = src.splitlines()
    out: list[str] = [LPTHW_HEADER.rstrip(), ""]
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            out.append("")
            continue
        if stripped.startswith("#"):
            out.append(line)
            continue
        leading = line[: len(line) - len(line.lstrip(" \t"))]
        code = line[len(leading) :]
        out.append(f"{leading}# {code}")
    out.append(LPTHW_FOOTER)
    return "\n".join(out).rstrip() + "\n"


def extract_q_section(md: str, qnum: int) -> str:
    """Pull Q{n} task description from 教练出题 markdown."""
    # Patterns like **Q1** or ### Q1
    patterns = [
        rf"(?:\*\*Q{qnum}\b|###\s*Q{qnum}\b|##\s*Q{qnum}\b)([\s\S]*?)(?=\n(?:\*\*Q|\*\*C|###\s*Q|###\s*C|##\s*[一二三四五六七八]|##\s*五、|##\s*六、|\Z))",
        rf"(?:Q{qnum}[（(])([\s\S]*?)(?=\nQ\d+[（(]|\n###|\n##\s*[一二三四五六]|\Z)",
    ]
    for pat in patterns:
        m = re.search(pat, md, flags=re.IGNORECASE)
        if m:
            return m.group(0).strip()[:4000]
    return ""


def extract_models_blurb(md: str) -> str:
    """Short consensus model table / intro for body."""
    # Take from start through first code-task section header
    cut = re.search(r"##\s*[三四].*代码", md)
    head = md[: cut.start()] if cut else md[:2500]
    # drop yaml front matter
    if head.startswith("---"):
        parts = head.split("---", 2)
        if len(parts) >= 3:
            head = parts[2]
    lines = [ln for ln in head.splitlines() if not ln.strip().startswith(">")]
    text = "\n".join(lines).strip()
    return text[:2200]


def topic_title_from_path(path: Path) -> str:
    name = path.stem
    # T1-01-教练出题-Python基础
    m = re.search(r"教练出题-(.+)$", name)
    return m.group(1) if m else name


def pick_q_files(code_dir: Path) -> dict[int, list[Path]]:
    """Map Q number -> files (excluding 学员作答)."""
    by_q: dict[int, list[Path]] = {}
    if not code_dir.is_dir():
        return by_q

    # Flat Q*.py / Q*.md / Q*.swift
    for f in sorted(code_dir.iterdir()):
        if f.name.startswith(".") or "学员" in f.name:
            continue
        if f.is_file():
            m = re.match(r"Q(\d+)", f.name)
            if m:
                by_q.setdefault(int(m.group(1)), []).append(f)
        elif f.is_dir() and re.match(r"Q\d+", f.name):
            m = re.match(r"Q(\d+)", f.name)
            qn = int(m.group(1))
            for sub in sorted(f.rglob("*")):
                if sub.is_file() and "__pycache__" not in sub.parts:
                    by_q.setdefault(qn, []).append(sub)
    return by_q


def choose_primary_py(files: list[Path]) -> Path | None:
    pys = [f for f in files if f.suffix == ".py"]
    if not pys:
        return None
    # Prefer non-体验, longer descriptive Chinese names often are reference
    def score(p: Path) -> tuple:
        n = p.name
        return (
            0 if "体验" in n else 1,
            0 if "采样器.py" == n.replace("Q2-mock", "") else 1,  # weak
            len(n),
        )

    # Prefer 字符级 / 概率采样器 over short duplicates
    preferred = []
    for p in pys:
        if "字符级" in p.name or "概率" in p.name:
            preferred.append(p)
    if preferred:
        return sorted(preferred, key=lambda p: len(p.name), reverse=True)[0]
    # Drop *体验* if another exists
    non_exp = [p for p in pys if "体验" not in p.name]
    pool = non_exp or pys
    return sorted(pool, key=lambda p: (-len(p.name), p.name))[0]


def timeout_for(track: str, topic: int, q: int, name: str) -> int:
    if "并发" in name or "SVD" in name or "训练" in name or "Transformer" in name:
        return 120
    if "蒙特卡洛" in name or "耗时" in name or "TopK" in name:
        return 90
    if track == "mit-llm" and topic >= 5:
        return 60
    if "torch" in name.lower() or topic == 4 and track == "mit-python":
        return 90
    return 30


def requires_for(name: str, topic: int, track: str) -> list[str]:
    req: list[str] = []
    if track == "mit-python" and topic >= 4:
        if topic == 4 or "torch" in name.lower():
            req.append("torch")
    if "numpy" in name.lower() or topic in (2, 3) and track == "mit-python":
        # numpy often needed; torch extra pulls numpy
        pass
    if track == "mit-llm" and topic == 2:
        req.append("torch")  # some use torch/numpy; torch covers
    # embedding/attention often numpy only - still ok without requires
    if any(k in name for k in ("注意力", "embedding", "LayerNorm", "残差", "PCA", "SVD", "matmul")):
        if "torch" not in req:
            # numpy is in ml extra; don't hard-require
            pass
    return req


def write_lesson(track: str, lesson_id: str, payload: dict) -> None:
    folder = OUT / track
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{lesson_id}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def build_track(
    track: str,
    track_title: str,
    inbox_dir: Path,
    topics: range,
    id_prefix: str,
) -> int:
    code_root = inbox_dir / "代码"
    count = 0
    for t in topics:
        # find 出题 file
        outs = list(inbox_dir.glob(f"T{t}-01-教练出题-*.md"))
        if not outs:
            print(f"WARN missing 出题 T{t} in {inbox_dir.name}")
            continue
        topic_md = outs[0].read_text(encoding="utf-8")
        topic_name = topic_title_from_path(outs[0])
        models = extract_models_blurb(topic_md)
        by_q = pick_q_files(code_root / f"T{t}")

        for q in sorted(by_q):
            files = by_q[q]
            primary = choose_primary_py(files)
            q_section = extract_q_section(topic_md, q)
            # Title from primary filename
            if primary:
                short = re.sub(r"^Q\d+-?", "", primary.stem)
            elif files:
                short = re.sub(r"^Q\d+-?", "", files[0].stem)
            else:
                short = f"Q{q}"

            lesson_id = f"{id_prefix}-t{t}-q{q}"
            title = f"T{t}Q{q}: {short}"

            body_parts = [
                f"# {title}",
                "",
                f"来源：inbox `{inbox_dir.name}` · **{topic_name}**（一期；原创组装讲义，手敲练习）。",
                "",
                "## 主题骨架（摘录）",
                "",
                models.strip() or f"（见 inbox 出题稿 T{t}）",
                "",
                "## 本题任务",
                "",
                q_section.strip()
                or f"实现并跑通 `代码/T{t}/` 中 Q{q} 对应练习。对照出题稿完成。",
                "",
                "## 动手要求",
                "",
                "- 起始代码已用注释标出：**请自行输入**（或去掉 `#`），再删除占位 `print`。",
                "- 跑通后对照讲义自检；不要先看密卷。",
                "",
                "## 自检",
                "",
                "- [ ] 去掉注释后能运行",
                "- [ ] 能讲清本题在练哪个模型/机制",
            ]
            body = "\n".join(body_parts) + "\n"

            starter: dict[str, str] = {}
            entry = "main.py"

            if primary is not None and primary.parent != code_root / f"T{t}":
                # multi-file dir e.g. Q4-工程化
                base = primary.parent
                for f in files:
                    rel = str(f.relative_to(base)).replace("\\", "/")
                    text = f.read_text(encoding="utf-8", errors="replace")
                    if f.suffix == ".py":
                        starter[rel] = comment_out_python(text)
                    else:
                        starter[rel] = text
                if "demo.py" in starter:
                    entry = "demo.py"
                elif primary.name in starter:
                    entry = primary.name
                else:
                    entry = next(iter(starter))
            elif primary:
                entry = f"q{q}.py"
                starter[entry] = comment_out_python(
                    primary.read_text(encoding="utf-8", errors="replace")
                )
                for f in files:
                    if f == primary or f.suffix == ".py":
                        continue
                    starter[f.name] = f.read_text(encoding="utf-8", errors="replace")
            else:
                # markdown-only / no py (e.g. architecture review)
                md_files = [f for f in files if f.suffix == ".md"]
                if md_files:
                    entry = "q_notes.py"
                    note = md_files[0].read_text(encoding="utf-8", errors="replace")
                    starter["README_TASK.md"] = note
                    starter[entry] = comment_out_python(
                        'print("本课以架构复盘笔记为主：请阅读 README_TASK.md，用自己的话写总结再 print。")\n'
                    )
                    body += "\n> 本题以笔记复盘为主，代码占位仅用于跑通手敲流程。\n"
                else:
                    print(f"SKIP {track} T{t}Q{q}: no usable files")
                    continue

            if not starter:
                print(f"SKIP {track} T{t}Q{q}: empty starter")
                continue

            req = requires_for(short, t, track)
            timeout = timeout_for(track, t, q, short)

            payload = {
                "title": title,
                "priority": True,
                "outlineOnly": False,
                "timeoutSec": timeout,
                "requires": req,
                "entry": entry,
                "body": body,
                "starterFiles": starter,
                "checklist": [
                    "读完本题任务",
                    "手敲参考实现并跑通",
                    "能向同事讲清机制",
                ],
                "source": {
                    "inbox": inbox_dir.name,
                    "topic": topic_name,
                    "t": t,
                    "q": q,
                },
            }
            write_lesson(track, lesson_id, payload)
            count += 1
            print(f"  + {track}/{lesson_id} entry={entry} files={len(starter)}")
    return count


def main() -> None:
    py = INBOX / "MIT-Python-Migration"
    llm = INBOX / "MIT-LLM-Migration"
    if not py.is_dir() or not llm.is_dir():
        raise SystemExit(f"inbox folders missing under {INBOX}")

    print("Building mit-python T1–T6…")
    n1 = build_track("mit-python", "MIT-Python", py, range(1, 7), "py")
    print("Building mit-llm T1–T7…")
    n2 = build_track("mit-llm", "MIT-LLM", llm, range(1, 8), "llm")
    print(f"done: mit-python={n1} mit-llm={n2} total={n1 + n2}")


if __name__ == "__main__":
    main()
