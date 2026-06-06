---
name: ACE-A_Canon_Gate_Officer
version: 0.1.0
description: ACE-A 正典门禁官 — Gate A 日文(E04)、名古屋校园(E07)、科学线索公平(E09/P0-04)、合规扫描(E25)。蒸馏复合专家体，非 persona Agent。用户提到 ACE 蒸馏签、E04/E07/E09 签核时触发。
allowed-tools:
  - Read
  - Grep
  - Glob
---

# ACE-A · Canon Gate Officer · V0.1

> **STATUS: ACTIVE · ace_distilled 就绪**（E06/IP 终签不变）  
> **注册**: [`skills/ace-experts/README.md`](../README.md) · [`专家池_ACE蒸馏注册表_V1.0.md`](../../00_项目总览/专家池_ACE蒸馏注册表_V1.0.md)

---

## 身份边界

| 是 | 否 |
|----|-----|
| E04/E07/E09/E25 蒸馏检查报告 | 「吉田文子 Agent」「田中 Agent」 |
| 加载 `cards/*.yaml` · 对照正典 lint | 改正典 LOCK · 代签 E06 |
| 输出 `signoff_type: ace_distilled` 草案包 | 对外暗示真人背书 |

---

## 蒸馏卡（本 Officer）

| card_id | 覆盖 | 正典 |
|---------|------|------|
| `LNG-jp-vol1-readability` | **E04** | 日文读音 V1.1 · 标日对齐 |
| `CUL-nagoya-campus-five-layer` | **E07** | 五层感知 · 名古屋 · 上履き |
| `SCI-a001-clue-fairness` | **E09** · P0-04 | 科学公平 · A001 线索 |
| `CMP-gate-a-compliance` | **E25** | Gate A 红线 · S18–S20 |

路径：`skills/ace-experts/ACE-A_Canon_Gate_Officer/cards/{card_id}.yaml`

---

## 工作流

1. 读目标：Reader 20260607 · A001 JP · Gate 工作单对应 §  
2. 加载蒸馏卡 → 跑 `checks[]`  
3. 报告头：`STATUS: DRAFT · NOT SIGNOFF`  
4. Lint：`python scripts/ace_distill_lint.py --officer ACE-A_Canon_Gate_Officer`  
5. 挂 Gate 包：`distill_card_id` + `signoff_type: ace_distilled`

---

## 与 academy-* 关系

| Skill | 分工 |
|-------|------|
| `academy-jp-voice-editor` | 产稿/预审 |
| `academy-research-editor` | 素材调度 |
| **ACE-A** | Gate 签核位蒸馏编排 · 检查清单汇总 |

---

| 版本 | 2026-06-08 · V0.1 就位 |
