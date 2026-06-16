#!/usr/bin/env python3
"""Generate full manifests from topics-map batch definitions."""
from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = "505bdb1c-0034-4e14-89df-0b14bf3fc723"
ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "notebooklm-raw" / "manifests"


def b(id_: str, layer: str, priority: str, title: str, prompt: str) -> dict:
    return {
        "id": id_,
        "layer": layer,
        "priority": priority,
        "title": title,
        "clear_conversation": True,
        "prompt": prompt,
    }


def save(name: str, module: str, desc: str, sources: list[str], batches: list[dict]) -> None:
    data = {
        "module": module,
        "notebook_id": NOTEBOOK,
        "description": desc,
        "workflow": "v3-one-question-per-chat",
        "sources_hint": sources,
        "batches": batches,
    }
    path = OUT / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path.name}: {len(batches)} batches")


SRC8 = ["笔记-week08-周五-AI", "课件09-Deep-Learning"]
SRC10 = ["笔记-week10-周五-AI", "课件09-Deep-Learning"]
SRC12 = ["笔记-week12-周五-AI", "课件09-Deep-Learning", "PJ2-作业说明"]
SRC1314 = [
    "笔记-week13-周五-AI",
    "笔记-week14-周五-AI",
    "课件05-Uncertainty",
    "课件02-Knowledge-representation",
    "课件07-Logics-and-Prolog",
]

W8 = [
    b("L0-positioning", "L0", "critical", "Week8 在课程中的位置",
      "【单问】请仅回答：Week 8 在 AI(H) 课程中解决什么核心问题？与 Week 6-7 及 Week 10 如何衔接？\n\n依据：Week 8 课程记录、课件 09。\n要求：中文；3-5 段；每点标注来源；不要展开具体公式。"),
    b("w8-generative-goal", "L1+L2", "critical", "生成模型目标",
      "【单问·核心】请仅讲解：生成模型的目标为何是学习 P(X)？潜在空间 Z 的「紧致性」和「可生成性」分别指什么？\n\n依据：Week 8 课程记录、课件 09。\n要求：中文；标注来源；不要讲 VAE 公式。"),
    b("w8-vae-elbo", "L2", "critical", "VAE 与 ELBO",
      "【单问·核心】请仅推导/讲解：VAE 中 ELBO 如何分解为重构项与 KL 正则项？各自起什么作用？\n\n依据：Week 8 课程记录、课件 09、花书第 20 章。\n要求：关键公式+符号表；中文；标注来源；不要讲扩散或 GAN。"),
    b("w8-reparameterization", "L2", "important", "重参数化技巧",
      "【单问·重要】请仅讲解：VAE 的重参数化技巧是什么？为何使随机采样可反向传播？\n\n依据：Week 8 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w8-vae-compactness", "L1+L2", "important", "紧致性约束",
      "【单问·重要】请仅说明：VAE 为何需要 KL 紧致性约束？若缺少会怎样（shortcut 问题）？\n\n依据：Week 8 课程记录、课件 09。\n要求：直觉优先；中文；标注来源。"),
    b("w8-diffusion", "L1+L2", "critical", "扩散模型",
      "【单问·核心】请仅讲解：扩散模型的前向加噪与反向去噪过程；「分而治之」直觉是什么？\n\n依据：Week 8 课程记录、课件 09。\n要求：中文；标注来源；不要讲 GAN。"),
    b("w8-flow-matching", "L2", "optional", "流匹配",
      "【单问】请仅说明：流匹配（Flow Matching）与扩散/GAN 相比的特点——确定性向量场、多样性 vs 保真度权衡。\n\n依据：Week 8 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w8-gan", "L1+L2", "critical", "GAN 对抗训练",
      "【单问·核心】请仅讲解：GAN 中生成器与判别器的对抗博弈如何训练？各自损失目标是什么？\n\n依据：Week 8 课程记录、课件 09。\n要求：中文；标注来源；不要讲 VAE。"),
    b("w8-model-compare", "L3", "important", "生成模型对比",
      "【单问·重要】请用对比表说明：VAE、扩散模型、流匹配、GAN 各自优势、局限与典型应用。\n\n依据：Week 8 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w8-bridge-w67", "L4", "important", "与 Week6-7 衔接",
      "【单问】请仅说明：从 Week 6-7 的判别/特征学习到 Week 8 生成模型，知识上如何自然过渡？\n\n要求：条目式；中文；标注来源。"),
    b("w8-bridge-w10", "L4", "optional", "通向 Week10",
      "【单问】请仅说明：Week 8 生成模型训练依赖 Week 10 哪些优化技术？\n\n要求：中文；标注来源。"),
    b("w8-mistakes", "L3", "important", "Week8 易错点",
      "【单问】请列出 Week 8 最易混淆的 4-5 组概念（ELBO/KL/对抗训练/扩散 vs GAN 等），用对比表说明。\n\n要求：中文；标注来源。"),
    b("w8-study-order", "L4", "important", "Week8 复习优先级",
      "【单问】请仅给出 Week 8 推荐学习顺序和复习优先级（极高/高/中）。\n\n要求：中文；条目式；标注来源。"),
]

