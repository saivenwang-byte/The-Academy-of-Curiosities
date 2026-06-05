# CC 交付包 · 使用说明

> **Status**: 2026-06-05 · 专家组 remap 后  
> **执行正典**：仓库内 markdown/xlsx V0.3 · **非** 本目录原始 PDF/docx 未经 remap 版

---

## zip 批次对照

| 批次 | 目录 | 主要内容 | 迁入状态 |
|------|------|----------|----------|
| **zip-1** | `files20260605-1_extracted/` | 200 篇计划书 PDF/docx · **前 50 篇**原理去重台账 xlsx | ✅ V0.2 台账（#1–50）· 已被 V0.3 supersede |
| **zip-2** | `files20260605-2_extracted/` | **前 100 篇**原理去重台账 xlsx · 案01 湿椅子完整样章 md | ✅ **V0.3 主编台账** · 湿椅子参考样章已归档 |

---

## 文件地图

| 文件 | 用途 | 状态 |
|------|------|------|
| `files20260605-1_extracted/学堂奇事録_200篇…pdf` | 投资人叙事 **参考** | ⚠️ 含旧 Vol1/全藏/侦探团 · 勿直接引用 |
| `files20260605-1_extracted/…xlsx` | 前 50 篇台账 **V0.1 原件** | 已迁入 `docs/story_database/` |
| `files20260605-2_extracted/…xlsx` | 前 100 篇台账 **V0.1 原件** | ★ V0.3 主编台账来源 |
| `files20260605-2_extracted/学堂奇事録_案01_湿椅子_完整样章.md` | CC 湿椅子样章 | 已归档 → `03_故事内容/第1卷_总是湿的椅子/CC_案01_湿椅子_参考样章_20260605.md` · **C001 · 非 Vol1** |
| `characters.html` | 角色 SVG demo | ⚠️ **废止执行** · 见 [`00_CC_collateral_废止说明.md`](00_CC_collateral_废止说明.md) |
| `scenes.html` | 场景 demo | 参考 only |
| `12–15_*.docx` | 视觉 docx | 以 `05_视觉设定/` + `07_设计原档/` 为准 |

---

## 正典入口

- [`docs/story_database/02_前100篇原理去重台账_V0.3.xlsx`](../docs/story_database/02_前100篇原理去重台账_V0.3.xlsx) · **主编台账**
- [`docs/canon_remap/前100篇_remap对照表_V0.1.md`](../docs/canon_remap/前100篇_remap对照表_V0.1.md)
- [`docs/canon_remap/前50篇_remap对照表_V0.1.md`](../docs/canon_remap/前50篇_remap对照表_V0.1.md) · #1–50 子集
- [`04_产品与商业/02_200案可持续性引擎_论证附录_V0.1.md`](../04_产品与商业/02_200案可持续性引擎_论证附录_V0.1.md)

**构建脚本**：`scripts/build_ledger_v03.py`（源：`files20260605-2_extracted/*.xlsx` · sheet `前100篇台账`）

---

最后更新：2026-06-05 · zip-2 集成
