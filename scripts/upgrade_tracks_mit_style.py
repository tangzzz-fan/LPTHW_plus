#!/usr/bin/env python3
"""Upgrade async-llm / pytorch / llm-from-scratch to mit-python lesson standard.

Run AFTER generators (raw starter code), BEFORE or instead of generic annotate
section-markers for these tracks.

mit-python standard:
- Body: 来源 → 关键概念（机制写在题目文档）→ 本题任务 → 动手要求 → 自检
- Starter: 手敲横幅 → 本题说明/撞墙提示 → 全注释参考实现 → 占位 print
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "content" / "tracks"

MIT_HEADER = """\
# =============================================================================
# 自己动手敲（笨方法 / 代码题）：
# 1) 先读左侧「本题任务 / 关键概念」，再敲下面「已注释」的参考实现（或去掉行首 #）
# 2) 删掉最底部的占位 print
# 3) 保存并运行（⌘/Ctrl+Enter）
# 关键机制以题目文档为准；代码注释只是现场提示，不要只抄不读讲义。
# =============================================================================
"""

MIT_FOOTER = """
# =============================================================================
# 写完练习后，删除下面这行占位再运行：
print("(请在上方自行输入代码)")
"""

TRACK_META = {
    "async-llm": {
        "source": "本站优先轨 · 企业 LLM 异步落地（原创讲义；手敲练习）",
    },
    "pytorch": {
        "source": "本站优先轨 · PyTorch 入门到推理（原创讲义；手敲练习）",
    },
    "llm-from-scratch": {
        "source": "对照《从零开始构建大模型》附录 A（原创提纲，非书中原文；手敲练习）",
    },
}

LESSONS: dict[str, dict[str, dict]] = {
    "async-llm": {
        "a01": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `async def` | 调用后得到 **coroutine 对象**，函数体此时还不跑 |
| `await` | 当前协程让出；等的对象完成后才继续 |
| `asyncio.run` | 创建事件循环、跑到主协程结束、再关掉循环 |
| 顺序 await | 两个 `await` 串行：总耗时 ≈ 相加（本课刻意先感受「还不并发」） |

**易错**：把 `async def` 当成普通函数「一调用就执行」——那是线程/GCD 心智，不是 asyncio。""",
            "task": """手敲一个 `fetch_fake`，在 `main` 里 **先后** `await` 两次，打印结果与 `perf_counter` 耗时。

验收：能解释「为何总时间接近两次 delay 之和」。""",
            "walls": [
                "墙：先写了两次 await 却以为已经并发——看耗时才发现仍是串行（并发在 A02）。",
                "墙：忘了 asyncio.run，直接调 main() 得到 coroutine 警告。",
            ],
            "brief": "A01：协程基础——先串行 await，建立「调用≠执行」的直觉。",
        },
        "a02": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `asyncio.gather` | 并发调度多个 awaitable，一起等结果 |
| Task | `create_task` 把协程丢进 loop 立即返回 Task；gather 内部也会包 Task |
| 耗时对比 | 三个 0.4s IO 并发 ≈ 0.4s，不是 1.2s |

**与 A01 对照**：A01 串行叠时间；A02 叠等待。""",
            "task": """用 `gather` 并发三个假 IO，打印结果与耗时。

验收：耗时接近单个 delay，并能口述 gather 在等什么。""",
            "walls": ["墙：写成三个顺序 await，耗时仍是 1.2s 量级——对照才懂 gather。"],
            "brief": "A02：gather 并发——把多个等待叠在一起。",
        },
        "a03": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `asyncio.wait_for` | 超时则取消内部 awaitable，并向调用方抛 `TimeoutError` |
| 取消 | 被取消的协程通常在下一个 await 点收到取消；清理靠 finally |
| 企业含义 | LLM 上游必须设超时，否则连接/工人被拖死 |

**注意**：教学环境常见 `TimeoutError`；生产还要区分取消与业务失败。""",
            "task": """对一个故意 sleep 2s 的 `slow_llm` 设 0.5s 超时，捕获并打印超时信息。""",
            "walls": ["墙：超时后仍以为协程会跑完——取消语义要另做实验（见 mit-python T6）。"],
            "brief": "A03：wait_for 超时——上游 LLM 必须有截止时间。",
        },
        "a04": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `httpx.AsyncClient` | 异步 HTTP 客户端；用 `async with` 管理连接池生命周期 |
