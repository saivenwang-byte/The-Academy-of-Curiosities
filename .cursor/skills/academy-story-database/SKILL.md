---
name: academy-story-database
version: 1.0.0
description: 学堂趣事录 200 篇故事资产库与 Case Card 状态管理。当用户需要维护故事总表、Case Card、卷状态、线索/实验索引或规划 50 卷时触发。
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# 学堂趣事录 · 故事资产库 · Story Database

## 何时触发

- 新建/更新 **Case Card** 或卷级任务包
- 维护 **200 篇** 故事总表（编号、状态、科学主题）
- 查「哪卷用了什么机制/季节/角色弧」
- 与 `academy-series-architect` 联调 50 卷规划

## 启动必读

1. `docs/00_PROJECT_STARTUP_GATE.md`
2. `docs/world_reference/04_MYSTERY_SCIENCE_CASE_STANDARD.md`
3. `docs/story_database/00_story_asset_table.md`（主表模板）
4. `docs/volume_planning/`（分卷执行卡）
5. `00_项目总览/正典文件索引.md`

## 主表字段（Case / 卷级）

| 字段 | 说明 |
|------|------|
| `id` | 如 `Vol01` / `Story-001` |
| `title_cn` / `title_jp` | 中日书名 |
| `status` | `IDEA` · `OUTLINE` · `DRAFT` · `PENDING_REVIEW` · `READY_FOR_SAMPLE` · `READY_FOR_TRANSLATION` · `READY_FOR_ARTIST` · `LOCKED` |
| `month_nagoya` | 名古屋月份（环境门） |
| `science_core` | 核心科学机制（一句话） |
| `fair_clues` | ≥3 公平线索摘要 |
| `experiment_id` | 可复现实验编号/链接 |
| `characters` | 主役 |
| `l1_gates` | 文化/环境/公平 过门日期或 Y/N |
| `paths` | 正文、Case Card、插图夹路径 |
| `notes` | 待决项 |

**状态铁律**：未过 L1 → 不得 `READY_FOR_*`（见 startup gate）

## 工作流

```
series-architect 拆卷
  → 在本表新增行（IDEA/OUTLINE）
  → research-editor 填 L2 引用
  → engine 写 Case Card + 正文
  → voice-editor / jp-voice-editor
  → 更新 l1_gates + status
  → visual-auditor（插图行）
```

## 输出

- 更新 `docs/story_database/00_story_asset_table.md`
- 新卷 Case Card：`docs/volume_planning/VolXX_case_card.md`（或项目既有命名）
- 重大变更：同步 `00_项目总览/正典文件索引.md`

## 与 architect 分工

| 角色 | 负责 |
|------|------|
| series-architect | 50 卷战略、阶段、优先级 |
| **story-database** | 表结构、状态、跨卷检索、Case 元数据 |
| engine | 单卷正文与实验细节 |

## 第二批（脚本）

- `scripts/case_card_lint.py` — Case Card / 故事表 / Vol1 插图 lint（见 `scripts/README.md`）

---

最后更新：2026-06-02 · 合并方案第一批
