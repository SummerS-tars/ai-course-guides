# 课件 01 — Introduction 学习指南

> **课件**：`01Introduction.pdf`｜NotebookLM `课件01-Introduction`  
> **原则**：按课件原序、按知识点分块、**课件板块无遗漏**  
> **课堂**：Week 1 概述；Part A 延伸至 Week 14；Part B 深入 Week 15  
> **术语**：**中文（English）**

---

## 课件内容覆盖索引

| 课件原序 | 课件板块 | Slide | 本指南 |
|----------|----------|-------|--------|
| 1 | 三段论与逻辑基础 | ~1 | Part A · 块 A.1–A.2 |
| 2 | 产生式系统与专家系统架构 | ~2 | Part B · 块 B.1–B.3 |
| 3 | 致谢与联系方式 | ~3 | Part C · 块 C.1 |
| — | *课件未写但课纲/期末相关* | — | 附录 · 块 X.1–X.3 |

---

## Part A — 逻辑与 AI 哲学根源（Slide ~1）

### 块 A.1 三段论（Syllogism）与符号主义

**课件要点**：苏格拉底三段论；形式化从公理导出结论。

- **本块要解决的问题**：AI 如何把「人会推理」改写成机器能执行的符号步骤。
- **经典例**：所有人都会死；苏格拉底是人；故苏格拉底会死。
- **三段论（Syllogism）**：由大前提、小前提推出结论；它展示「只要规则形式正确，结论可机械推出」。
- **符号主义（Symbolism）关联**：推理 = 对符号做合法改写，**不必理解语义**（霍布斯：Reasoning is but reckoning，推理就是计算）。
- **肯定前件（Modus Ponens）**：最常用的规则模板，形式为 $P \to Q,\; P \vdash Q$，意思是「若 P 则 Q，且 P 已成立，所以 Q 成立」。

**一步推理链**：

1. 规则：$man(x) \to mortal(x)$（人都会死）
2. 事实：$man(Socrates)$（苏格拉底是人）
3. 代入：令 $x = Socrates$
4. 结论：$mortal(Socrates)$

> **直观理解**：像按菜谱做菜——不懂烹饪也能按步骤得到结论。

（来源：课件01 Slide 1、Week 1）

### 块 A.2 一阶谓词演算（First-order predicate calculus）

**课件要点**：罗素/怀特海德逻辑发展；$\forall x (man(x) \to mortal(x))$ 等。

- **为何重要**：命题逻辑只能说整句真假，不能表达「所有人」「存在某人」这类泛化知识；**一阶谓词演算（First-order Logic, FOL）**用 $\forall/\exists$ 描述个体、类别和关系。
- **全称量词（Universal quantifier, $\forall$）**：表示「对所有对象都成立」；**存在量词（Existential quantifier, $\exists$）**：表示「至少有一个对象成立」。
- **与机器推理**：通过**合一（Unification）**把变量 $x$ 绑到常量（如 Socrates），从一般规律得到具体结论；合一就是「找一个代换，让两个逻辑式能对上」。
- **后续衔接**：课件 07 消解、Prolog 均建立在 FOL 之上。

> **重难点**：课件图多字少——复习时能手写 $\forall x (dog(x) \to animal(x))$ 并做一步代换。

（来源：课件01、Week 14）

---

## Part B — 产生式系统与专家系统（Slide ~2）⭐

### 块 B.1 产生式规则 IF-THEN

**课件要点**：把专家经验写成「条件满足就执行动作」的规则。

| 部分 | 英文 | 含义 |
|------|------|------|
| 前件 | LHS / Antecedent | IF：模式，与事实匹配 |
| 后件 | RHS / Consequent | THEN：动作（增删事实、输出） |

- **产生式规则（Production rule）**：专家系统中最小的知识单位；一条规则通常形如「IF 症状匹配 THEN 给出诊断/新增事实」。
- **模式匹配（Pattern matching）**：不是简单字符串相等，而是检查工作内存中的事实是否满足 LHS 的结构和约束。
- **考试定位**：PPT01 只需会解释 LHS/RHS；可执行语法和复杂匹配放到 PPT03 CLIPS。

