根据**课件 07**（Slide 16–23），关于霍恩子句与 Prolog 的相关概念讲解如下：

### 1. 霍恩子句的三种形式与 Prolog 规则对应
霍恩子句（Horn Clauses）是至多包含一个正文字的子句 [1]。Prolog 解释器将其映射为以下三种编程结构 [1]：

*   **事实（Facts）**：没有负文字，表示绝对为真的断言。
    *   *逻辑形式*：$a \leftarrow$
    *   *代码*：`parent(tom, bob).`
*   **规则（Rules）**：包含一个正文字（头部）和一个或多个负文字（身体），表示蕴含关系。
    *   *逻辑形式*：$a \leftarrow b_1 \land b_2 \land \dots \land b_n$
    *   *代码*：`friends(X, Y) :- likes(X, Z), likes(Y, Z).` [2]
*   **目标/查询（Goals/Queries）**：没有正文字，表示待证明的命题。
    *   *逻辑形式*：$\leftarrow a_1 \land a_2 \land \dots \land a_n$
    *   *代码*：`?- parent(tom, X).`

### 2. 合一（Unification）在 Prolog 查询中的角色
合一在 Prolog 中扮演着**模式匹配与变量绑定**的核心角色 [3]：
*   **触发推理**：Prolog 解释器会按顺序搜索第一个头部能与当前目标子目标（如 $a_1$）进行**合一**的子句 [1, 3]。
*   **变量替换**：合一产生一个代换（Unification/Substitution）$\xi$，将目标中的变量替换为具体项，从而将原始目标还原为更简单的子目标集合 [3]。
*   **验证成功**：如果目标最终能被还原为空子句（Null Clause），则说明在这些合一代换的解释下，原始目标为真 [3]。

### 3. 深度优先搜索与回溯（Backtracking）
Prolog 采用**自顶向下、由左至右**的深度优先搜索（DFS）策略来减少目标 [3, 4]：
*   **深度优先**：解释器总是持续尝试减少最左侧的目标（子目标 $b_1$）[3]。
*   **回溯（Backtracking）**：当当前分支无法找到可合一的子句或后续子目标失败时（例如在“骑士遍历”中，移动到的位置已被访问过），解释器会返回到最近的一个选择点，撤销绑定，并尝试下一个可用的子句 [5]。
    *   *示例*：在查找路径时，如果 `move(7, Z)` 匹配到的 $Z=6$ 导致后续失败，系统会回溯并尝试下一个匹配 $Z=2$ [5]。

### 4. 剪枝 `!` 的作用
剪枝（Cut，符号为 `!`）用于**控制搜索过程**并提高效率 [6, 7]：
*   **冻结选择**：一旦执行到 `!`，解释器就承诺当前的执行路径。它会抛弃当前子句中 `!` 之前所有子目标的备选方案，并且不再尝试该目标的后续其他子句 [7]。
*   **限制结果**：它可以防止系统寻找不必要的重复解。
    *   *代码对比*：
        *   无剪枝：`path2(X, Y) :- move(X, Z), move(Z, Y).`（会回溯寻找所有可能的 $W$）[6]
        *   有剪枝：`path3(X, Y) :- move(X, Z), !, move(Z, Y).`（锁定第一个 $Z$ 后不再寻找其他 $Z$）[7]

### 5. 递归规则示例（如 predecessor）
递归允许通过自身定义复杂的逻辑关系，通常包含**基础情形**和**递归情形** [4, 8]：

```prolog
% 递归示例：前辈 (predecessor)
% 基础情形：Parent 直接就是 Child 的前辈
predecessor(Parent, Child) :- 
    parent(Parent, Child). [8]

% 递归情形：Predecessor 是某个 Child 的家长，而该 Child 是 Successor 的前辈
predecessor(Predecessor, Successor) :- 
    parent(Predecessor, Child), 
    predecessor(Child, Successor). [8]
```
这种结构使得 Prolog 能够沿着 `parent` 事实链条不断向上追溯 [8]。