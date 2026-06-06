# Git 索引清理 · 过期/错误版本 · 2026-06-09

> **操作**：`git rm --cached` — 文件 **保留本地**，仅从 Git 跟踪移除。  
> **规则**：见 [`.gitignore`](../.gitignore) 对应段。

---

## 已移出索引

| 类别 | 路径模式 | 原因 |
|------|----------|------|
| Reader 构建 HTML | `03_…/正式版/05_出版成果/Reader/*.html` | base64 嵌入 · ~106MB · 可本地重建 |
| 薄样张 HTML | `03_…/薄样张_试读/*.html` · `…/PDF/*.html` | 构建产物 |
| CC 镜像 | `【CC】files/*.html` · `*.docx` | 正本在 `07_设计原档/*.md` |
| 废止 LOCK | `01_…/00_十人名称_LOCK_2026-06-05.md` | SUPERSEDED → 6-07 |
| Vol2 旧稿 | `第2卷_…/完整文字稿.txt` | ARCHIVED · A006 取代 |
| 错年级 baseline | `CLASSROOM_4-2_baseline.html` | 4年2組 废止 |
| 抓取页 | `06_参考资料/放学后的推理俱乐部/` | 天猫快照 · 非正典 |
| v1 docx | `07_…/12–15_*.docx` · 湿椅子卷 docx | v2 md 正本 |
| 重复工具 | `08_…/japan_campus_consultant_agent.html` | 与根目录副本重复 |

---

## 仍保留在 Git（故意）

| 路径 | 原因 |
|------|------|
| `第1卷_总是湿的椅子/` | C001 **素材库** · 非 Vol1 但需版本化 |
| `docs/volume_01_wet_chair/` | 归档 README · 漂移对照 |
| `japan_campus_consultant_agent.html`（根） | 田中工具 **入口** |
| `【CC】files/**/*.xlsx` | `build_ledger_*.py` 源表 |
| SUPERSEDED **.md**（带横幅） | 历史对照 · 体量小 |

---

| 版本 | 2026-06-09 |