| `timeout=` | 必须显式设置；默认过长等于没设 |
| 网络依赖 | 本课打公开 API；无网时失败属环境问题 |

**企业习惯**：Client 在 app 生命周期内复用，而不是每个请求新建。""",
            "task": """用 AsyncClient GET 一个 JSON URL，打印 status、body、耗时。需本机网络。""",
            "walls": [
                "墙：忘了 timeout，请求挂死难排查。",
                "墙：每次请求 new Client，连接建得又慢又费。",
            ],
            "brief": "A04：httpx.AsyncClient——异步 HTTP 的基本形。",
        },
        "a05": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 异步生成器 | `async def` + `yield`：每次 yield 可挂起，适合 token 流 |
| `async for` | 消费异步可迭代；背后是 `__aiter__` / `__anext__` |
| 与同步 for | 同步 for 不能直接消费异步生成器 |

**对照 A13**：本课是内存里的流；A13 是 HTTP/SSE 上的流。""",
            "task": """实现 `fake_llm_stream`，用 `async for` 边收边打印（`end=\"\"`）。""",
            "walls": ["墙：用普通 for 去迭代 async gen → TypeError。"],
            "brief": "A05：异步生成器模拟 LLM token 流。",
        },
        "a06": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `Semaphore(n)` | 同时进入临界区的协程最多 n 个 |
| `async with sem` | acquire → 做事 → release；异常路径也会释放 |
| 限流位置 | 客户端限流保护配额；服务端限流保护自身 |

**观察点**：6 个任务、容量 2 时，应成批进入（看 enter/leave 日志）。""",
            "task": """Semaphore(2) 包住假模型调用，gather 6 个任务，观察并发度与总耗时。""",
            "walls": ["墙：把 sleep 放在 semaphore 外面，限流形同虚设。"],
            "brief": "A06：Semaphore 限流——别打爆模型配额。",
        },
        "a07": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `asyncio.Queue` | 协程间传递工作项；可设 `maxsize` 做背压 |
| 毒丸 (None) | 约定结束信号；worker 数与毒丸数要匹配 |
| 削峰 | 入口快速入队，工人池慢慢消费 |

**企业形状**：网关/API 入队，推理工人消费。""",
            "task": """一个 producer 入队，两个 worker 消费；用 None 毒丸结束。""",
            "walls": ["墙：毒丸数量 < worker 数 → 有人永远阻塞在 get。"],
            "brief": "A07：Queue 生产者-消费者削峰。",
        },
        "a08": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 结构化输出 | 模型返回必须能 `json.loads` 且过字段校验 |
| 有限重试 | 校验失败再要一次；设 `max_attempts`，避免无限烧钱 |
| 失败分类 | JSON 坏 / 缺字段 / 业务拒绝——策略可以不同 |

**与 A11**：A08 是内容校验失败；A11 是 HTTP 层失败。""",
            "task": """实现 `call_with_retry`：拉假模型 → validate → 失败则重试，成功打印 attempt。""",
            "walls": ["墙：捕获太宽把 KeyboardInterrupt 也吞了；或重试不打日志导致瞎等。"],
            "brief": "A08：JSON 结构化输出 + 有限重试。",
        },
        "a09": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| RAG 骨架 | retrieve → 拼 prompt（问题+上下文）→ generate → 落盘/返回 |
| 检索 | 本课用词重叠假检索；真项目换向量库/BM25 |
| 边界 | 「有上下文」≠「答案正确」——还要引用与拒答策略 |

**企业主干**：换客户端与检索实现，流水线形状常不变。""",
            "task": """实现 retrieve + fake_llm，写出 `answer.txt` 并打印答案。""",
            "walls": ["墙：把整库 docs 塞进 prompt 不截断——token 爆炸（习惯要早养成）。"],
            "brief": "A09：迷你 RAG 流水线骨架。",
        },
        "a10": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 阻塞杀 loop | 在协程里直接 `time.sleep` / 同步 SDK → 整个事件循环卡住 |
