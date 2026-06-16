根据 **Week 10** 和 **Week 12** 的课程笔记及相关参考资料，Transformer 的大规模训练主要依赖于以下在 Week 10 中详细讨论的优化、正则化与归一化技术：

### 1. 优化算法 (Optimization)
*   **Adam 与 AdamW 优化器**：Transformer 模型的训练高度依赖 **Adam** 算法，它结合了动量法（一阶矩）和 RMSprop（二阶矩）的优势 [1]。特别是 **AdamW**，它将权重衰减（Weight Decay）从梯度更新中解耦，解决了标准 Adam 在正则化效果上的扭曲问题，是目前大规模模型训练中最常用的优化器之一 [1]。
*   **梯度裁剪 (Gradient Clipping)**：为了防止深层网络训练中出现的梯度爆炸问题，Transformer 依赖 **按模长裁剪（Clip by Norm）** 的技术。这种方法能保持梯度方向不变，仅缩放步长，避免破坏梯度方向信息 [2]。
*   **学习率衰减 (Learning Rate Decay)**：由于 Transformer 参数量巨大且训练后期梯度噪声增加，需要配合 Week 10 提到的学习率动态衰减策略，以保证模型最终收敛 [3]。

### 2. 正则化技术 (Regularization)
*   **随机失活 (Dropout)**：Transformer 架构在多头注意力层和前馈网络层中广泛使用 Dropout。Week 10 强调了 **Inverted Dropout** 的使用，即在训练时通过除以 $1-p$ 进行缩放，以保持训练与推理时信号强度的一致性 [4]。
*   **标签平滑 (Label Smoothing)**：在处理大规模分类（如机器翻译中的词表预测）时，使用标签平滑防止模型过度自信（Overconfidence），从而显著提高模型的泛化能力 [4, 5]。
*   **权重衰减 (Weight Decay / L2 正则化)**：通过在损失函数中增加参数平方项来限制模型复杂度，配合 AdamW 确保正则化在自适应学习率下的有效性 [1, 2]。

### 3. 归一化技术 (Normalization)
*   **归一化原理与层归一化 (Layer Normalization)**：虽然 Week 10 重点讲解了批量归一化（Batch Normalization），但其核心在于揭示了 **归一化能够解决内部协变量偏移（Internal Covariate Shift）** 并在数学上平滑损失函数景观（Loss Landscape）的原理 [1, 6]。Transformer 模型正是基于此理论，在每个子层（如注意力层和前馈层）之后采用了 **层归一化 (Layer Normalization)** [7]。

### 4. 初始化策略 (Initialization)
*   **破坏对称性与信号保持**：Transformer 的大规模训练依赖于 Week 10 提到的 **随机初始化** 以破坏参数对称性，并参考如 **Xavier 初始化** 或 **He 初始化** 的原则，确保前向传播激活值和反向传播梯度的方差稳定，防止在深层结构中信号消失 [2, 6]。