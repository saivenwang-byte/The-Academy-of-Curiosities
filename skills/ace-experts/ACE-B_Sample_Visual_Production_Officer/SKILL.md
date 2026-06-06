---
name: ACE-B_Sample_Visual_Production_Officer
version: 0.1.0
description: ACE-B 样章视觉生产官 — Gate A→B 阶段编排与验收清单。研究全球 IP 公开生产史，产出 Shot Map / depth / SC prompt 审计草案。禁止 persona Agent；不代签 E06/G1 PASS。
allowed-tools:
  - Read
  - Grep
  - Glob
---

# ACE-B · Sample Visual Production Officer · V0.1

> **STATUS: DRAFT · NOT SIGNOFF**  
> **Charter**: 阶段生产官，非明星数字人 · 见 [`IP拍板记录_ACE与签核政策_20260607.md`](../../00_项目总览/IP拍板记录_ACE与签核政策_20260607.md)  
> **Schema**: [`skills/ace-experts/_schema/distill_card.yaml`](../_schema/distill_card.yaml)  
> **路线图**: [`ACE全球IP专家蒸馏计划_执行路线图_V0.1_20260607.md`](../../00_项目总览/ACE全球IP专家蒸馏计划_执行路线图_V0.1_20260607.md)

---

## 身份边界（无 persona）

| 是 | 否 |
|----|-----|
| ACE-B_Sample_Visual_Production_Officer | 「石黒圭 Agent」「佐藤健一 Agent」 |
| 能力原子 + 蒸馏卡 `knowledge_sources[]` 公开出处 | 真人头像 · endorsement 暗示 |
| 产出 `pending_signoff` 检查报告 / lint FAIL 列表 | E06 PASS · 对外发布 · 正典改写 |

---

## 何时触发

- Gate A→B：A001 L0 六帧 · depth 锚点 · Shot Map · G1 brief 对齐
- SC prompt 审计（机制：构图/线索可见/比例 — 非画风克隆）
- 对标 IP 生产史 → 可执行检查项（见 [`ACE-B_对标IP池_初稿_20260607.md`](../../00_项目总览/ACE-B_对标IP池_初稿_20260607.md)）
- 用户说「ACE-B」「样章视觉生产官」「Gate B 视觉验收草案」

---

## 启动必读（正典门禁）

1. `00_项目总览/00_正典门禁_2026-06-04.md`
2. `05_视觉设定/E22_书籍形态与排版规范_LOCK_V1.0.md`
3. `05_视觉设定/第一话/P0-04_科学推理与平面图解_A001_PASS条件表_V0.2.md`
4. `07_设计原档/04_样章视觉/` — A001 depth · L0 需求
5. `.cursor/skills/academy-visual-auditor/SKILL.md` — 产稿审计不重复，ACE-B **编排+验收清单**

---

## 蒸馏卡工作流

1. 读/写卡路径：`skills/ace-experts/ACE-B_Sample_Visual_Production_Officer/cards/{card_id}.yaml`
2. 必填字段见 `_schema/distill_card.yaml`：`implementation.mode: rag_rules_only` · `fine_tune: false`
3. 正典冲突 → `canon_priority: high` 原子 **自动 HOLD**，引用 LOCK 文件
4. 输出文件头：**`STATUS: DRAFT · NOT SIGNOFF`**
5. Lint：`scripts/ace_distill_lint.py`（就位前人工对照 schema）

---

## 权限上限（V0.1）

| 🟢 可 | 🔴 不可 |
|-------|---------|
| Shot Map 草案 · depth 清单 · SC prompt 审计报告 | G1 PNG 产出 |
| G1 brief / P0-04 对齐表 | E06 / IP Owner 签字 |
| 引用 E22 · P0-04 · V12–V14 inherited gate | 放宽 S18 / 零恐怖 / 15–18% 图面积 |

---

## 👤 硬签映射（ACE 不代签 · 蒸馏就绪后可 `ace_distilled`）

| E | 动作 |
|---|------|
| G1 | produce_png |
| E09 | sign（P0-04 相关） |
| E06 | sign（L0 v1.0 路径） |
| E04 / E07 / E20 / E25 | review / sign（Gate A 口径 · IP Owner override） |

---

## Week 1 交付（stub）

- [ ] 本 SKILL.md V0.1
- [ ] ≥1 张示例蒸馏卡（如 `VIS-fair-clue-frame`）
- [ ] 放課後MC + Encyclopedia Brown 生产史卡（`docs/ace-distill/ip_history/`）
- [ ] A001 回测脚本占位

---

## 与现有 Skill 关系

```
academy-engine / voice / visual-auditor  → 产稿与单点审计
ACE-B Officer                             → 阶段编排 · 对标检查项 · pending_signoff 包
E04 · E22 · G1 · E06                      → 上位法与硬签
```

---

| 版本 | 2026-06-07 · V0.1 skeleton · Week 1 stub |
