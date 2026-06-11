# Week 7 知识图谱（CNN 数学与实现深化）

> **Canonical run**：`runs/20260612-015756/`（13/13）  
> **指南落点**：`guides/AI-Week3-4-学习指南.md` §2.3  
> **前置**：Week 4 §2.2 K–N

## 叙事链

```
Week4: CNN 直觉（局部连接、权重共享、池化、LeNet 骨架）
  → Week7: LTI/离散卷积 → 互相关 vs 卷积 → 经典核 → 填充
       → 多通道参数量 → Sigmoid/ReLU/BN → 池化细节 → LeNet/互相关手算
  → Week8+: 卷积编码器为 VAE 等生成模型铺垫；局部性局限引向 Transformer
```

## Raw → 指南映射

| Batch | 指南节 | 要点 |
|-------|--------|------|
| `L0-positioning` | O | Week7=数学+工程；Week4→7 概览→深化；Week8 编码器、Transformer 动机 |
| `w7-lti-discrete-conv` | P | LTI、y[n]=Σx[m]h[n-m]、翻转与交换律、二维推广 |
| `w7-cross-correlation` | Q | PyTorch=互相关；学习等价、工程省事 |
| `w7-classic-kernels` | R | 8 中心边缘核、1/9 模糊、5 中心锐化 |
| `w7-padding` | R | 保尺寸+边缘公平；P=(K-1)/2；32×32 K=5 P=2 |
| `w7-multichannel` | S | 三维核、跨通道求和；RGB→64 核 4864 参 |
| `w7-relu-bn` | T | Sigmoid 之字形；ReLU 仍非零中心；BN 按通道归一化 |
| `w7-pooling-detail` | U | 无填充、S=K；最大池化=逻辑或；等变 vs 局部不变 |
| `w7-lenet-numeric` | U | 32→28→14 手算 |
| `w7-conv-numeric` | U 附录 | 3×3 输入 2×2 核互相关手算 |
| `w7-w47-bridge` | O | 感受野、等变性、池化强先验 |
| `w7-mistakes` | §3 | 卷积/互相关、通道/特征图、参数量/FLOPs 等 |
| `w7-study-order` | §4.3 | LeNet 尺寸、多通道参数、激活、等变/不变 |

## 与课纲一致性

- FiCS Week 7 主线已覆盖；PJ2 提及在 L0，指南正文不展开作业细节
- Week 10 将深化 BN/Dropout，§2.3 T 节仅入门
