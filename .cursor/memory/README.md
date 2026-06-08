# `.cursor/memory/` · 项目会话记忆层（Lite ECC）

> **全指南**：[`docs/learning/ecc/00_ECC_长期记忆全指南_V1.0.md`](../../docs/learning/ecc/00_ECC_长期记忆全指南_V1.0.md)  
> **Checkpoint 工具**：[`tools/ecc-memory/`](../../tools/ecc-memory/)

---

## 三层分工（本仓库）

| 层 | 文件 | 谁写 | 内容 |
|----|------|------|------|
| **人类规则** | `CLAUDE.md` · `.cursor/rules/` | 主编 / 架构 | 启动门禁、红线、Skill 路由 |
| **Agent 工作记忆** | **`MEMORY.md`**（本目录） | Agent + 人审 | 当前阶段、待办、决策、路径 SSOT |
| **会话快照** | `sessions/YYYY-MM-DD_topic.md` | Agent / checkpoint 脚本 | 单次交接的完整上下文 |

**Hooks**：`.cursor/hooks/on_agent_stop.py` — 保留 `volume_lint`；若无近期 checkpoint 则 **信息性** 提醒（不阻断）。

---

## Agent 约定

1. **会话开始**：读 `MEMORY.md`，再读 `CLAUDE.md` Layer 0  
2. **显著状态变化**：更新 `MEMORY.md` 的「当前快照」与「待办」  
3. **会话结束 / 长任务交接**：运行 `tools/ecc-memory/bin/memory_checkpoint.*` 或写入 `sessions/`  
4. **不写入**：密钥、未核实对外数据、临时草稿正文（正文仍在 `03_故事内容/`）

---

## 与 gstack 的关系

| 工具 | 范围 | 何时用 |
|------|------|--------|
| **gstack `/context-save`** | 用户级 `~/.gstack/` · 跨仓库 | 个人机器上保存任意会话进度 |
| **本目录 `sessions/`** | **本仓库** · 可 git 共享 | IP 生产流水线交接、Vol1 状态 |

推荐：gstack 保存 **过程细节**；checkpoint 写入 **项目可提交摘要**；`MEMORY.md` 保持 **一页纸当前态**。

---

## 目录

```
.cursor/memory/
├── README.md          ← 本文件
├── MEMORY.md          ← 项目记忆索引（Agent 每会话读）
└── sessions/          ← 按日期/topic 的 checkpoint
    └── .gitkeep
```

---

最后更新：2026-06-08
