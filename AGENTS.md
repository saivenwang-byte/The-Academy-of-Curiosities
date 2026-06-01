# 《学堂趣事录》Agent 编排

本项目使用 **三个协作 skill**（子分身），无需额外下载外部 agent。

## 角色一览

| Skill | 路径 | 角色 | 何时用 |
|-------|------|------|--------|
| **academy-series-architect** | `skills/academy-series-architect/` | 总策划 | 愿景、分卷、阶段、卷任务包、先讨论 |
| **academy-research-editor** | `skills/academy-research-editor/` | 资料总编辑 | 主动搜料、维护 `09_日本参考资料库`、调度知识 |
| **academy-engine** | `skills/academy-engine/` | 创作引擎 | 写正文、实验、角色台词、质量清单 |

定稿门禁（L1 三并列）：

1. **田中みどり** — `japan_campus_consultant_agent.html`（文化）
2. **Project World Metrics** — `docs/world_reference/00_MASTER_ENVIRONMENT_INDEX.md`（环境/科学）
3. **本格公平** — `docs/world_reference/04_MYSTERY_SCIENCE_CASE_STANDARD.md`

**完整验收清单**：`00_项目总览/创作标准与验收流程.md`
## 典型流水线

```
总策划 → 资料总编辑 → 创作引擎 → 文化校准 → 定稿入 03_故事内容/
```

## 安装说明（已完成）

Skill 已部署于：

- `skills/academy-series-architect/`
- `skills/academy-research-editor/`
- `skills/academy-engine/`
- `.cursor/skills/`（Cursor 项目 skill 镜像）

在 Cursor 对话中直接说：

- 「按总策划拆第2卷任务包」
- 「资料总编辑补全梅雨相关素材」
- 「用创作引擎写第1卷」

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