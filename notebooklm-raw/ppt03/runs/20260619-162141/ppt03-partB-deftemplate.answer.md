在 CLIPS（C Language Integrated Production System）中，事实（Facts）是系统工作内存的基础。以下是根据课件 **03 CLIPS Part B** 整理的 `deftemplate` 语法、槽属性约束及事实操作的详细讲解。

### 符号说明表
根据课件惯例，使用以下符号表示语法规则 [1]：
| 符号 | 含义 |
| :--- | :--- |
| `( )` | 基本定界符 |
| `< >` | 必选替换内容 |
| `[ ]` | 可选内容 |
| `*` | 零个或多个 |
| `+` | 一个或多个 |
| `\|` | 多选一（逻辑或） |

---

### 一、 `deftemplate` 语法：槽与多字段槽
`deftemplate` 用于定义非结构化事实的“模板”，类似于编程语言中的结构体或类 [2, 3]。

**基本语法：**
```clips
(deftemplate <relation-name> [<optional-comment>]
   <slot-definition>*)
```
其中 `<slot-definition>` 可以是以下两种形式之一 [3]：

1.  **槽 (slot)**：**单字段槽 (Single-field Slot)**。该槽位只能存储一个值 [3, 4]。
    *   *示例*：`(slot age)`。
2.  **多字段槽 (multislot)**：**多字段槽 (Multifield Slot)**。该槽位可以存储零个、一个或多个值 [3, 4]。
    *   *示例*：`(multislot name)`。

---

### 二、 五种槽属性约束 (Slot Attributes)
在定义模板时，可以对槽添加属性约束。以下内容重点对齐 **Slide 13/16** 的属性总结表 [3, 5-8]：

| 属性 | 语法格式 [8] | 含义与说明 | 极简 CLIPS 示例 |
| :--- | :--- | :--- | :--- |
| **type** | `(type <type-spec>)` | **类型约束**：限定槽值的类型（如 SYMBOL, STRING, INTEGER, FLOAT 等）。默认为 `?VARIABLE` [3]。 | `(slot age (type INTEGER))` |
| **allowed-values** | `(allowed-values <value>+)` | **允许值约束**：限定槽位只能取特定的一组值（也可以使用 `allowed-symbols` 等更具体的限定） [5]。 | `(slot sex (allowed-values male female))` |
| **range** | `(range <lower> <upper>)` | **范围约束**：限定数值（INTEGER/FLOAT）的上下限。可以使用 `?VARIABLE` 表示不设限 [5, 6]。 | `(slot score (range 0 100))` |
| **cardinality** | `(cardinality <low> <up>)` | **基数约束**：**仅用于 multislot**，限定多字段槽中元素的个数范围 [6]。 | `(multislot hobby (cardinality 1 3))` |
| **default** | `(default <default-spec>)` | **默认值约束**：若在 assert 事实时未指定该槽的值，则自动填入默认值 [7]。 | `(slot color (default white))` |

---

### 三、 事实操作：assert、retract、modify 与 deffacts
CLIPS 提供了多种操作事实的指令，其使用场景和底层逻辑有所不同 [9]：

#### 1. `assert` (添加事实)
*   **功能**：向事实列表（Fact List）中添加一个或多个新事实 [9]。
*   **使用场景**：推理过程中动态产生新信息，或在交互界面手动输入初始数据。
*   **示例**：`(assert (person (name "Zhang") (age 20)))`

#### 2. `retract` (撤销事实)
*   **功能**：通过**事实索引 (Fact Index)** 从事实列表中移除指定事实 [9]。
*   **使用场景**：当某个事实不再成立或推理已完成需要清理工作内存时使用。
*   **示例**：`(retract 1)`（撤销索引为 1 的事实）。

#### 3. `modify` (修改事实)
*   **功能**：修改现有事实中一个或多个槽的值 [9]。
*   **底层逻辑**：其本质是先 `retract` 旧事实，再 `assert` 一个带有新值的新事实，因此修改后事实的**索引会改变**。
*   **使用场景**：更新实体的属性状态（如更新一个人的年龄）。
*   **示例**：`(modify 1 (age 21))`（将索引为 1 的事实中 age 槽改为 21）。

#### 4. `deffacts` (定义事实组)
*   **功能**：定义一组初始事实 [9]。
*   **使用场景**：用于定义系统的**初始状态**。当执行 `(reset)` 命令时，`deffacts` 中定义的所有事实会被自动 `assert` 到事实列表中 [9, 10]。
*   **示例**：
    ```clips
    (deffacts initial-people "一些初始人员"
       (person (name "Sean") (age 21))
       (person (name "John") (age 24)))
    ```

**区别总结：**
*   `assert` 和 `retract` 是最基本的新增与删除操作。
*   `modify` 是针对模板类事实的快捷“更新”指令（注意索引变化）。
*   `deffacts` 是批量初始化事实的**构造结构**，而非单一执行命令 [9]。