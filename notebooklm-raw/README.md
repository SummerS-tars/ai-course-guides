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
├── manifests/              # 采集计划（JSON）
│   └── week1-2.json
└── week1-2/                # 按模块名
    └── runs/
        └── 20260609-120000/    # 每次运行一个时间戳目录
            ├── run.meta.json       # 运行元数据、批次状态
            ├── run.log             # 文本日志
            ├── manifest.snapshot.json
            ├── L0-positioning.prompt.txt
            ├── L0-positioning.answer.md
            ├── L0-positioning.answer.json
            └── ...
```

## 采集脚本

```bash
cd ~/development/ai

# 预览计划（不调用 API）
python scripts/nlm-collect.py notebooklm-raw/manifests/week1-2.json --dry-run

# 完整采集
python scripts/nlm-collect.py notebooklm-raw/manifests/week1-2.json

# 只跑某一批
python scripts/nlm-collect.py notebooklm-raw/manifests/week1-2.json --only L0-positioning

# 失败后续跑（跳过已有 .answer.json）
python scripts/nlm-collect.py notebooklm-raw/manifests/week1-2.json \
  --resume notebooklm-raw/week1-2/runs/20260609-120000

# 批次间多等几秒（默认 3s）
python scripts/nlm-collect.py notebooklm-raw/manifests/week1-2.json --delay 5
```

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

## Agent 整合流程（更新）

```
Phase 1  运行 nlm-collect.py → notebooklm-raw/<module>/runs/<ts>/
Phase 2  Agent 只读 *.answer.md / *.json 写 guides/ 初稿（不必再 inline 调 NotebookLM）
Phase 3–5  叙事串联、用户迭代、定稿（见 .cursor/rules/ai-notebooklm-learning.mdc）
```

## Week 1–2 说明

Week 1–2 指南已在 Agent 对话中手工采集完成；`manifests/week1-2.json` 保留当时 prompt，可用脚本**重新采集**以生成可归档的 raw run。历史手工采集未落盘，后续周次统一走脚本。
