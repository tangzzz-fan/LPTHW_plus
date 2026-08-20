#!/usr/bin/env python3
"""Generate LPTHW skeleton + priority track lessons (original study guides)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "content" / "tracks"

LPTHW_TITLES = {
    0: "The Setup",
    1: "A Good First Program",
    2: "Comments and Pound Characters",
    3: "Numbers and Math",
    4: "Variables and Names",
    5: "More Variables and Printing",
    6: "Strings and Text",
    7: "More Printing",
    8: "Printing, Printing",
    9: "Printing, Printing, Printing",
    10: "What Was That?",
    11: "Asking Questions",
    12: "Prompting People",
    13: "Parameters, Unpacking, Variables",
    14: "Prompting and Passing",
    15: "Reading Files",
    16: "Reading and Writing Files",
    17: "More Files",
    18: "Names, Variables, Code, Functions",
    19: "Functions and Variables",
    20: "Functions and Files",
    21: "Functions Can Return Something",
    22: "What Do You Know So Far?",
    23: "Strings, Bytes and Character Encodings",
    24: "More Practice",
    25: "Even More Practice",
    26: "Congratulations, Take a Test!",
    27: "Memorizing Logic",
    28: "Boolean Practice",
    29: "What If",
    30: "Else and If",
    31: "Making Decisions",
    32: "Loops and Lists",
    33: "While Loops",
    34: "Accessing Elements of Lists",
    35: "Branches and Functions",
    36: "Designing and Debugging",
    37: "Symbol Review",
    38: "Doing Things to Lists",
    39: "Dictionaries, Oh Lovely Dictionaries",
    40: "Modules, Classes, and Objects",
    41: "Learning to Speak Object Oriented",
    42: "Is-A, Has-A, Objects, and Classes",
    43: "Basic Object-Oriented Analysis and Design",
    44: "Inheritance Versus Composition",
    45: "You Make a Game",
    46: "A Project Skeleton",
    47: "Automated Testing",
    48: "Advanced User Input",
    49: "Making Sentences",
    50: "Your First Website",
    51: "Getting Input from a Browser",
    52: "The Start of Your Web Game",
}

FULL_LPTHW = {
    0: {
        "body": """# Ex 0 · The Setup

对照你的书完成环境确认。本站用本机 `python3` 执行代码。

## 目标
- 确认本机 Python 可运行
- 习惯：先读说明 → 改代码 → 运行 → 看输出

## 自检
- [ ] 下方代码能跑出版本信息
""",
        "entry": "ex00.py",
        "starterFiles": {
            "ex00.py": "import sys\n\nprint(\"Python OK\")\nprint(sys.version)\n"
        },
        "timeoutSec": 5,
    },
    1: {
        "body": """# Ex 1 · A Good First Program

练习 `print`。多敲几遍，观察引号与括号。

## 自检
- [ ] 至少三行不同输出
""",
        "entry": "ex01.py",
        "starterFiles": {
            "ex01.py": 'print("Hello World!")\nprint("Hello Again")\nprint("I like typing this.")\n'
        },
        "timeoutSec": 5,
    },
    2: {
        "body": """# Ex 2 · Comments

`#` 后面是注释。用注释给未来的自己留言。
""",
        "entry": "ex02.py",
        "starterFiles": {
            "ex02.py": '# A comment, this is so you can read your program later.\nprint("I could have code like this.")  # and the comment after is ignored\n'
        },
    },
    3: {
        "body": """# Ex 3 · Numbers and Math

练习 `+ - * / % < > <= >=`。先心算再核对输出。
""",
        "entry": "ex03.py",
        "starterFiles": {
            "ex03.py": 'print("I will now count my chickens:")\nprint("Hens", 25 + 30 / 6)\nprint("Roosters", 100 - 25 * 3 % 4)\nprint("Is it true that 3 + 2 < 5 - 7?")\nprint(3 + 2 < 5 - 7)\n'
        },
    },
    4: {
        "body": """# Ex 4 · Variables and Names