| `asyncio.to_thread` | 把阻塞调用丢默认线程池，主协程可继续调度别人 |
| 对比实验 | good：两个 to_thread 可重叠；bad：两次直接阻塞 ≈ 两倍时间 |

**企业习惯**：同步厂商 SDK 一律 to_thread / executor，主路径只编排。""",
            "task": """实现 sync SDK 假函数；对比 `good_call`（to_thread）与 `bad_call`（直接调）的耗时。""",
            "walls": ["墙：在 FastAPI async 路由里直接调同步 SDK，线上 QPS 一掉到底。"],
            "brief": "A10：to_thread 桥接同步 LLM SDK。",
        },
        "a11": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 可重试状态码 | 通常 429、5xx；多数 4xx（除 429）重试无意义 |
| 指数退避 | delay、2×delay… + 可选抖动，防重试风暴 |
| MockTransport | 本课不依赖外网，用 httpx 模拟 503→200 |

**与 A08**：A08 内容校验；本课 HTTP 层。""",
            "task": """实现 `get_with_backoff`：503 重试，最终拿到 200 JSON。""",
            "walls": ["墙：对 400 也狂重试，只会放大事故。"],
            "brief": "A11：HTTP 错误分类 + 指数退避（Mock）。",
        },
        "a12": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| FastAPI `async def` | 路由协程跑在事件循环上；内部不要阻塞 |
| 路由内超时 | `wait_for` 卡死上游；超时映射为 HTTP 504 等 |
| ASGITransport | 用 httpx 测 app，不必起 uvicorn |

**企业形状**：HTTP 入口 → 超时预算 → await 模型客户端。""",
            "task": """定义 `/chat`：成功路径 200；slow>budget 返回 504。用 ASGITransport 自测。""",
            "walls": ["墙：路由写成 def（同步）却在里面 asyncio.run——套娃与阻塞风险。"],
            "brief": "A12：FastAPI 异步路由 + 上游超时。",
        },
        "a13": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| SSE / chunk | `data: ...` 行协议；`[DONE]` 常作结束 |
| `client.stream` + `aiter_lines` | 边下边解析，不要一次性 `read()` 大 body |
| 与 A05 | A05 内存生成器；本课 HTTP 流 |

**背压**：生产快消费慢时用有界缓冲（进阶见 Queue 课）。""",
            "task": """Mock SSE body，用 stream API 拼出完整文本并打印 chunk。""",
            "walls": ["墙：用 resp.text 一次读完，失去「流式」意义。"],
            "brief": "A13：消费 HTTP/SSE 流式响应。",
        },
        "a14": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 熔断状态 | 关闭（正常）→ 打开（快速失败）→ 半开（试探）→ 成功则关闭 |
| 阈值 | 连续失败 N 次打开；冷却后允许一次探测 |
| 目的 | 保护自己与下游，避免雪崩；与重试搭配而非替代 |

**教学级**：生产可换网关/pybreaker；语义要先懂。""",
            "task": """实现简易 CircuitBreaker，对 flaky_upstream 调用并打印 open/fast-fail/ok。""",
            "walls": ["墙：打开后从不半开，服务恢复了也一直失败。"],
            "brief": "A14：简易熔断器状态机。",
        },
    },
    "pytorch": {
        "p01": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| Tensor | 多维数组 + 设备 + dtype；后续一切计算的载体 |
| device | `cpu` / `mps`（Apple）/ `cuda`；张量与运算要在同一设备 |
| 安装 | `uv sync --extra ml`；**不要**用 Linux `whl/cpu` 索引装 Mac 包 |""",
            "task": """检测 MPS/CPU，创建 2×2 张量，打印版本、设备、运算结果。""",
            "walls": ["墙：装了 CPU 轮子在 Mac 上，MPS 永远 False。"],
            "brief": "P01：Tensor 基础与设备选择。",
        },
        "p02": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `requires_grad=True` | 该张量参与微分磁带 |
