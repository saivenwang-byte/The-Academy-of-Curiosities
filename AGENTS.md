# 《学堂趣事录》Agent 编排

> **定位**：**Agent / Cursor Skill 编排的主文档** — 主流程 + P0 生产 Skill、专家调度。  
> **人类统一入口**：[`CLAUDE.md`](./CLAUDE.md) — 启动必读 · **含强制状态表述规范**  
> **状态表述（Agent 汇报必读）**：[`00_项目总览/项目状态表述规范_V1.0.md`](00_项目总览/项目状态表述规范_V1.0.md)  
> 品牌名：中文 学堂趣事录 · 日文 学堂奇事録 · 英文 **The Curious Logbook**（系列标语 The Academy of Curiosities）— 见 `00_项目总览/品牌名称定稿.md`

本项目使用 **十二个协作 skill**（八主流程 + 四 P0 生产）+ 已废弃 char-01…10，无需额外下载外部 agent。  
> **正典审计 2026-06-07**：七 skill 已对齐 `篇幅与单位构架_V1.1` · 详见 [`Skill正典审计报告_20260607.md`](00_项目总览/Skill正典审计报告_20260607.md)

## 文档层级（CLAUDE ↔ AGENTS）

| 文档 | 读者 | 职责 |
|------|------|------|
| **CLAUDE.md** | 人类 · Claude Code · 任意工具 | 项目门面 · Layer 0 必读清单 · 正典速查 · Git |
| **AGENTS.md**（本文件） | Cursor Agent · 子 skill | **编排主文档** · 谁调用谁 · 专家调度 · Rule 索引 |
| `skills/*/SKILL.md` | 被路由的 Agent | 单角色执行细则 |
| `00_项目总览/专家组审议工作流_V1.0.md` | IP 开放议题时 | 模拟 E01–E25 审议 · 待裁决单选题 |

**冲突时**：Skill 执行细节 → **SKILL.md**；多 skill 顺序 → **AGENTS.md**；Gate/阶段/自动化口径 → **项目状态表述规范**；P0 门禁 → **正典门禁 + CLAUDE Layer 0**。

## ACE 签核口径（勿误读）

| 层级 | 含义 |
|------|------|
| `ace_distill_lint PASS` | 蒸馏卡 **结构** 有效 |
| ACE review | 规则卡预审 · **非** 真人法律责任 |
| E04/E07/E09 human PASS | 专业签核 |
| **E06 PASS** | **KarfWang IP Owner 终签** · 唯一总闸 |

Gate A 内样机可 **ACE 预审 + IP 终签**；对外宣称「经专家审核」前须 **真人资格审查**。

## 角色一览

| Skill | 路径 | 角色 | 何时用 |
|-------|------|------|--------|
| **academy-series-architect** | `skills/academy-series-architect/` | 总策划 | 愿景、分卷、阶段、卷任务包、先讨论 |
| **academy-research-editor** | `skills/academy-research-editor/` | 资料总编辑 | 主动搜料、维护 `09_日本参考资料库`、调度知识 |
| **academy-engine** | `skills/academy-engine/` | 创作引擎 | 写正文、实验、角色台词、质量清单 |
| **academy-voice-editor** | `skills/academy-voice-editor/` | 文学语感编辑（中文） | Hybrid Voice v3、§7 文学维度 |
| **academy-literary-audit** | `skills/academy-literary-audit/` | **文学描写审计** | 初稿后 · 场级20项 · L16算法 · 变奏 · P10 · **C05/L12–L15** |
| **academy-jp-voice-editor** | `skills/academy-jp-voice-editor/` | 日文语感编辑 | 日译推敲、去直译腔、J1–J5 |
| **academy-visual-auditor** | `skills/academy-visual-auditor/` | 视觉审计 | 插图 prompt、成图统调、角色/环境 P0 |
| **academy-story-database** | `skills/academy-story-database/` | 故事资产库 | 200 篇总表、Case 状态、跨卷检索 |
| **academy-character-director** | `skills/academy-character-director/` | 角色灵魂导演 **V1.0** | soul 校验、对白归属、语义审核报告 |
| **academy-character-scale** | `skills/academy-character-scale/` | 角色规模/关系 SSoT | `characters.yaml` · 出场规模 · 关系向量 |
| **academy-canon-governor** | `skills/academy-canon-governor/` | 正典治理 **任务书** | 漂移扫描 · 引用影响 · **非自治** |
| **academy-gate-orchestrator** | `skills/academy-gate-orchestrator/` | Gate 编排 **任务书** | 四栏/E06 汇总 · **不代签** · **非自治** |

**已废弃（勿路由）**：`skills/academy-char-01`…`10` → 改指 **character-director** + `characters.yaml` + `characters/soul/*.yaml`

定稿门禁（L1 三并列）：

1. **田中みどり** — `japan_campus_consultant_agent.html`（文化）
2. **Project World Metrics** — `docs/world_reference/00_MASTER_ENVIRONMENT_INDEX.md`（环境/科学）
3. **本格公平** — `docs/world_reference/04_MYSTERY_SCIENCE_CASE_STANDARD.md`

**完整验收清单**：`00_项目总览/创作标准与验收流程.md`

