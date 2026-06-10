# Week 5–6 子主题地图（采集前规划）

> **Skill**：`.cursor/skills/ai-course-notebooklm/SKILL.md`  
> **模块**：序列建模 HMM/CRF → 词嵌入/早期 DL  
> **原则**：一次 chat 只专注一个问题；`clear_conversation: true` 于每个 batch  
> **来源依据**：`guides/AI课程-14周内容梳理.md` Week 5–6 + Week 3–4 衔接

## 学习顺序与重要程度

| # | Batch ID | 子主题 | 解决什么问题 | 程度 | 拆问策略 |
|---|----------|--------|-------------|------|----------|
| 0 | L0-positioning | 模块定位 | Week5-6 在课程/Project 中干什么 | 核心 | 单问 |
| 1 | w5-seq-challenges | 序列建模难点 | 为何静态分类不够 | 重要 | 单问 |
| 2 | w5-markov-hmm-intro | 马尔可夫性与 HMM 直觉 | 什么是「隐状态」 | 核心 | 单问 |
| 3 | w5-hmm-five-tuple | HMM 五元组 | λ=(S,O,π,A,B) 各是什么 | **核心** | 单问 |
| 4 | w5-hmm-three-problems | HMM 三问题 | 评估/解码/学习各干什么 | **核心** | 单问 |
| 5 | w5-forward-algo | 前向算法 | 评估问题怎么 DP 解 | **核心** | 单问推导 |
| 6 | w5-backward-algo | 后向算法 | 为 Baum-Welch 铺路 | 重要 | 单问 |
| 7 | w5-viterbi | Viterbi 解码 | 解码问题怎么找最优路径 | **核心** | 单问 |
| 8 | w5-baum-welch | Baum-Welch / EM | 学习问题怎么估参 | **核心** | 单问（复杂，独立） |
| 9 | w5-forward-numeric | 前向算法数值例 | 手算 tiny HMM 验证 | 重要 | L3 专问 |
| 10 | w6-hmm-generative | HMM 生成模型回顾 | P(X,Y) 与局部归一化偏差 | 重要 | 单问 |
| 11 | w6-crf-intro | CRF 判别模型 | P(Y\|X) 为何优于 HMM 标注 | **核心** | 单问 |
| 12 | w6-crf-features | CRF 特征与全局归一化 | φ_k、Z(X) 是什么 | **核心** | 单问 |
| 13 | w6-hmm-vs-crf | HMM vs CRF 对比 | 生成 vs 判别、特征工程 | **核心** | 对比表单问 |
| 14 | w6-word-embedding | 词嵌入 | 分布式表征、one-hot 局限 | 重要 | 单问 |
| 15 | w6-window-network | 窗口序列标注网络 | 拼接→FC→Softmax 怎么做 | 重要 | 单问 |
| 16 | w6-early-dl-limits | 早期 DL 局限 | 为何不建模标签依赖 | 重要 | 单问 |
| 17 | w6-to-rnn | 通向 RNN/LSTM | Week6 如何衔接到后续 | 了解 | 单问 |
| 18 | w56-bridge-w34 | 与 Week3-4 衔接 | 从 CNN/分类到序列 | 重要 | 单问 |
| 19 | w56-project | Project 要求 | 手写 HMM/CRF/DL 对比 | 重要 | 单问 |
| 20 | w56-mistakes | 易错点 | 三问题/生成判别/归一化等 | 重要 | 对比表单问 |
| 21 | w56-study-order | 复习优先级 | 先掌握什么 | 重要 | 单问 |

## 叙事链（整合指南时用）

```
Week3-4: 图像用 CNN → 文本/语音等序列怎么办？
  → w5: 序列难点 → 马尔可夫/HMM 五元组 → 三问题
       → 前向(评估) → 后向 → Viterbi(解码) → Baum-Welch(学习) → 数值验证
Week5 能建模序列了，但 HMM 有何局限？
  → w6: 生成模型回顾 → CRF 判别 → 特征/全局归一化 → HMM vs CRF
       → 词嵌入 → 窗口网络 → 局限 → 通向 RNN
  → 串联 Week3-4、Project 要求、易错点
```

## 待 L0 校验

- Week 5 记录是否含后向/Viterbi/Baum-Welch（课纲写「后续」，Week 7 无记录）
- Project 是 PJ2 还是独立序列标注作业——以 NotebookLM 课程记录为准
- 课件 09 序列章节与 Week 5/6 记录的对应关系