| `backward()` | 从标量损失反传，填 `.grad` |
| 叶子参数 | 一般对叶子参数求梯度；中间量默认不保留 |""",
            "task": """对可导标量做简单函数，backward 后打印 grad。""",
            "walls": ["墙：对非标量调用 backward 忘了指定 grad_tensors。"],
            "brief": "P02：autograd 一次最小闭环。",
        },
        "p03": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `nn.Module` | 参数容器 + `forward`；`model(x)` 走 `__call__`→forward |
| `parameters()` | 优化器要知道更新哪些张量 |
| 一步优化 | loss → backward → optimizer.step → zero_grad |""",
            "task": """小 Linear（或 Sequential），跑通一步前向+反传+step。""",
            "walls": ["墙：忘记 zero_grad，梯度越加越大。"],
            "brief": "P03：nn.Module 与一步优化。",
        },
        "p04": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| Dataset | `__len__` + `__getitem__`：按索引取样本 |
| DataLoader | 批采样、打乱；collate 默认 stack 成 batch 维 |
| 管道 | 文件 → Dataset → DataLoader → 训练循环 |""",
            "task": """读本课 CSV（或内置样本），Dataset+DataLoader 迭代打印一个 batch。""",
            "walls": ["墙：getitem 返回 list 而不是 tensor，collate 行为怪异。"],
            "brief": "P04：Dataset / DataLoader。",
        },
        "p05": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 训练循环 | 多 epoch：batch → forward → loss → backward → step |
| `state_dict` | 只存参数（与结构分离）；`torch.save` 落盘 |
| train mode | `model.train()` 影响 Dropout/BN 等 |""",
            "task": """短训几步并 `torch.save` 权重文件。""",
            "walls": ["墙：只 pickle 整个 model，路径迁徙后脆弱——优先 state_dict。"],
            "brief": "P05：训练循环并保存权重。",
        },
        "p06": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 推理 | `model.eval()` + `torch.no_grad()`：关 dropout、不建图 |
| `load_state_dict` | 先建同结构模型再加载 |
| 训练/推理分裂 | 避免误用 train 模式上线 |""",
            "task": """写推理脚本：load → eval → no_grad → 打印输出。""",
            "walls": ["墙：推理时仍在 train()，dropout 随机扰动结果。"],
            "brief": "P06：推理脚本。",
        },
        "p07": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 文本→特征 | 本课用极简特征，重点在闭环不是 SOTA |
| 分类头 | 线性层 + 交叉熵（或 BCE） |
| 玩具数据 | 能 memorise 只证明管道通，不证明泛化 |""",
            "task": """小文本（或假特征）分类，打印准确率或预测。""",
            "walls": ["墙：标签 dtype/形状与 loss 不匹配（Long vs Float）。"],
            "brief": "P07：小文本分类闭环。",
        },
        "p08": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 同步推理 | `model(x)` 对事件循环是阻塞的 |
