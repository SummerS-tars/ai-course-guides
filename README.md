# AI H 课件梳理与学习指南

复旦大学 2025-2026 学年第 2 学期 **人工智能（H）**（CS30057h.01）课程的课件结构梳理与 NotebookLM 辅助学习指南。

## 目录结构

```
├── guides/                    # 学习指南（定稿）
│   ├── AI课程-14周内容梳理.md   # 全学期知识脉络总览
│   ├── AI-Week1-2-学习指南.md
│   ├── AI-Week3-4-学习指南.md
│   ├── ...
│   └── AI课件-PPT梳理索引.md    # 逐章 PPT 结构梳理
├── notebooklm-raw/           # NotebookLM 采集原始数据
│   ├── manifests/             # 采集 manifest（提问计划）
│   ├── week1-2/               # 按周模块采集结果
│   ├── week3-4/
│   ├── ...
│   └── ppt/                   # 课件结构分析采集
└── .cursor/                   # Cursor IDE 配置（个人使用）
```

## 工作流

1. **课件结构分析**：NotebookLM 逐章 PPT → 提取章节结构与重点
2. **按周采集**：设计 manifest → NotebookLM 单问单答 → `notebooklm-raw/`
3. **知识图谱**：通读 raw → 产出认知阶梯与叙事承接
4. **叙事整合**：按图谱撰写学习指南，补全景节、mermaid 图、易混对比
5. **定稿**：用户 Review → 更新进度索引

## 课件覆盖

共 10 章：Introduction → Knowledge Representation → CLIPS → Decision Tree → Uncertainty → Rough Set → Logics & Prolog → Connectionist → Deep Learning → Genetic Algorithm

## 许可

仅供个人学习参考。
