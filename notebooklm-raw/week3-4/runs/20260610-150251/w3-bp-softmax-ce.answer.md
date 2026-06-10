根据 Week 3 课程记录和课件 08，在分类任务中使用 **Softmax 激活函数**配合**交叉熵损失（Cross-Entropy Loss）**时，输出层误差项 $\delta_k = y_k - t_k$ 的完整推导如下。这一推导被认为是本模块最难的数学环节之一，其简洁的最终形式体现了神经网络设计中的“优美对称性” [1]。

### 1. 符号定义
*   **$a_k$**：输出层第 $k$ 个神经元的**净输入**（Net Input/Logit）[1]。
*   **$y_k$**：输出层第 $k$ 个神经元的 **Softmax 输出值**，代表预测概率 [1, 2]。
*   **$t_k$**：第 $k$ 个类别的真实标签（Target），采用 **One-hot 编码**（仅正确类别为 1，其余为 0）[3, 4]。
*   **$L$**：交叉熵损失函数 [3]。

### 2. 基础公式准备
1.  **交叉熵损失**：$L = - \sum_i t_i \ln y_i$ [3, 4]。
2.  **Softmax 函数**：$y_i = \frac{e^{a_i}}{\sum_s e^{a_s}}$ [1, 2]。

### 3. 逐步链式法则推导
我们的目标是求损失函数 $L$ 对输出层净输入 $a_k$ 的偏导数 $\frac{\partial L}{\partial a_k}$。根据链式法则，需要考虑 $a_k$ 对所有输出节点 $y_i$ 的影响：
$$\frac{\partial L}{\partial a_k} = \sum_i \frac{\partial L}{\partial y_i} \cdot \frac{\partial y_i}{\partial a_k}$$ [1]

#### 第一步：求损失对预测值的偏导 ($\frac{\partial L}{\partial y_i}$)
由于 $L = - \sum_i t_i \ln y_i$，对特定的 $y_i$ 求导得：
$$\frac{\partial L}{\partial y_i} = - \frac{t_i}{y_i}$$ [3]

#### 第二步：求 Softmax 对净输入的偏导 ($\frac{\partial y_i}{\partial a_k}$) —— 分情况讨论
这是推导的核心难点。由于 Softmax 的分母包含所有 $e^{a_s}$，我们需要分两种情况讨论 [1]：

*   **情况 1：$i = k$（Softmax 输出对自身的输入求导）**
    利用商的求导法则 $(\frac{u}{v})' = \frac{u'v - uv'}{v^2}$：
    $$\frac{\partial y_k}{\partial a_k} = \frac{e^{a_k} (\sum_s e^{a_s}) - e^{a_k} \cdot e^{a_k}}{(\sum_s e^{a_s})^2} = \frac{e^{a_k}}{\sum_s e^{a_s}} \cdot \frac{\sum_s e^{a_s} - e^{a_k}}{\sum_s e^{a_s}} = y_k(1 - y_k)$$

*   **情况 2：$i \neq k$（Softmax 输出对其他位置的输入求导）**
    $$\frac{\partial y_i}{\partial a_k} = \frac{0 \cdot (\sum_s e^{a_s}) - e^{a_i} \cdot e^{a_k}}{(\sum_s e^{a_s})^2} = - \frac{e^{a_i}}{\sum_s e^{a_s}} \cdot \frac{e^{a_k}}{\sum_s e^{a_s}} = -y_i y_k$$

#### 第三步：代回链式法则公式并合并
将上述结果代入总公式中，并将求和拆分为 $i=k$ 和 $i \neq k$ 两部分：
$$\frac{\partial L}{\partial a_k} = \left( \frac{\partial L}{\partial y_k} \cdot \frac{\partial y_k}{\partial a_k} \right) + \sum_{i \neq k} \left( \frac{\partial L}{\partial y_i} \cdot \frac{\partial y_i}{\partial a_k} \right)$$
$$\frac{\partial L}{\partial a_k} = \left( -\frac{t_k}{y_k} \right) \cdot y_k(1 - y_k) + \sum_{i \neq k} \left( -\frac{t_i}{y_i} \right) \cdot (-y_i y_k)$$

#### 第四步：化简
1.  左边项消去 $y_k$：$-t_k(1 - y_k) = -t_k + t_k y_k$。
2.  右边项消去 $y_i$：$\sum_{i \neq k} t_i y_k$。
3.  合并：$\frac{\partial L}{\partial a_k} = -t_k + t_k y_k + \sum_{i \neq k} t_i y_k$。
4.  提取公因子 $y_k$：$\frac{\partial L}{\partial a_k} = y_k (t_k + \sum_{i \neq k} t_i) - t_k$。
5.  由于 One-hot 标签的性质，所有标签之和 $\sum_{all i} t_i = 1$，因此括号内为 1。

最终得出：
$$\frac{\partial L}{\partial a_k} = \mathbf{y_k - t_k}$$ [1]

### 4. 为什么与回归任务形式统一？
在回归任务中，使用 **MSE 损失 + 恒等激活 ($y_k = a_k$)** 时，误差项推导结果也是 $\delta_k = y_k - t_k$。

**统一的原因**：
Softmax 的指数函数（$\exp$）与交叉熵的对数函数（$\ln$）在求导过程中发生了完美的**数学对冲** [1]。这种“锁与钥匙”般的配对设计，使得输出层对于分类和回归任务都能产生“**预测值减真实值**”这一最符合物理直觉的梯度信号 [1, 5]。这极大地简化了代码实现，使得开发者只需一套通用的反向传播框架，就能无缝处理不同类型的学习任务 [1]。