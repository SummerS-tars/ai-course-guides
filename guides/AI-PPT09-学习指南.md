# 课件 09 — Deep Learning 学习指南

> **课件**：`09DeepLearning.pdf`｜NotebookLM `课件09-DeepLearning`  
> **原则**：按课件原序、按知识点分块、**课件板块无遗漏**  
> **课堂**：Week 4–12 贯穿；Week 12 Transformer 课堂讲授（**课件 09 无详页**，见附录 X）  
> **项目**：**Project 1 Part 2**（手写 CNN）；GAN **不考核**  
> **术语**：**中文（English）**

---

## 课件内容覆盖索引

| 课件原序 | 课件板块 | Slide（约） | 本指南 |
|----------|----------|-------------|--------|
| 1 | 引言与动机（Questions & Motivation） | 1–15 | Part 0 · 块 0.1–0.2 |
| 2 | 表示学习（AE / DBN / RBM） | 1–15 | Part I · 块 I.1–I.3 |
| 3 | 优化与数学基础（曲线拟合、卷积定义） | 穿插 | Part II 前导；Part VI |
| 4 | 卷积神经网络 CNN | 16–35 | Part II · 块 II.1–II.4 ⭐ |
| 5 | 序列建模与 NLP（分词、HMM、CRF） | 36–60 | Part III · 块 III.1–III.3 ⭐ |
| 6 | 词嵌入 Word2Vec | 60–75 | Part III · 块 III.4 |
| 7 | 循环神经网络 RNN / LSTM / GRU | 76–95 | Part IV · 块 IV.1–IV.4 |
| 8 | 生成对抗网络 GAN | 96–105 | Part V · 块 V.1 ⚠️不考核 |
| 9 | 多模态与对抗样本 | 穿插后期 | Part VII · 块 VII.1–VII.2 |
| 10 | 硬件与类脑计算 | 末尾 | Part VIII · 块 VIII.1 |
| 11 | 优化技巧（BN、Dropout、SGD/Adam） | 106–end | Part VI · 块 VI.1–VI.3 ⭐ |
| — | *课件无详页，Week 12 课堂* | — | **附录 X** Transformer 缺口补充 |

---

## Part 0 — 深度学习动机（Slide 1–15）

### 块 0.1 为何需要深度学习

**课件核心问题**：浅层模型够吗？为何要「深」？

| 动机 | 说明 |
|------|------|
| 人工特征瓶颈 | 传统 ML（SVM 等）依赖**手工特征 Hand-crafted features**，需领域专家数十年积累 |
| 层次化表征 | 复杂任务（图像、语音）需**组合低层特征成高层特征**（边缘→纹理→部件→语义） |
| 特征重用指数增长 | 深层结构可指数级增加特征组合方式（课件：Representation is very, very, very important!） |
| 维数灾难缓解 | **分布式表示 Distributed Representation** 用较少参数覆盖大量模式，泛化强于局部模板 |

**浅 vs 深**：

```text
浅层：手工特征 → 单一分类器
深层：原始数据 → 多层可学习变换 → 任务输出（端到端）
```

（来源：课件09 前期、Week 4）

### 块 0.2 深度学习史脉络（与课件 08 衔接）

```text
Sigmoid 深层 → 梯度消失 → RBM 逐层预训练(2006) → ReLU/ResNet/BN → 端到端 BP 主流
     ↑                              ↑
  课件08 BP                     Part I RBM/DBN
```

- 详细 BP 数学推导见 **`guides/AI-PPT08-学习指南.md` Part 3**。
- 本课件侧重**应用与架构**；损失函数 MSE vs CE 对比见 PJ1 与课件 08。

（来源：课件09、Week 4、课件08）

---

## Part I — 表示学习（Slide 1–15）

### 块 I.1 表示学习 Representation Learning

**核心思想**：让模型**自动从数据中发现特征**，替代繁琐特征工程。

- **层次结构 Hierarchy**：低层（边缘）→ 中层（形状）→ 高层（语义）。
- **鲁棒性 Robustness**：好的表示使下游分类器压力减小、性能跃升。
- **与分类解耦**：先学 $Z = \text{encode}(X)$，再学 $Y = f(Z)$。

（来源：课件09 Part I、Week 4–6）

### 块 I.2 自编码器 Autoencoder（AE）

