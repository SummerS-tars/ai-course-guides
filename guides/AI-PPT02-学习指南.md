# 课件 02 — Knowledge Representation 学习指南

> **课件**：`02Knowledge representation.pdf`｜NotebookLM `课件02-Knowledge-Representation`  
> **原则**：按课件原序、按知识点分块、**课件板块无遗漏**  
> **课堂**：Week 12 符号主义 KR 引入；Part D 概念图操作需自学补全  
> **术语**：**中文（English）**

---

## 课件内容覆盖索引

| 课件原序 | 课件板块 | Slide | 本指南 |
|----------|----------|-------|--------|
| 1 | 标题页与导引（专家系统公式） | ~1 | Part A · 块 A.1 |
| 2 | Knowledge representation 定义 | ~1–3 | Part A · 块 A.2 |
| 3 | Semantic Network（金丝雀分层图） | ~4–5 | Part B · 块 B.1–B.2 |
| 4 | Frames（旅馆房间/椅子） | ~6 | Part C · 块 C.1 |
| 5 | Types of slot | ~6 | Part C · 块 C.2 |
| 6 | Inference in frame systems（John/消防车） | ~7 | Part C · 块 C.3 |
| 7 | Conceptual graph 基础（一元/二元/三元） | ~8 | Part D · 块 D.1 |
| 8 | Unique token / Generic marker | ~9–11 | Part D · 块 D.2 |
| 9 | Propositional concept（信念表示） | ~12 | Part D · 块 D.3 |
| 10 | Inference in CG（Restriction/Join/Simplify） | ~13–14 | Part D · 块 D.4 |
| 11 | Others（其他 KR 方法清单） | ~15 | Part E · 块 E.1 |
| — | *易混概念对照* | — | 附录 · 块 X.1 |

---

## Part A — KR 基础与概述（Slide ~1–3）

### 块 A.1 标题页与专家系统公式

**课件要点**：Programs = Algorithms + Data Structures；Expert Systems = Knowledge + Inference。

- **本块要解决的问题**：为什么专家系统不把所有逻辑硬写进程序，而要把「知识」单独拿出来表示。
- **传统程序**：算法与数据耦合，改功能常需改代码逻辑。
- **专家系统**：**知识库**与**推理机**分离；换领域主要换知识，推理框架可复用。
- **定性 vs 定量**：专家系统侧重定性推理与不确定性，传统程序侧重数值与确定流程。

> **直观理解**：传统程序像专用计算器——电路为特定账目设计；专家系统像可换教材的导师——换「知识」不必换「思考方式」。

（来源：课件02 Slide 1、Week 12）

### 块 A.2 KR 三要素：表示、获取、使用

**课件要点**：Knowledge Representation 涵盖 **Representation / Acquirement / Use** 三者。

**知识表示（Knowledge Representation, KR）**：把人对世界的认识写成机器可检索、可推理的结构；它不只是「存数据」，还要支持从已有知识推出隐含结论。

| 要素 | 含义 |
|------|------|
| 表示 Representation | 将世界知识编码为计算机可处理的形式 |
| 获取 Acquirement | 专家录入、机器学习等获得知识 |
| 使用 Use | 推理、决策、问答 |

- **基石地位**：KR 是获取与使用的**起点**；符号主义认为智能 = 符号操作，表示方式决定系统上限。
- **与数据库区别**：数据库存显式事实、缺通用推理；KR 可表达规则、否定、层级语义并推导隐含结论。

> **直观理解**：KR 像「笔记格式」——格式乱则难记难查；符号主义里它更是「成文法典」，法官（推理机）无典不可判。

（来源：课件02 Slide 1–3、Week 12）

---

## Part B — 语义网络 Semantic Networks（Slide ~4–5）⭐

### 块 B.1 节点、有向边与 is-a 层级

**课件要点**：节点 = 对象/类别；有向边 = 关系。

- **语义网络（Semantic Network）**：用图表示知识；节点代表对象/类别，有向边代表关系。
- **is-a**：子类/实例关系，构成**分类层级**（Taxonomic Hierarchy，越往上越抽象）。
- **属性边**：`can`（能）、`has`（有）、`is`（是）、`cannot`（不能）等。
- **课件层级（文字版）**：
  - **ANIMAL**：`can` Breathe/Move，`has` Skin
  - **BIRD** `is-a` ANIMAL：`has` Wings/Feathers，`can` Fly
  - **CANARY** `is-a` BIRD：`can` Sing，`is` Yellow
  - **OSTRICH** `is-a` BIRD：`is` Tall；**异常** `cannot` Fly

（来源：课件02 Slide 4–5、Week 12）

### 块 B.2 继承 Inheritance 推理机制

**课件要点**：属性存于**最高合适抽象层**；查询时本地无则沿 `is-a` **向上**搜索。

