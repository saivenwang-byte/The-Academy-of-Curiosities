# ECC 四层基础设施框架 · IP 成立的 Agent 底座

> **Status**: FRAMEWORK DRAFT — 主编共建  
> **开启日期**: 2026-06-04  
> **定位**: IP 成立前置条件中的 **「第 0 层」** — 在创作正典、视觉、商业之前，先让长期协作机器跑起来  
> **性质**: 讨论稿，定案后升格至 `docs/00_AGENT_INFRASTRUCTURE.md`

---

## 0. 为什么单独开这一层

《学堂趣事录》是 **50 卷 · 多年 · 多 Agent 协作** 项目。  
IP 能否「成立并持续产出」，不只取决于故事写得好不好，还取决于：

> **重启会话后，AI 是否还能接着昨天的标准、记忆、安全检查往下干。**

ECC 四层框架描述的是 **生产机器本身**；`00_讨论主稿` 描述的是 **机器要产出的 IP 产品**。  
两层都 PASS，才算真正「IP 成立」。

---

## 1. 四层总览（主编定义 · v0.1）

```
┌─────────────────────────────────────────────────────────┐
│  第四层 · 持续学习    从会话中提取可复用模式 → 新 Skill   │
├─────────────────────────────────────────────────────────┤
│  第三层 · 安全扫描    AgentShield · 执行前自动安检         │
├─────────────────────────────────────────────────────────┤
│  第二层 · 记忆持久化  Hooks · 跨会话上下文自动存取         │
├─────────────────────────────────────────────────────────┤
│  第一层 · 技能体系    60+ 场景化专业代理 · 按需路由       │
└─────────────────────────────────────────────────────────┘
                              ↓
              《学堂趣事录》7 IP Skill + 6 Rule + 7 Script
                              ↓
              Vol1–50 正文 · 插图 · 日译 · 资产表
```

| 层 | ECC 能力 | 对本 IP 的含义 |
|----|----------|----------------|
| **L1 技能体系** | 60+ 专门化代理，各管一场景 | 创作/审计/安全/文档/测试等 **分工明确**，不靠一个通用 Agent 硬扛 |
| **L2 记忆持久化** | Hooks 自动保存/加载上下文 | 今天改的 Vol2 稿、昨天定的视觉坐标，**明天新会话仍能接续** |
| **L3 安全扫描** | AgentShield 执行前安检 | AI 写代码、改正典、跑脚本前 **自动拦截** 破坏性/越权操作 |
| **L4 持续学习** | 从会话提取模式 → 新 Skill | Vol1 插图教训、日译踩坑 **沉淀为可复用 Skill**，越写越准 |

---

## 2. 第一层 · 技能体系

### 2.1 ECC 原意

预置 **60+ 专门化 AI 代理**，每个代理负责一个具体场景，例如：

- 代码审查代理
- 安全扫描代理
- 性能优化代理
- 文档生成代理
- 测试编写代理

**设计原则**：通用 Agent 做路由；**专业 Agent 做执行**。

### 2.2 本仓库现状映射

| 类别 | 数量 | 落地位置 | 状态 |
|------|------|----------|------|
| **IP 专用 Skill** | 8 | `skills/academy-*` · `.cursor/skills/` | ✅ 已部署 |
| **Cursor 常驻 Rule** | 6 | `.cursor/rules/*.mdc` | ✅ always-on |
| **Lint / 脚本代理** | 7 | `scripts/*.py` | ✅ 可复跑 |
| **L1 门禁工具** | 1 | `japan_campus_consultant_agent.html` | ✅ 田中五维 |
| **用户全局 Skill 池** | 60+ | Cursor 用户级 `~/.cursor/skills/` · gstack 等 | 🟡 可用但未与本 IP 路由表绑定 |
| **ECC 预置 60 代理清单** | — | 未入库 | 🔴 待 ECC 导出 / 主编筛选 |

#### IP 专用 Skill 一览（L1 子集 · 已存在）

