以下是根据 **课件 05 Uncertainty** 英文 PPT 结合 **Week 13 课堂记录** 完成的内部结构梳理：

### 1. 课件章节/板块原始顺序
1.  **不确定性定义与错误类型** (Uncertainty & Types of Error) [1]
2.  **归纳与演绎中的错误** (Errors and Induction/Deduction) [2, 3]
3.  **不确定性逻辑问题** (Specific Problems: Buridan's ass, Defeat cycle) [4]
4.  **经典概率与假设检验及其缺陷** (Classical Probability & Hypothesis Test Problems) [4-6]
5.  **贝叶斯定理与贝叶斯决策** (Bayes' Theorem & Bayesian Decision Making) [6-11]
6.  **确定性因子理论** (Certainty Factors) [12-18]
7.  **模糊集合与模糊逻辑** (Fuzzy Set & Fuzzy Logic) [19-23]

---

### 2. 知识点维度 Part 划分
*   **Part A：基础背景** —— 不确定性的定义、误差分类（随机/系统误差等）、演绎与归纳的区别 [1-3]。
*   **Part B：贝叶斯决策框架** —— 经典概率、贝叶斯公式在专家系统（如 PROSPECTOR）中的应用、损失函数 (Loss function) 与 Bayes 风险计算 [6, 9, 10]。
*   **Part C：确定性因子 (CF)** —— 针对规则系统的不确定性处理，包含 MB (增加信任度) 和 MD (增加不信任度) 的定义及合成计算 [13, 16, 17]。
*   **Part D：模糊逻辑** —— 处理语义不确定性，包含隶属度函数、语言算子 (Hedges) 及模糊推理规则 [19, 20, 22]。
*   **Part E：随机过程 (课堂补充)** —— 离散马尔可夫链与 PageRank 算法 [Week 13 记录]。

---

### 3. 各 Part 重要程度及补充建议
*   **确定性因子 (CF)：** **极高程度**。明确标注为 **期末考试必考计算题**，需熟练掌握证据合成公式 [31, Week 13 记录]。
*   **贝叶斯决策：** **高程度**。涉及复杂的概率推理和风险最小化决策，是贝叶斯框架的核心 [8, 9]。
*   **模糊逻辑：** **中等偏上**。解决非黑即白的硬边界问题，是计算理论的重要贡献 [24]。
*   **图多需补充处：**
    *   贝叶斯决策树图 (Decision making flow) [8]。
    *   模糊逻辑中的隶属度函数曲线 (TALL 示例) [20]。
    *   语言算子的集中 (Concentration) 与扩散 (Dilation) 效果对比图 [21]。

---

### 4. 课堂对照 (Week 13 深入讲解部分)
*   **贝叶斯框架缺陷：** 课堂深入探讨了经典概率论在不考虑先验知识、未关联决策行动以及高维拟合困难方面的缺陷 [25]。
*   **符号主义优势：** 深入对比了符号主义与深度学习在可解释性和样本效率上的差异 [26]。
*   **确定性因子计算：** 课堂重点强调了证据不确定性、规则不确定性和结论合成三个层面的计算框架 [26]。
*   **马尔可夫链与 PageRank：** 课堂深入讲解了转移矩阵、稳态分布及其在搜索引擎质量评估中的应用 [24, 26]。

---

### 5. 关键英文术语及中文对照
*   **Uncertainty**: 不确定性 [1]
*   **Induction / Deduction**: 归纳 / 演绎 [3]
*   **Bayesian Decision Making**: 贝叶斯决策 [7]
*   **Loss Function**: 损失函数 [9]
*   **Certainty Factor (CF)**: 确定性因子 [13]
*   **Measure of Belief (MB)**: 增加信任度 [13]
*   **Measure of Disbelief (MD)**: 增加不信任度 [13]
*   **Fuzzy Set / Membership Function**: 模糊集 / 隶属度函数 [19, 20]
*   **Linguistic Hedges**: 语言修饰词/语言算子 [21]
*   **Markov Chain / Transition Matrix**: 马尔可夫链 / 转移矩阵 [Week 13 记录]

---

### 6. 讲解不足/需补充处
*   **PageRank 算法细节：** 课件 05 原始 PPT 中对 PageRank 的数学推导较少，需补充 **转移矩阵乘以初始向量最终收敛至稳态** 的计算逻辑 [24]。
*   **先验知识的作用：** 需进一步补充先验概率 (Prior probability) 在专家决策中为何至关重要的实例说明 [25]。
*   **语义不确定性：** 课件对模糊逻辑解决“硬边界”问题的哲学背景讲解较简略，需补充 Zadeh 理论对经典集合论的突破性意义 [24]。