**日文版（翻译后必做）**：`docs/00_JP_TRANSLATION_REVIEW_GATE.md` — 田中みどり **全文**五维督查，产出 `文化校准报告_日本語.txt`；未过不得 `READY_FOR_TRANSLATION`。

**范式与 IP 战略正典**：`00_项目概览/01_分支讨论_范式与框架/` — 日常见 `09_`；**专家调度**见 `11_` + `06_` §9。

## 专家调度 v0.1（关键节点）

| 场景 | 必读 |
|------|------|
| 新角色 / 改关系 | `11_` §5 总控模板 · 检查项 P05 |
| 新案件 / 写稿 | `11_检查项` C03 C04 · **C05/L12–L15** · **literary-audit** |
| 群像 / 插图定稿 | `visual-auditor` · V13 V14 · **硬门禁** |
| 日文稿 | `jp-voice-editor` · L09 · 田中 · **硬门禁** |
| 卷任务包 | `series-architect` · `E1`/`F1` |

详表：`11_专家池与Agent调度_v0.1.md` · **人类 Expert 25 类**：`12_人类专家池_V1.0.md`

## 典型流水线

```
总策划 → 资料总编辑 → 创作引擎 → **文学描写审计** → 文学语感编辑（中文）→ L1+L2 → 03_/
                                              ↓
              日译 → 日文语感编辑 → 田中みどり全文督查 → READY_FOR_TRANSLATION
                                    ↓
              插图：academy-visual-auditor（统调后）· 资产表：academy-story-database
```

## Cursor 常驻 Rule（Layer 1）

| Rule | 路径 |
|------|------|
| 启动门 | `.cursor/rules/00-project-startup-gate.mdc` |
| 日本校园文化 | `.cursor/rules/01-japan-school-culture.mdc` |
| 名古屋环境 | `.cursor/rules/02-nagoya-environment-metrics.mdc` |
| 本格公平 | `.cursor/rules/03-honkaku-fair-play.mdc` |
| 创作红线 | `.cursor/rules/04-creative-redline.mdc` |
| Git 与索引 | `.cursor/rules/05-git-and-index.mdc` |

## 外部 Skill 策略（GitHub / skills.sh）

- **可以装**：与本 IP 对齐的 open skill（日译推敲、textlint-ja、文学分析等），优先 GitHub 高 star / skills.sh 1K+ installs
- **不装**：WPS 及国产中文写作助手（中文排版向，非日文儿童出版）
- **参考已 IP 化**：[novel2hermes_jp](https://github.com/kgmkm/novel2hermes_jp) MoA 推敲 → `academy-jp-voice-editor`；22 领域 → `02_创作原则与世界观/22领域与七范式映射.txt`
- **可选 CLI**：`tools/textlint/`（`@textlint-ja/preset-ai-writing`）— 日译稿完成后本地 lint

## 安装说明（已完成）

Skill 已部署于：

- `skills/academy-series-architect/`
- `skills/academy-research-editor/`
- `skills/academy-engine/`
- `skills/academy-voice-editor/`
- `skills/academy-literary-audit/`
- `skills/academy-jp-voice-editor/`
- `skills/academy-visual-auditor/`
- `skills/academy-story-database/`
- `skills/academy-character-director/`
- `skills/academy-character-scale/`（SSoT · 无独立 Cursor 镜像）
- `skills/academy-canon-governor/`（任务书）
- `skills/academy-gate-orchestrator/`（任务书）
- `.cursor/skills/`（Cursor 项目 skill 镜像 · 不含 character-scale）

在 Cursor 对话中直接说：

- 「按总策划拆第2卷任务包」
- 「立项/受众/钩子怎么定」→ 先读 `10_IP战略参考_ChatGPT对话/00_INDEX.md`
- 「观察社/部活动/校刊线」→ `10_…/E1_校园趣事观察社_战略定稿.md`
- 「Vol1 结构或理紗伏笔」→ `10_…/F1`（**方案 B + B-3**）
- 「资料总编辑补全梅雨相关素材」
- 「用创作引擎写第1卷」
- 「文学审计 / 描写 QA / 变奏检查」→ **academy-literary-audit**
- 「用文学语感编辑过 Hybrid Voice v3」
- 「日文语感编辑过 完整文字稿_日本語.txt」
- 「视觉审计 Vol1 插图 SC03」
- 「更新故事资产表 Vol2 状态」

Agent 应自动读取对应 `SKILL.md`。

## 资料库入口

- **总索引**：`09_日本参考资料库/INDEX.md`
- URL 清单：`09_日本参考资料库/00_来源索引_全站URL清单.txt`（107+ URL）
- L类八大主题：`09_日本参考资料库/12_L类八大主题_完整素材库.txt`
- 归档说明：`09_日本参考资料库/_归档与合并说明.md`

## 规则与笔法

- 红线：`02_创作原则与世界观/创作红线与原则.txt`
- **Project World Metrics**：`docs/world_reference/00_MASTER_ENVIRONMENT_INDEX.md`
- 硬指标速查：`02_创作原则与世界观/名古屋写作硬指标_本格科学参考.md`
- 叙事笔法：`02_创作原则与世界观/写作技巧与叙事笔法.md`
- 正典地图：`00_项目总览/正典文件索引.md`
- 启动门：`docs/00_PROJECT_STARTUP_GATE.md`