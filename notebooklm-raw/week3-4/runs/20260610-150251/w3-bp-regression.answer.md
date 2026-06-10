根据 Week 3 课程记录与课件 08，针对回归任务（MSE 损失 + 恒等激活）的输出层梯度推导如下：

### 1. 符号含义说明
为了推导清晰，我们首先定义涉及的数学符号 [1-3]：
*   **$L$**：损失函数（此处为均方误差 MSE）。
*   **$t_k$**：输出层第 $k$ 个神经元的真实目标值（Target）。
*   **$y_k$**：输出层第 $k$ 个神经元的预测输出值。
*   **$z_k$**：输出层第 $k$ 个神经元的**净输入**（Net Input），即 $z_k = \sum_j w_{kj} h_j + b_k$。
*   **$h_j$**：来自上一层（隐藏层）第 $j$ 个神经元的**激活值**，作为当前层的输入。
*   **$w_{kj}$**：连接隐藏层节点 $j$ 与输出层节点 $k$ 的权重。
*   **$\delta_k$**：输出层第 $k$ 个节点的**误差项**（局部梯度），定义为 $\frac{\partial L}{\partial z_k}$。

---

### 2. 核心公式推导

#### 第一步：定义损失函数与激活函数
在 Project 1 的回归任务中，配置如下 [3-6]：
1.  **MSE 损失函数**：$L = \frac{1}{2} \sum_k (y_k - t_k)^2$ （注：系数 $1/2$ 用于求导后消去平方项的 $2$）。
2.  **恒等激活函数**：由于是回归任务，输出层激活函数 $f(z) = z$，因此预测值 **$y_k = z_k$**。

#### 第二步：推导误差项 $\delta_k$
根据链式法则，误差项 $\delta_k$ 是损失函数对净输入的偏导数 [6-9]：
$$\delta_k = \frac{\partial L}{\partial z_k} = \frac{\partial L}{\partial y_k} \cdot \frac{\partial y_k}{\partial z_k}$$

1.  **求 $\frac{\partial L}{\partial y_k}$**：对 MSE 公式求导，得 $\frac{\partial}{\partial y_k} [\frac{1}{2}(y_k - t_k)^2] = y_k - t_k$。
2.  **求 $\frac{\partial y_k}{\partial z_k}$**：由于采用恒等激活 $y_k = z_k$，其导数 $f'(z_k) = 1$。
3.  **合并**：
    $$\delta_k = (y_k - t_k) \cdot 1 = \mathbf{y_k - t_k}$$

#### 第三步：推导权重梯度 $\frac{\partial L}{\partial w_{kj}}$
再次利用链式法则，将损失对权重的总导数分解 [6, 7, 10]：
$$\frac{\partial L}{\partial w_{kj}} = \frac{\partial L}{\partial z_k} \cdot \frac{\partial z_k}{\partial w_{kj}}$$

1.  **误差项部分**：已知 $\frac{\partial L}{\partial z_k} = \delta_k$。
2.  **输入部分**：由于 $z_k = w_{k1}h_1 + \dots + w_{kj}h_j + \dots + b_k$，对 $w_{kj}$ 求偏导后，只剩下对应的输入信号 $h_j$ [10]。
3.  **合并**：
    $$\frac{\partial L}{\partial w_{kj}} = \mathbf{\delta_k h_j}$$

---

### 3. 推导结论
在回归任务的输出层中，**权重梯度 = 误差项（预测值 - 真实值） $\times$ 输入信号** [6, 10, 11]。这种简洁的线性形式得益于 MSE 损失与恒等激活函数（导数为 1）的配合。在编写 Project 1 的 NumPy 代码时，输出层的 $\delta$ 矩阵直接由 `output - target` 即可得出 [12, 13]。

**资料来源：**
*   **Week 3 记录**：笔记-week03-周五-AI [3, 6, 11]
*   **课件 08**：08Connectionist.pdf [1, 7]
*   **代码参考**：Project 1 知识点与要求 [5, 9, 13]