**结构**：编码器 $X \to Z$ + 解码器 $Z \to \hat{X}$，最小化重构误差。

| 要点 | 说明 |
|------|------|
| 瓶颈层 | 隐层维度 < 输入 → 被迫学习压缩表征 |
| 与 VAE 区别 | 普通 AE 仅重构，无 KL 约束 → 不一定能生成新样本（Week 8 拓展） |
| 考试定位 | 理解「无监督学表示」概念；细节以 RBM 预训练史为主 |

（来源：课件09 结构图、Week 4/8）

### 块 I.3 RBM 与 DBN 无监督预训练的历史地位

**RBM（Restricted Boltzmann Machine，受限玻尔兹曼机）**

- 层内无连接、层间全连接的双向随机网络。
- 可见层 ↔ 隐层能量模型，可用对比散度（CD）等无监督训练。

**DBN（Deep Belief Network，深度信念网络）**

- 多层 RBM 堆叠；**逐层贪心无监督预训练 Greedy layer-wise pre-training**（Hinton 2006）。
- 将参数初始化在**吸引盆 Basins of attraction** 附近，缓解梯度消失与局部最优，具正则化效果。

**历史地位 vs 现状**

| 时期 | 做法 |
|------|------|
| 2006–约2012 | RBM 预训练 → 有监督微调，深度学习复兴标志 |
| 现今 | ReLU、ResNet、Xavier/He 初始化、Batch Norm → **端到端 BP** 为主，预训练已少见 |

> **考试**：RBM/DBN 常作「深层网络如何突破训练瓶颈」的典型案例，体现分层抽象思想。

（来源：课件09 Part I、Week 4）

---

## Part II — 卷积神经网络 CNN（Slide 16–35）⭐

### 块 II.1 CNN 三大核心特性

| 特性 | 英文 | 原理 | 作用 |
|------|------|------|------|
| 局部连接 | Local connectivity | 每单元仅连感受野内像素 | 尊重空间局部性；参数量从 $O(n^2)$ 降至 $O(l \cdot n)$ |
| 权重共享 | Weight sharing | 同一特征图共享卷积核 | 检测不同位置相同模式；极大减参 |
| 平移等变/不变 | Translation equivariance / invariance | 卷积等变 + 池化不变 | 物体微移时特征稳健 |

**生物启发**：视觉皮层感受野机制。

（来源：课件09 Part II、Week 4/7）

### 块 II.2 卷积参数与输出尺寸公式

**核心参数**

| 参数 | 符号 | 说明 |
|------|------|------|
| 卷积核 | $K$ | 检测边缘/纹理等的权重矩阵 |
| 步长 | $S$ | 核滑动步距；$S$ 越大输出越小 |
| 填充 | $P$ | 边缘补零；Same Padding 可保持尺寸 |
| 通道 | $C_{in}, C_{out}$ | 输入通道（RGB=3）；核深度=$C_{in}$；核数量=$C_{out}$ |

**输出尺寸**：

$$O = \left\lfloor \frac{I - K + 2P}{S} \right\rfloor + 1$$

**参数量**：

$$\text{Params} = (C_{in} \times K \times K + 1) \times C_{out}$$

（$+1$ 为偏置）

> **重难点**：PJ1 Part 2 须逐层手算 Tensor 尺寸，确保 Flatten 后维度匹配全连接层。

（来源：课件09、Week 7、PJ1 Part 2）

### 块 II.3 卷积 vs 互相关

| 操作 | 定义 | 深度学习实践 |
|------|------|--------------|
| **卷积 Convolution** | 核需**翻转**再滑动：$y[n]=\sum x[m]h[n-m]$ | 数学信号处理严格定义 |
| **互相关 Cross-correlation** | 对应位置直接相乘求和 | **框架 `Conv2d` 实际多实现互相关**（核可学习，翻转等价） |

（来源：课件09、Week 7、Goodfellow 花书）

### 块 II.4 池化与 LeNet-5

**池化 Pooling**：无参数下采样。

| 类型 | 特点 |
|------|------|
| 最大池化 Max Pooling | 取窗口最大值，保留显著特征（最常用） |
| 平均池化 Average Pooling | 平滑，可能淡化显著特征 |

**LeNet-5 结构**（手写数字 MNIST）：

