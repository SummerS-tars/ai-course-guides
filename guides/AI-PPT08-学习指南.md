# 课件 08 — Connectionist 学习指南

> **课件**：`08Connectionist.pdf`｜NotebookLM `课件08-Connectionist`  
> **原则**：按课件原序、按知识点分块、**课件板块无遗漏**  
> **课堂**：Week 1–4 联结主义与 BP 基础；Week 7 卷积信号处理背景（详见课件 09）  
> **项目**：**Project 1 Part 1**（纯 NumPy BP）  
> **术语**：**中文（English）**

---

## 课件内容覆盖索引

| 课件原序 | 课件板块 | Slide（约） | 本指南 |
|----------|----------|-------------|--------|
| 1 | 联结主义导论与背景 | 1–15 | Part 1 · 块 1.1–1.3 |
| 2 | 神经元模型与激活函数 | 4–5, 16–30 | Part 2 · 块 2.1–2.2 |
| 3 | 学习算法基础（梯度下降、MSE） | 4, 6, 16–30 | Part 2 · 块 2.3–2.4 |
| 4 | 有监督学习：反向传播（BP） | 4, 7–8, 31–50 | Part 3 · 块 3.1–3.5 ⭐ |
| 5 | 经典案例（NETtalk、XOR） | 7, 9–10, 51–60 | Part 4 · 块 4.1–4.3 |
| 6 | 无监督/竞争学习（WTA） | 9, 11, 61–70 | Part 5 · 块 5.1–5.2 |
| 7 | 联结主义任务总结 | 12–13, 71–end | Part 6 · 块 6.1 |

---

## Part 1 — 联结主义导论与生物启发（Slide 1–15）

### 块 1.1 联结主义起源与历史脉络

**课件要点**：从 MP 神经元到感知机，再到深度学习复兴。

| 里程碑 | 人物/事件 | 意义 |
|--------|-----------|------|
| 1943 MP 模型 | McCulloch & Pitts | 证明简单神经元可实现与/或/非逻辑门，奠定计算完备性 |
| 1958 感知机 | Frank Rosenblatt | 首个可学习权重的有监督分类器 |
| 2006–至今 | Hinton 等（DBN/RBM） | 深度学习复兴，语音识别、图像识别突破 |

> **直观理解**：联结主义不是「突然火起来」，而是经历了感知机寒冬后的第三次浪潮。

（来源：课件08 Part 1、Week 1）

### 块 1.2 生物神经元 → 人工神经元映射

```text
树突 Dendrite ──接收──→ 细胞体 Cell body ──轴突 Axon──→ 输出脉冲
                              ↑
                         突触 Synapse（权重 w）
```

| 生物结构 | 人工对应 | 说明 |
|----------|----------|------|
| 输入刺激 | $x_i$ | 来自环境或其他单元 |
| 突触强度 | $w_i$ | **学习 = 调权重** |
| 阈值发放 | $f(\sum w_i x_i)$ | 阶跃 → Sigmoid → ReLU 等 |

- **赫布规则（Hebbian）**：「一起激活的神经元，连接变强」——学习本质是突触强度变化（Eric Kandel 海兔研究）。

（来源：课件08、Week 1）

### 块 1.3 联结主义 vs 符号主义

| 维度 | 符号主义 Symbolism / GOFAI | 联结主义 Connectionism |
|------|------------------------------|------------------------|
| 核心假设 | 物理符号系统：智能 = 符号操作 | 分布式表征：智能 = 大量单元并行交互 |
| 知识表示 | 显式（规则、逻辑、框架） | 隐式（拓扑 + 权重） |
| 学习 | 知识获取难，难从原始数据学 | 数据驱动，BP 等自动学特征 |
| 鲁棒性 | 脆弱，噪声敏感 | 容错，局部损伤不崩溃 |
| 可解释性 | 高（可追溯规则） | 低（黑箱） |

> **重难点**：符号主义模拟「宏观逻辑」，联结主义模拟「微观生物结构」——课件 01 三段论 vs 本课件 BP 形成对照。

（来源：课件08 Part 1、课件01、Week 1）

---

## Part 2 — 数学基础、激活函数与梯度下降（Slide 16–30）

### 块 2.1 硬限幅与 Sigmoid 激活函数

**硬限幅 Hard Limiting（阶跃函数）**

- 输出离散（0/1 或 −1/+1），本质是**线性双极性阈值**。
- **局限**：阈值点不连续，其余处导数为 0 → **无法用梯度下降优化**。

**Sigmoid（对数几率函数）**

$$f(\sigma) = \frac{1}{1 + e^{-\sigma}}$$

- 连续可微，输出 $(0,1)$；0 附近近似线性，两端为**软阈值**。
- **导数优美形式**（复习必背）：

