# Week 12 子主题地图（采集前规划）

> **模块**：Transformer 与大语言模型  
> **来源依据**：`guides/AI课程-14周内容梳理.md` Week 12  
> **衔接**：P6 优化 → **P7 Transformer** → P8 符号主义回归

## 学习顺序与重要程度

| # | Batch ID | 子主题 | 解决什么问题 | 程度 | 拆问策略 |
|---|----------|--------|-------------|------|----------|
| 0 | L0-positioning | 模块定位 | Week12 在 DL 脉络中干什么 | 核心 | 单问 |
| 1 | w12-attention-intuition | 注意力直觉 | Q/K/V 检索模型 | **核心** | 单问类比 |
| 2 | w12-self-attention | Self-Attention | 公式与计算流程 | **核心** | 单问 |
| 3 | w12-transformer-encoder | Encoder 结构 | 双向 MHAttn+FFN+残差+LN | **核心** | 单问 |
| 4 | w12-transformer-decoder | Decoder 结构 | 因果 Attn+交叉 Attn | **核心** | 单问 |
| 5 | w12-pretrain-paradigms | 三种预训练范式 | T5/BERT/GPT 架构差异 | **核心** | 对比表 |
| 6 | w12-gpt-wins | GPT 为何胜出 | KV 缓存、效率、零样本 | **核心** | 单问 |
| 7 | w12-gen-unified | 生成模型统一视角 | VAE/扩散/流/GAN 统一 | 了解 | 单问 |
| 8 | w12-bridge-symbolic | 铺垫符号主义 | 语义网络、框架 | 重要 | 单问 |
| 9 | w12-bridge-w56 | 与 Week5-6 衔接 | 从 HMM/CRF 到 Transformer | 重要 | 单问 |
| 10 | w12-bridge-w13 | 通向 Week13 | DL 黑箱 vs 符号可解释 | 重要 | 单问 |
| 11 | w12-pj2 | PJ2 Transformer | 作业要求（若有） | 重要 | 单问 |
| 12 | w12-mistakes | 易错点 | Encoder/Decoder、BERT/GPT 等 | 重要 | 对比表 |
| 13 | w12-study-order | 复习优先级 | 先掌握什么 | 重要 | 单问 |

## 叙事链

```
Week5-6 序列标注 → Week10 优化 → Week12 注意力统一长程依赖
  → Transformer 编解码 → 预训练范式 → GPT 胜出原因
  → 生成模型统一视角 → 转折：符号主义可解释性（Week13）
```

## 待 L0 校验

Attention Is All You Need 论文是否在 NotebookLM source 中；PJ2 说明是否需并入 batch。