给值起名字。变量名要可读。
""",
        "entry": "ex04.py",
        "starterFiles": {
            "ex04.py": 'cars = 100\nspace_in_a_car = 4.0\ndrivers = 30\npassengers = 90\ncars_not_driven = cars - drivers\ncars_driven = drivers\ncarpool_capacity = cars_driven * space_in_a_car\naverage_passengers_per_car = passengers / cars_driven\n\nprint("There are", cars, "cars available.")\nprint("There are only", drivers, "drivers available.")\nprint("We can transport", carpool_capacity, "people today.")\nprint("We have", passengers, "to carpool today.")\nprint("We need to put about", average_passengers_per_car, "in each car.")\n'
        },
    },
    5: {
        "body": """# Ex 5 · More Variables and Printing

用 f-string 或 `.format` 把变量嵌进字符串。
""",
        "entry": "ex05.py",
        "starterFiles": {
            "ex05.py": 'my_name = "Zed A. Shaw"\nmy_age = 35\nmy_height = 74  # inches\nmy_weight = 180  # lbs\n\nprint(f"Let\'s talk about {my_name}.")\nprint(f"He\'s {my_height} inches tall.")\nprint(f"He\'s {my_weight} pounds heavy.")\n'
        },
    },
    11: {
        "body": """# Ex 11 · Asking Questions

`input()` 从终端读一行。运行后在下方终端输入答案并回车。
""",
        "entry": "ex11.py",
        "starterFiles": {
            "ex11.py": 'print("How old are you?", end=" ")\nage = input()\nprint("How tall are you?", end=" ")\nheight = input()\nprint("How much do you weigh?", end=" ")\nweight = input()\nprint(f"So, you\'re {age} old, {height} tall and {weight} heavy.")\n'
        },
        "timeoutSec": 3,
    },
    15: {
        "body": """# Ex 15 · Reading Files

右侧文件树里有 `sample.txt`。用 `open` / `read` 读出内容。
""",
        "entry": "ex15.py",
        "starterFiles": {
            "ex15.py": 'filename = "sample.txt"\nwith open(filename) as f:\n    print(f"Here is your file {filename}:")\n    print(f.read())\n',
            "sample.txt": "This is stuff I typed into a file.\nIt is really cool stuff.\nLots and lots of fun to have in here.\n",
        },
    },
    16: {
        "body": """# Ex 16 · Reading and Writing Files

练习 `write`。运行后刷新文件树，打开新文件确认内容。
""",
        "entry": "ex16.py",
        "starterFiles": {
            "ex16.py": 'filename = "out.txt"\nwith open(filename, "w") as f:\n    f.write("I am truncating and writing.\\n")\n    f.write("Line two.\\n")\nprint(f"Wrote {filename}")\n'
        },
    },
}


def write_lesson(track: str, lesson_id: str, data: dict) -> None:
    folder = TRACKS / track
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{lesson_id}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def gen_lpthw() -> None:
    for n in range(0, 53):
        lesson_id = f"ex{n:02d}"
        title = LPTHW_TITLES.get(n, f"Exercise {n}")
        if n in FULL_LPTHW:
            payload = {
                "title": f"Ex {n}: {title}",
                "priority": False,
                "outlineOnly": False,
                "requires": [],
                "checklist": ["对照书本做一遍", "改几个数字/字符串再跑"],
                **FULL_LPTHW[n],
            }
            payload.setdefault("timeoutSec", 5)
        else:
            payload = {
                "title": f"Ex {n}: {title}",
                "priority": False,
                "outlineOnly": True,
                "timeoutSec": 5,
                "requires": [],
                "entry": f"{lesson_id}.py",
                "body": f"""# Ex {n} · {title}

提纲占位：对照《Learn Python the Hard Way》本课阅读并在此练习。

## 建议
- 手敲代码，不要复制粘贴
- 每改一处就运行一次
- 把不懂的符号记进笔记

把你的练习代码写在入口文件里即可。
""",
                "starterFiles": {
                    f"{lesson_id}.py": f'# Ex {n}: {title}\nprint("TODO: complete exercise {n}")\n'
                },
                "checklist": ["阅读书中本课", "在此完成练习并运行"],
            }
        write_lesson("lpthw", lesson_id, payload)


ASYNC_LESSONS = [
    (
        "a01",
        "asyncio 基础",
        """# A01 · asyncio 基础