W10 = [
    b("L0-positioning", "L0", "critical", "Week10 在课程中的位置",
      "【单问】请仅回答：Week 10 在 AI(H) 课程中解决什么核心问题？与 Week 8 生成模型及 Week 12 Transformer 如何衔接？\n\n依据：Week 10 课程记录、课件 09。\n要求：中文；3-5 段；每点标注来源。"),
    b("w10-optimizer-evolution", "L1+L2", "critical", "优化器演进",
      "【单问·核心】请仅梳理：SGD → Momentum → Adagrad → RMSprop → Adam → AdamW 的演进脉络，各解决什么问题？\n\n依据：Week 10 课程记录、课件 09、花书第 8 章。\n要求：对比表；中文；标注来源。"),
    b("w10-sgd-momentum", "L2", "important", "SGD 与 Momentum",
      "【单问·重要】请仅讲解：标准 SGD 的局限；Momentum 如何加速收敛、缓解震荡？\n\n依据：Week 10 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w10-adaptive", "L2", "critical", "自适应学习率",
      "【单问·核心】请仅讲解：Adagrad、RMSprop、Adam 的自适应学习率机制有何异同？\n\n依据：Week 10 课程记录、课件 09。\n要求：中文；标注来源；不要讲 AdamW。"),
    b("w10-adamw", "L2", "optional", "AdamW 与正交化",
      "【单问】请仅说明：AdamW 如何解耦权重衰减？矩阵正交化初始化在本课中提及的作用是什么？\n\n依据：Week 10 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w10-preprocessing", "L2", "important", "数据预处理",
      "【单问·重要】请仅讲解：条件数、白化（whitening）与标准化（standardization）对优化的影响。\n\n依据：Week 10 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w10-hessian-geometry", "L2", "important", "损失曲面几何",
      "【单问·重要】请仅说明：海森矩阵如何刻画损失曲面几何？与优化困难（鞍点、病态条件）的关系？\n\n依据：Week 10 课程记录、课件 09。\n要求：直觉优先；中文；标注来源。"),
    b("w10-init-xavier-he", "L2", "critical", "Xavier/He 初始化",
      "【单问·核心】请仅讲解：Xavier 与 He 初始化的原理、适用激活函数及公式。\n\n依据：Week 10 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w10-batch-norm", "L2", "critical", "Batch Normalization",
      "【单问·核心】请仅讲解：Batch Norm 如何缓解内部协变量偏移、稳定训练？训练与推理时行为差异？\n\n依据：Week 10 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w10-layer-norm", "L2", "important", "Layer Normalization",
      "【单问·重要】请仅对比：Layer Norm 与 Batch Norm 的区别；为何 Transformer 用 LN？\n\n依据：Week 10 课程记录、课件 09。\n要求：对比表；中文；标注来源。"),
    b("w10-regularization", "L2", "critical", "L2/Dropout/早停",
      "【单问·核心】请仅讲解：L2 正则、Dropout、早停各自如何防止过拟合？\n\n依据：Week 10 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w10-hyperparams", "L2", "important", "超参数选择",
      "【单问·重要】请仅说明：学习率衰减策略；Batch Size 与学习率的正相关关系。\n\n依据：Week 10 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w10-bridge-w8", "L4", "optional", "与 Week8 衔接",
      "【单问】请仅说明：Week 8 生成模型训练如何用到 Week 10 的优化技巧？\n\n要求：中文；标注来源。"),
    b("w10-bridge-w12", "L4", "important", "通向 Week12",
      "【单问·重要】请仅说明：Week 12 Transformer 大规模训练依赖 Week 10 哪些优化/正则/归一化技术？\n\n要求：中文；标注来源。"),
    b("w10-mistakes", "L3", "important", "Week10 易错点",
      "【单问】请列出 Week 10 最易混淆的 4-5 组概念（BN/LN、Adam vs SGD、白化 vs 标准化等），用对比表说明。\n\n要求：中文；标注来源。"),
    b("w10-study-order", "L4", "important", "Week10 复习优先级",
      "【单问】请仅给出 Week 10 推荐学习顺序和复习优先级。\n\n要求：中文；条目式；标注来源。"),
]