| `to_thread` | 把推理丢线程池，async API 不被拖死 |
| 与 async-llm A10 | 同一模式：编排在协程，重活在线程/加速器 |""",
            "task": """假/真 sync_infer，用 gather + to_thread 并发两个请求并比耗时。""",
            "walls": ["墙：在 async 路由里直接 model(x)，高并发时事件循环卡死。"],
            "brief": "P08：asyncio.to_thread 桥接推理。",
        },
    },
    "llm-from-scratch": {
        "lfs01": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| PyTorch 角色 | 张量库 + autograd + nn；附录 A 为后续 LLM 章节打底座 |
| 环境探测 | 版本、CUDA/MPS、默认 dtype |

**说明**：讲义为原创提纲，不含书中原文。""",
            "task": """打印 torch 版本与 cuda/mps/default_dtype。""",
            "walls": ["墙：环境没装 torch 就跑后续课——先过本课。"],
            "brief": "LFS01：确认 PyTorch 环境。",
        },
        "lfs02": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 标量/向量/矩阵/张量 | 0D/1D/2D/ND；LLM 里常见 batch×seq×hidden |
| `torch.tensor` | 从 Python 数据创建；注意 dtype 推断 |""",
            "task": """创建 scalar、vector、matrix 并打印 shape。""",
            "walls": ["墙：把 Python list 当张量做广播，类型错误。"],
            "brief": "LFS02：标量到张量的维度直觉。",
        },
        "lfs03": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| dtype | float32 训练常用；int64 常作索引/类别 |
| 转换 | `.to(dtype=...)` / `.float()` / `.long()` |
| 混算 | 不同 dtype 可能自动提升或报错——要自觉 |""",
            "task": """创建张量并转换 dtype，打印前后类型。""",
            "walls": ["墙：索引张量用了 float，gather/embedding 报错。"],
            "brief": "LFS03：Tensor 数据类型。",
        },
        "lfs04": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 逐元素 vs 矩阵乘 | `*` 与 `@` / `matmul` 不同 |
| 广播 | 维度从后对齐，1 可扩；不懂广播=静默错 shape |
| 归约 | sum/mean；注意 `dim=` 与 `keepdim` |""",
            "task": """对 arange 张量做 reshape、运算、归约并打印。""",
            "walls": ["墙：该 matmul 时写成 *，得到逐元素积还以为对。"],
            "brief": "LFS04：常用张量运算。",
        },
        "lfs05": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 索引/切片 | 与 NumPy 类似；视图共享要小心 |
| 高级索引 | 整数列表/布尔 mask 行为不同 |
| 改值联动 | 改切片可能改原张量 |""",
            "task": """reshape 后切片、修改，观察原张量是否联动。""",
            "walls": ["墙：误以为切片总是深拷贝。"],
            "brief": "LFS05：张量索引与切片。",
        },
        "lfs06": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 计算图 | 前向搭图，backward 求梯度 |
| 与训练关系 | MLP/LLM 训练都建立在 autograd 上 |
| 对照 | 与 pytorch 轨 P02 同主题，节奏贴附录 A |""",
            "task": """可导张量上构造标量损失并 backward，打印 grad。""",
            "walls": ["墙：中间量需要 grad 却没 retain/钩子。"],
            "brief": "LFS06：自动求导。",
        },
        "lfs07": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `nn.Module` | 子模块与参数注册；`forward` 定义计算 |
| `nn.Sequential` | 线性堆叠快捷写法 |
| `parameters()` | 供优化器遍历；在 forward 里临时 new 层不会注册 |""",
            "task": """实现 TinyMLP，随机输入前向，打印参数形状。""",
            "walls": ["墙：在 forward 里 new 了 Linear，参数不进 parameters()。"],
            "brief": "LFS07：nn.Module 多层网。",
        },
        "lfs08": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| Dataset / DataLoader | 与 P04 同构：索引取样本 + 批迭代 |
| 为何重要 | LLM 训练本质是大规模批数据管道 |""",
            "task": """自定义 Dataset，DataLoader 迭代打印。""",
            "walls": ["墙：__getitem__ 返回结构与 collate 不一致。"],
            "brief": "LFS08：Dataset 与 DataLoader。",
        },
        "lfs09": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 典型循环 | epoch → batch → forward → loss → backward → step → zero_grad |
| 日志 | 每隔 n step 打 loss，确认在下降（玩具数据） |

**这是全书训练套路的缩影。**""",
            "task": """短训循环，打印 loss 变化。""",
            "walls": ["墙：学习率过大 loss 变 nan。"],
            "brief": "LFS09：典型训练循环。",
        },
        "lfs10": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| `state_dict` | 参数字典；跨设备迁移更稳 |