| 层 | 配置 | 输出尺寸（32×32 输入） |
|----|------|------------------------|
| Input | 灰度 | $32\times32$ |
| C1 | $5\times5$ 卷积, $S=1$, 6 核 | $6\times28\times28$ |
| S2 | $2\times2$ 池化, $S=2$ | $6\times14\times14$ |
| C3 | 卷积 | $16\times10\times10$ |
| S4 | 池化 | $16\times5\times5$ |
| C5/F6/Output | 全连接 + 分类 | 10 类 |

**层级直觉**：卷积提特征（线→形），池化降维；越深特征越抽象。

**PJ1 Part 2 实践**：手动组合 `nn.Conv2d` + `nn.MaxPool2d`（**禁止**直接调用 `torchvision.models`）；归一化到 $[0,1]$ 或 $[-1,1]$；Bonus 可加 Dropout/BN/数据增强。

（来源：课件09、Week 4/7、PJ1）

---

## Part III — 序列建模、HMM/CRF 与 Word2Vec（Slide 36–75）⭐

### 块 III.1 中文分词与序列标注背景

**课件语境**：NLP 许多任务可建模为**序列标注**（分词、词性、命名实体）。

- 中文无天然空格 → 分词是首要步骤。
- 传统方法：HMM、CRF 等概率图模型（深度学习时代仍作理解基础）。

（来源：课件09 Part III、Week 5）

### 块 III.2 HMM 五元组与三问题

**五元组** $\lambda = (S, K, \Pi, A, B)$：

| 符号 | 含义 |
|------|------|
| $S = \{S_1,\ldots,S_N\}$ | 隐藏状态集合 |
| $K = \{K_1,\ldots,K_M\}$ | 观察符号集合 |
| $\Pi$ | 初始状态概率 |
| $A$ | 状态转移矩阵 $a_{ij} = P(S_j \mid S_i)$ |
| $B$ | 发射概率 $b_{ijk}$：状态下生成观察符号的概率 |

**三个基本问题**：

| 问题 | 英文 | 任务 |
|------|------|------|
| 评估 | Evaluation | 给定 $\lambda, O$，求 $P(O \mid \lambda)$ |
| 解码 | Decoding | 给定 $O, \lambda$，求最优隐藏序列 $X$（Viterbi） |
| 学习 | Learning | 给定 $O$，调整 $\lambda$ 最大化 $P(O \mid \lambda)$ |

**前向算法直觉**（评估问题）：

- 动态规划在**栅栏图 Trellis** 上递推，避免穷举路径的指数爆炸。
- 前向变量 $\alpha_i(t)$：「观察到前 $t$ 个符号且当前在状态 $i$」的联合概率。
- 复杂度 $O(N^2 T)$。

（来源：课件09 Part III、Week 5）

### 块 III.3 CRF vs HMM

| 维度 | HMM | CRF |
|------|-----|-----|
| 模型类型 | **生成式** $P(X,Y)$ | **判别式** $P(Y \mid X)$ |
| 归一化 | **局部归一化** → **标注偏置 Label Bias** | **全局归一化** $Z(X)$，消除偏置 |
| 特征 | 仅当前+前一状态（马尔可夫） | 任意**特征模板**（当前字、前后字、词性等） |
| 局限 | 独立性假设强，长程依赖弱 | 特征工程繁琐，特征空间易爆炸 |
| 解码 | Viterbi | Viterbi（在全局得分上） |

> **重难点**：课件中 **CRF 特征模板** 讲解较多——复习须能举例「当前词+前一词+后一词」类模板。

（来源：课件09 Part III、Week 5–6）

### 块 III.4 Word2Vec：CBOW 与 Skip-gram

**核心直觉**：「通过上下文推断词义」→ 离散符号 → 低维稠密**词嵌入 Word Embedding**。

| 模型 | 输入 → 输出 | 直觉 | 特点 |
|------|-------------|------|------|
| **CBOW** | 上下文词 → **中心词** | 完形填空；上下文向量求和/平均 | 训练快；忽略语序 |
| **Skip-gram** | **中心词** → 上下文词 | 「苹果」周围易出现「吃、红、甜」 | 大语料、生僻词表现常更好 |

**向量运算**：$king - man + woman \approx queen$（分布式语义假设）。

（来源：课件09 Part III、Week 6）

---

## Part IV — RNN / LSTM / GRU（Slide 76–95）

### 块 IV.1 RNN 基础与展开

**适用**：序列数据（文本、语音、时间序列）。