W12 = [
    b("L0-positioning", "L0", "critical", "Week12 在课程中的位置",
      "【单问】请仅回答：Week 12 在 AI(H) 课程中解决什么核心问题？与 Week 5-6 序列建模及 Week 13 符号主义如何衔接？\n\n依据：Week 12 课程记录、课件 09。\n要求：中文；3-5 段；每点标注来源。"),
    b("w12-attention-intuition", "L1", "critical", "注意力直觉",
      "【单问·核心】请仅用 Q/K/V 检索模型类比讲解：注意力机制在做什么？\n\n依据：Week 12 课程记录、课件 09、Attention Is All You Need。\n要求：大白话；中文；标注来源；不要写完整公式。"),
    b("w12-self-attention", "L2", "critical", "Self-Attention 公式",
      "【单问·核心】请仅讲解：Scaled Dot-Product Self-Attention 的计算流程与公式；多头注意力如何并行？\n\n依据：Week 12 课程记录、课件 09。\n要求：符号表；中文；标注来源。"),
    b("w12-transformer-encoder", "L2", "critical", "Transformer Encoder",
      "【单问·核心】请仅讲解：Transformer Encoder 层结构（双向 MHAttn + FFN + 残差 + LayerNorm）。\n\n依据：Week 12 课程记录、课件 09。\n要求：中文；标注来源；不要讲 Decoder。"),
    b("w12-transformer-decoder", "L2", "critical", "Transformer Decoder",
      "【单问·核心】请仅讲解：Transformer Decoder 层结构（因果注意力 + 交叉注意力 + FFN + 残差 + LN）。\n\n依据：Week 12 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w12-pretrain-paradigms", "L2", "critical", "三种预训练范式",
      "【单问·核心】请用对比表说明：T5/BART（编解码）、BERT（仅编码器）、GPT（仅解码器）的架构与任务差异。\n\n依据：Week 12 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w12-gpt-wins", "L1+L2", "critical", "GPT 为何胜出",
      "【单问·核心】请仅说明：GPT 架构最终胜出的原因——计算效率（KV 缓存）、任务性能、范式一致性、零样本能力。\n\n依据：Week 12 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w12-gen-unified", "L2", "optional", "生成模型统一视角",
      "【单问】请仅说明：Week 12 如何将 VAE/扩散/流匹配/GAN 置于统一理论视角？\n\n依据：Week 12 课程记录、课件 09。\n要求：中文；标注来源。"),
    b("w12-bridge-symbolic", "L4", "important", "铺垫符号主义",
      "【单问·重要】请仅说明：Week 12 如何铺垫符号主义（语义网络、框架）？与 Week 13 的关系？\n\n要求：中文；标注来源。"),
    b("w12-bridge-w56", "L4", "important", "与 Week5-6 衔接",
      "【单问】请仅说明：从 Week 5-6 HMM/CRF 到 Week 12 Transformer，序列建模路径如何演进？\n\n要求：中文；标注来源。"),
    b("w12-bridge-w13", "L4", "important", "通向 Week13",
      "【单问】请仅说明：Week 12 DL 黑箱与 Week 13 符号主义可解释性如何形成对比与转折？\n\n要求：中文；标注来源。"),
    b("w12-pj2", "L4", "important", "PJ2 要求",
      "【单问·重要】请仅汇总：PJ2（Transformer）的作业要求、实现要点与 GPU 申请提醒（若有）。\n\n依据：Week 12 课程记录、PJ2 作业说明。\n要求：中文；标注来源。"),
    b("w12-mistakes", "L3", "important", "Week12 易错点",
      "【单问】请列出 Week 12 最易混淆的 4-5 组概念（Encoder/Decoder、BERT/GPT、Self/Cross-Attn 等），用对比表说明。\n\n要求：中文；标注来源。"),
    b("w12-study-order", "L4", "important", "Week12 复习优先级",
      "【单问】请仅给出 Week 12 推荐学习顺序和复习优先级。\n\n要求：中文；条目式；标注来源。"),
]

