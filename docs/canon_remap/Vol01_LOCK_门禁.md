# Vol01 → LOCKED · 门禁清单

> **Status**: ACTIVE · 2026-06-04  
> **适用**: `docs/story_database/00_story_asset_table.md` 卷级行 `Vol01`  
> **原则**: 未过 L1 三门 · 不得 `LOCKED`（见 startup gate）

---

## 何时写入 LOCKED

当 **全部** 下列条件为 ✅ 时，将 `Vol01` status 从 `DRAFT`/`PENDING_REVIEW` 更新为 **`LOCKED`**：

| # | 条件 | 验收物 |
|---|------|--------|
| 1 | 五案 Case Card | A001–A005 · `02_case_card_案*` |
| 2 | 五案正文 CN | 序 + 案①–⑤ HybridVoice · 6500–8000 字 |
| 3 | 五案正文 JP | 完整 `完整文字稿_日本語.txt` 或分案合并 |
| 4 | L1 culture | 田中 HTML · `l1_culture: Y` + 日期 |
| 5 | L1 env | 环境指标 · `l1_env: Y` |
| 6 | L1 fair | 公平线索 · `l1_fair: Y` |
| 7 | 卷末实验页 | 1 个家庭实验 · 观察习惯汇总 |
| 8 | 陸瑆笔记 | 全卷 1 篇总笔记 |
| 9 | 样章/全卷插图 | Vol1 关键 SC · L0 脸库互认 |
| 10 | F1 / E1 自检 | 卷任务包 §九 验收项 |

---

## 子案 status（不必单独 LOCKED）

| 子案 | 建议终态 | 说明 |
|------|----------|------|
| Vol01-A001–A005 | `DRAFT` → 卷 LOCK 时一并归档 | 子案无独立 LOCKED |
| Vol01（卷级） | **`LOCKED`** | 唯一卷级锁稿标记 |

---

## 当前缺口（2026-06-04）

| 项 | 状态 |
|----|------|
| A001 正文 CN/JP | 样章 ✅ |
| A002 正文 CN | ✅ · JP ⬜ |
| A003 正文 CN | ✅ · JP ⬜ |
| A004–A005 正文 | ⬜ |
| L1 三门 | N / N / N |
| **Vol01 LOCKED** | **⬜ 未满足** |

---

## 操作命令

```powershell
# 漂移扫描（4年2組）
python scripts/canon_sweep_4-2.py

# Case Card lint
python scripts/case_card_lint.py --file "03_故事内容/第1卷_觉得奇怪就先观察/02_case_card_案03_空着的那一栏.md"
```

锁稿时更新：

1. `docs/story_database/00_story_asset_table.md` — `Vol01` → `LOCKED` · `l1_*` → Y + ISO 日期  
2. `00_项目总览/00_正典门禁_2026-06-04.md` — Vol1 进度行  
3. `00_项目总览/正典文件索引.md` — 如有版本 bump

---

最后更新：2026-06-04
