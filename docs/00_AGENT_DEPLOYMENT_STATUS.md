# Agent 生产系统 · 部署状态

> **项目**：《学堂趣事录》· 合并方案全六批  
> **Status**: PRODUCTION_KICKOFF · 2026-06-02  
> **能力地图**：`docs/00_AGENT_CAPABILITY_MAP.md`

---

## 批次总览

| 批 | 主题 | 交付 |
|----|------|------|
| **1** | 安全底座 | `CLAUDE.md` · 6× `.cursor/rules/` · visual/story-database Skill · capability map |
| **2** | 生产效率 | `case_card_lint.py` · `visual_asset_index.md` |
| **3** | 质量控制 | engine Phase 0–7 · `character_canon_index` · `scene_card_lint` · `pre_push_check` |
| **4** | 素材与 Vol2 | Vol2 Case/Scene · `art_review/` · `import_reference_library.py` · PNG 归档 |
| **5** | 收尾自动化 | `volume_lint.py` · hooks · CI · Vol2 决策锁定 |
| **6** | **生产启动** | Vol2 初稿 · 调研/章纲 · `body_lint.py` · Vol03–10 IDEA · 50卷大纲同步 |

---

## Layer 架构（最终）

```
Layer 0   CLAUDE.md + AGENTS.md
Layer 1   .cursor/rules/          (6 always-on)
Layer 2   skills/academy-*        (7 skills · .cursor/skills 镜像)
Layer 3   scripts/                (7 scripts)
Layer 4   docs/ · 02_/ · 09_/ · HTML 正典
```

---

## 脚本一览

| 脚本 | 用途 |
|------|------|
| `case_card_lint.py` | Case / 故事表 / Vol1 图 |
| `scene_card_lint.py` | Scene Cards |
| `volume_lint.py` | **按卷** 统一 lint |
| `pre_push_check.py` | 推送前全套 |
| `import_reference_library.py` | 09_ 盘点 |
| `archive_vol1_duplicate_pngs.py` | 重复 PNG 归档 |
| `body_lint.py` | 正文禁直译/结构 lint |

**日常**：

```bash
python scripts/pre_push_check.py
python scripts/volume_lint.py --all
```

---

## 注册卷（volume_lint）

| Vol | Case | Scene | 正文 | 备注 |
|-----|------|-------|------|------|
| 01 | ✅ | ✅ | ✅ | scorecard · 插图 12 |
| 02 | ✅ | ✅ | ✅ DRAFT | 第六批初稿 · L1 待过 |

新卷：在 `scripts/volume_lint.py` 的 `VOLUMES` 注册 + 故事总表一行。

---

## Cursor Hooks

`.cursor/hooks.json` · `stop` → `on_agent_stop.py`  
Agent 回合结束时若 planning lint 失败，提示跑 `pre_push_check`。

---

## Claude Code

`.claude/README.md` → 指向根目录 `CLAUDE.md` 与 `skills/`（不第三套正文）。

---

## 刻意未建

- 20 条 always-on Rule  
- 第三方 skills.sh  
- 独立 sample-chapter / reference-import Skill  

---

## 下一步（生产）

1. Vol2：`japan_campus_consultant_agent.html` → `PENDING_REVIEW` → voice-editor 润色  
2. Vol2 日译 → `academy-jp-voice-editor`  
3. Vol2 插图批次（待 prompt 库）

---

最后更新：2026-06-02 · 第六批
