# 人工智能（H）— 课件 PPT 按序梳理索引

> **课程**：CS30057h.01 人工智能（H）  
> **依据**：期末开卷，**考试内容全在 PPT 中**（Week 15 课堂说明）  
> **梳理原则**：按课件原始顺序 → 课件内按知识点分 Part → 补充课件/课堂缺失讲解  
> **与周次指南关系**：`AI-Week*-学习指南.md` 以 FiCS 课堂记录为主线；本系列以 **10 份课件 PDF** 为主线，二者交叉对照  
> **生成日期**：2026-06-19  
> **NotebookLM**：`505bdb1c-0034-4e14-89df-0b14bf3fc723`

---

## 一、为何单独做 PPT 梳理

| 维度 | 周次学习指南 | 课件 PPT 梳理（本系列） |
|------|-------------|------------------------|
| 主线 | FiCS 课堂实际讲了什么 | 课件里有什么、按 slide 顺序 |
| 顺序 | 按上课周次 | 按课件 01→10 原始顺序 |
| 适用场景 | 跟课复习、Project 衔接 | **期末开卷**、核对「PPT 有没有但老师没讲」 |
| 已知偏差 | 课纲 vs 实际授课（见课纲 §1.8） | 课件 04/06/10 等可能未单独授课 |

---

## 二、流水线（NotebookLM）

```
Phase 0  discovery  →  notebooklm-raw/manifests/ppt-discovery.json（10 份结构图）
Phase 1  按 Part 深采 →  notebooklm-raw/manifests/ppt{NN}-deep.json
Phase 1.5 通读 raw →  notebooklm-raw/ppt{NN}/structure-map.md
Phase 2  整合正文 →  guides/AI-PPT{NN}-课件梳理.md
```

**采集命令**（仓库根目录）：

```bash
NLM=.cursor/skills/ai-course-notebooklm/scripts/nlm-collect.py

# L0：10 份课件内部结构（先跑这个）
python $NLM notebooklm-raw/manifests/ppt-discovery.json --delay 8

# L1+：单课件深入（结构图产出后按 Part 生成 manifest）
python $NLM notebooklm-raw/manifests/ppt01-deep.json --delay 8
```

**raw 落盘**：`notebooklm-raw/ppt/runs/<timestamp>/`

---

## 三、10 份课件一览

| 编号 | 本地 PDF | NotebookLM Source | 课堂覆盖 | 梳理文档 | L0 结构 | L1+ 深采 |
|------|----------|-------------------|----------|----------|---------|----------|
| 01 | `01Introduction.pdf` | `课件01-Introduction` | ✅ Week 1 概述；W14/W15 延伸 | `AI-PPT01-学习指南.md` | ✅ | ✅ |
| 02 | `02Knowledge representation.pdf` | `课件02-Knowledge-representation` | ⚠️ Week 12 概念；演算少 | `AI-PPT02-学习指南.md` | ✅ | ✅ |
| 03 | `03CLIPS.pdf` | `课件03-CLIPS` | ✅ Week 15 深入 | `AI-PPT03-学习指南.md` | ✅ | ✅ |
| 04 | `04Decision tree.pdf` | `课件04-Decision-tree` | ⚠️ **FiCS 未授课** | `AI-PPT04-学习指南.md` | ✅ | ✅ |
| 05 | `05Uncertainty.pdf` | `课件05-Uncertainty` | ✅ Week 13（CF 必考） | `AI-PPT05-学习指南.md` | ✅ | ✅ |
| 06 | `06Rough set.pdf` | `课件06-Rough-set` | ⚠️ **FiCS 未授课** | `AI-PPT06-学习指南.md` | ✅ | ✅ |
| 07 | `07Logics and Prolog.pdf` | `课件07-Logics-and-Prolog` | ✅ Week 14 深入 | `AI-PPT07-学习指南.md` | ✅ | ✅ |
| 08 | `08Connectionist.pdf` | `课件08-Connectionist` | ✅ W1–4 深入；WTA 未核心讲 | `AI-PPT08-学习指南.md` | ✅ | ✅ |
| 09 | `09Deep learning.pdf` | `课件09-Deep-Learning` | ✅ W4–12；**无 Transformer 详页** | `AI-PPT09-学习指南.md` | ✅ | ✅ |
| 10 | `10Genetic algorithm.pdf` | `课件10-Genetic-algorithm` | ⚠️ Week 1 概述 | `AI-PPT10-学习指南.md` | ✅ | ✅ |

> L0 结构图产出后，本表「课堂覆盖」列将以 discovery raw 审计结果为准更新。

---

## 四、单份课件学习指南结构（模板）

每份 `guides/AI-PPT{NN}-学习指南.md` 包含：

1. **元信息**：课件 PDF、NotebookLM source、课堂覆盖  
2. **课件内容覆盖索引**（★无遗漏）：structure discovery 中**每个课件板块**一行，映射到 `Part · 块`  
3. **Part 正文**（严格按课件原序，不按上课周）  
   - Part 内按**知识点维度分块**（块 X.Y），**不按页**  
   - 每块：**课件要点**（列举 PPT 所含信息）→ **讲解** → 重难点加 **直观理解 / 手算例**  
4. **术语表**、**复习优先级**、**raw 路径**  

标杆：`guides/AI-PPT01-学习指南.md`

---

## 五、与现有 Part 流水线对照

| 原 Part | 周次 | 主要课件 | PPT 梳理优先顺序 |
|---------|------|----------|------------------|
| P8/P9 | W13–15 | 05, 02, 07, 03 | **PPT03, 05, 07**（期末符号主义） |
| P2/P4 | W3–7 | 08, 09 | PPT08, PPT09（前半） |
| P1 | W1–2 | 01, 08 | PPT01, PPT08（前半） |

**建议深采顺序**：03 → 05 → 07 → 01 → 08 → 09 → 02 → 04/06/10

---

## 六、进度日志

| 日期 | 事项 |
|------|------|
| 2026-06-19 | 深采：10 份课件 Part 讲解 raw 完成（`ppt01`–`ppt10/runs/`） |
| 2026-06-19 | 指南：`guides/AI-PPT01`–`AI-PPT10-学习指南.md`（覆盖索引 + Part + 知识块） |

---

*配合 `guides/AI课程-14周内容梳理.md` 与 `notebooklm-raw/semester-parts.md` 使用。*
