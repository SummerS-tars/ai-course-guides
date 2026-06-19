根据课件 **07 Logics and Prolog** 的 Part 2（Resolution 归结原理）部分，将一阶谓词逻辑表达式转换为**子句集（Clause Form）**的 9 个标准步骤如下。请注意，本课程中提到的术语“析取范式”与通用逻辑学定义存在术语对齐问题，详见文末说明。

### 子句集转换的 9 个步骤

1.  **消去蕴含式 (Eliminate Implications)**
    利用逻辑等价式 $P \to Q \equiv \neg P \lor Q$ 替换所有的蕴含符号 [1]。
    *   **例子**：$a(x) \to b(x)$ 转换为 $\neg a(x) \lor b(x)$。
    *   **Slide 号**：Slide 9

2.  **否定内移 (Reduce Scope of Negation)**
    利用德·摩根律和量词否定律将否定符号 $\neg$ 移到原子谓词紧邻的位置 [1]。
    *   **例子**：$\neg \exists x P(x)$ 转换为 $\forall x \neg P(x)$。
    *   **Slide 号**：Slide 10

3.  **变量标准化 (Standardize Variables)**
    对变量进行重命名，确保每个量词约束的变量名在整个表达式中是唯一的，消除命名冲突 [2]。
    *   **例子**：$(\forall x P(x)) \lor (\forall x Q(x))$ 转换为 $(\forall x P(x)) \lor (\forall y Q(y))$。
    *   **Slide 号**：Slide 11

4.  **前束化 (Move Quantifiers to Left)**
    在不改变顺序的情况下，将所有的全称量词和存在量词移动到表达式的最左边（形成 Prenex 范式）[3]。
    *   **例子**：$\forall x (P(x) \lor \exists y Q(y))$ 转换为 $\forall x \exists y (P(x) \lor Q(y))$。
    *   **Slide 号**：Slide 12

5.  **存在量词 Skolem 化 (Skolemization)**
    消去存在量词，将受全称量词约束的存在变量替换为 Skolem 函数，不受约束的替换为 Skolem 常量 [3, 4]。
    *   **例子**：$\forall x \exists y Mother(x, y)$ 转换为 $\forall x Mother(x, f(x))$，其中 $f(x)$ 是 Skolem 函数。
    *   **Slide 号**：Slide 12

6.  **略去全称量词 (Drop All Universal Quantifiers)**
    由于经过前几步处理，所有剩余变量均默认受全称量词约束，因此可以直接去掉前缀中的全称量词 [4]。
    *   **例子**：$\forall x (P(x) \lor Q(f(x)))$ 变为 $P(x) \lor Q(f(x))$。
    *   **Slide 号**：Slide 13

7.  **化为合取范式 (Convert to Conjunct of Disjuncts Form)**
    利用分配律（将 $\lor$ 分配到 $\land$ 之上）和结合律，将表达式转换为由 $\land$ 连接的多个“文字析取项”的形式 [5]。
    *   **例子**：$A \lor (B \land C)$ 转换为 $(A \lor B) \land (A \lor C)$。
    *   **Slide 号**：Slide 14

8.  **拆分为独立子句 (Call Each Conjunct a Separate Clause)**
    将第 7 步中由 $\land$ 分隔的每个析取项提取出来，作为一个独立的子句放入子句集中 [6]。
    *   **例子**：从 $(A \lor B) \land (C \lor D)$ 中得到两个子句 $\{A, B\}$ 和 $\{C, D\}$。
    *   **Slide 号**：Slide 15

9.  **子句变量再次标准化 (Standardize Variables Apart)**
    对每个独立子句中的变量重新命名，确保不同子句之间不共用同名变量，以方便后续的合一操作 [6]。
    *   **例子**：子句 $P(x) \lor Q(x)$ 与子句 $R(x)$ 转换为 $P(x) \lor Q(x)$ 与 $R(u)$。
    *   **Slide 号**：Slide 16

---

### 💡 术语对齐说明（重要）

在课堂讲解及期末考试要求中，老师所称的 **“析取范式 (DNF)”** 与课件及标准逻辑教材中的术语存在以下对应关系，请务必在答题时注意：

*   **课堂/考试术语**：**析取范式**（描述为“由多个析取式组成的合取式”）[7, 8]。
*   **课件/标准术语**：**合取范式 (CNF)** 或 **子句集形式 (Clause Form)**。
*   **术语对齐**：本课程定义的“析取范式（DNF）”实际上指的是 **文字的析取（Clause）之合取**。在做消解大题时，你通过上述 9 步得到的最终结果即为课堂所要求的证明前提 [8]。