| Skill | 场景 |
|-------|------|
| `academy-series-architect` | 总策划、分卷、任务包 |
| `academy-research-editor` | 资料检索、09_ 维护 |
| `academy-engine` | 正文、实验、质量清单 |
| `academy-voice-editor` | 中文 Hybrid Voice |
| `academy-jp-voice-editor` | 日文语感推敲 |
| `academy-visual-auditor` | 插图 prompt / 统调 |
| `academy-story-database` | 200 篇 Case 资产 |
| `academy-character-scale` | 角色身高/年级尺度 |

#### 建议从 ECC 60+ 中 **优先接入** 的场景（与本 IP 强相关）

| 优先级 | ECC 类代理 | 本 IP 用途 | 现状 |
|--------|------------|------------|------|
| P0 | 文档生成 | 卷任务包、Case Card、正典同步 | 🟡 靠 engine/architect 合并 |
| P0 | 代码/脚本审查 | `scripts/` · `tools/` 变更 | 🔴 无专用 Skill |
| P1 | 安全扫描 | 见第三层 | 🔴 无 AgentShield |
| P1 | 测试编写 | lint 脚本回归 | 🟡 有 lint，无 test 套件 |
| P2 | 性能优化 | 大库检索、插图批处理 | ⚪ 暂不需要 |
| P2 | CI 调查 | PR check 失败根因 | 🟡 用户有 `gh-fix-ci` 全局 Skill |

### 2.3 L1 成立条件（讨论稿）

| # | 条件 | 目标 |
|---|------|------|
| S1 | IP 流水线 7+ Skill 可触发、可路由 | ✅ 已达成 |
| S2 | **Skill 路由表** 写入正典（何时用谁） | 🟡 `AGENTS.md` 有，缺 ECC 扩展表 |
| S3 | ECC 60+ 中 **≥10 个** 与本 IP 绑定并文档化 | 🔴 待主编提供 ECC 清单或导出 |
| S4 | 禁止「无 Skill 硬写正文/改正典」的例外清单 | 🟡 Rule 有，未写成门禁 |

**开放问题 L1-1**：ECC 的 60+ 代理，是 **全部纳入** 还是 **按 IP 需求白名单接入**？

**开放问题 L1-2**：是否需要新增 IP 级代理，例如 `academy-illustration-batch`（批量插图 QC）、`academy-principle-dedup`（50 卷原理去重）？

---

## 3. 第二层 · 记忆持久化

### 3.1 ECC 原意

每次重启会话，AI **牢记之前的工作**。  
通过 **Hooks 机制**，自动保存和加载上下文 — 「今天写的代码，明天 AI 还能接着写」。

### 3.2 本仓库现状映射

| 记忆类型 | 机制 | 位置 | 跨会话？ |
|----------|------|------|----------|
| **正典记忆** | 文件即真理 | `00_项目总览/` · `docs/` · `02_/` | ✅ 永久 |
| **启动记忆** | 入口强制读 | `CLAUDE.md` · 6× Rule | ✅ 每会话注入 |
| **流水线记忆** | Skill + 状态文件 | Case Card · scorecard yaml · 故事总表 | ✅ 文件持久 |
| **Hook 自动化** | `stop` → lint 提醒 | `.cursor/hooks/on_agent_stop.py` | 🟡 仅 lint，**不存上下文** |
| **会话工作记忆** | context-save / restore | 用户全局 gstack Skill | 🔴 **未接入本仓库** |
| **Agent 转录** | Cursor transcripts | `.cursor/projects/.../agent-transcripts/` | 🟡 只读，未结构化 |

#### 当前 Hook 能力（极简）

```json
// .cursor/hooks.json
"stop" → on_agent_stop.py → volume_lint 失败则提示跑 pre_push_check
```

**缺口**：无 `session_start` 加载、无自动写 `WORKING.md`、无决策增量归档。

### 3.3 L2 成立条件（讨论稿）

| # | 条件 | 目标 |
|---|------|------|
| M1 | 正典 + 入口文档完整（Layer 0） | ✅ |
| M2 | 每卷 **工作状态** 可文件化查询（Case/Scene/正文状态） | 🟡 Vol1–2 有，Vol3+ 未注册 |
| M3 | **会话结束 Hook** 写入工作摘要（非仅 lint） | 🔴 |
| M4 | **会话开始 Hook** 加载上次摘要 + 未决项 | 🔴 |
| M5 | 与 `context-save` / `context-restore` 打通或等效 | 🔴 |

