# NotebookLM 原始对话存档

存放与 NotebookLM 对话的**原始采集结果**，与学习指南（`guides/`）分离。

## 为什么单独存？

| 问题 | 对策 |
|------|------|
| Agent 上下文 compact 后丢失 NotebookLM 回答 | 原始内容落盘，可随时重读 |
| 手工 `notebooklm ask` 不可追踪 | 脚本按 manifest 分层执行，有 run 日志 |
| 整合指南与素材混在一起难维护 | `notebooklm-raw/` = 素材；`guides/` = 成品 |

## 目录结构

```
notebooklm-raw/
├── README.md
├── manifests/              # 采集计划（JSON）→ ✅ git
│   └── week3-4.json
└── week3-4/                # 按模块名
    ├── knowledge-graph.md      # Phase 1.5 认知图谱 → ✅ git
    ├── topics-map.md           # → ✅ git
    └── runs/
        └── 20260610-150251/    # canonical run（已完成的正式采集）
            ├── run.meta.json       # ✅ git
            ├── run.log             # ✅ git
            ├── manifest.snapshot.json  # ✅ git
            ├── L0-positioning.prompt.txt   # ✅ git
            ├── L0-positioning.answer.md    # ✅ git（整合主素材）
            └── L0-positioning.answer.json  # ❌ gitignore（体积大、与 .md 重复）
```

## Git 版本管理策略

| 纳入 git | 不纳入 git |
|----------|-----------|
| `manifests/*.json` | `**/*.answer.json`（含完整 citations，约为 .md 的 60 倍） |
| `knowledge-graph.md`、`topics-map.md` | 已合并的冗余/失败 run 目录 |
| `runs/<canonical>/*.prompt.txt` | 进行中的 scratch run（`runs/_*/`） |
| `runs/<canonical>/*.answer.md` | |
| `run.meta.json`、`manifest.snapshot.json`、`run.log` | |

**原则**：`.answer.md` 是 Agent 整合的唯一必要原始素材；`.answer.json` 仅在本地调试引用链路时需要，可随时 `--resume` 重采。

**Week 3-4 正式 run**：`week3-4/runs/20260610-150251/`（20/20 完成）。失败或已合并的临时 run 应直接删除，不写入 gitignore。

详见仓库根目录 `.gitignore`。

## 采集脚本

```bash
cd ~/development/ai

# 预览计划（不调用 API）
python scripts/nlm-collect.py notebooklm-raw/manifests/week3-4.json --dry-run

# 完整采集（默认失败继续、每 batch 最多重试 3 次、HTTP 超时 120s）
python scripts/nlm-collect.py notebooklm-raw/manifests/week3-4.json --delay 8

# 续跑 canonical run（以 .answer.md 判定已完成）
python scripts/nlm-collect.py notebooklm-raw/manifests/week3-4.json \
  --resume notebooklm-raw/week3-4/runs/20260610-150251

# 补采指定 batch（未写 --resume 时自动找最新未完成 run）
python scripts/nlm-collect.py notebooklm-raw/manifests/week3-4.json \
  --only w34-mistakes --resume notebooklm-raw/week3-4/runs/20260610-150251

# 合并补采目录到 canonical run
python scripts/nlm-collect.py merge-runs \
  notebooklm-raw/week3-4/runs/<补采run> \
  notebooklm-raw/week3-4/runs/20260610-150251

# 遇错即停（调试用）
python scripts/nlm-collect.py ... --fail-fast
```

**关键参数**：`--nlm-timeout 120`（notebooklm-py HTTP 读超时）、`--retries 3`、`--retry-base-delay 15`（指数退避）

**完成标志**：`runs/latest` → 最近 `completed` run 的符号链接

### 前置条件

- WSL 侧 NotebookLM 认证有效（`sync-auth.py`）
- Clash 代理运行在 `127.0.0.1:7897`
- openclaw skill venv：`~/service/openclaw/workspace/skills/notebooklm-integration/.venv`

## Manifest 格式

新建 `manifests/week3-4.json`：

```json
{
  "module": "week3-4",
  "notebook_id": "505bdb1c",
  "description": "…",
  "batches": [
    {
      "id": "L0-positioning",
      "layer": "L0",
      "title": "简短标题",
      "clear_conversation": true,
      "prompt": "完整 prompt 文本…"
    }
  ]
}
```

- `clear_conversation: true` → 该 batch 前执行 `notebooklm clear`，开新对话（**v3 默认每个 batch 均为 true**）
- `priority`：`critical` / `important` / `normal`，写入 prompt 控制回答深度
- **禁止**一个 batch 包含多个子主题（见 `manifests/week3-4.json` 范例）

### v3 采集流程（推荐）

```bash
# 1. 子主题发现（可选，与 topics-map.md 交叉校验）
python scripts/nlm-collect.py notebooklm-raw/manifests/week3-4-discovery.json

# 2. 完整单问采集（约 20 批 × 1–2 min）
python scripts/nlm-collect.py notebooklm-raw/manifests/week3-4.json --delay 5

# 3. 学习后补充（手动追加 manifest 或 --only supplement-xxx）
```

## Agent 整合流程（v4）

```
Phase 1    运行 nlm-collect.py → notebooklm-raw/<module>/runs/<ts>/
Phase 1.5  通读全部 *.answer.md → 产出 <module>/knowledge-graph.md（认知阶梯 + raw 映射）
Phase 2    按知识图谱从 raw 选取、补写全景/衔接 → guides/AI-Week*-学习指南.md
Phase 3–5  叙事、mermaid、用户迭代、定稿
```

详见 `guides/学习指南整合规范.md`、范例 `week3-4/knowledge-graph.md`。

## Week 1–2 说明

Week 1–2 指南已在 Agent 对话中手工采集完成；`manifests/week1-2.json` 保留当时 prompt，可用脚本**重新采集**以生成可归档的 raw run。历史手工采集未落盘，后续周次统一走脚本。