$$f'(\sigma) = f(\sigma)\bigl(1 - f(\sigma)\bigr)$$

- 导数在 $\sigma=0$ 时最大为 **0.25**；$|\sigma|$ 很大时 → **饱和区**，$f' \approx 0$ → **梯度消失**。

> **训练建议**：权重初始化为较小随机值，使初始激活落在 Sigmoid 敏感区（导数较大）。

（来源：课件08 Part 2、Week 2–3）

### 块 2.2 MSE 均方误差损失

$$L = \frac{1}{2}\sum_i (d_i - O_i)^2$$

- $d_i$：目标值；$O_i$：网络输出。
- 系数 $\frac{1}{2}$ 使求导后系数为 1，简化 BP 公式。
- 平方项保证误差非负，大误差惩罚更重。

（来源：课件08、Week 2）

### 块 2.3 误差曲面与梯度下降直觉

**误差曲面 Error Surface**

- 所有权重配置构成 **n 维空间**上的损失函数。
- 线性模型：平滑碗状；引入非线性后曲面**极其崎岖**（「被揉皱的纸」）。
- 易陷入**局部极小值 Local Minimum** 或停滞于**鞍点 Saddle Point**（高维中鞍点更常见）。

**梯度下降 Gradient Descent**

$$\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)$$

- $\eta$：学习率；沿梯度**反方向**走一小步（「下山法」）。
- **验证集早停**：监控验证误差，防止过拟合（Week 3 课堂补充）。

（来源：课件08 Part 2、Week 3）

### 块 2.4 梯度下降 vs 反向传播（概念辨析）

| 概念 | 角色 |
|------|------|
| **梯度下降** | 通用优化**目的**：如何沿曲面找最低点 |
| **反向传播 BP** | 多层网络中高效计算梯度的**工具**（链式法则） |

BP 解决隐层权重的**权责分配（Credit Assignment）**问题，使深层网络可训。

（来源：课件08、Week 3）

---

## Part 3 — 反向传播算法 BP（Slide 31–50）⭐

> **PJ1 Part 1 核心**：纯 NumPy 实现须严格区分 $z$（净输入）与 $h$（激活值），并正确实现下列推导。

### 块 3.1 网络结构与符号表

**三层网络**（输入层 → 隐层 → 输出层）：

```text
输入 x ──w──→ [隐层 j: z_j → h_j=f(z_j)] ──w_kj──→ [输出 k: z_k → y_k=f(z_k)] ──→ L
```

| 符号 | 含义 |
|------|------|
| $L$ | 损失函数（MSE / Cross-Entropy） |
| $t_k$ ($d_k$) | 目标值 Target |
| $y_k$ ($O_k$) | 输出层激活值（预测） |
| $h_j$ | 隐层神经元 $j$ 的激活值 |
| $z_k = \sum_j w_{kj} h_j + b_k$ | 净输入 Net Input |
| $w_{kj}$ | 隐层 $j$ → 输出层 $k$ 的权重 |
| $f(\cdot)$ | 激活函数（Sigmoid / Tanh / ReLU / 恒等） |
| $\delta$ | 误差项/灵敏度：$\delta = -\dfrac{\partial L}{\partial z}$ |
| $\eta$ | 学习率 |

（来源：课件08 Slide 22 缺口补充、Week 3–4、PJ1）

### 块 3.2 链式法则与输出层 $\delta_k$ 推导

**目标**：求 $\dfrac{\partial L}{\partial w_{kj}}$，需先求 $\delta_k$。

由定义：
$$\delta_k = -\frac{\partial L}{\partial z_k}$$

**链式法则分解**：
$$\delta_k = -\frac{\partial L}{\partial y_k} \cdot \frac{\partial y_k}{\partial z_k}$$

**Step 1 — 损失对输出的偏导**（以 MSE 为例）：

$$L = \frac{1}{2}(y_k - t_k)^2 \quad\Rightarrow\quad -\frac{\partial L}{\partial y_k} = t_k - y_k$$

**Step 2 — 激活函数导数**：

$$\frac{\partial y_k}{\partial z_k} = f'(z_k)$$

**合并**：

