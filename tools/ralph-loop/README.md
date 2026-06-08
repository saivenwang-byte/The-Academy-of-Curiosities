# tools/ralph-loop · 可运行 Ralph Loop 脚手架

> **文档**：[`docs/learning/ralph-loop/`](../../docs/learning/ralph-loop/)  
> **原则**：HITL 先试 1 轮 · AFK 必设 max iterations · 独立 git 分支

---

## 目录结构

```
tools/ralph-loop/
├── README.md           ← 本文件
├── bin/
│   ├── ralph.sh        Git Bash / macOS / Linux
│   └── ralph.ps1       Windows PowerShell
├── templates/
│   ├── prompt.md.template
│   └── RALPH_TASK.md.template   Cursor 社区风格
├── examples/
│   └── academy-g-shot-map/      学堂项目示例
└── workspace/          运行时工作区（复制 template 到此）
    ├── prompt.md       ← 你编辑的任务（勿提交含密钥内容）
    ├── progress.txt    ← 每轮追加（可选）
    └── .ralph/         ← 日志（gitignore）
```

---

## 使用

### 1. 准备工作区

```powershell
cd tools/ralph-loop/workspace
Copy-Item ..\templates\prompt.md.template .\prompt.md
# 编辑 prompt.md
```

### 2. 运行（HITL：先 MaxIterations=1）

```powershell
# PowerShell（需 PATH 中有 claude CLI，或改 ralph.ps1 里的 $AgentCmd）
..\bin\ralph.ps1 -MaxIterations 1

# Git Bash
../bin/ralph.sh 1
```

### 3. 完成条件

Agent 输出含 `<promise>COMPLETE</promise>` 时脚本退出 0；否则打满 max 退出 1。

---

## Claude Code 官方（推荐）

不依赖本目录脚本，在 Claude Code 内：

```bash
/plugin install ralph-loop@claude-plugins-official
/ralph-loop "<prompt>" --completion-promise "COMPLETE" --max-iterations 50
```

---

## Windows 注意

Claude Code 官方 Ralph 插件 Stop Hook 需 **Git for Windows** 的 `bash.exe`。见全指南 §2.1。

---

最后更新：2026-06-08
