# Week 1–2 子主题地图（采集前规划）

> **模块**：AI 概述 + 感知机/MLP 基础  
> **来源依据**：`guides/AI课程-14周内容梳理.md` Week 1–2  
> **说明**：指南已定稿；本表供补采 raw 时对照。现有 manifest 为 4 batch 粗粒度版，可按 L0 发现结果拆细。

## 学习顺序与重要程度

| # | Batch ID | 子主题 | 解决什么问题 | 程度 | 拆问策略 |
|---|----------|--------|-------------|------|----------|
| 0 | L0-positioning | 模块定位 | Week1-2 在整门课中干什么 | 核心 | 单问 |
| 1 | w1-three-schools | 三大流派 | 符号/连接/进化各是什么 | **核心** | 单问 + 类比 |
| 2 | w1-turing-test | 图灵测试 | 如何评估智能、局限在哪 | 重要 | 单问 |
| 3 | w1-connectionist-history | 连接主义史 | MP→感知机→DL 里程碑 | 重要 | 单问 |
| 4 | w1-course-setup | 课程与 Project | 考核比例、手写实现要求 | 了解 | 单问 |
| 5 | w2-perceptron-xor | 感知机与 XOR | 单层为何不够 | **核心** | 单问 |
| 6 | w2-activation-sigmoid | 激活函数 | 阶跃→Sigmoid 为何可微 | 重要 | 单问 |
| 7 | w2-normal-equation | 正规方程 | 线性模型解析解、伪逆 | **核心** | 单问 |
| 8 | w2-mlp-structure | MLP 结构 | 深度/宽度/对称性 | 核心 | 单问 |
| 9 | w2-convex-nonconvex | 凸 vs 非凸 | NN 损失为何非凸 | 重要 | 单问 |
| 10 | w2-gd-basics | 梯度下降基础 | 泰勒一阶、学习率、鞍点 | **核心** | 单问 |
| 11 | w2-minibatch | Mini-batch SGD | 实践训练怎么采样 | 重要 | 单问 |
| 12 | w12-bridge | 通向 Week3 | MLP 有了，怎么训练？ | 重要 | 单问 |
| 13 | w12-mistakes | 易错点 | 正规方程/非凸/激活等 | 重要 | 对比表 |
| 14 | w12-study-order | 复习优先级 | 先掌握什么 | 重要 | 单问 |

## 叙事链

```
Week1: 什么是 AI？三大流派 → 图灵测试 → 连接主义历史 → 课程要求
Week2: 感知机不够 → 激活函数 → 线性模型回顾 → MLP → 非凸与 GD → Mini-batch
  → 自然引出 Week3 反向传播
```

## 待 L0 校验

认证恢复后可跑 `manifests/week1-2-discovery.json`，对比 NotebookLM 子主题清单与本表。