企业 LLM 服务几乎都是异步的。先建立直觉：`async def` 定义协程，`await` 让出等待。

## 目标
- 写一个异步函数并 `asyncio.run`
- 理解「看起来像同步，实际可并发」
""",
        "a01_main.py",
        {
            "a01_main.py": '''import asyncio
import time


async def fetch_fake(name: str, delay: float) -> str:
    print(f"start {name}")
    await asyncio.sleep(delay)
    print(f"done {name}")
    return f"{name}-ok"


async def main() -> None:
    t0 = time.perf_counter()
    # Sequential awaits (not concurrent yet)
    a = await fetch_fake("A", 0.3)
    b = await fetch_fake("B", 0.3)
    print(a, b, f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a02",
        "create_task 与 gather",
        """# A02 · 并发：task / gather

把多个 IO 等待叠在一起。对比 A01 的耗时。
""",
        "a02_main.py",
        {
            "a02_main.py": '''import asyncio
import time


async def fetch_fake(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name}-ok"


async def main() -> None:
    t0 = time.perf_counter()
    results = await asyncio.gather(
        fetch_fake("A", 0.4),
        fetch_fake("B", 0.4),
        fetch_fake("C", 0.4),
    )
    print(results, f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a03",
        "超时与取消",
        """# A03 · 超时与取消

LLM 调用必须设超时。练习 `wait_for` 与 `CancelledError`。
""",
        "a03_main.py",
        {
            "a03_main.py": '''import asyncio


async def slow_llm() -> str:
    await asyncio.sleep(2)
    return "too-late"


async def main() -> None:
    try:
        result = await asyncio.wait_for(slow_llm(), timeout=0.5)
        print(result)
    except asyncio.TimeoutError:
        print("TIMEOUT: upstream LLM did not respond in time")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a04",
        "httpx AsyncClient",
        """# A04 · httpx 异步 HTTP

用 `httpx.AsyncClient` 打一个公开 JSON API（需本机网络）。把状态码与耗时打出来。
""",
        "a04_main.py",
        {
            "a04_main.py": '''import asyncio
import time
import httpx


async def main() -> None:
    t0 = time.perf_counter()
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get("https://httpbin.org/json")
        print("status", resp.status_code)
        print(resp.json())
    print(f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        15,
    ),
    (
        "a05",
        "流式 chunk（模拟 LLM）",
        """# A05 · 流式输出

企业聊天接口常用 token/chunk 流。这里用异步生成器模拟。
""",
        "a05_main.py",
        {
            "a05_main.py": '''import asyncio


async def fake_llm_stream(prompt: str):
    tokens = ["Hello", ", ", "this", " ", "is", " ", "streamed", " ", "output", "."]
    for t in tokens:
        await asyncio.sleep(0.05)
        yield t


async def main() -> None:
    print("prompt accepted")
    async for chunk in fake_llm_stream("hi"):
        print(chunk, end="", flush=True)
    print("\\n[done]")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a06",
        "Semaphore 限流",
        """# A06 · 并发限流

对模型 API 必须限流，避免打爆配额。用 `Semaphore` 控制同时进行的调用数。
""",
        "a06_main.py",
        {
            "a06_main.py": '''import asyncio
import time

SEM = asyncio.Semaphore(2)


async def call_model(i: int) -> str:
    async with SEM:
        print(f"enter {i}")
        await asyncio.sleep(0.3)
        print(f"leave {i}")
        return f"r{i}"


async def main() -> None:
    t0 = time.perf_counter()
    results = await asyncio.gather(*(call_model(i) for i in range(6)))
    print(results, f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a07",
        "Queue 缓冲",
        """# A07 · 生产者-消费者 Queue