| save/load | `torch.save` / `load_state_dict` |
| 结构匹配 | 加载前模型结构必须一致 |""",
            "task": """保存再加载，确认输出或参数一致。""",
            "walls": ["墙：strict=True 时键名不匹配——先看 missing/unexpected keys。"],
            "brief": "LFS10：保存与加载模型。",
        },
        "lfs11": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 设备 | CPU 总可用；MPS/CUDA 需硬件+构建支持 |
| `.to(device)` | 模型与输入要在同一设备 |
| 统一入口 | `pick_device()`，避免散落 if |""",
            "task": """实现设备选择，张量 to(device) 并打印。""",
            "walls": ["墙：模型在 mps、输入在 cpu → 运行时错误。"],
            "brief": "LFS11：计算设备 CPU/MPS/CUDA。",
        },
        "lfs12": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| 单设备训练 | 数据与模型都 `.to(device)`，循环内保持一致 |
| 合成 | 把 LFS09 + LFS11 合成一次完整短训 |""",
            "task": """在选定设备上跑一个最小训练循环。""",
            "walls": ["墙：只有模型 to 了，batch 忘了 to。"],
            "brief": "LFS12：单设备训练串起来。",
        },
        "lfs13": {
            "concepts": """\
| 概念 | 必须讲清 |
|------|----------|
| DataParallel vs DDP | 老式 DP 简单但有瓶颈；DDP 是多机多卡主流 |
| 概念课 | 以讲解+探测/口述为主，不要求真多卡 |
| 何时需要 | 单卡放不下或要吞吐 |""",
            "task": """阅读参考实现中的概念提纲，跑通探测/总结输出。""",
            "walls": ["墙：没多卡却硬抄 DDP 模板，环境问题当成代码问题。"],
            "brief": "LFS13：多 GPU 概念概览（可口述）。",
        },
    },
}


def strip_to_raw_python(src: str) -> str:
    """Best-effort: turn hand-typed/annotated starter back into reference code."""
    if "自己动手敲" not in src and "【优先课注释】" not in src:
        return src if not src.lstrip().startswith("print(\"(请在上方") else src

    out: list[str] = []
    for line in src.splitlines():
        s = line.strip()
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
                "先读左侧",
                "先读讲义",
                "关键机制以",
                "写完练习后",
                "【优先课注释】",
                "课题：",
                "建议：",
                "不要复制",
                "少复制",
            )
        ):
            continue
        if s.startswith("# -----"):
            continue
        if re.match(r"^# --- .+ ---$", s):
            continue
        if s.startswith("# 撞墙") or s.startswith("#   墙"):
            continue
        if re.match(r"^# (A|P|LFS)\d+", s):
            continue

        m = re.match(r"^(\s*)# (.*)$", line)
        if m:
            leading, rest = m.group(1), m.group(2)
            # Original teaching comments stay comments
            if rest.startswith(("注", "注意", "Sequential", "Pretend", "DO NOT", "Simulate", "Two ")):
                out.append(f"{leading}# {rest}")
                continue
            if rest.startswith(("墙", "期望", "翻车", "修复")):
                continue
            out.append(f"{leading}{rest}")
            continue
        if s.startswith("#"):
            out.append(line)
            continue
        out.append(line)

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text


def comment_out_mit(src: str, brief: str, walls: list[str]) -> str:
    raw = strip_to_raw_python(src)
    preamble = [MIT_HEADER.rstrip(), "", f"# {brief}"]
    if walls:
        preamble.append("# 撞墙记录（预习，敲时对照）：")
        for w in walls:
            preamble.append(f"#   {w}")
    preamble.append("")

    out: list[str] = list(preamble)
    for line in raw.splitlines():
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
    out.append(MIT_FOOTER)
    return "\n".join(out).rstrip() + "\n"


def build_body(track: str, title: str, meta: dict) -> str:
    tm = TRACK_META[track]
    return f"""# {title}

