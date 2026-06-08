# Ralph Loop · 学习资料

> **可执行脚本**：[`tools/ralph-loop/`](../../../tools/ralph-loop/)  
> **全指南**：[`00_全指南_V1.0.md`](./00_全指南_V1.0.md)

---

## 文件

| 文件 | 用途 |
|------|------|
| [`00_全指南_V1.0.md`](./00_全指南_V1.0.md) | 安装 · 学习 · 部署 · 运行 · 升级 · 故障排查 |
| [`examples/academy-g-shot-map/`](./examples/academy-g-shot-map/) | 《学堂趣事录》Shot Map 批量任务 prompt 示例 |

---

## 快速开始

**Claude Code（官方插件）**

```bash
/plugin install ralph-loop@claude-plugins-official
/ralph-loop "你的任务…输出 <promise>COMPLETE</promise>" --max-iterations 20
```

**本仓库（Bash / Windows）**

```bash
cd tools/ralph-loop/workspace
cp ../templates/prompt.md.template ./prompt.md
# 编辑 prompt.md 后：
../bin/ralph.sh 10          # Git Bash / macOS / Linux
# 或 PowerShell：
../bin/ralph.ps1 -MaxIterations 10
```

---

## 来源

- [今日头条 · Boris Cherny 访谈](https://www.toutiao.com/article/7648314194437227060/)
- [Anthropic ralph-loop 插件](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop)
