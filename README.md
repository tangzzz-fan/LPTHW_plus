# LPTHW Learner（仅本地个人学习）

本机互动学习站：对照《Learn Python the Hard Way》打基础，并重点练习 **Async / LLM 企业落地** 与 **PyTorch**。代码用本机 Python（via `uv`）真实执行。

仓库内是原创学习提纲与练习，不含书的全文。

## 快速开始

本机需已安装 [`uv`](https://github.com/astral-sh/uv)（你已有即可）。

```bash
# 0) 下载依赖前先开代理（本机 zsh: proxy_on）
proxy_on

# 1) Python 环境 + API 依赖（uv 管理 .venv）
uv sync

# 2) 前端依赖 + 并发启动器
npm install
npm run install:web

# 3) （可选）PyTorch 轨道 — macOS / Apple Silicon / MPS
#    不要使用 download.pytorch.org/whl/cpu（Linux CPU 轮子）
uv sync --extra ml
# 或: npm run install:ml

proxy_off   # 可选：装完关掉代理

# 4) 生成/刷新课程内容（首次已生成可跳过）
npm run generate:content

# 5) 同时启动 API :8000 与 Web :5173
npm run dev
```

浏览器打开 http://127.0.0.1:5173 。

## macOS + PyTorch（uv）

```bash
proxy_on
uv sync --extra ml
uv run python -c "import torch; print(torch.__version__, 'mps=', torch.backends.mps.is_available())"
```

- 安装源：默认 PyPI（`macosx_*_arm64`）
- **不要**加 `--index-url https://download.pytorch.org/whl/cpu`
- 有 MPS 时可用 `torch.device("mps")`；小练习默认 CPU 也可

## 轨道

| 轨道 | 说明 |
|------|------|
| `lpthw` | Ex 0–52 骨架；前几课可完整练习，其余为提纲占位 |
| `async-llm` | 重点：asyncio、httpx、流式、限流、Queue、结构化重试、迷你 RAG |
| `pytorch` | 重点：Tensor → 训练/推理 → `asyncio.to_thread` 桥接 |

学习产生的文件在 `learner_workspace/`（已 gitignore）。

## API 摘要

- `GET /api/health`
- `GET /api/tracks` / `GET /api/tracks/{track}/exercises`
- `GET /api/exercises/{track}/{id}`
- `GET|PUT|DELETE /api/files/...`
- `POST /api/run` · `POST /api/run/stdin`

## 票据

实现拆票见 [.scratch/lpthw-learner/issues/](.scratch/lpthw-learner/issues/)。