**继承（Inheritance）**：子类/实例自动获得父类属性；这样「动物有皮肤」只需写在 ANIMAL，不必在每个动物节点重复写一遍。

**手算例**：「金丝雀有皮肤吗？」

1. 查 CANARY：仅有 Sing、Yellow → 无 Skin  
2. 沿 `is-a` 到 BIRD：Wings/Fly/Feathers → 仍无  
3. 沿 `is-a` 到 ANIMAL：发现 `has` Skin  
4. **结论**：金丝雀有皮肤（继承自动物）

- **异常覆盖**：鸵鸟本地 `cannot` Fly 覆盖鸟类默认「能飞」。
- **继承 vs 默认**：继承是层级传递；默认值是「暂时假定」，可被更具体事实覆盖，推理**非单调**。

> **重难点**：向上追溯直到找到属性或到根；冲突时**更具体节点优先**（鸵鸟 > 鸟）。

（来源：课件02、Week 12）

---

## Part C — 框架 Frames（Slide ~6–7）⭐

### 块 C.1 框架基本结构

**课件要点**：框架表示**刻板印象情境**（Stereotyped Situations）的静态结构。

- **框架（Frame）**：把某个对象/场景的相关属性集中成一张「模板卡片」，比语义网络的分散节点更适合表示复杂对象。
- **槽 Slot**：命名属性或关系（如 `location`、`contains`、`height`、`legs`）。
- **侧面 Facet**：槽的约束、类型、程序挂钩（Demons）；可理解为「这个槽怎么填、填错怎么办、填完触发什么」。
- **默认值 Default**：无反证时假定槽值（旅馆椅子 `legs: 4`，房间默认含床、电话）。

（来源：课件02 Slide 6）

### 块 C.2 槽位类型 Types of slot

**课件要点**：槽可承载多种信息类型。

| 类型 | 说明 | 例 |
|------|------|-----|
| 标识 | 框架名称 | hotel-room |
| 关系 | `isa` / `specialization of` / `superclass` | 旅馆床 superclass → 床 |
| 约束 | 值域、类型限制 | 椅子高度 20–40 cm |
| 程序性 | 填槽时触发的守护程序 | 修改价格时重算 |

- **与语义网络**：框架把对象及其全部属性**打包**在一个实体里，结构更透明；语义网络是扁平节点+弧，复杂对象时图易膨胀。

（来源：课件02 Slide 6、参考书 Luger）

### 块 C.3 框架推理：John 与消防车

**课件要点**：部分信息 → 模式匹配激活框架 → 补全缺失槽。

**这个例子要解释的问题**：框架如何用一个熟悉模板补全未明说的属性，而不是只保存显式事实。

**推理链**：

1. 已知：John `isa` human；描述「John like a fire engine」  
2. 激活 **fire engine** 框架：`activity: high`，`volume: very high`  
3. 类比填充 John 框架 → `activity: high`（原先未知）

- **继承逻辑**：子框架继承父槽与默认值；**本地值覆盖**继承值（单腿 John：`legs: 1` 覆盖默认 2）。
- **冲突处理（课件未详述）**：多父类属性冲突时常用** specificity / 本地优先**；默认值可被撤销 → **非单调推理**。

> **直观理解**：见到「像消防车一样的人」，大脑自动补全「吵、忙」——框架即这类「场景模板」。

（来源：课件02 Slide 7、Week 12）

---

## Part D — 概念图 Conceptual Graphs（Slide ~8–14）⭐⭐

### 块 D.1 CG 基础与多元关系优势

**课件要点**：CG = **有限、连接的二部图**——概念节点（方框）+ 关系节点（椭圆）。

- **概念图（Conceptual Graph, CG）**：用「概念节点 + 关系节点」共同表达命题；关系节点可以连接多个概念。
- **二部图（Bipartite graph）**：两类节点分开，边只在概念节点与关系节点之间连接，不直接概念连概念。
- **vs 语义网络**：SN 用标记弧，**三元及以上关系**需 Reification（重化：把关系临时变成一个对象）拆成多条二元弧；CG 一个关系节点可连多个概念，保持原子性。
- **例**：Parents 关系节点同时连 child、father、mother。

（来源：课件02 Slide 8、Week 12）

### 块 D.2 Unique token 与 Generic marker

**课件要点**：概念节点 = **类型 Type** : **指称 Referent**。

| 标记 | 形式 | 含义 |
|------|------|------|
| 个体标记 Individual | `"emma"` 或 `#007` | 确定实体；#ID 唯一，名称可重复 |
| 通用标记 Generic | `*`（`[dog]` = `[dog: *]`） | 该类型中未指定个体 ≈ $\exists X$ |
| 命名变量 | `*X`、`*foo` | 同一未指定个体多处引用 |

