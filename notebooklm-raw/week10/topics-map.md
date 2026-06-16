# Week 10 子主题地图（采集前规划）

> **模块**：神经网络优化技术  
> **来源依据**：`guides/AI课程-14周内容梳理.md` Week 10  
> **衔接**：P5 生成模型 → **[W9 停课]** → **P6 优化** → P7 Transformer

## 学习顺序与重要程度

| # | Batch ID | 子主题 | 解决什么问题 | 程度 | 拆问策略 |
|---|----------|--------|-------------|------|----------|
| 0 | L0-positioning | 模块定位 | Week10 在训练管线中干什么 | 核心 | 单问 |
| 1 | w10-optimizer-evolution | 优化器演进 | SGD→Momentum→Adam→AdamW | **核心** | 单问 |
| 2 | w10-sgd-momentum | SGD 与 Momentum | 为何需要动量 | 重要 | 单问 |
| 3 | w10-adaptive | Adagrad/RMSprop/Adam | 自适应学习率直觉 | **核心** | 单问 |
| 4 | w10-adamw | AdamW 与正交化 | 解耦权重衰减、矩阵正交化 | 了解 | 单问 |
| 5 | w10-preprocessing | 数据预处理 | 条件数、白化 vs 标准化 | 重要 | 单问 |
| 6 | w10-hessian-geometry | 损失曲面几何 | 海森矩阵与优化难度 | 重要 | 单问 |
| 7 | w10-init-xavier-he | 参数初始化 | Xavier/He 原理 | **核心** | 单问 |
| 8 | w10-batch-norm | Batch Norm | 训练稳定与内部协变量偏移 | **核心** | 单问 |
| 9 | w10-layer-norm | Layer Norm | 与 BN 区别、Transformer 用 LN | 重要 | 单问 |
| 10 | w10-regularization | L2/Dropout/早停 | 如何防过拟合 | **核心** | 单问 |
| 11 | w10-hyperparams | 超参数 | lr 衰减、Batch Size 关系 | 重要 | 单问 |
| 12 | w10-bridge-w8 | 与 Week8 衔接 | 生成模型训练如何用优化器 | 了解 | 单问 |
| 13 | w10-bridge-w12 | 通向 Week12 | 大模型训练依赖哪些技巧 | 重要 | 单问 |
| 14 | w10-mistakes | 易错点 | BN/LN、Adam vs SGD 等 | 重要 | 对比表 |
| 15 | w10-study-order | 复习优先级 | 先掌握什么 | 重要 | 单问 |

## 叙事链

```
Week8 生成模型需要稳定训练 → Week10 系统讲优化
  → 优化器族 → 预处理/曲面 → 初始化 → BN/LN → 正则 → 超参
  → 为 Week12 Transformer 大规模训练铺路
```

## 待 L0 校验

PJ2 GPU 提醒是否在记录中单独成节——以 NotebookLM 为准。
