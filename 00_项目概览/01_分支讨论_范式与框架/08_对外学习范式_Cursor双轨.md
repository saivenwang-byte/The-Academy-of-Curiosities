# 对外学习范式 · Cursor Rules + Skills

> **性质**: 学习卡片 · 三段式 · 无项目绑定  
> **主透镜**: D1 · D2 · C1（路由）  
> **来源**: Cursor 产品形态（Rules always-on + Skills on-demand）

---

## 学习三段式

### [Cursor] · Rules + Skills 双轨

**学什么**

- **Rules = Ring 2 常驻 ISA**：每次会话自动注入的不可协商约束（少而精，~6 条量级优于 20 条）  
- **Skills = L1 协处理器**：按意图触发，带完整工作流与检查清单  
- **双轨分工**：Rule 管「绝不能做什么」；Skill 管「怎么做一整条流水线」  
- **项目入口单文件**：`CLAUDE.md` / `AGENTS.md` 类 Layer 0，避免 Agent 找不到地图  

**不学什么**

- **Rule 堆叠替代 Skill**：把 50 步流程全塞进 always-on Rule → 上下文浪费、难维护  
- **Skill 替代 Rule 红线**：伦理/安全/文化红线不应只在 Skill 里，会话未触发 Skill 时会漏  
- **每仓库复制 60 个全局 Skill**：应用职能路由 + 白名单，非全量镜像  
- **把范式讨论写进 Rule**：控制平面内容应进讨论区/决策记录，升格后再 distill 成短 Rule  

**为什么**

- 我们已有 **6 Rule + 7 IP Skill** 形态，缺的是与 **ECC 四层**、**A2 平面** 的 **命名对齐**  
- Cursor 双轨 ≈ **L3 常驻约束 + L1 按需 syscall**，与 `05_` 架构参照一致  

**抽象层**

- **双轨协作模型**：Always-on 约束轨 + On-demand 工作流轨  

---

## 同构映射（D2）

| Cursor | ECC/本参照系 | 计算机等价 |
|--------|--------------|------------|
| Rules `.mdc` | L3 部分 + L1 ISA 子集 | 微码 / 特权指令 |
| Skills `SKILL.md` | L1 协处理器 | 专用指令扩展 |
| `AGENTS.md` 路由 | L1 路由表 | 跳转表 |
| Hooks | L2 + L3 执行点 | 中断 / 探针 |
| User Rules | Ring 0 外延 | 机器级策略 |

---

## 反模式（D3 → FWP 候选）

| 反模式 | 后果 | 范式对策 |
|--------|------|----------|
| Rule 膨胀 | 上下文噪音、冲突 | Rule ≤N 条；其余升格 Skill |
| 无路由表 | 错误 Skill 或未触发 | `AGENTS.md` 意图→Skill 表 |
| Skill 无边界 | 越权写 Ring 0 | L3 能力白名单 |
| 讨论区内容直下 Rule | 配置漂移 | A2：控制→数据 distill |

---

## 可迁移原则（候选）

| # | 原则 |
|---|------|
| CR-1 | **Rule 短、Skill 长** |
| CR-2 | **入口单文件指向地图** |
| CR-3 | **意图路由先于执行** |
| CR-4 | **升格：讨论区 distill → Rule 摘要 + Skill 详流程** |

---

## 与 ECC 案例关系

| 系统 | 补 ECC 哪块 |
|------|-------------|
| ECC 四层 | 全栈愿景 |
| Cursor 双轨 | **L1+L3 落地形态**（本仓库已在用） |
| gstack ship | L3+L4 流水线（待写卡片） |

---

最后更新：2026-06-04
