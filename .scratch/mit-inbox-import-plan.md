# Inbox → LPTHW 式练习轨道（执行计划）

> 状态：**已按默认一期执行并提交**（MIT-Python T1–T6 + MIT-LLM T1–T7）。

## Inbox 内容结论

两个文件夹结构同构，都是 MIT 三问闭环材料：

| 文件夹 | 定位 | 主题 | 代码题规模 |
|--------|------|------|------------|
| `inbox/MIT-Python-Migration` | iOS 老手复习 Python + LLM 数学/工程前置 | T1–T9 | 每主题约 4 道 Q |
| `inbox/MIT-LLM-Migration` | LLM 全栈从零（mock 可跑） | T1–T7 | 每主题 4 道 Q |

每主题四件套：教练出题 / 学员作答 / 批改 / 费曼 + `代码/Tn/Q*.py`。

学习站只消费：

- **题干与目标**：`T{n}-01-教练出题-*.md`
- **可跑参考实现**：`代码/T{n}/Q*.py` → 转成「全注释 + 占位 print」的 starter

**不进站点**：教练密卷、`.venv/`、批改/费曼/学员作答。

**重叠**：Python 线已写明 T7–T9 由 LLM 线整合接管。

- **MIT-Python 轨道**：一期落地 **T1–T6**（约 24 课）
- **MIT-LLM 轨道**：一期落地 **T1–T7**（约 28 课）
- Python T7–T9：二期可选归档，避免与 LLM T2/T3/T4 重复

## 网站组织

- 侧栏：**MIT-Python**（`mit-python`）、**MIT-LLM**（`mit-llm`），均 `priority: true`
- 课 ID：`py-t{n}-q{m}` / `llm-t{n}-q{m}`
- 每课：`body`（出题稿压缩）+ `starterFiles`（LPTHW 注释手敲）+ `timeoutSec` + `requires`

## LPTHW 手敲规则（强制）

1. 顶部：自己输入 / 去 `#` / 删占位 / ⌘+Enter  
2. 参考实现全部 `# ` 注释  
3. 不提供密卷弱/中/强提示  
4. 旧 workspace 需删目录重开课才更新 starter

## 技术步骤（下令后再做）

1. `.gitignore`：`inbox/**/.venv/`、`**/__pycache__/`
2. `scripts/gen_mit_tracks.py`：扫描 inbox → `content/tracks/mit-python|mit-llm/`
3. 注册 API tracks + README + `npm run generate:*`
4. 依赖：根目录 `uv sync --extra ml`；LLM 默认 mock 可跑
5. 抽样验收 + commit（不含 venv）

## 默认首批范围

**一期**：MIT-Python T1–T6 + MIT-LLM T1–T7  

可选改口令：

- 「两线全部代码题一次做完」（含 Python T7–T9）
- 「MVP：每线先只做 T1」

## 明确不做

- 密卷/批改/费曼进站点  
- 双 agent 阅卷流程  
- 提交 inbox `.venv`  
- **在你下令前不改代码、不生成课程**
