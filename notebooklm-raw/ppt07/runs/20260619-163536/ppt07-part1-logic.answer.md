根据课件 **07 Logics and Prolog** 及相关课程笔记，为您讲解命题逻辑与一阶谓词逻辑的基础知识：

### 1. 连接词与真值表；善意推定原则（Minimal Translation）

**命题逻辑（Propositional Logic）** 是逻辑系统中最简单的形式，其基本元素是 **命题符号（Propositional symbols）**（如 $P, Q, R$），用于表示真或假的断言 [1, 2]。

*   **逻辑连接词（Logical connectives）**：利用连接词可以将简单的命题构造为 **复合命题（Complex sentences）** [1, 3]：
    *   **否定（Negation）** $\neg$：表示“非”，若 $P$ 为真，则 $\neg P$ 为假 [3, 4]。
    *   **合取（Conjunction）** $\land$：表示“且”，仅当两个 **合取项（Conjuncts）** 均为真时，结果为真 [3, 4]。
    *   **析取（Disjunction）** $\lor$：表示“或”，仅当两个 **析取项（Disjuncts）** 均为假时，结果为假 [4, 5]。
    *   **蕴含（Implication）** $\rightarrow$：表示“如果……那么……”，其中左侧为 **前提（Premise/Antecedent）**，右侧为 **结论（Conclusion/Consequent）** [5, 6]。
    *   **等价（Equivalence）** $\equiv$：表示“当且仅当”，两个表达式具有相同的真值时为真 [6, 7]。

*   **真值表（Truth table）**：用于定义连接词的语义，它列出了所有可能的 **解释（Interpretation）**（即给命题分配真值的可能世界）下表达式的真假情况 [8, 9]。

*   **善意推定原则（Minimal translation / Presumption）**：这主要体现在对 **蕴含（Implication）** 的语义解释中 [2]。根据此原则，对于表达式 $P \rightarrow Q$，如果前提 $P$ 为假，无论结论 $Q$ 的真假如何，整个表达式均被视为真 [2, 6]。逻辑上，该原则意味着我们默认前提为假的情况不构成对规则的违背，只有在“前提为真且结论为假”这一种情况下，蕴含关系才不成立 [6, 10]。

### 2. 项、谓词、量词 $\forall/\exists$；原子公式

为了克服命题逻辑的局限，**一阶逻辑（First-order Logic / FOL）** 引入了更细致的构造：

*   **项（Terms）**：是逻辑表达式中用于指代 **对象（Objects）** 的部分 [11]。它包括：
    *   **常量符号（Constant symbols）**：代表特定个体（如 $Socrates$） [12, 13]。
    *   **变量符号（Variable symbols）**：作为占位符，指代论域中的通用类别 [12, 13]。
    *   **函数表达式（Function expressions）**：由 **函数符号（Function symbols）** 和参数组成，指代通过映射得到的唯一对象（如 $Mother(John)$ 指代 John 的母亲） [12, 14]。

*   **谓词（Predicates）**：用于描述对象之间的 **关系（Relations）** 或对象的 **属性（Properties）** [15, 16]。谓词具有 **元数（Arity）**，指明其所需的参数数量 [12, 17]。

*   **量词（Quantifiers）**：用于表达关于对象集合的性质，而无需逐个命名 [18]：
    *   **全称量词（Universal quantifier）** $\forall$：表示“对于所有……”，说明在其范围内的性质对论域中的每一个对象都成立 [19-21]。
    *   **存在量词（Existential quantifier）** $\exists$：表示“存在一个……”，说明论域中至少有一个对象满足该性质 [19, 21, 22]。

*   **原子语句/原子公式（Atomic sentences / Atomic formulas）**：逻辑语言中最基本的单位 [16]。它由一个谓词后接若干个括在括号内的项组成（例如 $Likes(george, kate)$），当该谓词所描述的关系在这些项所指代的个体间成立时，该原子公式为真 [12, 23, 24]。此外，逻辑常数 $true$ 和 $false$ 也被视为原子公式 [12, 25]。

### 3. 表达能力局限：为何需要一阶逻辑

命题逻辑虽然基础，但在处理复杂知识表示时存在严重的 **表达能力局限（Limitations of expressive power）** [26, 27]：

1.  **无法区分个体与集合（Individuals vs. Collections）**：命题逻辑将每一个命题视为不可分割的整体，无法访问其内部成分 [28]。例如，无法通过机械匹配直接处理经典的三段论：给定“所有人都会死”和“苏格拉底是人”，命题逻辑无法自动识别出“苏格拉底”是“人”这一集合的一个 **个体实例（Individual instance）**，从而无法推导出结论 [27]。
2.  **缺乏通用性的描述能力**：在命题逻辑中，要表达通用的自然定律非常臃肿 [29]。例如在 Wumpus 世界中，要表达“所有靠近坑的格子都有微风”，命题逻辑必须为地图上的每一个具体格子各写一条规则（如 $B_{1,1} \iff P_{1,2} \lor P_{2,1}$），当环境规模扩大（如 $100 \times 100$ 棋盘）时，规则数量将爆炸式增长 [30, 31]。
3.  **需要一阶逻辑的原因**：一阶逻辑通过引入变量和量词（如“对于所有格子 $s$……”），可以用简洁的一条语句（例如 $\forall s, Breezy(s) \iff \exists r, Adjacent(r,s) \land Pit(r)$）表达跨越时间、空间和对象之间通用关系的规律 [32, 33]。这种 **结构化表示（Structured representation）** 能够更 Concisely 地捕捉自然语言中常见的复杂含义 [34, 35]。