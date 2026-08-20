#!/usr/bin/env python3
"""Generate LLMFromScratch track — Appendix A (PyTorch intro) study guides.

Aligned with Sebastian Raschka, Build a Large Language Model (From Scratch),
Appendix A section topics. Original Chinese guides + runnable starters;
does NOT copy book prose.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "tracks" / "llm-from-scratch"


def write(lesson_id: str, payload: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{lesson_id}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def lesson(
    lesson_id: str,
    title: str,
    body: str,
    entry: str,
    code: str,
    *,
    extra: dict[str, str] | None = None,
    timeout: int = 60,
    section: str = "",
) -> None:
    files = {entry: code}
    if extra:
        files.update(extra)
    header = f"# {lesson_id.upper()} · {title}\n\n"
    if section:
        header += f"对应《从零开始构建大模型》**附录 A · {section}**（原创练习提纲，非书中原文）。\n\n"
    else:
        header += "对应《从零开始构建大模型》**附录 A**（原创练习提纲，非书中原文）。\n\n"
    write(
        lesson_id,
        {
            "title": f"{lesson_id.upper()}: {title}",
            "priority": True,
            "outlineOnly": False,
            "timeoutSec": timeout,
            "requires": ["torch"],
            "entry": entry,
            "body": header + body.strip() + "\n",
            "starterFiles": files,
            "checklist": ["对照书本附录 A 阅读", "运行本课代码", "改参数再跑一次"],
        },
    )


def main() -> None:
    lesson(
        "lfs01",
        "What is PyTorch",
        """## 目标
- 确认本机已安装 PyTorch
- 理解：张量计算 + 自动求导，是后续 LLM 实现的底座

## 自检
- [ ] 打印出版本与设备信息
""",
        "lfs01_main.py",
        '''import torch

print("torch", torch.__version__)
print("cuda", torch.cuda.is_available())
print("mps", torch.backends.mps.is_available())
print("default_dtype", torch.get_default_dtype())
''',
        section="A.1 What is PyTorch",
        timeout=30,
    )

    lesson(
        "lfs02",
        "Scalars, vectors, matrices, tensors",
        """## 目标
- 分清 0D/1D/2D/3D 张量
- 会用 `.shape` / `.ndim` 观察结构

## 自检
- [ ] 能说出每个示例的维度含义
""",
        "lfs02_main.py",
        '''import torch

scalar = torch.tensor(1.0)
vector = torch.tensor([1.0, 2.0, 3.0])
matrix = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
tensor3d = torch.tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], dtype=torch.float32)

for name, t in [("scalar", scalar), ("vector", vector), ("matrix", matrix), ("3d", tensor3d)]:
    print(f"{name:8} ndim={t.ndim} shape={tuple(t.shape)} -> {t}")
''',
        section="A.2.1 Scalars, vectors, matrices, and tensors",
    )

    lesson(
        "lfs03",
        "Tensor data types",
        """## 目标
- 认识常见 dtype：`float32` / `int64` / `bool`
- 会用 `.to(dtype=...)` 转换

## 自检
- [ ] 理解 LLM 训练里常用 float32（有时再混精度）
""",
        "lfs03_main.py",
        '''import torch

x = torch.tensor([1, 2, 3])
print("default int tensor", x, x.dtype)

y = x.to(torch.float32)
print("as float32", y, y.dtype)

z = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float64)
print("float64", z.dtype, "-> float32", z.to(torch.float32).dtype)

mask = y > 1.5
print("bool mask", mask, mask.dtype)
''',
        section="A.2.2 Tensor data types",
    )

    lesson(
        "lfs04",
        "Common tensor operations",
        """## 目标
- 练习 `reshape` / `view`、转置、矩阵乘、广播
- 知道 `view` 要求内存连续，必要时 `.contiguous()`

## 自检
- [ ] 改形状再 matmul，不报错
""",
        "lfs04_main.py",
        '''import torch

x = torch.arange(6)
print("x", x)
print("reshape (2,3)", x.reshape(2, 3))
print("view (3,2)", x.view(3, 2))

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
b = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
print("a @ b\\n", a @ b)
print("a.T\\n", a.T)

# broadcasting
v = torch.tensor([10.0, 20.0])
print("a + v\\n", a + v)
''',
        section="A.2.3 Common PyTorch tensor operations",
    )

    lesson(
        "lfs05",
        "Indexing tensors",
        """## 目标
