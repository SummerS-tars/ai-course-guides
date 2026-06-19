# 采集与整合排错

> **认证权威 SOP**：`~/service/openclaw/workspace/skills/notebooklm-integration/docs/auth-sop.md`

## RPC GET_NOTEBOOK / null result（短 Notebook ID）

**现象**：`RPC rLM1Ne returned null result data`，`GET_NOTEBOOK failed`；CLI `notebooklm ask` 正常但 `nlm-collect.py` 失败。

**原因**：manifest 里用了短前缀（如 `505bdb1c`）；`notebooklm-py` 的 `chat.ask()` 需要**完整 UUID**。

**处理**：
1. `notebooklm list` 查完整 ID
2. 更新 manifest 中的 `notebookId` 为完整 UUID
3. 当前 AI Notebook：`505bdb1c-0034-4e14-89df-0b14bf3fc723`

## 认证失败

**现象**：`Authentication expired or invalid`，或 sync-auth 失败。

**处理（唯一正确流程）**：
1. **用户**在 Windows 运行桌面 `notebooklm-login.ps1`，或 `fix_login_edge.py`（见 auth-sop.md）
2. WSL：
   ```bash
   python3 ~/service/openclaw/workspace/skills/notebooklm-integration/scripts/sync-auth.py --force
   python3 ~/service/openclaw/workspace/skills/notebooklm-integration/scripts/sync-auth.py --check
   ```

**Agent 禁止**：`notebooklm login`、WSL 浏览器登录、从 WSL 触发 Windows Edge、`sync-auth --refresh`（已废弃）。

CLI 报 `Run 'notebooklm login'` 时忽略，改走 Windows + sync-auth。

## 超时（~32s）

**现象**：`Chat request timed out`，elapsed ≈ 30–35s。

**原因**：notebooklm-py 默认 HTTP 读超时 30s；成功回答常需 40–50s。

**处理**：
- 脚本已默认 `--nlm-timeout 120`、`--retries 3`
- 加大间隔：`--delay 8`
- 续跑：`--resume notebooklm-raw/<module>/runs/latest`

## 部分 batch 失败

- 默认继续跑完其余 batch（不加 `--fail-fast`）
- 查看 `run.log` 与 `run.meta.json` 的 `error_kind`
- 补采：`--only <batch> --resume runs/latest`
- 或 `merge-runs <补采run> runs/latest`

## 代理

WSL 访问 Google 必须 `http://127.0.0.1:7897`；`nlm-collect.py` / `sync-auth.py` 已默认设置。

## 整合质量

| 症状 | 对策 |
|------|------|
| 公式堆砌、无全景 | 补 Phase 1.5 知识图谱 + 全景节 |
| 语言生硬 | 按 `integration-guide.md` 加类比、追问块 |
| NotebookLM 与课纲不符 | 以 FiCS 课程记录为准，指南中标注 |
