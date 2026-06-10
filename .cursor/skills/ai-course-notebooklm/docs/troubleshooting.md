# 采集与整合排错

## 认证失败

**现象**：`Authentication expired or invalid`，3–5s 内失败。

**处理**：
1. Windows 侧运行 `fix_login_edge.py` 刷新浏览器登录
2. WSL：`python3 ~/service/openclaw/workspace/skills/notebooklm-integration/scripts/sync-auth.py`
3. 验证：`notebooklm auth check --test`（需代理）

## 超时（~32s）

**现象**：`Chat request timed out`，elapsed ≈ 30–35s。

**原因**：notebooklm-py 默认 HTTP 读超时 30s；成功回答常需 40–50s。

**处理**：
- 脚本已默认 `--nlm-timeout 120`、`--retries 3`
- 加大间隔：`--delay 8`
- 续跑：`--resume notebooklm-raw/<module>/runs/latest`

**不是**：API 时段限额（限额会有 rate limit / 429 文案）。

## 部分 batch 失败

**处理**：
- 默认继续跑完其余 batch（不加 `--fail-fast`）
- 查看 `run.log` 与 `run.meta.json` 的 `error_kind`
- 补采：`--only <batch> --resume runs/latest`
- 或 `merge-runs <补采run> runs/latest`

## 代理

WSL 访问 Google 必须：

```bash
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
```

脚本默认已设置；手工调试时需自行 export。

## 整合质量

| 症状 | 对策 |
|------|------|
| 公式堆砌、无全景 | 补 Phase 1.5 知识图谱 + 全景节 |
| 语言生硬 | 按 `integration-guide.md` 加类比、追问块 |
| NotebookLM 与课纲不符 | 以 FiCS 课程记录为准，指南中标注 |
