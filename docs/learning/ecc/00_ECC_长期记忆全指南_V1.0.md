# ECC · 长期记忆 · 安装 · 学习 · 部署 · 运行 · 升级 · 全指南 V1.0

> **整理来源**：[今日头条 · ECC 跨会话记忆](https://www.toutiao.com/article/7646217240630755881/)（2026-06-08，抓取不稳定）  
> **校正来源**：[affaan-m/everything-claude-code · README.zh-CN](https://github.com/affaan-m/everything-claude-code/blob/main/README.zh-CN.md) · [Anthropic · Claude Code Memory](https://docs.anthropic.com/en/docs/claude-code/memory)  
> **适用环境**：**Cursor（本仓库主路径）** · Claude Code CLI（完整 ECC 可选）· Windows / macOS / Linux  
> **最后更新**：2026-06-08

---

## 0. 一句话定义

| 概念 | 是什么 |
|------|--------|
| **ECC（Everything Claude Code）** | 开源 **Claude Code 配置全集**：Skills、Agents、Hooks、Rules、MCP、持续学习、AgentShield |
| **跨会话记忆** | 把「上次做到哪、决定了什么、路径在哪」**写到磁盘**，新会话 **先读再干** |
| **本仓库 Lite ECC** | 不装 260+ Skills；用 **`MEMORY.md` + `sessions/` + checkpoint 脚本** 实现 **L2 记忆层** |
| **gstack context-save** | 用户级进度保存（`~/.gstack/`），与本仓库 **sessions/** 互补 |

头条文章核心判断（保留、已对照 GitHub 校正）：

- 长期项目的瓶颈常在 **协作连续性**，不在单次生成质量  
- **Hooks** 可在 session start/end 自动 load/save 上下文  
- **持续学习** 可从会话提取模式 → Skill，但 **创作 IP 须人审升格**（见本仓库范式层）  
- 完整 ECC 体积大；**按 IP 需求白名单接入**，勿与插件 + 手动 full install 叠加

---

## 1. 三层记忆（学习用）

```
┌─────────────────────────────────────────────────────────┐
│ Layer A · 人类规则（慢变）                               │
│ CLAUDE.md · AGENTS.md · .cursor/rules/*.mdc             │
│ → 门禁、红线、Skill 路由、禁止事项                       │
├─────────────────────────────────────────────────────────┤
│ Layer B · Agent 工作记忆（快变）                         │
│ .cursor/memory/MEMORY.md                                │
│ → 当前 Gate、待办、SSOT 路径表、近期决策                 │
├─────────────────────────────────────────────────────────┤
│ Layer C · 会话快照（交接用）                             │
│ .cursor/memory/sessions/YYYY-MM-DD_topic.md             │
│ tools/ecc-memory/bin/memory_checkpoint.*                │
│ → 单次任务完整上下文；可 git 共享                        │
└─────────────────────────────────────────────────────────┘
         ▲                              ▲
         │ sessionStart / Rule          │ sessionEnd / Stop Hook / 手动
         │                              │
    ECC 官方 hooks:              本仓库:
    session-start.js             01-session-memory.mdc
    session-end.js               on_agent_stop.py（lint + 记忆 nudge）
    evaluate-session.js          gstack /context-save（用户级）
```

| 层 | ECC 原话 | 本仓库映射 |
|----|----------|------------|
| **Rules / CLAUDE.md** | 项目级配置、必须遵守 | `CLAUDE.md` + 6 条 always-on Rule |
| **Auto memory / MEMORY** | 跨会话 agent learnings | `.cursor/memory/MEMORY.md` |
| **Session hooks** | 生命周期自动持久化 | `.cursor/hooks.json` + Lite checkpoint |

**与 ECC 四层范式对齐**（详见 `02_对外学习范式_ECC四层案例.md`）：

| ECC 层 | 本指南重点 |
|--------|------------|
| L1 分工 | `AGENTS.md` · academy-* Skills（非 60+ 全量） |
| **L2 记忆** | **本文 + `.cursor/memory/`** |
| L3 安全 | AgentShield 可选 · 本仓库 pre_push / volume_lint |
| L4 学习 | 人审升格 Skill；ECC `/learn` 为附录 |

---

## 2. 环境准备

### 2.1 Cursor 路线（本仓库 · 默认）

| 项 | 要求 |
|----|------|
| IDE | Cursor · hooks 已启用（`.cursor/hooks.json`） |
| Python | 3.x（stop hook · volume_lint） |
| PowerShell | Windows 下运行 `memory_checkpoint.ps1` |
| Git Bash | 可选，运行 `memory_checkpoint.sh` |

**无需** Node/npm 即可使用 Lite 路径。

### 2.2 Claude Code 完整 ECC（可选）

| 项 | 要求 |
|----|------|
| CLI | Claude Code **≥ v2.1.0**（`claude --version`） |
| 插件市场 | 可访问 GitHub marketplace |
| Node | ECC hooks 为跨平台 Node 脚本 |
| **注意** | `/plugin install ecc@ecc` 后 **勿再** `npx ecc-install --profile full`（重复加载） |

---

## 3. 安装

### 3.1 方法一 · 本仓库 Cursor Lite（**推荐 · 已完成脚手架**）

仓库已包含：

```
.cursor/memory/MEMORY.md          # 项目记忆索引
.cursor/memory/sessions/          # checkpoint 目录
.cursor/rules/01-session-memory.mdc
tools/ecc-memory/bin/memory_checkpoint.ps1
tools/ecc-memory/bin/memory_checkpoint.sh
docs/learning/ecc/                # 本指南
```

**验证**：

```powershell
cd "D:\【AI Project】\【The Academy of Curiosities】"
Get-Content .cursor\memory\MEMORY.md -Head 5
.\tools\ecc-memory\bin\memory_checkpoint.ps1 -Topic "test" -DryRun
```

首次非 DryRun 会在 `sessions/` 生成 markdown，并提示更新 `MEMORY.md` 索引。

### 3.2 方法二 · Claude Code ECC 插件

```bash
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```

**Rules 须手动复制**（插件不分发 rules）：

```powershell
git clone https://github.com/affaan-m/everything-claude-code.git
New-Item -ItemType Directory -Force -Path "$HOME\.claude\rules" | Out-Null
Copy-Item -Recurse everything-claude-code\rules\common "$HOME\.claude\rules\"
# 按需：typescript / python / …
```

验证：

```bash
/plugin list ecc@ecc
/ecc:plan "hello"   # 或手动安装后的 /plan
```

### 3.3 方法三 · npm ecc-universal（纯手动 · 无插件）

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code
npm install
# Windows:
.\install.ps1 --profile full
# Unix:
./install.sh --profile full
```

> **警告**：若已用 §3.2 插件安装，**不要**运行 `--profile full`，会 duplicate skills/hooks。

### 3.4 AgentShield（可选 · L3 安全）

```bash
npx ecc-agentshield scan
npx ecc-agentshield scan --fix
```

扫描 CLAUDE.md、hooks、MCP、agents、skills 的配置风险。

---

## 4. 学习路径

| 阶段 | 做什么 | 产出 |
|------|--------|------|
| **L1 读三层** | 区分 CLAUDE.md vs MEMORY.md vs sessions | 知道「改哪一层」 |
| **L2 跑一次 checkpoint** | `memory_checkpoint.ps1 -Topic "试跑"` | `sessions/` 下第一份 md |
| **L3 模拟新会话** | 新 Chat · 让 Agent 读 MEMORY.md · 续做待办 | 验证连续性 |
| **L4 gstack 联用** | `/context-save` 后把摘要写入 MEMORY | 双轨不丢上下文 |
| **L5 完整 ECC** | 仅在 Claude Code 侧装插件 + 自选 Skills | 开发向子项目可用 |

**练习任务（学堂项目向）**

1. checkpoint 主题：`G-SHOT-T A001 分镜修订`  
2. 更新 `MEMORY.md` 待办勾选一项  
3. 读 `02_对外学习范式_ECC四层案例.md` §「不学什么」并写一句团队约定

---

## 5. 部署与运行

### 5.1 日常会话（Cursor）

```
1. 开 Chat → Agent 读 MEMORY.md（Rule 触发）
2. 干活 …
3. 显著变更 → 更新 MEMORY.md
4. 结束 / 交接 → memory_checkpoint.ps1 -Topic "…"
5. （可选）说「save progress」→ gstack context-save
```

### 5.2 Checkpoint 命令

```powershell
# Windows
.\tools\ecc-memory\bin\memory_checkpoint.ps1 -Topic "G-SHOT-T 批次1"
.\tools\ecc-memory\bin\memory_checkpoint.ps1 -Topic "Voice 复审" -Notes "A003 海报场待改"

# 预览不写文件
.\tools\ecc-memory\bin\memory_checkpoint.ps1 -Topic "test" -DryRun
```

```bash
./tools/ecc-memory/bin/memory_checkpoint.sh "G-SHOT-T 批次1"
./tools/ecc-memory/bin/memory_checkpoint.sh "Voice 复审" --notes "A003 海报场待改"
```

生成文件命名：`sessions/YYYY-MM-DD_<slug>.md`

### 5.3 Stop Hook 行为

`.cursor/hooks/on_agent_stop.py`：

1. **始终**：跑 `volume_lint --all -q`（失败 → followup 提醒）  
2. **附加**：若 `sessions/` 无 **7 日内** checkpoint → 信息性提醒保存记忆（**不阻断**）

### 5.4 Claude Code ECC 会话命令（附录）

```bash
/instinct-status          # 持续学习 v2
/learn                    # 从会话提取模式
/checkpoint               # ECC 内置验证状态
/sessions                 # 会话历史管理
/security-scan            # AgentShield
```

环境变量（ECC hooks 调参）：

```bash
export ECC_HOOK_PROFILE=standard
export ECC_DISABLED_HOOKS="post:edit:typecheck"
```

---

## 6. 与 gstack context-save / restore 集成

| 维度 | gstack | 本仓库 Lite ECC |
|------|--------|-----------------|
| 存储位置 | `~/.gstack/` | `.cursor/memory/` |
| 范围 | 用户 · 跨项目 | **本 IP 仓库** |
| 触发 | 「save progress」skill | checkpoint 脚本 · Agent 写 sessions |
| 恢复 | `/context-restore` | 新会话读 MEMORY + 最新 session md |

**推荐工作流**

1. 长调试 / 多仓库 → **gstack save**  
2. Vol1 生产状态 → **MEMORY.md + sessions/**（可 commit）  
3. 会话末：checkpoint **摘要** 进 sessions；**一行** 更新 MEMORY 索引表

---

## 7. 《学堂趣事录》SSOT 指针（记忆层应指向的正典）

Agent 更新 MEMORY 时 **优先链接这些路径**，勿在 MEMORY 里复制大段正文：

| 主题 | 路径 |
|------|------|
| G-CN 阅读入口 | `03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文/00_第一单元_V2_中文正文_阅读索引.md` |
| 五案正文 LOCK | `03_故事内容/…/正式版/01_正文/案0*_HybridVoice_V2.0.txt` |
| V2 迁移总览 | `03_故事内容/…/V2迁移/00_V2迁移总览.md` |
| 分镜 / 插图 MVP 顺序 | `03_故事内容/…/V2迁移/14_第一单元MVP生产顺序_CN→分镜→JP_LOCK_V0.1.md` |
| 范式 · ECC 四层学习 | `00_项目概览/01_分支讨论_范式与框架/02_对外学习范式_ECC四层案例.md` |
| Ralph Loop（迭代任务） | `docs/learning/ralph-loop/` · `tools/ralph-loop/` |

**当前生产态（2026-06-08）**：五案中文 LOCK + Voice v3 → 待 G-CN → **G-SHOT-T**。

---

## 8. 最佳实践

1. **MEMORY 保持一页纸** — 细节进 `sessions/`，SSOT 进正典文件  
2. **checkpoint 要可交接** — 含：做了什么、未做什么、下步命令、相关路径  
3. **创作 IP 禁止自动升格** — L4 学习须主编审；ECC `/learn` 不直接改正典  
4. **不重复安装 ECC** — 插件 vs full install 二选一  
5. **commit 策略** — MEMORY + sessions 可入库共享；含密钥的 checkpoint 禁止 commit  
6. **与 Ralph 分工** — Ralph = 同任务多轮直到 DONE；ECC = 跨会话记住从哪继续  
7. **Stop hook 不替代人** — 7 日无 checkpoint 只是 nudge，不是强制

---

## 9. 升级

### 9.1 Lite 路径（本仓库）

| 组件 | 升级方式 |
|------|----------|
| MEMORY 模板 | 改 `.cursor/memory/MEMORY.md` 结构 · 更新 Rule |
| checkpoint 脚本 | 改 `tools/ecc-memory/bin/*` · 见 CHANGELOG |
| 全指南 |  bump `docs/learning/ecc/00_*` 版本号 |

### 9.2 Claude Code ECC 插件

```bash
/plugin update ecc@ecc
claude --version    # 保持 ≥ 2.1.0
```

关注 [everything-claude-code Releases](https://github.com/affaan-m/everything-claude-code/releases) — v2.0 起含 `ecc2/` Rust 控制层（`dashboard` / `sessions` / `daemon`）。

### 9.3 AgentShield

```bash
npx ecc-agentshield@latest scan
```

---

## 10. 故障排查

| 现象 | 原因 | 处理 |
|------|------|------|
| Agent 不读 MEMORY | Rule 未加载 | 确认 `.cursor/rules/01-session-memory.mdc` 存在；Cursor Settings → Rules |
| checkpoint 脚本无法执行 | 执行策略 | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Stop hook 无输出 | volume_lint 通过且无记忆 nudge | 正常；lint 失败才有 blocking 式 followup |
| 装 ECC 后 skill 重复 | 插件 + full install 叠加 | 只保留一种；清理 `~/.claude/skills` 重复项 |
| hooks 重复加载报错 | plugin.json 显式声明 hooks | ECC 上游：勿在 plugin.json 加 hooks 字段 |
| 头条原文打不开 | 网络/反爬 | 以 GitHub README.zh-CN 为准 |

---

## 附录 A · ECC 组件地图（查阅用）

| 目录 | 内容 |
|------|------|
| `agents/` | 36+ 子 Agent（planner、reviewer、…） |
| `skills/` | 260+ 工作流（continuous-learning、security-scan、…） |
| `hooks/` | session-start/end、evaluate-session、strategic-compact |
| `rules/` | 须手动复制到 `~/.claude/rules/` |
| `commands/` | 斜杠命令兼容层 |
| `ecc2/` | ECC 2.0 alpha · Rust CLI |

## 附录 B · 本仓库 **未** 默认安装的内容

- 64 代理 / 261 Skills 全量  
- `multi-*` 命令（需 `npx ccg-workflow`）  
- ECC 内置 session-start.js（用 Lite Rule + checkpoint 代替）  
- 自动 `/learn` 升格（范式层要求人审）

---

## 附录 C · 相关链接

- [everything-claude-code](https://github.com/affaan-m/everything-claude-code)  
- [AgentShield](https://github.com/affaan-m/agentshield)  
- [ecc-universal npm](https://www.npmjs.com/package/ecc-universal)  
- 本仓库 Ralph Loop：[`docs/learning/ralph-loop/`](../ralph-loop/)

---

最后更新：2026-06-08 · V1.0