$$\boxed{\delta_k = (t_k - y_k)\, f'(z_k)}$$

（来源：课件08、Week 3）

### 块 3.3 隐层 $\delta_j$ 完整推导

隐层 $j$ 不直接与 $L$ 相连，误差须从输出层**反向流动**。

$$\delta_j = -\frac{\partial L}{\partial z_j} = -\sum_k \frac{\partial L}{\partial z_k} \cdot \frac{\partial z_k}{\partial z_j}$$

- 已知 $-\dfrac{\partial L}{\partial z_k} = \delta_k$。
- 因 $z_k = \sum_j w_{kj}\, f(z_j) + b_k$：

$$\frac{\partial z_k}{\partial z_j} = w_{kj}\, f'(z_j)$$

代入：
$$\delta_j = \sum_k \delta_k \cdot w_{kj} \cdot f'(z_j) = f'(z_j) \sum_k \delta_k\, w_{kj}$$

$$\boxed{\delta_j = f'(z_j) \sum_k \delta_k\, w_{kj}}$$

**物理意义**：隐层误差 = **后一层所有 $\delta$ 的加权和**（权重为连接强度 $w_{kj}$）× **本层激活导数**。

```text
输出层 δ_k ──沿 w_kj 反向──→ 隐层 δ_j = f'(z_j) · Σ_k δ_k w_kj
```

（来源：课件08 Slide 22 链式法则缺口补充、Week 3）

### 块 3.4 权重更新 $\Delta w$ 推导

$$\Delta w_{kj} = -\eta \frac{\partial L}{\partial w_{kj}}$$

链式法则：
$$\frac{\partial L}{\partial w_{kj}} = \frac{\partial L}{\partial z_k} \cdot \frac{\partial z_k}{\partial w_{kj}}$$

- $\dfrac{\partial L}{\partial z_k} = -\delta_k$
- 因 $z_k = \sum_j w_{kj} h_j + b_k$，故 $\dfrac{\partial z_k}{\partial w_{kj}} = h_j$

$$\boxed{\Delta w_{kj} = \eta\, \delta_k\, h_j}$$

**偏置更新**：$\Delta b_k = \eta\, \delta_k$（因 $\dfrac{\partial z_k}{\partial b_k} = 1$）。

**口诀**：修正量 = **学习率 × 本层误差项 × 前层输入信号**。

（来源：课件08、Week 3、PJ1）

### 块 3.5 MSE 回归 vs CE+Softmax 分类的统一形式

| 任务 | 损失 + 输出激活 | 输出层 $\delta_k$ |
|------|-----------------|-------------------|
| 回归 | MSE + 恒等 $f(z)=z,\; f'=1$ | $t_k - y_k$ |
| 分类 | Cross-Entropy + Softmax | $t_k - y_k$（可证） |

> **PJ1 实现要点**：正确配对损失与激活后，输出层 $\delta$ 统一为 **预测 − 真实**；隐层仍须乘 $f'(z)$。

**矩阵化**（效率实现）：

$$\boldsymbol{\delta}_{\text{hidden}} = (\boldsymbol{\delta}_{\text{output}}\, \mathbf{W}^T) \odot f'(\mathbf{z}_{\text{hidden}})$$

$\odot$ 为逐元素乘。每 mini-batch 前**梯度清零**；权重小随机初始化，偏置可略负以稳定初期收敛。

（来源：课件08、Week 3、PJ1 Part 1）

---

## Part 4 — 经典案例：XOR 与 NETtalk（Slide 51–60）

### 块 4.1 XOR：单层感知机为何失败

**真值表**：$(0,0)\mapsto 0,\;(1,1)\mapsto 0,\;(0,1)\mapsto 1,\;(1,0)\mapsto 1$。

**2D 几何**：四个点中，输出 1 的两点在对角线位置——**不存在直线**将 $\{0,0),(1,1)\}$ 与 $\{(0,1),(1,0)\}$ 分开 → **线性不可分 Nonlinearly separable**。

**代数**：感知机不等式组关于 $w_1,w_2,t$ **无解**（Minsky & Papert 1969 打击感知机热潮）。

（来源：课件08、Week 2）

### 块 4.2 隐层如何实现非线性

- **特征空间变换**：隐层 + 非线性激活（Sigmoid/ReLU）对输入空间**扭曲、折叠**。
- **升维**：2D 线性不可分 → 映射到高维后可用超平面分开（XOR 经典 2 隐元构造）。
- **逻辑组合**：隐层学简单边界（与/或），输出层叠加得复杂函数。

> **重难点**：没有隐层或非线性激活，多层网络退化为单层线性模型。

（来源：课件08 Part 4、Week 2）

### 块 4.3 NETtalk 案例直觉

**任务**（1987）：神经网络朗读英文文本。

| 设计 | 说明 |
|------|------|
| 滑动窗口 | **7 字符**宽，目标字母居中，利用前后各 3 字上下文决定发音 |
| 隐层 | **80 个神经元**，远小于输入编码维度 → 被迫**特征压缩** |
| 泛化 | 不同单词在隐层可能映射相近模式 → 能处理未见词 |
| 类人行为 | 学习先快后慢；随机损伤权重后**优雅降级**且重学极快 |

（来源：课件08、Week 2–3）

---

## Part 5 — 竞争学习与 WTA（Slide 61–70）

### 块 5.1 Winner-Take-All 机制

**范式**：**无监督学习 Unsupervised Learning**。

1. 输入向量 $\mathbf{X} = (x_1,\ldots,x_n)$ 与各节点权向量 $\mathbf{W}$ 计算**欧氏距离**。
2. **距离最小**（激活最高）者为**胜者 Winner**，输出 1，其余为 0。
3. **仅胜者更新**：$\Delta \mathbf{W} = c\,(\mathbf{X} - \mathbf{W})$，$c$ 为学习率 → 权向量趋近输入**原型 Prototype**。

**应用**：聚类、Kohonen 自组织映射（拓展阅读）。

（来源：课件08 Part 5）

### 块 5.2 WTA vs 感知机 Delta 规则

| 维度 | WTA | 感知机 Delta / BP |
|------|-----|-------------------|
| 范式 | 无监督 | 有监督 |
| 反馈 | 内部竞争，无教师标签 | 外部目标 $d_i$ |
| 目标 | 权向量贴近输入（原型匹配） | 减小输出误差 |
| 激活 | 硬竞争 0/1 | 连续可微（Sigmoid 等） |
| 应用 | 聚类、特征发现 | 分类、回归、BP 网络 |

> **考试提示**：WTA **非期末重点**；课堂展开较少，理解概念即可，复习优先 BP/CNN。

（来源：课件08 Part 5、课程安排说明）

---

## Part 6 — 联结主义擅长任务总结（Slide 71–end）

### 块 6.1 六类任务

| 任务 | 英文 | 说明 |
|------|------|------|
| 分类 | Classification | 判定输入所属类别 |
| 模式识别 | Pattern recognition | 识别数据结构/模式 |
| 记忆召回 | Memory recall | 内容可寻址存储 |
| 预测 | Prediction | 症状→疾病、结果→原因 |
| 优化 | Optimization | 约束下求最佳组织 |
| 噪声过滤 | Noise filtering | 信号与背景分离 |

**共同特征**：感知基础、缺乏明确语法结构 → 符号模型难表达；联结主义擅捕**不变性 Invariances** 与非线性模式。

（来源：课件08 末尾总结）

---

## 重难点解析

### 1. $z$ vs $h$（代码最易混淆）

| 量 | 定义 | BP 中的角色 |
|----|------|-------------|
| $z$ | $\sum w x + b$（净输入） | $\delta$ 定义为 $-\partial L/\partial z$ |
| $h = f(z)$ | 激活后输出 | 作为下一层输入出现在 $\Delta w = \eta\delta h$ |

### 2. 局部极小 vs 鞍点

- **局部极小**：各方向梯度均为正（Hessian 正定）。
- **鞍点**：部分方向极小、部分极大（Hessian 特征值有正有负）。
- **SGD 小批量噪声**有助于逃离鞍点。

### 3. MSE vs Cross-Entropy

- MSE 用于回归；CE+Softmax 用于分类，缓解输出层饱和。
- 输出层 $\delta$ 形式可统一为 $t - y$（配对正确前提下）。

### 4. 梯度下降 vs BP vs BPTT

- 本课件：**BP**（前馈网络）。
- 课件 09 RNN 延伸：**BPTT**（沿时间展开后做 BP）。

（来源：课件08 mistakes 采集、Week 3）

---

## 术语表

| English | 中文 |
|---------|------|
| Connectionism | 联结主义 |
| Hard limiting / Threshold | 硬限幅 / 阈值 |
| Sigmoidal activation | S 型激活函数 |
| Gradient descent | 梯度下降 |
| Mean squared error (MSE) | 均方误差 |
| Backpropagation (BP) | 反向传播 |
| Hidden layer | 隐藏层 |
| Net input ($z$) | 净输入 |
| Sensitivity ($\delta$) | 误差项 / 灵敏度 |
| Nonlinearly separable | 非线性可分 |
| Winner-take-all (WTA) | 胜者全得 |
| Unsupervised learning | 无监督学习 |
| Local minimum / Saddle point | 局部极小 / 鞍点 |
| Credit assignment | 权责分配 |

---

## 复习优先级

| 优先级 | 内容 |
|--------|------|
| **极高** | Part 3 BP 完整推导 + PJ1 Part 1 实现 |
| **高** | Part 2 Sigmoid 导数、MSE、梯度下降；Part 4 XOR 几何解释 |
| **中** | Part 1 符号主义对比；Part 4 NETtalk |
| **了解** | Part 5 WTA；Part 6 任务列表 |

---

**raw**：`notebooklm-raw/ppt08/runs/20260619-171324/`｜**结构**：`notebooklm-raw/ppt/runs/20260619-161000/ppt08-structure.answer.md`