W1314 = [
    b("L0-positioning", "L0", "critical", "Week13-14 在课程中的位置",
      "【单问】请仅回答：Week 13-14 为何在课程末尾回归符号主义？与 Week 12 及 Week 15 CLIPS 如何衔接？\n\n依据：Week 13/14 课程记录、课件 05/02/07。\n要求：中文；3-5 段；每点标注来源。"),
    b("w13-exam-info", "L4", "important", "期末说明",
      "【单问·重要】请仅汇总：期末考试形式（开卷/英文等）、确定性因子必考、Project 期末安排。\n\n依据：Week 13/14 课程记录。\n要求：中文；标注来源。"),
    b("w13-bayes-framework", "L2", "critical", "贝叶斯框架",
      "【单问·核心】请仅讲解：贝叶斯推理框架——先验+似然→后验→决策；L2 正则即高斯先验的联系（若有）。\n\n依据：Week 13 课程记录、课件 05、AIMA。\n要求：中文；标注来源。"),
    b("w13-gmm-conjugate", "L2", "important", "GMM 与共轭先验",
      "【单问·重要】请仅讲解：高斯混合模型直觉；共轭分布在本课中的作用。\n\n依据：Week 13 课程记录、课件 05。\n要求：中文；标注来源。"),
    b("w13-certainty-factor", "L2", "critical", "确定性因子",
      "【单问·核心·必考】请仅讲解：确定性因子（Certainty Factor）中证据不确定性与规则不确定性的含义及合成计算规则。\n\n依据：Week 13 课程记录、课件 05。\n要求：公式+符号表；中文；标注来源。"),
    b("w13-cf-numeric", "L3", "critical", "确定性因子数值例",
      "【单问·要数值·必考】请仅给出一个确定性因子合成的完整数值手算例子，逐步展示计算过程。\n\n依据：Week 13 课程记录、课件 05。\n要求：完整数值步骤；中文；标注来源。"),
    b("w13-markov-pagerank", "L2", "important", "马尔可夫链与 PageRank",
      "【单问·重要】请仅讲解：马尔可夫链直觉及 PageRank 算法原理。\n\n依据：Week 13 课程记录、课件 05。\n要求：中文；标注来源。"),
    b("w13-fuzzy-logic", "L1+L2", "optional", "模糊逻辑",
      "【单问】请仅说明：Zadeh 模糊逻辑如何处理语义不确定性？与概率方法的区别？\n\n依据：Week 13 课程记录、课件 05。\n要求：中文；标注来源。"),
    b("w13-symbolic-vs-dl", "L4", "important", "符号主义 vs 深度学习",
      "【单问·重要】请用对比表说明：符号主义在可解释性、样本效率等方面相对 DL 的优势。\n\n依据：Week 13 课程记录、课件 02。\n要求：中文；标注来源。"),
    b("w14-propositional", "L2", "critical", "命题逻辑",
      "【单问·核心】请仅讲解：命题逻辑连接词、真值表、善意推定原则及表达能力局限。\n\n依据：Week 14 课程记录、课件 07、AIMA。\n要求：中文；标注来源。"),
    b("w14-fol", "L2", "critical", "一阶谓词逻辑",
      "【单问·核心】请仅讲解：一阶谓词逻辑——量词 ∀/∃、项/谓词、变量替换推理。\n\n依据：Week 14 课程记录、课件 07。\n要求：中文；标注来源。"),
    b("w14-entailment", "L2", "important", "逻辑蕴含",
      "【单问·重要】请仅讲解：逻辑蕴含的解释（可能世界）、模型论直觉。\n\n依据：Week 14 课程记录、课件 07。\n要求：中文；标注来源。"),
    b("w14-resolution", "L2", "critical", "消解原理",
      "【单问·核心·期末大题】请仅推导/讲解：消解原理（Resolution）作为自动推理核心算法的步骤与关键规则。\n\n依据：Week 14 课程记录、课件 07。\n要求：逐步写清；中文；标注来源。"),
    b("w14-exam-pipeline", "L3", "critical", "期末大题流程",
      "【单问·核心·期末大题】请仅说明：期末大题典型流程——自然语言→逻辑表达式→析取范式→消解证明，各步要点。\n\n依据：Week 14 课程记录、课件 07。\n要求：中文；标注来源。"),
    b("w14-prolog", "L2", "critical", "Prolog 反向推理",
      "【单问·核心】请仅讲解：Prolog 如何基于逻辑做反向推理编程？与 Week 15 CLIPS 前向推理的对比要点。\n\n依据：Week 14 课程记录、课件 07。\n要求：中文；标注来源。"),
    b("w1314-bridge-w12", "L4", "important", "与 Week12 衔接",
      "【单问】请仅说明：Week 12 DL 巅峰后，Week 13-14 符号主义回归的逻辑。\n\n要求：中文；标注来源。"),
    b("w1314-bridge-w15", "L4", "important", "通向 Week15",
      "【单问·重要】请仅说明：Week 14 Prolog 反向推理与 Week 15 CLIPS 前向推理如何构成符号主义两条路径？\n\n要求：中文；标注来源。"),
    b("w1314-mistakes", "L3", "important", "Week13-14 易错点",
      "【单问】请列出 Week 13-14 最易混淆的 4-5 组概念（确定性因子/贝叶斯、消解/归结、量词范围等），用对比表说明。\n\n要求：中文；标注来源。"),
    b("w1314-study-order", "L4", "important", "Week13-14 复习优先级",
      "【单问】请仅给出期末复习 Week 13-14 的推荐顺序和优先级（标注必考项）。\n\n要求：中文；条目式；标注来源。"),
]

if __name__ == "__main__":
    save("week8.json", "week8", "Week 8：深度生成模型 VAE/扩散/GAN（单问单答）", SRC8, W8)
    save("week10.json", "week10", "Week 10：神经网络优化技术（单问单答）", SRC10, W10)
    save("week12.json", "week12", "Week 12：Transformer 与大语言模型（单问单答）", SRC12, W12)
    save("week13-14.json", "week13-14", "Week 13-14：不确定性推理 + 逻辑/消解（单问单答）", SRC1314, W1314)
