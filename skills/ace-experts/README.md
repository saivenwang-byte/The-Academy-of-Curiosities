# ACE 专家池 · 阶段审核 Officer 注册表 · V1.0

> **Status**: ACTIVE · 2026-06-08  
> **政策**: [`00_项目总览/IP拍板记录_ACE与签核政策_20260607.md`](../../00_项目总览/IP拍板记录_ACE与签核政策_20260607.md) §4.1  
> **人读索引**: [`00_项目总览/专家池_ACE蒸馏注册表_V1.0.md`](../../00_项目总览/专家池_ACE蒸馏注册表_V1.0.md)  
> **Lint**: `python scripts/ace_distill_lint.py`

---

## 原则

| 是 | 否 |
|----|-----|
| **ACE Officer** = 阶段能力编排 + 蒸馏卡检查 | `academy-expert-<假名>` persona Agent |
| `signoff_type: ace_distilled`（E04/E07/E09/G1/E20/E25） | 代签 **E06** · **IP Owner** 终签 |
| `knowledge_sources[]` 公开出处 | 真人 endorsement |

---

## Officer 一览

| Officer ID | 阶段 | 覆盖 Gate 位 | Skill | 蒸馏卡 |
|------------|------|--------------|-------|--------|
| **ACE-A_Canon_Gate_Officer** | Gate A 正典/语言/文化/合规 | E04 · E07 · E09 · E25 | [`ACE-A_Canon_Gate_Officer/SKILL.md`](./ACE-A_Canon_Gate_Officer/SKILL.md) | `cards/` ×4 |
| **ACE-B_Sample_Visual_Production_Officer** | Gate A→B 样章视觉 | G1 brief · depth · L0 | [`ACE-B_Sample_Visual_Production_Officer/SKILL.md`](./ACE-B_Sample_Visual_Production_Officer/SKILL.md) | `cards/` ×2 |
| **ACE-C_Trial_Market_Officer** | Gate A/C 试读 | E20 | [`ACE-C_Trial_Market_Officer/SKILL.md`](./ACE-C_Trial_Market_Officer/SKILL.md) | `cards/` ×1 |
| ACE-D_Publishing_IP_Extension_Officer | Gate D 出版扩展 | E16 · E22 印前 | PLANNED | — |

---

## 与七 Skill 关系

```
academy-engine / voice / jp-voice / visual-auditor  → 产稿
academy-gate-orchestrator                           → 汇总四栏 + ACE 草案
ACE-A / ACE-B / ACE-C                               → 缺口专家蒸馏签核路径
E06 · IP Owner                                      → 终签（不可代）
```

---

## 激活检查

```powershell
python scripts/ace_distill_lint.py
python scripts/ace_distill_lint.py --officer ACE-A_Canon_Gate_Officer
```

全部 PASS → Gate A 可切换 E04/E07/E09/G1/E20/E25 至 `ace_distilled`（E06 仍 👤）。
