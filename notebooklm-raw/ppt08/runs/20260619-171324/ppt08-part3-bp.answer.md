在神经网络的训练中，**反向传播算法（Backpropagation, BP）** 是核心，其本质是微积分中**链式法则**在计算计算图梯度时的应用 [1-3]。根据**课件 08** 以及课程笔记和教材的补充，以下是对 BP 算法重难点的详细讲解，旨在为 **Project 1 Part 1** 的纯 NumPy 实现提供理论支撑。

### 0. 符号表 (Notation)
为了推导清晰，我们统一使用以下符号（参考 [1, 4-6]）：

| 符号 | 含义 | 备注 |
| :--- | :--- | :--- |
| $L$ | 损失函数 (Loss Function) | 如 MSE 或 Cross Entropy [7, 8] |
| $t_k$ ($d_k$) | 目标值 (Target / Desired) | 样本的真实标签 [4, 6] |
| $y_k$ ($O_k$) | 输出层神经元 $k$ 的激活值 | 网络最终的预测输出 [4, 6] |
| $h_j$ ($O_j$) | 隐层神经元 $j$ 的激活值 | 输出层的输入信号 [1, 9] |
| $z_k$ ($net_k$) | 神经元 $k$ 的净输入 (Net Input) | $z_k = \sum_j w_{kj} h_j + b_k$ [5, 10] |
| $w_{kj}$ | 权重 (Weight) | 从隐层神经元 $j$ 指向输出层神经元 $k$ [9, 11] |
| $f(\cdot)$ | 激活函数 (Activation Function) | 如 Sigmoid, Tanh, ReLU [4, 12] |
| $\delta$ | 误差项/灵敏度 (Sensitivity) | 损失对净输入的偏导 $\delta = -\frac{\partial L}{\partial z}$ [6, 13] |
| $\eta$ ($r$) | 学习率 (Learning Rate) | 控制参数更新步长的超参数 [1, 4, 14] |

---

### 1. 链式法则与 $\delta$ 的推导
BP 算法的目标是计算损失 $L$ 对每一层权重 $w$ 的梯度。由于 $L$ 通过层层嵌套的函数与权重相关联，必须使用**链式法则** [1, 3]。

#### **(1) 输出层误差项 $\delta_k$**
输出层神经元 $k$ 对损失的“贡献”可以表示为误差项 $\delta_k$。
**Slide 缺口补充：** 课件直接给出了 $\Delta w$ 的结果 [1]，这里补全 $\delta_k$ 的中间推导。
根据定义：
$$\delta_k = -\frac{\partial L}{\partial z_k}$$
通过链式法则分解：
$$\delta_k = -\frac{\partial L}{\partial y_k} \cdot \frac{\partial y_k}{\partial z_k}$$
1.  **第一项 $-\frac{\partial L}{\partial y_k}$**：反映了损失随输出变化的快慢。以回归任务（MSE）为例，$L = \frac{1}{2}(y_k - t_k)^2$，则 $-\frac{\partial L}{\partial y_k} = -(y_k - t_k) = t_k - y_k$ [4, 15]。
2.  **第二项 $\frac{\partial y_k}{\partial z_k}$**：即激活函数的导数 $f'(z_k)$ [16]。
因此，**输出层 $\delta_k = (t_k - y_k) f'(z_k)$** [17]。

#### **(2) 隐层误差项 $\delta_j = f'(z_j) \sum_k \delta_k w_{kj}$**
隐层神经元 $j$ 不直接与损失连接，其误差必须从下一层（输出层）传回 [18]。
**推导过程：**
根据定义 $\delta_j = -\frac{\partial L}{\partial z_j}$。由于 $z_j$ 通过影响下一层所有的 $z_k$ 来影响 $L$ [11]：
$$\delta_j = -\sum_k \frac{\partial L}{\partial z_k} \cdot \frac{\partial z_k}{\partial z_j}$$
1.  已知 $-\frac{\partial L}{\partial z_k} = \delta_k$。
2.  计算 $\frac{\partial z_k}{\partial z_j}$：
    $$z_k = \sum_j w_{kj} f(z_j) + b_k \implies \frac{\partial z_k}{\partial z_j} = w_{kj} \cdot f'(z_j)$$
将上述两项代入：
$$\delta_j = \sum_k \delta_k \cdot w_{kj} \cdot f'(z_j) = f'(z_j) \sum_k \delta_k w_{kj}$$
**物理意义**：隐层的误差项等于**后一层所有误差项的加权和**（权重为连接强度 $w_{kj}$）再乘以**本层激活函数的导数** [6, 9, 19]。

---

### 2. 回归 (MSE) 与分类 (Softmax+CE) 的统一梯度形式
在 **Project 1** 中，你会发现虽然回归和分类任务的损失函数不同，但输出层的更新逻辑惊人地相似 [20]。

*   **回归任务**：通常采用 **MSE + 恒等激活函数** ($f(z)=z, f'=1$)。
    $$\delta_k = (t_k - y_k) \cdot 1 = t_k - y_k$$
*   **分类任务**：采用 **交叉熵 (CE) + Softmax** [20, 21]。
    由于 Softmax 的输出 $y_k$ 耦合了所有 $z_s$，求导非常复杂，但最终可以证明 [20]：
    $$\frac{\partial L_{CE}}{\partial z_k} = y_k - t_k \implies \delta_k = t_k - y_k$$

**结论**：在实现代码时，只要正确选择了损失函数和激活函数的组合，输出层的误差项均可统一表示为 **$y_k - t_k$ (预测值 - 真实值)** [20]。这种统一性极大地方便了通用 BP 框架的编写 [20]。

---

### 3. 权重更新 $\Delta w_{kj} = \eta \delta_k h_j$
得到误差项 $\delta$ 后，权重的更新遵循**负梯度方向**以最小化损失 [22, 23]。

根据梯度下降公式：
$$\Delta w_{kj} = -\eta \frac{\partial L}{\partial w_{kj}}$$
利用链式法则分解为误差项和输入信号 [6, 15]：
$$\frac{\partial L}{\partial w_{kj}} = \frac{\partial L}{\partial z_k} \cdot \frac{\partial z_k}{\partial w_{kj}}$$
1.  由前述推导，$\frac{\partial L}{\partial z_k} = -\delta_k$。
2.  根据 $z_k = \sum_j w_{kj} h_j + b_k$，有 $\frac{\partial z_k}{\partial w_{kj}} = h_j$（即前一层的输出）[24]。
代入后得到：
$$\Delta w_{kj} = -\eta (-\delta_k \cdot h_j) = \eta \delta_k h_j$$

**公式口诀**：权重的修正量 = **学习率 $\times$ 本层的误差项 $\times$ 前一层的输入信号** [1, 6]。

---

### 4. 对应 Project 1 Part 1 实现要点
根据以上讲解，在不使用框架、纯 NumPy 实现时需注意（参考 [25-27]）：
1.  **前向传播**：务必区分 `z` (net input) 和 `h` (activation)，因为反向传播需要用到 $f'(z)$ [5]。
2.  **梯度清零**：在每个 Mini-batch 迭代前，确保梯度累加变量重置为零 [28]。
3.  **矩阵化实现**：为了效率，上述标量公式应转化为矩阵乘法。例如隐层误差 $\boldsymbol{\delta}_{hidden} = (\boldsymbol{\delta}_{output} \mathbf{W}^T) \odot f'(\mathbf{z}_{hidden})$。
4.  **初始化技巧**：对于手写汉字分类，建议将权重初始化为较小随机值，并将偏置项 (bias) 初始化为负数以稳定初期收敛 [26, 27]。