- **循环连接**：隐藏状态 $h_t$ 携带历史信息。
- **展开 Unfolding**：按时间步展开成链，**各步共享权重** $U, V, W$。
- **马尔可夫假设**：$h_t$ 理论上压缩了此前全部输入（实际受梯度问题限制）。

（来源：课件09 Part IV）

### 块 IV.2 BPTT 与梯度消失/爆炸

**BPTT（Back-Propagation Through Time，随时间反向传播）**

- 将 RNN 展开后做标准 BP，误差沿时间轴反向传播。

**梯度消失/爆炸**

- 因 $W$ 在时间步上**重复相乘**，梯度含 $W^n$。
- $|W|$ 特征值 $<1$ → **梯度消失**（难学长程依赖）；$>1$ → **梯度爆炸**。
- **对策**：梯度裁剪 Gradient Clipping（爆炸）；LSTM/GRU 门控（消失）。

（来源：课件09 Part IV、Week 5–6）

### 块 IV.3 LSTM 三门机制

**组件**：**细胞状态 Cell state** $c_t$（长期记忆）+ 三个门（sigmoid 输出 0–1）。

| 门 | 符号 | 功能 |
|----|------|------|
| 遗忘门 | $f_t$ | 决定 $c_{t-1}$ 多少保留 |
| 输入门 | $i_t$ | 决定新信息多少写入 $c_t$ |
| 输出门 | $o_t$ | 决定 $c_t$ 多少输出为 $h_t$ |

**拓扑文字版**：

```text
c_{t-1} ──×f_t──┐
                ├──⊕──→ c_t ──tanh──×o_t──→ h_t
候选值──×i_t───┘
输入: x_t, h_{t-1}
```

- $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$（$\tilde{c}_t$ 为候选值，$\tanh$ 输出）。
- $h_t = o_t \odot \tanh(c_t)$。

> **重难点**：须对照课件拓扑图理解 $\otimes$（逐元素乘）与 $\oplus$（逐元素加）。

（来源：课件09 Part IV、Week 5）

### 块 IV.4 GRU 简化直觉

| 对比 | LSTM | GRU |
|------|------|-----|
| 门数量 | 3 门 + 独立细胞状态 | **更新门** $z_t$（合并遗忘+输入）+ **重置门** $r_t$ |
| 输出门 | 有 | 无（$h_t$ 直接由 $c_t$ 导出） |
| 参数量 | 较多 | 较少，部分任务性能相当 |

（来源：课件09 Part IV）

---

## Part V — 生成对抗网络 GAN（Slide 96–105）⚠️

### 块 V.1 生成器与判别器对抗

| 角色 | 职责 | 比喻 |
|------|------|------|
| **生成器 G** | 噪声 → 假样本，骗过 D | 伪造者 |
| **判别器 D** | 判真伪 $P(\text{real})$ | 警察 |

**对抗过程**：零和博弈，双方共同进化；理想均衡：$G$ 生成分布 $\approx$ 真实分布，$D$ 无法优于随机猜测。

> ⚠️ **本课程不考核**：Week 13 明确「深度生成模型」不作考试内容，仅供拓展阅读。复习时间应让给 CNN、CRF、优化、Transformer 补充。

（来源：课件09 Part V、Week 13）

---

## Part VI — 优化与泛化（Slide 106–end）⭐

### 块 VI.1 优化算法演进：SGD → Momentum → Adam

| 算法 | 核心机制 | 优势 | 缺点 |
|------|----------|------|------|
| **SGD** | 沿 mini-batch 梯度反方向更新 | 简单，基线 | 峡谷曲面震荡、收敛慢 |
| **Momentum** | 指数加权累积历史梯度（惯性） | 抑制震荡、加速 | 额外超参（动量系数） |
| **Adam** | 一阶矩（Momentum）+ 二阶矩（RMSprop）自适应学习率 | 鲁棒，Transformer 常用 | 部分任务泛化不如调优 SGD |

（来源：课件09 Part VI、Week 10）

### 块 VI.2 初始化与归一化

