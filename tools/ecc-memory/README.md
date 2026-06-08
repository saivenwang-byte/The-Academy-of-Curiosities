# tools/ecc-memory · 会话 checkpoint 脚手架

> **文档**：[`docs/learning/ecc/`](../../docs/learning/ecc/)  
> **写入目录**：[`.cursor/memory/sessions/`](../../.cursor/memory/sessions/)

---

## 目录结构

```
tools/ecc-memory/
├── README.md           ← 本文件
├── bin/
│   ├── memory_checkpoint.sh    Git Bash / macOS / Linux
│   └── memory_checkpoint.ps1   Windows PowerShell
└── templates/
    └── checkpoint.md.template
```

---

## 使用

### Windows

```powershell
cd "D:\【AI Project】\【The Academy of Curiosities】"
.\tools\ecc-memory\bin\memory_checkpoint.ps1 -Topic "G-SHOT-T A001"
.\tools\ecc-memory\bin\memory_checkpoint.ps1 -Topic "试跑" -DryRun
```

### Bash

```bash
./tools/ecc-memory/bin/memory_checkpoint.sh "G-SHOT-T A001"
./tools/ecc-memory/bin/memory_checkpoint.sh "试跑" --dry-run
```

生成：` .cursor/memory/sessions/YYYY-MM-DD_<slug>.md`

**事后**：在 `.cursor/memory/MEMORY.md` 的「会话 checkpoint 索引」表补一行（Agent 或人）。

---

## 与 Stop Hook

`.cursor/hooks/on_agent_stop.py` 若发现 **7 日内无** sessions 文件，会 **信息性** 提醒运行本脚本（不阻断 volume lint）。

---

最后更新：2026-06-08
