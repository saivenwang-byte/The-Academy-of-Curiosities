# ECC · 长期记忆 · 学习资料

> **可执行脚本**：[`tools/ecc-memory/`](../../../tools/ecc-memory/)  
> **全指南**：[`00_ECC_长期记忆全指南_V1.0.md`](./00_ECC_长期记忆全指南_V1.0.md)  
> **项目记忆索引**：[`../../.cursor/memory/MEMORY.md`](../../.cursor/memory/MEMORY.md)

---

## 文件

| 文件 | 用途 |
|------|------|
| [`00_ECC_长期记忆全指南_V1.0.md`](./00_ECC_长期记忆全指南_V1.0.md) | 安装 · 学习 · 部署 · 运行 · 升级 · 故障排查 |
| [`../../.cursor/memory/README.md`](../../.cursor/memory/README.md) | 本仓库 Lite ECC 记忆层说明 |
| [`../../.cursor/rules/01-session-memory.mdc`](../../.cursor/rules/01-session-memory.mdc) | Agent 会话记忆 Rule |

---

## 快速开始（本仓库 · Cursor Lite）

**1. 会话开头** — Agent 读 `.cursor/memory/MEMORY.md`（Rule 已指向）

**2. 会话结束 / 交接** — 手动 checkpoint：

```powershell
cd "D:\【AI Project】\【The Academy of Curiosities】"
.\tools\ecc-memory\bin\memory_checkpoint.ps1 -Topic "G-SHOT-T 分镜推进"
```

```bash
./tools/ecc-memory/bin/memory_checkpoint.sh "G-SHOT-T 分镜推进"
```

**3. 或用 gstack** — 对话中说「save progress」/ `/context-save`，再按需同步摘要到 `MEMORY.md`

---

## 完整 ECC（可选 · Claude Code CLI）

```bash
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
# rules 需手动复制，见全指南 §3
```

---

## 来源

- [今日头条 · ECC 跨会话记忆](https://www.toutiao.com/article/7646217240630755881/)（原文抓取不稳定，内容已对照 GitHub 校正）
- [affaan-m/everything-claude-code · README.zh-CN](https://github.com/affaan-m/everything-claude-code/blob/main/README.zh-CN.md)
- 本仓库范式层：[`00_项目概览/01_分支讨论_范式与框架/02_对外学习范式_ECC四层案例.md`](../../../00_项目概览/01_分支讨论_范式与框架/02_对外学习范式_ECC四层案例.md)
