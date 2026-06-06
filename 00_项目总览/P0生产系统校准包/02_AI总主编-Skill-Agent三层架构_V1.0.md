# AI 总主编 — Skill — Agent 三层架构 · V1.0

> **Status**: LOCK · P0 校准包 · 2026-06-07  
> **原则**: Agent 领任务 · Skill 定方法 · 灵魂档案定「是谁」

---

## 架构图

```
IP Owner（宪法权 · LOCK · E06 终签）
        ↓
AI 总主编（单入口 · 读正典 · 选 Skill · 汇总 · 升级裁决）
        ↓
┌───────────────────────────────────────────────────┐
│  Gate A（现在）          Gate B 后（可选）          │
│  · 7 协作 Skill          · 故事生产 Agent           │
│  · character-director    · 事实审核 Agent           │
│  · ACE-B（并行研究轨）    · 视觉出版 Agent           │
└───────────────────────────────────────────────────┘
        ↓
E01–E25 检查表 / 四栏 / 蒸馏 Officer（签核或 ace_distilled）
        ↓
交付物（正文 · Reader · 插图 brief · Gate 报告）
```

---

## 三层职责

| 层 | 负责 | 不负责 |
|----|------|--------|
| **IP Owner** | LOCK · 正典变更 · 商业/授权 · E06 PASS/HOLD | 日常改稿 · 逐句审稿 |
| **AI 总主编** | 任务分解 · Skill 路由 · 冲突上报 · Batch 编排 | 随意改 LOCK · 冒充专家签字 |
| **Skill** | 方法 · 检查表 · 输入输出格式 | 自治改仓库 · 跨 Skill 抢活 |
| **Agent（Gate B+）** | 分支任务包 · 并行生产 | 合并 main · 改同一正典文件 |
| **灵魂档案** | 对白/行为/关系依据 | 写案结构 · 改世界观 |

---

## Gate A（当前）Skill 路由

| 任务类型 | 主 Skill | 辅 Skill |
|----------|----------|----------|
| 卷/系列规划 | series-architect | story-database |
| 单案写作 | engine | voice-editor · character-director |
| 日译润色 | jp-voice-editor | character-director |
| 资料/文化 | research-editor | — |
| 插图/prompt | visual-auditor | character-director |
| 角色表演校验 | **character-director** | characters.yaml + soul |
| 正典冲突 | **canon-governor**（待建） | 正典索引 |
| Gate 汇总 | **gate-orchestrator**（待建） | ACE-B · 四栏 |

---

## Gate B 三 Agent（启用条件）

**全部满足才启用**：

1. A001 角色回测 **PASS**（`06_A001角色一致性回测报告`）
2. 七 Skill 审计 **KEEP**
3. 五人 soul + 关系矩阵 **V0.1 LOCK**
4. Gate A E06 **PASS**

| Agent | Skills | 硬边界 |
|-------|--------|--------|
| 故事生产 | architect · engine · voice · character-director | 不改 yaml LOCK |
| 事实审核 | research · canon-governor · gate-orchestrator | 不改插图定稿 |
| 视觉出版 | visual-auditor · character-director · publication（后建） | 不改正文定稿 |

汇总权：**仅 AI 总主编**。

---

## 明确不做

- ❌ E01–E25 各一个自治 Agent  
- ❌ 十人各一个 Skill  
- ❌ Gate A 期间三 Agent 并行写同一卷  

关联：[`专家组审议_Agent架构与角色灵魂_20260607.md`](../专家组审议_Agent架构与角色灵魂_20260607.md)