**建议 M3/M4 最小实现（讨论用，未开工）**：

```
.cursor/hooks/
  on_agent_stop.py      ← 扩展：写 .cursor/working_buffer.md
  on_session_start.py   ← 新建：读 buffer + 指向最新决策记录
.cursor/working_buffer.md   ← gitignore 或 纳入版本（待决）
```

**开放问题 L2-1**：工作缓冲 `working_buffer.md` 是否 **进 Git**？（进 = 可追溯；不进 = 隐私/噪音少）

**开放问题 L2-2**：记忆边界 — 哪些只存 Hook 缓冲，哪些必须升格为正典？

---

## 4. 第三层 · 安全扫描（AgentShield）

### 4.1 ECC 原意

内置 **AgentShield**：AI 编程 **执行前** 自动安全检查，保证底层安全。

### 4.2 本仓库现状映射

| 安全层 | 机制 | 状态 |
|--------|------|------|
| **Git 安全** | User Rule：禁 force push、禁改 git config | ✅ 用户级 |
| **创作安全** | 五条红线 · 6 Rule · startup gate | ✅ 内容向 |
| **推送前检查** | `pre_push_check.py` | ✅ 手动/CI |
| **Hook 提醒** | stop → volume_lint | 🟡 被动 |
| **AgentShield 执行前拦截** | rm -rf、改正典、删 03_ 等 | 🔴 **无** |
| **Skill 供应链审计** | skill-vetter | 🟡 全局有，未绑定本仓库安装流程 |

#### 本 IP 特有风险面（AgentShield 应覆盖）

| 风险 | 示例 | 期望动作 |
|------|------|----------|
| 正典误改 | 改 `人物名称定稿.txt` 无讨论 | 警告 + 要求分支讨论 CLOSED |
| 讨论稿当正典 | 把 `05_创作对话记录` 写进正文 | lint + Rule 拦截 |
| 破坏性命令 | `git reset --hard`、批量删 PNG | 执行前确认 |
| 越权插图 | Vol1 出现 Vol11 角色 | visual-auditor + character-scale |
| Secrets | `.env` 进 commit | pre-commit / shield |

### 4.3 L3 成立条件（讨论稿）

| # | 条件 | 目标 |
|---|------|------|
| G1 | `pre_push_check` + `volume_lint` 日常必跑 | 🟡 靠自觉 / CI |
| G2 | **执行前 Hook**（或 Cursor 等价）拦截高危操作清单 | 🔴 |
| G3 | 正典路径 **写保护等级** 文档化（L0 禁 AI 单改） | 🔴 |
| G4 | 新 Skill 安装前 **vetter 流程** 写入 `AGENTS.md` | 🔴 |

**开放问题 L3-1**：AgentShield 是 **ECC 内置** 还是本项目 **自研 Hook 子集** 即可？

**开放问题 L3-2**：L0 正典（人名、品牌、4年2組）是否设为 **AI 不可直接 Write**，只能产出 patch 建议？

---

## 5. 第四层 · 持续学习

### 5.1 ECC 原意

ECC 从 **每次会话** 中自动提取可复用的模式和技能，越用越强。

### 5.2 本仓库现状映射

| 学习机制 | 示例 | 状态 |
|----------|------|------|
| **人工升格** | Vol1 教训 → `academy-visual-auditor` | ✅ 已发生 |
| **会议纪要归档** | `00_归档/2026-06-03_方案A/` | ✅ 手动 |
| **决策记录** | 本分支 `01_决策记录.md` | 🟡 刚建 |
| **自动模式提取** | self-improving-agent | 🔴 未接入 |
| **Skill 自动生成** | skillify / 从 transcript _codegen | 🔴 未接入 |

#### 已沉淀的「教训 → 规则」范例（L4 目标形态）

| 教训来源 | 沉淀去向 |
|----------|----------|
| 私服/上履き/椅背结露 | `academy-visual-auditor` · 风格规范 v2 |
| 绘本体 / Hybrid Voice | `academy-voice-editor` · 语感决策记录 |
| 4年2組 LOCK | `00_SCHOOL_CLASS_CANON_LOCKED.md` |
| 日语文案手改 | `lineup_text_canon.py` · 锁定 md |