| 技术 | 适用 | 核心思想 |
|------|------|----------|
| **Xavier** | Sigmoid / Tanh | 保持各层输出方差 ≈ 输入方差 |
| **He (Kaiming)** | ReLU | 补偿 ReLU 置零导致的方差减半，$Var(w)=2/n_{in}$ |
| **Batch Norm (BN)** | CNN 等 | 对 mini-batch 激活做标准化（零均值单位方差）；常置于线性层后、激活前 |
| **Layer Norm (LN)** | RNN / Transformer | 单样本内所有特征维度归一化，不依赖 batch 大小 |

**BN 效果**：缓解内部协变量偏移、平滑损失曲面、具轻微正则化；小 batch 时统计不稳。

（来源：课件09 Part VI、Week 10/12）

### 块 VI.3 正则化：L2、Dropout、早停

| 方法 | 操作 | 原理 |
|------|------|------|
| **L2 正则 / 权重衰减** | 损失 $+\lambda \sum w^2$ | 惩罚大权重，降低曲率；**偏置通常不正则** |
| **Dropout** | 训练时以概率 $p$ 置零神经元 | 打破协同适应，类似 Bagging；测试时全开启（Inverted Dropout 训练时除以 $1-p$） |
| **早停 Early Stopping** | 验证集损失不再下降则停 | 限制有效迭代次数；二次代价下等价 L2 |

（来源：课件09 Part VI、Week 10、Goodfellow 花书）

---

## Part VII — 多模态与对抗样本

### 块 VII.1 多模态学习 Multi-modal

**课件要点**：融合多种信息源（语音、文本、图像、情感）。

| 方向 | 课件/课堂涉及 |
|------|---------------|
| 语音 + 文本 | 语音识别、情感分析等联合建模 |
| Audio Words 等 | 课件提及具体模型参数，**课堂略讲** |
| 与单模态 CNN/RNN 关系 | 各模态先编码，再融合（拼接/注意力等，Transformer 时代更常见） |

> **考试定位**：了解「多源信息融合」动机即可；细节以 CNN/RNN/Attention 为主。

（来源：课件09 结构、课堂记录）

### 块 VII.2 对抗样本 Adversarial Examples

**定义**：对输入加**人眼难察觉的微小扰动**，使模型高置信度误判。

| 概念 | 说明 |
|------|------|
| vs GAN「对抗」 | **对抗样本** = 攻击输入；**GAN** = 训练时 G/D 博弈机制（不同含义） |
| 安全意义 | 自动驾驶标志识别、人脸识别等脆弱性 |
| 对抗训练 | 将对抗样本加入训练提升鲁棒性（拓展） |

（来源：课件09、Week 8）

---

## Part VIII — 硬件与类脑计算

### 块 VIII.1 IBM TrueNorth 与神经形态芯片

**课件要点**：

| 主题 | 内容 |
|------|------|
| **TrueNorth** | IBM 神经形态芯片：模拟神经元脉冲事件驱动，低功耗并行 |
| **动机** | 传统冯·诺依曼架构下 AI 计算能耗高；脑启发硬件可望突破能效瓶颈 |
| **计算神经科学** | 课件末尾展望：硬件与算法协同设计 |

> **考试定位**：了解级；课堂对 TrueNorth 细节**未深入展开**。复习优先软件算法。

（来源：课件09 末尾、结构梳理）

---

## 附录 X — 课件 09 无详页：Transformer 缺口补充（Week 12）

> ⚠️ **重要**：**课件 09 PDF 内无 Transformer 结构详页**；以下内容来自 **Week 12 课堂**与参考书，开卷/期末可能涉及。

### 块 X.1 为何需要 Transformer

| 架构 | 瓶颈 | Transformer 突破 |
|------|------|------------------|
| RNN | 顺序计算、长程梯度消失、难并行 | **Self-Attention** 一步检索全序列 |
| CNN | 局部感受野，长程依赖需堆深层 | 全局注意力，距离不是障碍（代价 $O(n^2)$） |

（来源：Week 12、课件09 supplement）

### 块 X.2 Self-Attention：Q / K / V

**直觉（图书馆检索）**：

| 向量 | 角色 |
|------|------|
| **Query Q** | 当前位置「想查什么」 |
| **Key K** | 各位置「能提供什么索引」 |
| **Value V** | 索引对应的「真实内容」 |

**Scaled Dot-Product Attention**：

$$\text{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^T}{\sqrt{d}}\right) V$$

- $\sqrt{d}$：防止点积过大导致 softmax 饱和。
- **多头注意力 MHAttn**：多组 $W_Q,W_K,W_V$ 并行，拼接后再投影。