请求洪峰时用队列削峰。一个生产者投递，多个 worker 消费。
""",
        "a07_main.py",
        {
            "a07_main.py": '''import asyncio


async def producer(q: asyncio.Queue) -> None:
    for i in range(5):
        await q.put({"id": i, "prompt": f"q{i}"})
        print("enqueued", i)
    for _ in range(2):
        await q.put(None)  # poison pills


async def worker(name: str, q: asyncio.Queue) -> None:
    while True:
        item = await q.get()
        if item is None:
            q.task_done()
            break
        await asyncio.sleep(0.1)
        print(name, "handled", item["id"])
        q.task_done()


async def main() -> None:
    q: asyncio.Queue = asyncio.Queue()
    await asyncio.gather(producer(q), worker("w1", q), worker("w2", q))
    print("drained")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a08",
        "结构化输出与重试",
        """# A08 · JSON 结构化输出 + 重试

工具调用/结构化输出常失败。练习：校验 JSON，失败则重试有限次。
""",
        "a08_main.py",
        {
            "a08_main.py": '''import asyncio
import json
import random
from typing import Any


async def flaky_model() -> str:
    await asyncio.sleep(0.05)
    if random.random() < 0.6:
        return "{not-json"
    return json.dumps({"action": "search", "query": "fastapi timeout"})


def validate(payload: str) -> dict[str, Any]:
    data = json.loads(payload)
    assert "action" in data and "query" in data
    return data


async def call_with_retry(max_attempts: int = 5) -> dict[str, Any]:
    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        raw = await flaky_model()
        try:
            data = validate(raw)
            print(f"success on attempt {attempt}")
            return data
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            print(f"attempt {attempt} failed: {exc}")
    raise RuntimeError(f"failed after retries: {last_err}")


async def main() -> None:
    print(await call_with_retry())


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a09",
        "迷你 RAG 流水线骨架",
        """# A09 · 异步 RAG 骨架

流程：读本地 docs → 朴素检索 → 拼 prompt → 假 LLM → 写 `answer.txt`。

这是企业落地的主干形状；真实项目会替换检索与模型客户端。
""",
        "a09_main.py",
        {
            "a09_main.py": '''import asyncio
from pathlib import Path


DOCS = {
    "fastapi.txt": "FastAPI supports async def routes and dependency injection.",
    "timeouts.txt": "Always set timeouts and retries for LLM HTTP calls.",
    "rag.txt": "RAG retrieves context documents before generation.",
}


async def retrieve(query: str, k: int = 2) -> list[str]:
    await asyncio.sleep(0.05)
    scored = []
    for name, text in DOCS.items():
        score = sum(1 for w in query.lower().split() if w in text.lower())
        scored.append((score, name, text))
    scored.sort(reverse=True)
    return [f"[{n}] {t}" for s, n, t in scored[:k] if s > 0] or [f"[{scored[0][1]}] {scored[0][2]}"]


async def fake_llm(prompt: str) -> str:
    await asyncio.sleep(0.1)
    return "Based on context: " + prompt.split("Context:", 1)[-1][:120].strip()


async def main() -> None:
    query = "How do I set timeouts in FastAPI LLM calls?"
    ctx = await retrieve(query)
    prompt = "Question: " + query + "\\nContext:\\n" + "\\n".join(ctx)
    answer = await fake_llm(prompt)
    Path("answer.txt").write_text(answer + "\\n", encoding="utf-8")
    print(answer)
    print("wrote answer.txt")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
]


PYTORCH_LESSONS = [
    (
        "p01",
        "Tensor 基础",
        """# P01 · Tensor 基础

张量是 PyTorch 的核心数据结构。练习创建、形状、dtype。

若报错 `No module named 'torch'`，在项目根执行（先 `proxy_on`）：
`uv sync --extra ml`
或 `npm run install:ml`

不要使用 Linux 的 `whl/cpu` 索引。本课会检测 MPS。
""",
        "p01_main.py",
        {
            "p01_main.py": '''import torch


def pick_device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


device = pick_device()
print("torch", torch.__version__)
print("device", device)
print("mps_built", torch.backends.mps.is_built(), "mps_available", torch.backends.mps.is_available())

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], device=device)
print("x", x)
print("shape", tuple(x.shape), "dtype", x.dtype)
print("x + 1", x + 1)
print("matmul", x @ x.T)
'''
        },
        30,
        ["torch"],
    ),
    (
        "p02",
        "autograd",
        """# P02 · 自动求导

