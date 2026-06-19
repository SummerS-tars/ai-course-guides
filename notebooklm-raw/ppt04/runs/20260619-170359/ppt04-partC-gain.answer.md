根据**课件 04 (Decision Tree)** 的内容，以下是对 Gender（性别）和 Age（年龄）属性信息增益（Information Gain）计算过程的完整复现。

### 1. 基础公式与初始信息熵计算

在决策树 ID3 算法中，信息增益定义为期望的熵减少量 [1]：
$$Gain(A) = H(S) - \sum_{v \in Values(A)} \frac{|S_v|}{|S|} H(S_v)$$
其中：
*   $H(S)$ 是当前集合 $S$ 的初始熵（课件中记为 $I(Credit)$）[2]。
*   $\sum \frac{|S_v|}{|S|} H(S_v)$ 是属性 $A$ 的期望熵（课件中记为 $E(A)$）[1]。

#### 初始熵 $H(S)$ 计算
训练集共有 6 个样本 [1, 2]：
*   **Credit = Bad (信用差)**：4 个样本 ($p_1 = 4/6$)
*   **Credit = Good (信用好)**：2 个样本 ($p_2 = 2/6$)

$$I(Credit) = -\frac{4}{6} \log_2(\frac{4}{6}) - \frac{2}{6} \log_2(\frac{2}{6})$$
$$= - (0.66667 \times -0.58496) - (0.33333 \times -1.58496)$$
$$= 0.38997 + 0.52831 \approx \mathbf{0.9183}$$ [2]

---

### 2. Gender 属性的信息增益计算

#### 数据统计 [2]
| Gender | Bad | Good | Total |
| :--- | :--- | :--- | :--- |
| **Male** | 2 | 1 | 3 |
| **Female** | 2 | 1 | 3 |

#### 逐步计算
1.  **计算子集熵：**
    *   $I(Gender/Male) = -\frac{2}{3} \log_2(\frac{2}{3}) - \frac{1}{3} \log_2(\frac{1}{3}) \approx 0.9183$
    *   $I(Gender/Female) = -\frac{2}{3} \log_2(\frac{2}{3}) - \frac{1}{3} \log_2(\frac{1}{3}) \approx 0.9183$
2.  **计算 Gender 的期望熵 $E(Gender)$：**
    $$E(Gender) = \frac{3}{6} \times I(Gender/Male) + \frac{3}{6} \times I(Gender/Female)$$
    $$= 0.5 \times 0.9183 + 0.5 \times 0.9183 = \mathbf{0.9183}$$
3.  **计算信息增益：**
    $$Gain(Gender) = I(Credit) - E(Gender) = 0.9183 - 0.9183 = \mathbf{0}$$ [2]

---

### 3. Age 属性的信息增益计算

#### 数据统计 [3]
| Age | Bad | Good | Total |
| :--- | :--- | :--- | :--- |
| **Young ($\le 35$)** | 3 | 0 | 3 |
| **Elder ($> 35$)** | 1 | 2 | 3 |

#### 逐步计算
1.  **计算子集熵：**
    *   $I(Age/Young) = -\frac{3}{3} \log_2(\frac{3}{3}) - \frac{0}{3} \log_2(\frac{0}{3}) = \mathbf{0}$ （纯度最高，无不确定性）
    *   $I(Age/Elder) = -\frac{1}{3} \log_2(\frac{1}{3}) - \frac{2}{3} \log_2(\frac{2}{3}) \approx \mathbf{0.9183}$
2.  **计算 Age 的期望熵 $E(Age)$：**
    $$E(Age) = \frac{3}{6} \times I(Age/Young) + \frac{3}{6} \times I(Age/Elder)$$
    $$= 0.5 \times 0 + 0.5 \times 0.9183 = \mathbf{0.4591}$$
3.  **计算信息增益：**
    $$Gain(Age) = I(Credit) - E(Age) = 0.9183 - 0.4591 = \mathbf{0.4592}$$ [3]

---

### 4. 为何选择 Age 作为根分裂属性？

算法根据 **最大信息增益原则 (Maximum Information Gain)** 来选择分裂属性 [3, 4]。

*   **比较结果**：
    *   $Gain(Age) = 0.4592$
    *   $Gain(Gender) = 0$
*   **决策原因**：
    由于 $Gain(Age) > Gain(Gender)$，Age 属性在分类时提供的“信息量”更大，能更有效地减少分类后的不确定性 [3]。
    *   **直观理解**：通过 Age 分裂后，Young 这一分支的样本全部分类为 "Bad"，实现了完美分类；而通过 Gender 分裂后，子集的类别比例（2:1）与分裂前完全一致，没有对分类起到任何实质性的帮助（故增益为 0）[2, 3]。