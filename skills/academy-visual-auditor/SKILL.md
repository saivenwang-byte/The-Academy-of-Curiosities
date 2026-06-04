---
name: academy-visual-auditor
version: 1.0.0
description: 学堂趣事录插图与视觉 prompt 审计。当用户需要审插图、写/改 SC prompt、统调成图、检查角色一致性或 Vol 背景板时触发。封装私服上履き、名古屋环境、椅背结露、日文 SUM 页等 Vol1 教训。
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# 学堂趣事录 · 视觉审计 · Visual Prompt Auditor

## 何时触发

- 写/改 `prompts_插图Vol*.md` 或单 SC prompt
- 评审 AI 成图（PNG）是否可进正典
- 背景板 P0 修订、角色设定与成图不一致
- 用户说「插图统调」「视觉审计」「prompt 过门」

## 启动必读

1. `docs/00_PROJECT_STARTUP_GATE.md`（环境 + 文化）
2. `07_设计原档/13_插画风格规范_v2.md`
3. `07_设计原档/14_角色设计稿创作简报_v2.md`
4. `07_设计原档/15_Vol1场景背景板_P0修订.md`
5. Vol1 范例：`03_故事内容/第1卷_总是湿的椅子/插图/prompts_插图Vol1.md` v2

## Vol1 统调教训（P0 检查清单）

### 空间与行为

| 项 | 正确 | 错误 |
|----|------|------|
| 室内鞋 | 私服 + **上履き** 仅在地板/榻榻米 | 运动鞋、皮鞋、裸足实验台 |
| 实验 | 上履き不进实验台；可跪/坐 floor | 穿室外鞋做实验 |
| 教室后方 | **流し**（洗物槽）在教室后方 RC 校舍 | 把流し画成独立厨房 |
| 椅子湿迹 | **椅背**贴アルミ窓枠 · **微结露** | 椅座大水渍、泼水感 |
| 月份 | **4月** 名古屋 · 樱尾声/新绿 | 深秋落叶、盛夏 |

### 角色一致性

- 陸珣 / 陸瑆 / 慧美 / 田中 — 对照 `14_角色设计稿创作简报_v2.md` 与 **`docs/characters/00_character_canon_index.md`**
- 4年2組（Vol1 正文正典）；与旧 docx「5年」冲突时以正文+ v2 视觉为准
- 校服：私服日须统一「便服+上履き」描述进每条 prompt

### 光与科学

- 窗侧 ** afternoon sun** 与结露机制一致（见 `02_/名古屋写作硬指标`）
- 科学插图：可复现、无超自然符号

### 日文 SUM 页（11–12）

- 页面语言：**日文**（副标可英）
- 文字短、可 OCR；避免长段中文叠在图上

## 输出格式

```markdown
## Visual Audit — [Vol/SC]

**Verdict**: PASS | REVISE | REJECT

### P0（任一项 fail → REJECT）
- [ ] …

### P1（建议修）
- …

### Prompt 修订建议（若 REVISE）
…
```

## 与流水线关系

- **engine** 定 Scene 与科学 → **本 skill** 审 prompt/成图
- 通过后更新 `Vol*插图评审备忘_*.md` · `docs/assets_index/visual_asset_index.md` · `docs/art_review/`

**专家检查（v0.1 · 硬门禁）**：[`11_检查项`](00_项目概览/01_分支讨论_范式与框架/11_检查项Skill包_v0.1.md) **V12 V13 V14** · P06 · 群像/lineup 未过不得入库（`06_` §9）。

## 禁止

- 未过 L1 环境/文化门标「定稿插图」
- 复制 Vol1 prompt 不改月份/机制直接用于 Vol2+
- 在 prompt 里写「generic anime classroom」

---

最后更新：2026-06-02 · 合并方案第一批
