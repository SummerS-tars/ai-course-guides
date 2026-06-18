---
name: ai-guides-pdf
description: >-
  guides/ Markdown 学习指南与课纲导出 PDF：Puppeteer 渲染、Sarasa UI SC / Fira Code
  字体、KaTeX 公式。在用户提到 PDF 导出、课纲 PDF、export-pdf、guides 转 PDF、
  字体粗体、Puppeteer 导出时使用。
---

# AI 课程 guides PDF 导出 Skill

> **工具链位置**：`.cursor/skills/ai-guides-pdf/`  
> **默认输入**：`guides/AI课程-14周内容梳理.md`  
> **默认输出**：`guides/AI课程-14周内容梳理.pdf`（git 忽略）

## 何时启用

- 更新 `guides/AI课程-14周内容梳理.md` 后需重导课纲 PDF
- 单周学习指南需导出 PDF（指定 input/output）
- 调整 PDF 样式、字体、Markdown 预处理逻辑
- 排查 **粗体/标题/表格** 在 PDF 中显示异常

**不启用**：NotebookLM 采集与学习指南**内容**整合（见 `ai-course-notebooklm` skill）。

## 架构

```
Markdown (guides/*.md)
  → marked (GFM) + 列表/引用块预处理
  → HTML + skill 内嵌 Sarasa/Fira @font-face
  → KaTeX auto-render ($...$ / $$...$$)
  → Puppeteer page.pdf()
```

| 路径 | 用途 |
|------|------|
| `scripts/export-pdf.mjs` | 主导出入口 |
| `scripts/install-fonts.mjs` | 下载并解压字体到 `fonts/` |
| `scripts/lib/fonts.mjs` | 字体清单与 `@font-face` 生成 |
| `assets/pdf-export.css` | 打印样式（对齐 MPE：Sarasa UI SC + Fira Code） |
| `fonts-manifest.json` |  pinned 下载源（Sarasa 1.0.32、Fira Code 6.2） |
| `fonts/*.ttf` | 本地缓存（git 忽略，postinstall 填充） |

字体栈与 Cursor MPE（`~/.local/state/crossnote/style.less`）一致：**正文 Sarasa UI SC，代码 Fira Code**。

## 首次 setup

在仓库根目录：

```bash
npm install --prefix .cursor/skills/ai-guides-pdf
```

postinstall 会：

1. 从 GitHub releases 下载 **Sarasa UiSC / MonoSC**（单族 7z）与 **Fira Code** zip，解压所需 7 个字重
2. 安装 Puppeteer 用 Chromium（若缺失）

仅补字体：

```bash
npm run install-fonts --prefix .cursor/skills/ai-guides-pdf
```

## 导出命令

```bash
# 默认课纲
node .cursor/skills/ai-guides-pdf/scripts/export-pdf.mjs

# 或经 guides/ 薄封装（兼容旧命令）
cd guides && npm run export-pdf

# 指定文件
node .cursor/skills/ai-guides-pdf/scripts/export-pdf.mjs \
  guides/AI-Week3-4-学习指南.md guides/AI-Week3-4-学习指南.pdf
```

## 与 master worktree 同步

按 `.cursor/rules/sync-master-worktree.mdc`：

1. commit skill / guides 改动
2. master wt `cherry-pick`
3. 若重导了 PDF：`cp guides/*.pdf` → master `guides/`

## 维护指南

### 改样式

编辑 `assets/pdf-export.css`。标题/粗体依赖 **真实 Bold 字重**（`font-weight: 700` + SarasaUiSC-Bold.ttf），勿仅用 `font-weight: bold` 指望系统伪粗体。

### 升级字体

1. 更新 `fonts-manifest.json` 中的 release URL 与版本
2. 删除 `fonts/*.ttf` 与 `fonts/.cache/`
3. `npm run install-fonts --prefix .cursor/skills/ai-guides-pdf`

### 故障排查

| 现象 | 处理 |
|------|------|
| 粗体与正文无区别 | 确认 `fonts/` 下 7 个 ttf 齐全；重跑 install-fonts |
| 找不到 Chrome | `npx puppeteer browsers install chrome`（在 skill 目录） |
| 公式不渲染 | 需网络加载 KaTeX CDN；检查 `networkidle0` 超时 |
| 列表/引用块排版错 | 检查 `prepareBlockquotes` / `prepareMarkdownLists` |

环境变量（ rarely needed）：

- `PDF_EXPORT_FONT_DIR` — 覆盖字体目录（须含全部 7 个 ttf）

## 禁止

- 依赖 Windows 用户字体路径作为**运行时**硬编码（字体应落在 skill `fonts/`）
- 把 `fonts/*.ttf`、`node_modules/` 提交进 git
- 用 WeasyPrint 等旧 Python 链路（已废弃）
