# Claude Code · 本仓库入口

> **不要在此目录复制 Skill 正文** — 与 Cursor 共用一套源文件。

## 每次进入项目

1. 读根目录 [`../CLAUDE.md`](../CLAUDE.md)
2. 读 [`../AGENTS.md`](../AGENTS.md)
3. 读 [`../docs/00_AGENT_DEPLOYMENT_STATUS.md`](../docs/00_AGENT_DEPLOYMENT_STATUS.md)

## Skills 路径

| 用途 | 路径 |
|------|------|
| 全部 Skill | [`../skills/`](../skills/) |
| Cursor 镜像 | [`../.cursor/skills/`](../.cursor/skills/) |

触发词与路由见 `../docs/00_AGENT_CAPABILITY_MAP.md`。

## 推送前

```bash
python scripts/pre_push_check.py
python scripts/volume_lint.py --all
```

---

最后更新：2026-06-02 · 第五批
