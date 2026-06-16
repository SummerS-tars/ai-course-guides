根据 Week 15 课程记录及课件 03，CLIPS（C Language Integrated Production System）的核心语法涵盖了从基础数据表示到复杂规则定义的完整体系 [1, 2]。以下是针对您要求的核心语法讲解：

### 1. 原始数据类型 (Primitive Data Types)
CLIPS 的基本语法以小括号作为分隔符，其核心数据类型共有四种 [1, 2]：

| 语法符号 | 数据类型 | 说明 | 极简代码示例 |
| :--- | :--- | :--- | :--- |
| **Integer** | 整数 | 包含正数、负数和零 [1] | `1`, `+3`, `-1` |
| **Float** | 浮点数 | 支持标准小数与科学计数法 [1] | `1.5`, `9e+1` |
| **Symbol** | 符号 | 以字母开头，不含空格，常用于表示名称或状态 [2, 3] | `fire`, `active-ok` |
| **String** | 字符串 | 必须使用双引号括起，可包含空格 [2, 3] | `"John Smith"` |

### 2. 前缀表达式 (Prefix Expression)
CLIPS 的数学运算和函数调用均采用 **前缀形式**，即操作符位于操作数之前 [4, 5]。

| 语法 | 说明 | 极简代码示例 |
| :--- | :--- | :--- |
| `(算术符 <项>+)` | 将算术运算符置于括号内的首位 [4] | `(+ 2 3)` (表示 $2+3$) |
| `(算术符 <项> (<嵌套>))` | 支持复杂算式的嵌套表达 [4, 5] | `(+ 3 (* 4 5))` (表示 $3+4 \times 5$) |

### 3. deftemplate 模板定义及五种约束
`deftemplate` 用于定义事实（Fact）的结构，类似于类定义。通过 **槽（slot）** 定义属性，并可施加约束 [5, 6]。

*   **语法结构**：`(deftemplate <名称> (slot <属性名> <约束>*) (multislot <属性名> <约束>*))` [5, 6]。
*   **五种属性约束 (Attributes)**：

| 约束类型 | 说明 | 极简代码示例 |
| :--- | :--- | :--- |
| **type** | 限制槽内数据类型（如 SYMBOL, INTEGER 等） [5, 6] | `(slot age (type INTEGER))` |
| **allowed-values** | 限定槽只能取特定的离散值 [5, 7] | `(slot sex (allowed-values male female))` |
| **range** | 限定数值槽的取值范围 [5, 7] | `(slot age (range 0 150))` |
| **cardinality** | 限定 **multislot**（多值槽）包含的元素个数 [5, 8] | `(multislot names (cardinality 1 6))` |
| **default** | 指定缺省值，未显式给出时自动填充 [5, 9] | `(slot status (default normal))` |

### 4. defrule 规则结构
规则是 CLIPS 的逻辑核心，基于“IF-THEN”模式，由左手边（LHS）的模式匹配和右手边（RHS）的操作组成 [10, 11]。

| 构成部分 | 语法符号 | 说明 | 极简代码示例 |
| :--- | :--- | :--- | :--- |
| **规则名称** | `defrule <name>` | 定义规则的唯一标识符 [10] | `(defrule fire-alert` |
| **LHS** | `(pattern)` | 条件部分：匹配事实库中的事实 [10, 11] | `(emergency (type fire))` |
| **箭头** | `=>` | 分隔条件与动作 [10, 11] | `=>` |
| **RHS** | `(action)` | 动作部分：执行断言、打印等操作 [10, 11] | `(printout t "Fire!" crlf))` |

**完整示例**：
```clips
(defrule fire-emergency
   (emergency (type fire))  ; LHS
   =>
   (assert (response (action activate-sprinkler))) ; RHS
)
```

### 5. 模式匹配变量与约束符
在规则的 LHS 中，可以使用变量捕获事实中的值，并利用约束符进行逻辑过滤 [11-14]。

| 语法符号 | 名称 | 说明 | 极简代码示例 |
| :--- | :--- | :--- | :--- |
| **?var** | 单字段变量 | 绑定并匹配事实中的一个字段值 [3, 14] | `(person (name ?n))` |
| **$?var** | 多字段变量 | 匹配事实中零个或多个字段值 [14, 15] | `(person (name $?names))` |
| **&** | 连接约束 (And) | 要求字段同时满足多个条件 [11, 14, 16] | `?c&brown|black` (是变量且为棕或黑色) |
| **\|** | 析取约束 (Or) | 字段只需满足其中一个值 [11, 13, 14] | `hair brown|black` (发色为棕或黑) |
| **~** | 否定约束 (Not) | 字段值不能是该指定值 [11, 13, 14] | `hair ~black` (发色不是黑色) |

**变量约束示例**：
`(person (name ?name) (eyes ?eyes&blue|green) (hair ~black))`
此模式将匹配姓名存入变量 `?name`，要求眼睛是“蓝色或绿色”，且头发“不是黑色” [11, 16]。