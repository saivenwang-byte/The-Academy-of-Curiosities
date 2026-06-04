# Agent 能力映射 · Claude 10 ↔ Cursor ↔ 仓库正典

> **用途**：避免重复建 Rule/Skill；改标准只改「正典列」  
> **Status**: ACTIVE · 2026-06-02 合并方案第一批

---

## 架构四层

| Layer | 形态 | 数量 |
|-------|------|------|
| 0 入口 | `CLAUDE.md` · `AGENTS.md` | 2 |
| 1 常驻 | `.cursor/rules/*.mdc` | 6 |
| 2 工作流 | `skills/academy-*/SKILL.md` | 7+ |
| 3 脚本 | 6 个 + CI | 6 |
| 4 正典 | `docs/` · `02_/` · `09_/` · HTML | — |

---

## 能力对照表

| # | 能力（Claude 10） | Cursor 合并 | 落地 | 状态 |
|---|-------------------|-------------|------|------|
| 1 | Project Memory | Startup Gate | `CLAUDE.md` + `rules/00-*` + 本文件 | ✅ 第一批 |
| 2 | Japan Cultural Calibration | 01-japan-school-culture | `japan_campus_consultant_agent.html` + `rules/01-*` | ✅ |
| 3 | Nagoya Environment Metrics | 02-nagoya-environment | `world_reference/` + `rules/02-*` | ✅ |
| 4 | Honkaku Fair-Play | 03-honkaku-fair-play | `04_MYSTERY_SCIENCE_*` + `rules/03-*` | ✅ |
| 5 | Creative Redline | 04-creative-redline | `创作红线与原则.txt` + `rules/04-*` | ✅ |
| 6 | Story Database Builder | academy-story-database | `docs/story_database/` + Skill | ✅ 第一批 |
| 7 | Visual Prompt Auditor | academy-visual-auditor | `07_设计原档/` · `art_review/` · Skill | ✅ 第四批 |
| 8 | Character Consistency | engine §九 + visual-auditor | `docs/characters/00_character_canon_index.md` | ✅ 第三批 |
| 9 | Reference Library Import | academy-research-editor | `09_/` · `import_reference_library.py` | ✅ 第四批 |
| 10 | Git Workflow | 05-git-and-index | User Rules + `pre_push_check.py` | ✅ |
| — | Sample Chapter Production | **academy-engine** 流水线 Phase 0–7 | `AGENTS.md` · engine §样章生产 | ✅ 第三批 |
| — | Case/Scene Card | series-architect + story-database | `docs/volume_planning/` · `scripts/case_card_lint.py` | ✅ 脚本 |
| — | IP 战略参考（立项/钩子/节奏/观察社/Vol1） | `10_IP战略参考_ChatGPT对话/00_INDEX` · E1 · F1 | 范式区 · architect 先讨论 | ✅ 2026-06-04 |
| — | Agent 协作范式（每会话） | `06_Agent运作卡` · `05_架构参照` | 范式区 | ✅ 2026-06-04 |
| — | **人类 Expert 池 V1.0** | `12_人类专家池` · `12_专家卡` | 范式区 · 链 `11_` | ✅ 2026-06-04 |
| — | **专家池 v0.1**（Agent/Skill） | `11_` · `11_检查项` · `06_` §9 | 范式区 | ✅ 2026-06-04 |

---

## Skill 路由（何时触发）

| 用户意图 | Skill |
|----------|-------|
| 拆卷、50卷、任务包 | `academy-series-architect` |
| 查资料、入库 09_ | `academy-research-editor` |
| 写正文、实验、质量清单 | `academy-engine` |
| Hybrid Voice 中文润色 | `academy-voice-editor` |
| 日译推敲 | `academy-jp-voice-editor` |
| 插图 prompt / 成图审 | `academy-visual-auditor` |
| 200篇表、Case 状态 | `academy-story-database` |
| 新角色/日译/群像 **该不该定稿** | `11_专家池与Agent调度_v0.1` · `06_` §9 |

---

## 不部署项（刻意合并）

- 第三方 skills.sh / 未知 GitHub Skill
- 独立 `sample-chapter-production` Skill（= engine）
- 独立 `reference-import` Skill（= research-editor）
- 20 条全 always-on Rule（仅 6 条常驻）
- **25 个独立 Expert Agent Skill**（v0.1 合并为 `11_` + 现有 7 Skill）

---

最后更新：2026-06-04 · 增范式区与 IP 战略参考
