# Agent 能力映射 · Claude 10 ↔ Cursor ↔ 仓库正典

> **用途**：避免重复建 Rule/Skill；改标准只改「正典列」  
> **Status**: ACTIVE · 2026-06-09  
> **状态表述（强制）**：[`00_项目总览/项目状态表述规范_V1.0.md`](../00_项目总览/项目状态表述规范_V1.0.md)

---

## 架构四层

| Layer | 形态 | 数量 |
|-------|------|------|
| 0 入口 | `README.md` · `CLAUDE.md` · `AGENTS.md` · **状态表述规范** | 4 |
| 1 常驻 | `.cursor/rules/*.mdc` | 6 |
| 2 工作流 | `skills/academy-*/SKILL.md` | **11**（7 主流程 + 4 P0） |
| 3 脚本 | lint / build / ledger | 10+ |
| 4 正典 | `docs/` · `02_/` · `09_/` · HTML 工具 | — |

---

## Skill 路由（11 · 2026-06-09）

| 用户意图 | Skill | 状态 |
|----------|-------|------|
| 拆卷、20卷×5案、任务包 | `academy-series-architect` | PRODUCTION |
| 查资料、入库 09_ | `academy-research-editor` | PRODUCTION |
| 写正文、实验、Phase 2b | `academy-engine` | PRODUCTION |
| Hybrid Voice 中文润色 | `academy-voice-editor` | PRODUCTION |
| 日译推敲 | `academy-jp-voice-editor` | PRODUCTION |
| 插图 prompt / 成图审 | `academy-visual-auditor` | PRODUCTION |
| 200篇表、Case 状态 | `academy-story-database` | PRODUCTION |
| **角色 soul · 语义审核** | **`academy-character-director`** | **V1.0 PRODUCTION** |
| 出场规模 · characters.yaml | `academy-character-scale` | SSoT |
| 正典漂移扫描 | `academy-canon-governor` | **PLANNED**（任务书） |
| Gate 四栏/E06 汇总 | `academy-gate-orchestrator` | **PLANNED**（任务书） |

**已废弃**：`academy-char-01`…`10` → **character-director** + soul YAML

---

## 能力对照表（节选）

| # | 能力 | Cursor 合并 | 落地 | 状态 |
|---|------|-------------|------|------|
| 1 | Project Memory | Startup Gate | `CLAUDE.md` + rules + **表述规范** | ✅ |
| 2 | Japan Cultural Calibration | 01-japan-school-culture | 田中 HTML + rules | ✅ |
| 6 | Story Database | academy-story-database | `docs/story_database/` | ✅ |
| 7 | Visual Auditor | academy-visual-auditor | `07_设计原档/` · Skill | ✅ |
| 8 | Character Consistency | **character-director** + engine 2b | soul YAML · lint | ✅ |
| — | Sample Chapter | academy-engine Phase 0–7 | `AGENTS.md` | ✅ |
| — | ACE 蒸馏卡 | `skills/ace-experts/` | lint **≠** 真人签核 | ✅ 结构 |

---

## 推送前检查（本地 · 非 CI 强制）

```bash
python scripts/pre_push_check.py
python scripts/character_soul_lint.py --vol1-core --strict
python scripts/volume_lint.py --all   # 按卷
python scripts/ace_distill_lint.py    # ACE 卡结构
```

> 仓库 **尚无** 主干 CI 强制门禁 — Agent 推送前 **须自跑** 上述脚本。

---

## 不部署项

- 第三方未知 Skill · 25 个独立 Expert Agent（→ `11_` + 7 主 Skill）
- 宣称 ACE lint = 科学/文化专家 PASS

---

最后更新：2026-06-09 · 11 Skill · 状态表述规范 · character-director PRODUCTION