- 掌握切片、花式索引、布尔索引
- 知道索引可能返回视图（改动可能影响原张量）

## 自检
- [ ] 取出矩阵第二行第一列
""",
        "lfs05_main.py",
        '''import torch

t = torch.arange(12).reshape(3, 4)
print(t)
print("row0", t[0])
print("col1", t[:, 1])
print("t[1, 2]", t[1, 2])
print("rows 0:2, cols 1:3\\n", t[0:2, 1:3])

idx = torch.tensor([0, 2])
print("fancy rows", t[idx])
print("where > 5", t[t > 5])
''',
        section="A.3 Seeing tensors in action / indexing",
    )

    lesson(
        "lfs06",
        "Automatic differentiation",
        """## 目标
- 理解 `requires_grad`、`backward`、`.grad`
- 知道训练步里为何要 `zero_grad`

## 自检
- [ ] 对简单函数求出正确梯度
""",
        "lfs06_main.py",
        '''import torch

x = torch.tensor(3.0, requires_grad=True)
y = torch.tensor(2.0, requires_grad=True)
# f = x^2 * y + y
f = x**2 * y + y
f.backward()
print("f", float(f))
print("df/dx", float(x.grad))  # 2*x*y = 12
print("df/dy", float(y.grad))  # x^2 + 1 = 10

# next step in a training loop would clear grads:
x.grad.zero_()
y.grad.zero_()
print("cleared", x.grad, y.grad)
''',
        section="A.4 Automatic differentiation via autograd",
    )

    lesson(
        "lfs07",
        "Multilayer nets with nn.Module",
        """## 目标
- 用 `nn.Module` 定义小型 MLP
- 前向：`model(x)`；参数：`model.parameters()`

## 自检
- [ ] 打印参数形状，完成一次前向
""",
        "lfs07_main.py",
        '''import torch
import torch.nn as nn

class TinyMLP(nn.Module):
    def __init__(self, in_dim=4, hidden=8, out_dim=2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x):
        return self.net(x)

torch.manual_seed(0)
model = TinyMLP()
x = torch.randn(3, 4)
logits = model(x)
print("out shape", tuple(logits.shape))
for name, p in model.named_parameters():
    print(name, tuple(p.shape))
''',
        section="A.5 Implementing multilayer neural networks",
    )

    lesson(
        "lfs08",
        "Dataset and DataLoader",
        """## 目标
- 实现最小 `Dataset`
- 用 `DataLoader` 按 batch 迭代（LLM 预训练同理，只是样本变成 token 块）

## 自检
- [ ] 看到两个 batch 打印
""",
        "lfs08_main.py",
        '''import torch
from torch.utils.data import DataLoader, Dataset


class ToyReg(Dataset):
    def __init__(self, n=20):
        self.x = torch.linspace(-1, 1, n).unsqueeze(1)
        self.y = 2 * self.x + 0.1

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return self.x[i], self.y[i]


loader = DataLoader(ToyReg(), batch_size=8, shuffle=True)
for step, (bx, by) in enumerate(loader):
    print(f"batch {step}: x{tuple(bx.shape)} y{tuple(by.shape)}")
''',
        section="A.6 Setting up efficient data loaders",
    )

    lesson(
        "lfs09",
        "A typical training loop",
        """## 目标
- 串起：前向 → loss → backward → optimizer.step
- 观察 loss 下降

## 自检
- [ ] loss 整体下降
""",
        "lfs09_main.py",
        '''import torch
import torch.nn as nn

torch.manual_seed(0)
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.MSELoss()
x = torch.linspace(-1, 1, 40).unsqueeze(1)
y = 3 * x - 1

for epoch in range(60):
    pred = model(x)
    loss = loss_fn(pred, y)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if epoch % 10 == 0:
        print(f"epoch={epoch:02d} loss={loss.item():.4f}")

print("weight", model.weight.item(), "bias", model.bias.item())
''',
        section="A.7 A typical training loop",
        timeout=90,
    )

    lesson(
        "lfs10",
        "Saving and loading models",
        """## 目标
