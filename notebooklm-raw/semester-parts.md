# 本学期 Part 总览（Phase 0 盘点）

> **课程**：CS30057h.01 人工智能（H）｜2025-2026 第 2 学期  
> **依据**：`guides/AI课程-14周内容梳理.md` §三 知识脉络 + §二 按周梳理  
> **Notebook**：`505bdb1c-0034-4e14-89df-0b14bf3fc723`  
> **盘点日期**：2026-06-16（Phase 1 raw 采集完成）

---

## Part 分层（与课纲梳理对齐）

按实际授课主线划分 **9 个采集/整合 Part**；Week 9（五一）、Week 11（校运会）为停课周，不单独建 Part。

| Part | module 目录 | 覆盖周次 | 主题 | 主要课件 | 指南目标 |
|------|-------------|----------|------|----------|----------|
| **P1** | `week1-2` | W1–W2 | AI 概述 + 感知机/MLP 基础 | 01, 08 | `guides/AI-Week1-2-学习指南.md` ✅ 定稿 |
| **P2** | `week3-4` | W3–W4 | 反向传播 + CNN 概览 + PJ1 | 08, 09 | `guides/AI-Week3-4-学习指南.md` ✅ v2.3 待 Review |
| **P3** | `week5-6` | W5–W6 | 序列建模 HMM/CRF → 词嵌入/早期 DL | 09, 05 | `guides/AI-Week5-6-学习指南.md` ✅ 初版 |
| **P4** | `week7` | W7 | 卷积数学原理、互相关、池化、LeNet | 08, 09 | 并入 P2 指南 §2.3 |
| **P5** | `week8` | W8 | 深度生成模型 VAE/扩散/GAN | 09 | `guides/AI-Week8-学习指南.md` ✅ 初版 |
| **P6** | `week10` | W10 | 神经网络优化技术 | 09 | `guides/AI-Week10-学习指南.md` ✅ 初版 |
| **P7** | `week12` | W12 | Transformer 与大语言模型 | 09 | `guides/AI-Week12-学习指南.md` ✅ 初版 |
| **P8** | `week13-14` | W13–W14 | 不确定性推理 + 逻辑/消解/Prolog | 05, 02, 07 | `guides/AI-Week13-14-学习指南.md` ✅ 初版 |
| **P9** | `week15` | W15 | 前向推理与 CLIPS 产生式系统 | 03 | `guides/AI-Week15-学习指南.md` ✅ 初版 |

### 叙事链（Part 间承接）

```
P1 三大流派/MLP → P2 BP+CNN+PJ1 → P3 序列 HMM/CRF
  → P4 CNN 数学深化（并入 P2 指南）
  → P5 生成模型 → [W9 停课] → P6 优化 → [W11 停课]
  → P7 Transformer → P8 贝叶斯/逻辑/消解 → P9 CLIPS 前向推理
```

---

## 本地资料对齐（`1_人工智能H/`）

| 类别 | 本地状态 | NotebookLM 期望 |
|------|----------|-----------------|
| 课件 01–10 | ✅ 10/10 PDF | `课件01-Introduction` … `课件10-Genetic-algorithm` |
| 课程记录 W1–W8, W10, W12–W15 | ✅ 13 份 md（W1/2/7 另有 pdf） | `笔记-week0N-周五-AI` |
| 课纲 | ✅ pdf + doc | `课纲-人工智能H` |
| 教材 ×3 | ✅ pdf（花书另有 epub） | `参考书-*` |
| PJ1 / PJ2 文档 | ✅ | `Project1-*`、`PJ2-作业说明` |

---

## 流水线进度矩阵

| Part | manifest | topics-map | raw 采集 | knowledge-graph | 学习指南 |
|------|----------|------------|----------|-----------------|----------|
| P1 week1-2 | ✅ 4 | ✅ | ✅ 4/4 | — | ✅ 定稿 |
| P2 week3-4 | ✅ 20 | ✅ | ✅ 20/20 | ✅ | ✅ v2.3 待 Review |
| P3 week5-6 | ✅ 22 | ✅ | ✅ 22/22 | ✅ | ✅ 初版 |
| P4 week7 | ✅ 13 | ✅ | ✅ 13/13 | ✅ | 并入 P2 §2.3 |
| P5 week8 | ✅ 13 | ✅ | ✅ 13/13 | ✅ | ✅ 初版 |
| P6 week10 | ✅ 16 | ✅ | ✅ 16/16 | ✅ | ✅ 初版 |
| P7 week12 | ✅ 14 | ✅ | ✅ 14/14 | ✅ | ✅ 初版 |
| P8 week13-14 | ✅ 19 | ✅ | ✅ 19/19 | ✅ | ✅ 初版 |
| P9 week15 | ✅ 8 | ✅ | ✅ 8/8 | ✅ | ✅ 初版 |

**Phase 2 初版指南**：P3–P9 完成（2026-06-16）；129 batch raw ✅

---

## NotebookLM Source 对齐（待刷新认证后拉取）

认证过期时无法执行 `notebooklm source list`。以下为各 Part manifest 中 `sources_hint` 汇总，认证恢复后需与 NotebookLM 实际 source 标题逐项核对。

| Part | 期望 Source |
|------|-------------|
| P1 | 笔记-week01/02-周五-AI，课件01/08 |
| P2 | 笔记-week03/04，课件08/09，Project1 任务书/指导 |
| P3 | 笔记-week05/06，课件09/05，PJ2 说明 |
| P4 | 笔记-week07，课件08/09 |
| P5 | 笔记-week08，课件09 |
| P6 | 笔记-week10，课件09 |
| P7 | 笔记-week12，课件09 |
| P8 | 笔记-week13/14，课件05/02/07 |
| P9 | 笔记-week15，课件03 |

**下一步（认证恢复后）**：

```bash
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
python3 ~/service/openclaw/workspace/skills/notebooklm-integration/scripts/sync-auth.py
notebooklm source list   # 核对上表

# 对新 Part 先跑 L0 discovery，再跑完整 manifest
python3 .cursor/skills/ai-course-notebooklm/scripts/nlm-collect.py \
  notebooklm-raw/manifests/<module>-discovery.json --delay 8
```

---

## 建议采集顺序

~~Phase 1 raw 已于 2026-06-16 全部完成。~~

**下一步（Phase 4）**：用户 Review 迭代；期末优先 Review P8/P9

---

*Phase 0 产出；各 Part 子主题详见 `notebooklm-raw/<module>/topics-map.md`。*
