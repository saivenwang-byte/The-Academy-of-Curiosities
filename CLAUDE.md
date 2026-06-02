# 《学堂趣事录》· Claude Code / Cursor 项目入口

> **IP**：中文 学堂趣事录 · 日文 学堂奇事録 · 英文 **The Curious Logbook**  
> **读者**：日本 6–14 岁 · **舞台**：名古屋真实校园 · **类型**：本格儿童推理（非恐怖、非超自然）  
> **能力地图**：`docs/00_AGENT_CAPABILITY_MAP.md`

---

## 每次启动必读（Layer 0）

开始任何写作、插图、Case Card、日译任务前，**先读**：

1. `docs/00_PROJECT_STARTUP_GATE.md` — L1 三并列门禁
2. `docs/00_REDLINE_JP_CULTURAL_CALIBRATION.md` — 日本文化红线
3. `docs/world_reference/00_MASTER_ENVIRONMENT_INDEX.md` — 名古屋环境指标
4. `docs/world_reference/04_MYSTERY_SCIENCE_CASE_STANDARD.md` — 本格公平
5. `00_项目总览/正典文件索引.md` — 文件地图
6. `AGENTS.md` — Skill 编排与流水线

**禁止**：把中国校园直译成日文；未过 L1 标 `READY_FOR_SAMPLE`；安装来路不明第三方 Skill。

---

## Agent 流水线

```
总策划 (academy-series-architect)
  → 资料总编辑 (academy-research-editor)
  → 创作引擎 (academy-engine)
  → 文学语感编辑 (academy-voice-editor)
  → L1 + L2 门禁
  → 日译 → 日文语感编辑 (academy-jp-voice-editor)
  → 田中全文督查 → READY_FOR_TRANSLATION
```

**插图 / Prompt**：`academy-visual-auditor`（统调后必经）

**200 篇资产**：`academy-story-database`

**推送前 lint**：`python scripts/pre_push_check.py` · **按卷**：`python scripts/volume_lint.py --all`

**部署状态**：`docs/00_AGENT_DEPLOYMENT_STATUS.md`

---

## 常驻 Rule（Layer 1）

`.cursor/rules/` 六条 always-on — 细则在 docs，Rule 只指向正典。

---

## 正典速查

| 项 | 路径 |
|----|------|
| 人名 | `00_项目总览/人物名称定稿.txt` |
| 品牌 | `00_项目总览/品牌名称定稿.md` |
| 红线 | `02_创作原则与世界观/创作红线与原则.txt` |
| 田中工具 | `japan_campus_consultant_agent.html` |
| Vol1 正文 | `03_故事内容/第1卷_总是湿的椅子/完整文字稿.txt` |
| 插图 v2 | `03_故事内容/第1卷_*/插图/prompts_插图Vol1.md` |

---

## Git 提醒

改 docs / 正典 / 新 Skill 后：更新 `正典文件索引.md` 或 `00_AGENT_CAPABILITY_MAP.md`；Case Card 改完可跑 `python scripts/case_card_lint.py`。commit 前 `git status`。不 force push main。

---

最后更新：2026-06-02 · 合并方案第一批