- 保存 / 加载 `state_dict`
- 推理前 `model.eval()` + `torch.no_grad()`

## 自检
- [ ] 文件树出现 `toy.pt`，加载后预测一致
""",
        "lfs10_main.py",
        '''from pathlib import Path

import torch
import torch.nn as nn

torch.manual_seed(0)
model = nn.Linear(1, 1)
# quick fit
opt = torch.optim.SGD(model.parameters(), lr=0.1)
x = torch.linspace(-1, 1, 30).unsqueeze(1)
y = -0.5 * x + 0.2
for _ in range(80):
    loss = ((model(x) - y) ** 2).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()

path = Path("toy.pt")
torch.save(model.state_dict(), path)
print("saved", path)

loaded = nn.Linear(1, 1)
loaded.load_state_dict(torch.load(path, weights_only=True))
loaded.eval()
with torch.no_grad():
    q = torch.tensor([[0.0], [1.0]])
    print("pred", loaded(q).squeeze().tolist())
''',
        section="A.8 Saving and loading models",
        timeout=90,
    )

    lesson(
        "lfs11",
        "Compute devices (CPU / MPS / CUDA)",
        """## 目标
- 会选择设备：Mac 优先 MPS，否则 CPU；有 NVIDIA 则 CUDA
- `.to(device)` 移动模型与数据

## 自检
- [ ] 张量确实在所选 device 上
""",
        "lfs11_main.py",
        '''import torch


def pick_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


device = pick_device()
print("using", device)
x = torch.randn(2, 3, device=device)
w = torch.randn(3, 4, device=device)
y = x @ w
print("y", tuple(y.shape), y.device)
''',
        section="A.9.1 PyTorch computations on GPU devices",
        timeout=30,
    )

    lesson(
        "lfs12",
        "Single-device training",
        """## 目标
- 在选定 device 上跑完一个小训练循环（Mac 上通常是 MPS）
- 记住：模型和 batch 必须在同一 device

## 自检
- [ ] 无 device mismatch 报错，loss 下降
""",
        "lfs12_main.py",
        '''import torch
import torch.nn as nn


def pick_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


device = pick_device()
print("device", device)
torch.manual_seed(0)
model = nn.Sequential(nn.Linear(1, 16), nn.ReLU(), nn.Linear(16, 1)).to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-2)
x = torch.linspace(-1, 1, 64, device=device).unsqueeze(1)
y = torch.sin(3 * x)

for epoch in range(100):
    pred = model(x)
    loss = ((pred - y) ** 2).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()
    if epoch % 20 == 0:
        print(f"epoch={epoch} loss={loss.item():.4f}")
''',
        section="A.9.2 Single-GPU training",
        timeout=120,
    )

    lesson(
        "lfs13",
        "Multi-GPU overview (conceptual)",
        """## 目标
- 理解 DataParallel / DDP 在多卡时的角色
- 本机若无多 GPU，用「单卡模拟」跑通结构，不要求真多卡

## 说明
附录 A 后半讲多卡加速。笔记本学习站以单机为主；这里只建立概念，真正 DDP 需多进程启动。

## 自检
- [ ] 读懂注释；单卡路径跑通
""",
        "lfs13_main.py",
        '''import torch
import torch.nn as nn

print("cuda_device_count =", torch.cuda.device_count())
print("Tip: true DDP needs torchrun / multiple processes.")
print("Here we just train on one device, as you will on a laptop.")

device = torch.device("cpu")
model = nn.Linear(4, 2).to(device)
x = torch.randn(8, 4, device=device)
y = torch.randn(8, 2, device=device)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
loss = ((model(x) - y) ** 2).mean()
loss.backward()
opt.step()
print("single-process step ok, loss=", float(loss))
''',
        section="A.9.3 Training with multiple GPUs",
        timeout=30,
    )

    print(f"wrote {len(list(OUT.glob('*.json')))} lessons -> {OUT}")


if __name__ == "__main__":
    main()