`requires_grad=True` 的张量可反传。理解 `loss.backward()` 与 `.grad`。
注意：本课默认 CPU，梯度查看更直观。
""",
        "p02_main.py",
        {
            "p02_main.py": '''import torch

x = torch.tensor(2.0, requires_grad=True)
y = x**2 + 3 * x + 1
y.backward()
print("y", float(y))
print("dy/dx", float(x.grad))
'''
        },
        30,
        ["torch"],
    ),
    (
        "p03",
        "nn.Module 一步优化",
        """# P03 · Module + 一步优化

线性层拟合一个简单目标，跑几步 SGD。
""",
        "p03_main.py",
        {
            "p03_main.py": '''import torch
import torch.nn as nn

torch.manual_seed(0)
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.MSELoss()

x = torch.linspace(-1, 1, 20).unsqueeze(1)
y = 2 * x + 0.5

for step in range(50):
    pred = model(x)
    loss = loss_fn(pred, y)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step % 10 == 0:
        print(f"step={step} loss={loss.item():.4f}")

print("weight", model.weight.item(), "bias", model.bias.item())
'''
        },
        60,
        ["torch"],
    ),
    (
        "p04",
        "Dataset / DataLoader",
        """# P04 · Dataset 与 DataLoader

从 `data.csv` 读入，按 batch 迭代。
""",
        "p04_main.py",
        {
            "data.csv": "x,y\\n0,0.5\\n1,2.5\\n2,4.5\\n3,6.5\\n4,8.5\\n",
            "p04_main.py": '''import csv
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Dataset


class CsvXy(Dataset):
    def __init__(self, path: str) -> None:
        rows = list(csv.DictReader(Path(path).open()))
        self.x = torch.tensor([[float(r["x"])] for r in rows], dtype=torch.float32)
        self.y = torch.tensor([[float(r["y"])] for r in rows], dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, idx: int):
        return self.x[idx], self.y[idx]


ds = CsvXy("data.csv")
loader = DataLoader(ds, batch_size=2, shuffle=False)
for batch_x, batch_y in loader:
    print("batch", batch_x.tolist(), batch_y.tolist())
'''
        },
        60,
        ["torch"],
    ),
    (
        "p05",
        "训练循环并保存权重",
        """# P05 · 训练循环 + state_dict

训练后保存 `model.pt`，在文件树中确认生成。
""",
        "p05_main.py",
        {
            "p05_main.py": '''import torch
import torch.nn as nn

torch.manual_seed(0)
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.MSELoss()
x = torch.linspace(-1, 1, 40).unsqueeze(1)
y = -1.5 * x + 0.25

for epoch in range(80):
    loss = loss_fn(model(x), y)
    opt.zero_grad()
    loss.backward()
    opt.step()

torch.save(model.state_dict(), "model.pt")
print("saved model.pt loss=", float(loss))
'''
        },
        90,
        ["torch"],
    ),
    (
        "p06",
        "推理脚本",
        """# P06 · 加载权重推理

先运行 P05 生成 `model.pt`，或本课会训练一个临时模型再推理。把预测写入 `preds.txt`。
""",
        "p06_main.py",
        {
            "p06_main.py": '''from pathlib import Path

import torch
import torch.nn as nn

model = nn.Linear(1, 1)
path = Path("model.pt")
if not path.exists():
    # bootstrap if p05 not run
    opt = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = nn.MSELoss()
    x = torch.linspace(-1, 1, 40).unsqueeze(1)
    y = -1.5 * x + 0.25
    for _ in range(80):
        loss = loss_fn(model(x), y)
        opt.zero_grad()
        loss.backward()
        opt.step()
    torch.save(model.state_dict(), path)

model.load_state_dict(torch.load(path, weights_only=True))
model.eval()
with torch.no_grad():
    xs = torch.tensor([[-1.0], [0.0], [1.0]])
    preds = model(xs).squeeze(1).tolist()

lines = [f"{x[0]:.1f},{p:.4f}" for x, p in zip(xs.tolist(), preds)]
Path("preds.txt").write_text("\\n".join(lines) + "\\n", encoding="utf-8")
print("preds", preds)
'''
        },
        90,
        ["torch"],
    ),
    (
        "p07",
        "小文本分类",
        """# P07 · 迷你文本分类

