# Week 8 子主题地图（采集前规划）

> **模块**：深度生成模型（VAE / 扩散 / GAN / 流匹配）  
> **来源依据**：`guides/AI课程-14周内容梳理.md` Week 8  
> **衔接**：P3 序列建模 → P4 CNN 深化 → **P5 生成模型** → P6 优化

## 学习顺序与重要程度

| # | Batch ID | 子主题 | 解决什么问题 | 程度 | 拆问策略 |
|---|----------|--------|-------------|------|----------|
| 0 | L0-positioning | 模块定位 | Week8 在 DL 脉络中干什么 | 核心 | 单问 |
| 1 | w8-generative-goal | 生成模型目标 | 为何学 P(X)、潜在空间 Z | **核心** | 单问 |
| 2 | w8-vae-elbo | VAE 与 ELBO | 变分推断、重构+KL | **核心** | 单问推导 |
| 3 | w8-reparameterization | 重参数化技巧 | 为何能反向传播采样 | 重要 | 单问 |
| 4 | w8-vae-compactness | 紧致性约束 | 为何不能 shortcut | 重要 | 单问直觉 |
| 5 | w8-diffusion | 扩散模型 | 前向加噪+反向去噪 | **核心** | 单问 |
| 6 | w8-flow-matching | 流匹配 | 确定性向量场、保真度权衡 | 了解 | 单问 |
| 7 | w8-gan | GAN 对抗 | 生成器 vs 判别器 | **核心** | 单问 |
| 8 | w8-model-compare | 生成模型对比 | VAE/扩散/GAN/流 各擅什么 | 重要 | 对比表 |
| 9 | w8-bridge-w67 | 与 Week6-7 衔接 | 从判别到生成 | 重要 | 单问 |
| 10 | w8-bridge-w10 | 通向 Week10 | 生成模型训练依赖优化 | 了解 | 单问 |
| 11 | w8-mistakes | 易错点 | ELBO/KL/对抗训练等 | 重要 | 对比表 |
| 12 | w8-study-order | 复习优先级 | 先掌握什么 | 重要 | 单问 |

## 叙事链

```
Week6-7: 序列+CNN 会判别/标注 → 如何「生成」新样本？
  → 生成目标 P(X) → VAE(ELBO+重参数化) → 扩散 → 流匹配 → GAN
  → 对比各范式 → 衔接到 Week10 优化与 Week12 统一视角
```

## 待 L0 校验

跑 `manifests/week8-discovery.json` 后对照 FiCS Week8 记录与课件 09 生成模型章节。
