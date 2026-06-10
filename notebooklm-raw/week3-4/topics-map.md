# Week 3–4 子主题地图（Agent 预拆分，待 NotebookLM L0 校验）

> **模块**：反向传播 + CNN + PJ1  
> **原则**：一次 chat 只专注一个问题；`clear_conversation: true` 于每个 batch  
> **来源依据**：`guides/AI课程-14周内容梳理.md` Week 3–4 + Week 1–2 衔接

## 学习顺序与重要程度

| # | Batch ID | 子主题 | 解决什么问题 | 程度 | 拆问策略 |
|---|----------|--------|-------------|------|----------|
| 0 | L0-positioning | 模块定位 | Week3-4 在课程/PJ1 中干什么 | 核心 | 单问 |
| 1 | w3-gd-taylor | 梯度下降理论 | 为什么用小学习率、泰勒一阶 | 重要 | 单问 L1→L2 |
| 2 | w3-z-vs-h | 净输入 vs 激活值 | 写 BP 代码时区分 z 和 h | 核心 | 单问 + 后续可补数值 |
| 3 | w3-bp-regression | 回归 BP | MSE + $\delta_k=y_k-t_k$ 怎么来 | **核心** | 单问推导 |
| 4 | w3-bp-softmax-ce | 分类 BP | Softmax+CE 为何也是 $y_k-t_k$ | **核心** | 单问推导（复杂，不与其他合并） |
| 5 | w3-bp-hidden | 隐层误差传递 | $\delta_j$ 怎么从输出层传回来 | **核心** | 单问 |
| 6 | w3-training-loop | 训练流程 | 一个 iteration 做哪些步骤 | 重要 | 单问 |
| 7 | w3-bp-numeric | BP 数值例子 | 手算一小网络验证 BP | **核心** | L3 专问，要数值 |
| 8 | w4-pj1-overview | PJ1 要求 | Part1/Part2 各要什么 | 重要 | 单问 |
| 9 | w4-dl-history | DL 历史 | Hopfield/RBM/预训练为何过时 | 了解 | 普通深度即可 |
| 10 | w4-relu-resnet | 梯度消失与 ReLU | 为什么需要 ReLU/ResNet | 重要 | 单问 |
| 11 | w4-cnn-motivation | CNN 动机 | 为何不全连接处理图像 | 重要 | 单问直觉 |
| 12 | w4-conv-params | 卷积参数 | 核/步长/填充/通道 | **核心** | 单问 + 后续数值 |
| 13 | w4-pooling | 池化 | 最大池化做什么、BP 怎么传 | 重要 | 单问 |
| 14 | w4-feature-hierarchy | 特征层级 | 边缘→纹理→语义 | 了解 | 普通深度 |
| 15 | w4-conv-numeric | 卷积数值例子 | 手算 tiny conv | 重要 | L3 专问 |
| 16 | w34-bridge | 与 Week1-2 衔接 | 从 MLP 到 BP/CNN | 重要 | 单问 |
| 17 | w34-pj1-map | 知识点→PJ1 任务 | 每周知识对应哪道题 | 重要 | 单问 |
| 18 | w34-mistakes | 易错点 | 净输入/δ/池化梯度等 | 重要 | 对比表单问 |
| 19 | w34-study-order | 复习优先级 | 先掌握什么 | 重要 | 单问 |

## 叙事链（整合指南时用）

```
Week1-2: MLP 需要训练 → 怎么算梯度？
  → w3: 梯度下降基础 → z/h → 回归BP → 分类BP → 隐层δ → 训练循环 → 数值验证
Week3 能训练 MLP 了 → 图像怎么办？PJ1 Part2？
  → w4: PJ1 → DL史/ReLU → CNN动机 → 卷积参数 → 池化 → 特征层级 → 数值
  → 串联 Week1-2、映射 PJ1、易错点
```

## 待 L0 发现校验

认证恢复后先跑：

```bash
python scripts/nlm-collect.py notebooklm-raw/manifests/week3-4-discovery.json
```

对比 `L0-subtopic-map.answer.md` 与本表，增删 batch 后再跑完整 manifest。