Bag of Words + 线性层。数据很小，默认 CPU 即可；有 MPS 时可自行 `.to("mps")` 试验。
""",
        "p07_main.py",
        {
            "p07_main.py": '''import torch
import torch.nn as nn

pairs = [
    ("good film great actors", 1),
    ("amazing movie loved it", 1),
    ("terrible plot boring", 0),
    ("bad acting waste time", 0),
    ("wonderful story", 1),
    ("awful experience", 0),
]

vocab: dict[str, int] = {}
for text, _ in pairs:
    for w in text.split():
        vocab.setdefault(w, len(vocab))


def vectorize(text: str) -> torch.Tensor:
    v = torch.zeros(len(vocab))
    for w in text.split():
        if w in vocab:
            v[vocab[w]] += 1
    return v


X = torch.stack([vectorize(t) for t, _ in pairs])
y = torch.tensor([label for _, label in pairs], dtype=torch.float32).unsqueeze(1)

model = nn.Linear(len(vocab), 1)
opt = torch.optim.Adam(model.parameters(), lr=0.1)
loss_fn = nn.BCEWithLogitsLoss()

for epoch in range(200):
    logits = model(X)
    loss = loss_fn(logits, y)
    opt.zero_grad()
    loss.backward()
    opt.step()

with torch.no_grad():
    probs = torch.sigmoid(model(X)).squeeze(1)
print("probs", [round(float(p), 3) for p in probs])
print("loss", float(loss))
'''
        },
        120,
        ["torch"],
    ),
    (
        "p08",
        "asyncio.to_thread 桥接",
        """# P08 · 异步服务里跑同步推理

FastAPI/异步 worker 中不要直接在事件循环里跑重计算。用 `asyncio.to_thread` 包一层。
""",
        "p08_main.py",
        {
            "p08_main.py": '''import asyncio
import time

import torch
import torch.nn as nn

model = nn.Linear(4, 2)
model.eval()


def sync_infer(batch: list[list[float]]) -> list[list[float]]:
    # pretend this is heavy
    time.sleep(0.2)
    with torch.no_grad():
        x = torch.tensor(batch, dtype=torch.float32)
        return model(x).tolist()


async def handle_request(batch: list[list[float]]) -> list[list[float]]:
    return await asyncio.to_thread(sync_infer, batch)


async def main() -> None:
    t0 = time.perf_counter()
    a, b = await asyncio.gather(
        handle_request([[0.1, 0.2, 0.3, 0.4]]),
        handle_request([[0.5, 0.4, 0.3, 0.2]]),
    )
    print("results", a, b)
    print(f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        60,
        ["torch"],
    ),
]


def gen_async() -> None:
    for lesson_id, title, body, entry, files, timeout in ASYNC_LESSONS:
        write_lesson(
            "async-llm",
            lesson_id,
            {
                "title": f"{lesson_id.upper()}: {title}",
                "priority": True,
                "outlineOnly": False,
                "timeoutSec": timeout,
                "requires": [],
                "entry": entry,
                "body": body,
                "starterFiles": files,
                "checklist": ["阅读说明", "运行并解释输出", "改参数再跑一次"],
            },
        )


def gen_pytorch() -> None:
    for lesson_id, title, body, entry, files, timeout, requires in PYTORCH_LESSONS:
        # fix escaped newlines in csv accidentally double-escaped
        fixed = {}
        for k, v in files.items():
            fixed[k] = v.replace("\\n", "\n") if k.endswith(".csv") else v
        write_lesson(
            "pytorch",
            lesson_id,
            {
                "title": f"{lesson_id.upper()}: {title}",
                "priority": True,
                "outlineOnly": False,
                "timeoutSec": timeout,
                "requires": requires,
                "entry": entry,
                "body": body,
                "starterFiles": fixed,
                "checklist": ["确认 torch 已安装（如需要）", "运行通过", "查看生成的文件"],
            },
        )


if __name__ == "__main__":
    gen_lpthw()
    gen_async()
    gen_pytorch()
    print("content generated")