**手算例**：`[dog] -> (color) -> [brown]` →「存在一只狗，颜色为棕」。

（来源：课件02 Slide 9–11）

### 块 D.3 命题概念 Propositional concept

**课件要点**：表示**关于信念/命题**的知识（meta-level），而非仅实体关系。

- 用于表达「Agent 相信 P」「P 为真」等二阶信息。
- 与一阶实体图组合，可表达嵌套信念结构。
- **考试**：了解概念即可；操作题重心在 D.4 三操作。

（来源：课件02 Slide 12）

### 块 D.4 概念图推理：Restriction / Join / Simplify ⭐

**课件要点**：三大**规范化形成规则**（Canonical Formation Rules）。

#### A. 限制 Restriction（特化）

- 通用标记 → 个体标记；或类型 → 子类型（指称一致）。
- **机制**：信息变得更具体，外延变小；例如「某个动物」缩小为「Emma 这只狗」。
- **例**：`[animal: "emma"]` → `[dog: "emma"]`（向下转型，外延缩小）。

#### B. 连接 Join（合取）

- 两图有**完全相同**概念节点 → 合并为一图，弧挂到保留节点。
- **机制**：把两个知识片段做合取（AND）；共同节点是对齐点，合并后约束更多。
- **例**：G1「棕色狗」+ G2「Emma 在门廊」→「Emma 这只棕色狗在门廊」。

#### C. 简化 Simplify（去重）

- 两概念间**重复且同向**的关系节点 → 删至留一。
- **机制**：只删除重复表达，不增加也不减少语义。
- **语义不变**，仅精简；Join 后常需 Simplify。

> **重难点手算**：Join 找共同节点对齐；Simplify 查重复关系。Restriction 是特化，Join 是特化，Simplify 是等价变换。

- **与逻辑**：CG 与 FOL 等价；Week 14 逻辑课件可对照转化（本课件未给公式）。

（来源：课件02 Slide 13–14、Week 12）

---

## Part E — 其他 KR 方法概览（Slide ~15）

### 块 E.1 Others 清单与课程映射

**课件要点**：逻辑、产生式、神经网络、贝叶斯网络、Script、决策表等——本课件仅索引。

| KR 方法 | 对应课件 | 讲授周次 |
|---------|----------|----------|
| 逻辑 Logics | 课件 07 | Week 9、14 |
| 产生式 Production rule | 课件 03 CLIPS | Week 10、15 |
| 神经网络 Neural network | 课件 08、09 | Week 5–7 |
| 贝叶斯网络 Bayesian network | 课件 05 Uncertainty | Week 8、13 |
| 剧本 Script | 课件 02 提及 | Week 8、12 |
| 决策表/树 Decision table/tree | 课件 04 | **开卷自学** |

- **本课件定位**：符号主义 KR「工具箱」导览；深入见各独立课件。

（来源：课件02 Slide 15）

---

## 附录 X — 易混概念对照

### 块 X.1 四类核心对比

**1. 专家系统 vs 传统程序**：Knowledge+Inference vs Algorithm+Data；可解释性、知识可更新。

**2. KR vs 数据库**：KR 含规则与推理；DB 缺通用推导、难处理不完整信息。

**3. 语义网络 vs 框架 vs 概念图**（能力递进）：

| 方法 | 结构 | 强项 | 弱项 |
|------|------|------|------|
| 语义网络 | 节点+弧 | 继承直观 | 多元关系难 |
| 框架 | 槽+默认值 | 嵌套、默认、程序钩 | — |
| 概念图 | 二部图 | 多元关系、逻辑等价 | 操作抽象 |

**4. 继承 vs 默认**：继承沿 is-a 严格传递；默认在缺证时假定，可被覆盖（非单调）。

（来源：ppt02-mistakes.answer.md、课件02）

---

## 术语表

| English | 中文 |
|---------|------|
| Knowledge Representation | 知识表示 |
| Semantic Network | 语义网络 |
| Inheritance | 继承 |
| Frame / Slot / Facet | 框架 / 槽 / 侧面 |
| Default Value | 默认值 |
| Conceptual Graph (CG) | 概念图 |
| Generic Marker | 通用标记 |
| Restriction / Join / Simplify | 限制 / 连接 / 简化 |
| Production rule | 产生式规则 |

---

## 复习优先级

| 优先级 | 内容 |
|--------|------|
| 极高 | Part D 概念图三操作 + Generic/Individual 标记 |
| 高 | Part B 继承与金丝雀层级；Part C 框架槽与 John 推理 |
| 中 | Part A KR 定义与专家系统公式 |
| 了解 | Part E 清单映射；附录 X |

---

**raw**：`notebooklm-raw/ppt02/runs/latest/`｜**结构**：`notebooklm-raw/ppt/runs/20260619-161000/ppt02-structure.answer.md`
