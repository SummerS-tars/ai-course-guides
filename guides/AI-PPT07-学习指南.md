# 课件 07 — Logics and Prolog 学习指南

> **课件**：`07Logics and Prolog.pdf`｜`课件07-Logics-and-Prolog`  
> **原则**：按课件原序、按知识点分块、**课件板块无遗漏**  
> **课堂**：**Week 14 深入**  
> **期末大题**：自然语言 → 逻辑式 → **子句集** → 消解证明  
> **术语警示**：课堂称「DNF」，课件产出 **Clause Form / CNF**——以老师定义为准

---

## 课件内容覆盖索引

| 课件原序 | 课件板块 | Slide | 本指南 |
|----------|----------|-------|--------|
| 1 | KR 与逻辑基础 Foundation | 1 | Part 1 · 块 1.1 |
| 2 | 命题逻辑 Propositional Logic | 1–2 | Part 1 · 块 1.2 |
| 3 | 一阶逻辑 FOL | 2–4 | Part 1 · 块 1.3–1.4 |
| 4 | 消解反驳 Resolution | 5–14 | Part 2 · 块 2.1–2.5 |
| 5 | 逻辑系统分类 Categories | 15 | Part 2 · 块 2.6 |
| 6 | 霍恩子句 Horn Clauses | 16 | Part 3 · 块 3.1 |
| 7 | Prolog 解释器与语法 | 16–23 | Part 3 · 块 3.2–3.5 |

---

## Part 1 — 逻辑学基础（Slide 1–4）

### 块 1.1 逻辑作为知识表示基础

**课件要点**：逻辑是 KR 的形式化基础；符号改写即可推理。

- 符号主义：机器**不必理解语义**，合法符号操作即推理。

### 块 1.2 命题逻辑（Propositional Logic）

**课件要点**：连接词；真值表；句子构成。

| 连接词 | 符号 |
|--------|------|
| 非/与/或/蕴含/等价 | $\neg, \land, \lor, \to, \leftrightarrow$ |

- **善意推定**：自然语言转逻辑取最弱、最保守读法。

### 块 1.3 一阶谓词逻辑（FOL）

**课件要点**：项 Term、谓词 Predicate、原子公式、量词 $\forall/\exists$、一致性/有效性。

| 成分 | 例 |
|------|-----|
| 常量 | `fido`, `socrates` |
| 变量 | `x`, `y` |
| 谓词 | `dog(x)`, `parent(x,y)` |

### 块 1.4 量词搭配 ⭐

| 量词 | 常搭配 | 误配后果 |
|------|--------|----------|
| $\forall$ | $\rightarrow$ | 用 $\land$ →「万物皆人且皆死」 |
| $\exists$ | $\land$ | 用 $\rightarrow$ → 前提假则式子恒真，过弱 |

> **直观理解**：「所有鸟会飞」= $\forall x (bird(x) \to flies(x))$，不是 $\forall x (bird(x) \land flies(x))$。

（来源：课件07 Slide 1–4、Week 14）

---

## Part 2 — 消解反驳（Slide 5–16）⭐期末

### 块 2.1 消解思想（Resolution Refutation）

**课件要点**：子句集；互补文字；空子句 □。

1. KB + **¬结论** → 子句集  
2. 合一后消解互补文字  
3. 得 □ → 不可满足 → 结论为真  

### 块 2.2 子句集转换九步

| 步 | 名称 | 要点 |
|----|------|------|
| 1 | 消去蕴含 | $P\to Q \equiv \neg P \lor Q$ |
| 2 | 否定内移 | 德摩根 |
| 3 | 变量标准化 | 重命名 |
| 4 | 前束化 | 量词左移 |
| 5 | Skolem 化 | $\exists$ → Skolem 函/常 |
| 6 | 略去 $\forall$ | |
| 7 | CNF | 分配律 |
| 8 | 拆分子句 | |
| 9 | 子句变量再标准化 | |

（来源：课件07 Slide 9–16）

### 块 2.3 自然语言 → 逻辑式 ⭐

**例题**：「外祖父是母亲的父亲」

$$\forall x \forall z \big( mgf(z,x) \leftrightarrow \exists y\,(mother(y,x) \land father(z,y)) \big)$$

### 块 2.4 Fido 消解手算 ⭐

前提：$\forall x(dog(x)\to animal(x))$，$\forall y(animal(y)\to die(y))$，$dog(fido)$。证 $die(fido)$。

子句：C1 $\neg dog(x)\lor animal(x)$；C2 $\neg animal(y)\lor die(y)$；C3 $dog(fido)$；C4 $\neg die(fido)$。

C2+C4→C5 $\neg animal(fido)$；C1+C5→C6 $\neg dog(fido)$；C3+C6→**□**

### 块 2.5 消解树与策略

**课件要点**：消解树图；线性/宽度优先等策略。

- **完备**：宽度优先等可保证找到反驳（若存在）。  
- **高效**：线性消解可能不完备但常用。

### 块 2.6 逻辑系统分类（Slide 15）

**课件要点**：可判定性、表达力分类。

- FOL：**半可判定**——证伪可能终止，证真可能不终止（无限论域）。

（来源：课件07 Slide 15、Week 14）

---

## Part 3 — Prolog（Slide 16–23）

### 块 3.1 霍恩子句（Horn Clauses）

**课件要点**：至多一个正文字。

| 形式 | Prolog |
|------|--------|
| 事实 $a\leftarrow$ | `parent(tom,bob).` |
| 规则 | `friends(X,Y):- likes(X,Z), likes(Y,Z).` |
| 目标 | `?- parent(tom,X).` |

### 块 3.2 合一（Unification）

模式匹配 + 变量绑定，使查询与规则头一致。

### 块 3.3 深度优先与回溯

先化简最左子目标；失败则回溯试下一分支。

### 块 3.4 剪枝 `!`

承诺当前路径，放弃备选——快但可能漏解。

### 块 3.5 递归与列表（骑士巡游等）

```prolog
predecessor(P,C) :- parent(P,C).
predecessor(P,S) :- parent(P,C), predecessor(C,S).
```

（来源：课件07 Slide 16–23）

---

## 与 CLIPS 对照

| | Prolog | CLIPS |
|--|--------|-------|
| 方向 | 反向目标驱动 | 前向数据驱动 |
| 课堂 | Week 14 | Week 15 |

---

## 术语表

| English | 中文 |
|---------|------|
| Resolution Refutation | 消解反驳 |
| Clause Form | 子句形式 |
| Unification | 合一 |
| Skolemization | Skolem 化 |
| Horn Clause | 霍恩子句 |

---

## 复习优先级

| 优先级 | 内容 | Slide |
|--------|------|-------|
| **极高** | 九步转换 + 消解手算 | 9–16 |
| **极高** | 自然语言翻译 | — |
| **高** | Prolog/霍恩子句 | 16–23 |
| **中** | 逻辑系统分类 | 15 |

---

**raw**：`notebooklm-raw/ppt07/runs/latest/`