来源：{tm['source']}。

## 关键概念（先读文档，再敲代码）

{meta['concepts'].strip()}

## 本题任务

{meta['task'].strip()}

## 动手要求

- 起始代码已用注释标出：**请自行输入**（或去掉 `#`），再删除占位 `print`。
- **关键机制以本题「关键概念」为准**；代码里的撞墙注释只是现场提醒。
- 少复制粘贴，多手敲；敲错再改。

## 自检

- [ ] 去掉注释后能运行
- [ ] 能用自己的话复述上表中的关键机制
- [ ] 知道本课在整体轨道里卡住的是哪一环
"""


def upgrade_track(track: str) -> int:
    folder = TRACKS / track
    meta_all = LESSONS[track]
    n = 0
    for path in sorted(folder.glob("*.json")):
        lesson_id = path.stem
        if lesson_id not in meta_all:
            print(f"SKIP no meta: {track}/{lesson_id}")
            continue
        meta = meta_all[lesson_id]
        data = json.loads(path.read_text(encoding="utf-8"))
        title = data.get("title") or f"{lesson_id}: ?"
        data["body"] = build_body(track, title, meta)
        data["checklist"] = [
            "读完关键概念与本题任务",
            "手敲参考实现并跑通",
            "能复述关键机制",
        ]
        starters = data.get("starterFiles") or {}
        for name, content in list(starters.items()):
            if not name.endswith(".py"):
                continue
            starters[name] = comment_out_mit(
                content, meta["brief"], list(meta.get("walls") or [])
            )
        data["starterFiles"] = starters
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        n += 1
    return n


def scrub_duplicate_body_tails(track: str) -> int:
    """Remove duplicate 动手要求/注释 blocks left by older annotate passes (e.g. mit-*)."""
    n = 0
    folder = TRACKS / track
    if not folder.is_dir():
        return 0
    for path in folder.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        body = data.get("body") or ""
        # Keep first 动手要求; drop trailing annotate junk after 自检 if duplicated
        if body.count("## 动手要求") <= 1 and "## 注释\n" not in body:
            continue
        # Cut from second ## 动手要求 or from ## 注释 if after 自检
        parts = re.split(r"\n## 注释\n", body, maxsplit=1)
        body2 = parts[0]
        # collapse duplicate 动手要求: keep through first 自检 section end
        if body2.count("## 动手要求") > 1:
            first = body2.find("## 动手要求")
            second = body2.find("## 动手要求", first + 1)
            # if second comes after 自检, truncate before second; else remove second block
            selfcheck = body2.find("## 自检")
            if second != -1:
                if selfcheck != -1 and selfcheck < second:
                    body2 = body2[:second].rstrip() + "\n"
                else:
                    # remove from second 动手要求 until next ## or end, but keep later 自检
                    rest = body2[second:]
                    m = re.search(r"\n## (?!动手要求)", rest)
                    if m:
                        body2 = body2[:second].rstrip() + "\n" + rest[m.start() :]
                    else:
                        body2 = body2[:second].rstrip() + "\n"
        if body2 != body:
            data["body"] = body2.rstrip() + "\n"
            path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            n += 1
    return n


def main() -> None:
    total = 0
    for track in ("async-llm", "pytorch", "llm-from-scratch"):
        c = upgrade_track(track)
        print(f"{track}: upgraded {c}")
        total += c
    for track in ("mit-python", "mit-llm", "async-llm", "pytorch", "llm-from-scratch"):
        s = scrub_duplicate_body_tails(track)
        if s:
            print(f"{track}: scrubbed duplicate body tails in {s}")
    print(f"total upgraded {total}")


if __name__ == "__main__":
    main()