### 5.3 L4 成立条件（讨论稿）

| # | 条件 | 目标 |
|---|------|------|
| E1 | **教训升格 SOP**：何时从讨论 → Rule/Skill/脚本 | 🔴 |
| E2 | 每卷完成后 **retro 模板**（固定 5 问） | 🔴 |
| E3 | 可选：会话结束提取 **候选 Skill 片段** 进队列 | 🔴 |
| E4 | 季度 prune：过时 Skill/Rule 清理 | 🔴 |

**开放问题 L4-1**：持续学习是 **全自动**（ECC 提取）还是 **主编审核后升格**（推荐后者，防污染正典）？

---

## 6. 四层与「IP 成立」的挂接方式

建议把 ECC 四层作为 **IP 成立的前置 Layer 0**：

```
IP 成立 = Layer 0 (ECC 四层)  +  Layer 1–6 (创作/质量/视觉/资产/运营/商业)
```

| IP 成立方案 | Layer 0 最低要求 |
|-------------|------------------|
| **方案甲** 创作 IP | S1+S2, M1+M2, G1, E1 文档化 |
| **方案乙** 产品 IP | + M3, G2+G3, E2 每卷 retro |
| **方案丙** 商业 IP | + S3, M4+M5, G4, E3 审核队列 |

---

## 7. 与本仓库现有 Layer 架构的对照

`docs/00_AGENT_DEPLOYMENT_STATUS.md` 现有分层：

```
Layer 0   CLAUDE.md + AGENTS.md
Layer 1   .cursor/rules/
Layer 2   skills/academy-*
Layer 3   scripts/
Layer 4   docs/ · 02_/ · 09_/ · HTML 正典
```

**建议关系（不替换，而是正交）**：

| 现有 Layer | ECC 四层 | 说明 |
|------------|----------|------|
| Layer 0 入口 | L2 记忆 + L1 路由 | 入口负责「读什么」 |
| Layer 1 Rule | L3 安全子集 | Rule = 内容安全；AgentShield = 执行安全 |
| Layer 2 Skill | **L1 核心** | IP Skill 是 60+ 的子集 |
| Layer 3 Script | L1 + L3 | 脚本 = 可验证的安全网 |
| Layer 4 正典 | L2 长期记忆 | 文件即永久记忆 |
| （缺） | **L4 持续学习** | 需新建 SOP + 可选 Hook |

---

## 8. 建议实施路线（讨论用 · 未开工）

| 阶段 | 交付 | 对应层 |
|------|------|--------|
| **Phase A** | 主编确认 ECC 60+ 白名单 → 写入 `AGENTS.md` 扩展表 | L1 |
| **Phase B** | `working_buffer.md` + stop/start Hook 最小闭环 | L2 |
| **Phase C** | 正典写保护等级 + pre-exec 高危清单 Hook | L3 |
| **Phase D** | `教训升格 SOP.md` + Vol1 retro 试跑 | L4 |
| **Phase E** | 合成 `docs/00_AGENT_INFRASTRUCTURE.md` 升格正典 | 全层 |

---

## 9. 待主编确认（本场）

1. **ECC 60+ 代理**：能否提供清单或导出？我们按白名单接入，还是全量映射？  
2. **Layer 0 是否纳入 IP 成立**：方案甲是否要求 Phase A+B 最低闭环？  
3. **记忆进 Git 吗**：`working_buffer.md` / `context-save` 快照是否版本化？  
4. **AgentShield 来源**：等 ECC 内置，还是 Phase C 先用 Hook 自研？  
5. **持续学习审核权**：全自动提取 vs **主编审核后升格** — 你选哪种？

---

## 10. 关联文件

| 文件 | 关系 |
|------|------|
| `00_讨论主稿_IP成立前置条件.md` | IP 产品维成立条件 |
| `01_决策记录.md` | 定案写入处（含 Layer 0 节待增） |
| `docs/00_AGENT_DEPLOYMENT_STATUS.md` | 现有部署状态 |
| `docs/00_AGENT_CAPABILITY_MAP.md` | 能力对照 |
| `AGENTS.md` | Skill 路由入口 |

---

最后更新：2026-06-04 · v0.1 主编四层框架录入