（来源：Week 12、`ppt09-supplement-transformer`）

### 块 X.3 Encoder-Decoder 结构

| 模块 | 注意力类型 | 说明 |
|------|------------|------|
| **Encoder** | 双向 Self-Attention | 输入全序列可见，融合上下文 |
| **Decoder** | Masked Self-Attention（因果） | 只能看已生成 token |
| **Decoder** | **Cross-Attention** | Q 来自 Decoder，K/V 来自 Encoder（翻译时「查原文」） |

子层标配：**残差连接 + Layer Norm**。

（来源：Week 12）

### 块 X.4 预训练范式：BERT vs GPT vs 联合训练

| 范式 | 代表 | 结构 | 擅长 | 局限 |
|------|------|------|------|------|
| Encoder-only | **BERT** | 双向注意力 | 理解（分类、NER、情感） | 不直接生成 |
| Decoder-only | **GPT** | 因果注意力 | 生成、零样本泛化 | 双向上下文弱 |
| Encoder-Decoder | **T5, BART** | 完整结构 | 翻译、摘要等 seq2seq | 大模型时代竞争力弱于 GPT 范式 |

**GPT 范式胜出原因（课堂总结）**：

1. 因果注意力下 K/V **可缓存**，生成效率高。
2. 「预测下一词」与下游生成任务一致。
3. 规模化后**零样本 Zero-shot** 能力强。

（来源：Week 12、`ppt09-supplement-transformer`）

---

## 重难点解析

### 1. 卷积 vs 互相关

深度学习 `Conv2d` 多实现互相关；理解信号处理考试可能考翻转定义。

### 2. HMM vs CRF vs 神经网络

```text
HMM（生成式，局部归一化）→ CRF（判别式，全局特征）→ BiLSTM-CRF / Transformer（端到端）
```

### 3. 梯度消失的两条战线

| 场景 | 原因 | 对策 |
|------|------|------|
| 深层前馈 Sigmoid | $f' \leq 0.25$ 连乘 | ReLU、ResNet、BN |
| RNN 长序列 | $W^n$ 连乘 | LSTM/GRU、梯度裁剪 |

### 4. BN vs LN 选型

- **CNN + 固定尺寸 batch** → BN 常见。
- **RNN / Transformer / 小 batch / 变长序列** → LN 更稳。

### 5. GAN「对抗」vs 对抗样本

前者是训练架构；后者是安全攻击——**勿混淆**。

### 6. BP 推导不在本课件

回 **`AI-PPT08-学习指南.md` Part 3**；本课件假设已掌握 BP，讲应用层。

（来源：课件09 mistakes 采集）

---

## 术语表

| English | 中文 |
|---------|------|
| Representation learning | 表示学习 |
| RBM / DBN | 受限玻尔兹曼机 / 深度信念网络 |
| Feature map | 特征图 |
| Pooling | 池化 |
| Cross-correlation | 互相关 |
| HMM | 隐马尔可夫模型 |
| CRF | 条件随机场 |
| Label bias | 标注偏置 |
| Word embedding | 词嵌入 |
| BPTT | 随时间反向传播 |
| Vanishing / Exploding gradient | 梯度消失 / 爆炸 |
| LSTM / GRU | 长短期记忆 / 门控循环单元 |
| GAN | 生成对抗网络 |
| Batch Norm / Layer Norm | 批量归一化 / 层归一化 |
| Dropout | 随机失活 |
| Adversarial example | 对抗样本 |
| Self-Attention | 自注意力 |
| Multi-Head Attention | 多头注意力 |

---

## 复习优先级

| 优先级 | 内容 |
|--------|------|
| **极高** | Part II CNN（公式、LeNet、PJ1 Part 2）；Part III HMM/CRF/Word2Vec；Part VI 优化 |
| **高** | Part IV RNN/LSTM/BPTT；附录 X Transformer（课件无详页） |
| **中** | Part I 表示学习/RBM 史；Part 0 动机；Part VII 对抗样本 |
| **了解** | Part V GAN（**不考核**）；Part VII 多模态；Part VIII 硬件 |

---

**raw**：`notebooklm-raw/ppt09/runs/20260619-172048/`（含 `ppt09-supplement-transformer`）｜**结构**：`notebooklm-raw/ppt/runs/20260619-161000/ppt09-structure.answer.md`