（来源：课件01、Week 15）

### 块 B.2 专家系统架构（课件图文字版）

```text
用户 ↔ 用户界面
         ↓
  ┌─ 解释接口 / 知识获取接口 ─┐
  │      推理引擎             │
  │  Match → Agenda → Act     │
  └──────┬──────────┬────────┘
    知识库(Rules)  工作内存(Facts)
```

| 模块 | 职责 |
|------|------|
| 推理引擎 Inference Engine | 识别-动作循环；匹配、冲突消解、执行 |
| 知识库 Knowledge Base | 存 IF-THEN 规则 |
| 工作内存 Working Memory | 当前事实与中间结果 |
| 知识获取 Knowledge Acquisition | 专家录入/维护规则 |
| 解释 Explanation | 回答 How/Why，可解释性 |

**识别-动作循环（Recognize-Act cycle）**：

1. **Match**：推理引擎拿工作内存事实匹配规则 LHS。
2. **Agenda**：所有满足条件的规则实例进入议程，等待执行。
3. **Act**：选中一条规则，执行 RHS，工作内存被更新。
4. **循环**：新事实可能触发更多规则，直到 Agenda 为空。

> **课件补充**：Agenda 和 Salience 是控制结构的核心，详见课件 03。

（来源：课件01 Slide 2、Week 15）

### 块 B.3 与课件 03 CLIPS 的衔接

| 架构概念 | CLIPS 实现 |
|----------|------------|
| 工作内存 | Fact list |
| 知识库 | `defrule` 规则 |
| 推理引擎 | 内置 Rete + Agenda |
| LHS/RHS | `(pattern) => (action)` |

> **衔接提醒**：PPT01 考「架构是什么」；PPT03 考「给一段 CLIPS 代码，事实如何进入 Agenda、规则如何 fire」。

（来源：课件01、课件03、Week 15）

---

## Part C — 致谢（Slide ~3）

### 块 C.1 人物与课程信息

**课件要点**：Edward Feigenbaum（专家系统奠基）；复旦大学郑骁庆老师联系方式。

- **Feigenbaum**：MYCIN、专家系统运动核心人物；理解符号主义应用史即可。
- **考试**：一般不单独出题；作背景了解。

（来源：课件01 Slide 3）

---

## 附录 X — 课件 01 未展开、课纲/期末相关（Week 1 补充）

> 以下**不在课件 01 PDF 正文中**，但课纲与期末可能涉及；开卷时勿只翻本课件。

### 块 X.1 AI 定义与达特茅斯会议（1956）

- **达特茅斯会议**：AI 学科诞生标志；核心猜想——智能特征可被精确描述并由机器模拟。
- **AI 定义**：研究智能行为的自动化；含数据结构、算法、语言（McCarthy、Minsky、Shannon 等）。

### 块 X.2 三大流派一句话

| 流派 | 核心 |
|------|------|
| 符号主义 Symbolism | 知识→规则→字符串推理 |
| 连接主义 Connectionism | 神经网络调权重（课件 08） |
| 进化主义 Evolutionism | 选择/交叉/变异（课件 10） |

### 块 X.3 图灵测试及局限

- **定义**：双盲对话，无法区分人/机则通过。
- **局限**：鼓励欺骗、不评具身智能、忽视机器计算优势、模仿≠理解机制。

（来源：Week 1 记录；标注「课件01 未详述」）

---

## 术语表

| English | 中文 |
|---------|------|
| Syllogism | 三段论 |
| Production rule | 产生式规则 |
| Inference Engine | 推理引擎 |
| Working Memory | 工作内存 |
| LHS / RHS | 前件 / 后件 |

---

## 复习优先级

| 优先级 | 内容 |
|--------|------|
| 高 | Part B 专家系统架构 → 对照课件 03 |
| 中 | Part A 逻辑与 FOL 铺垫 → 对照课件 07 |
| 了解 | Part C；附录 X（课纲 breadth） |

---

**raw**：`notebooklm-raw/ppt01/runs/latest/`｜**结构**：`notebooklm-raw/ppt/runs/20260619-161000/ppt01-structure.answer.md`
