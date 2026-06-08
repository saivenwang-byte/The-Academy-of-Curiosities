# 《学堂趣事录》· Claude Code / Cursor 项目入口

> **定位**：**人类与多工具的统一入口** — 启动必读、正典速查、Git 提醒。  
> **Agent Skill 编排主文档**：[`AGENTS.md`](./AGENTS.md)（11 skill · 专家调度 · **AGENTS 优先**）  
> **IP**：日文 **学堂奇事録**（首市场）· 中文 学堂趣事录 · 英文 **The Curious Logbook**  
> **读者**：日本 **10–12 岁**（核心）· 宣传 **9–12 岁** · 兼容阅读能力较好的 **四年级**  
> **品类**：**儿童图文校园推理章节书** · 桥梁式低阻力阅读 · **非** 低龄桥梁启蒙书  
> **阶段**：**Gate A 样张验证** · A001=单案 MVP · Vol1=五案 144–160p · **非** 出版就绪  
> **正典门禁**：`00_项目总览/00_正典门禁_2026-06-04.md` · Vol1 Plan B · 年级 V2  
> **状态表述（强制）**：[`00_项目总览/项目状态表述规范_V1.0.md`](00_项目总览/项目状态表述规范_V1.0.md)  
> **能力地图**：`docs/00_AGENT_CAPABILITY_MAP.md`

---

## 每次启动必读（Layer 0）

开始任何写作、插图、Case Card、日译任务前，**先读**：

0. `00_项目总览/项目状态表述规范_V1.0.md` — **汇报口径 · Gate · 禁止过度承诺**
1. `00_项目总览/00_正典门禁_2026-06-04.md` — 首市场 · Vol1 · 年级 · 名称
2. `docs/00_PROJECT_STARTUP_GATE.md` — L1 三并列门禁
3. `docs/00_REDLINE_JP_CULTURAL_CALIBRATION.md` — 日本文化红线
4. `docs/world_reference/00_MASTER_ENVIRONMENT_INDEX.md` — 名古屋环境指标
5. `docs/world_reference/04_MYSTERY_SCIENCE_CASE_STANDARD.md` — 本格公平
6. `00_项目总览/正典文件索引.md` — 文件地图
7. `AGENTS.md` — Skill 编排与流水线

**禁止**：把中国校园直译成日文；日文正文出现 **标日外** 文字/语法/叫法（见 `日文正文文字与语法标准_标日对齐_V1.0.md`）；未过 L1 标 `READY_FOR_SAMPLE`；安装来路不明第三方 Skill。

**Layer 0.5 — Session Memory（Lite ECC）**：跨会话 continuity → 读 [`.cursor/memory/MEMORY.md`](.cursor/memory/MEMORY.md)（当前 Gate · 待办 · SSOT）；显著变更时更新；交接运行 [`tools/ecc-memory/bin/memory_checkpoint.ps1`](tools/ecc-memory/bin/memory_checkpoint.ps1) 或写 `sessions/`。全指南 [`docs/learning/ecc/00_ECC_长期记忆全指南_V1.0.md`](docs/learning/ecc/00_ECC_长期记忆全指南_V1.0.md) · 可选 gstack `/context-save` 互补。

**Agent 协作范式（每会话）**：先读 `06_Agent运作卡`；创作/日译/群像读 `11_`（§9 硬触发）；**找真人专家**读 `12_人类专家池_V1.0.md`；**IP 开放议题**读 `00_项目总览/专家组审议工作流_V1.0.md`。架构 `05_` · 返工 `07_`。

**IP 产品战略正典（立项/受众/钩子/节奏/观察社）**：`00_项目概览/01_分支讨论_范式与框架/10_IP战略参考_ChatGPT对话/00_INDEX.md` — 战略层正文正典 · A1–A7 · B1–B4 · **D1 · E1 · F1**（**对外统计数据须核实**）。日常路径见 `09_日常怎么用.md`。

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

**P0 生产 Skill（结构/门禁）**：`academy-character-director` · `academy-canon-governor` · `academy-gate-orchestrator` — 见 [`AGENTS.md`](./AGENTS.md) 全表

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
| Vol1 根目录 | `03_故事内容/第1卷_觉得奇怪就先观察/` |
| Vol1 正式版（正文·Reader·depth） | `03_故事内容/第1卷_觉得奇怪就先观察/正式版/` |
| Vol1 薄样张试读 | `03_故事内容/第1卷_觉得奇怪就先观察/薄样张_试读/` |
| Vol1 样章包（Gate A 分发） | `03_故事内容/第1卷_觉得奇怪就先观察/样章包/` |
| C001 湿椅子素材 | `03_故事内容/第1卷_总是湿的椅子/`（**非 Vol1 正典**） |
| 正典对齐 P0 | `00_项目总览/正典对齐清单_P0_2026-06-05.md` |
| IP 战略正典 | `00_项目概览/01_分支讨论_范式与框架/10_IP战略参考_ChatGPT对话/00_INDEX.md` |
| 日常怎么用 | `00_项目概览/01_分支讨论_范式与框架/09_日常怎么用.md` |
| Agent 范式 | `00_项目概览/01_分支讨论_范式与框架/06_Agent运作卡_每会话必读.md` |

---

## Git 提醒

改 docs / 正典 / 新 Skill 后：更新 `正典文件索引.md` 或 `00_AGENT_CAPABILITY_MAP.md`；Case Card 改完可跑 `python scripts/case_card_lint.py`。commit 前 `git status`。不 force push main。

---

最后更新：2026-06-09 · 读者 10–12 · 状态表述规范强制 · Gate A
