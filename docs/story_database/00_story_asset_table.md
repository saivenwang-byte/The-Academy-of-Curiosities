# 故事资产总表 · Story Asset Table

> **维护 Skill**：`academy-story-database`  
> **Status**: ACTIVE · 2026-06-04 remap + pipeline fix  
> **200 案正典**：[`04_产品与商业/00_200篇产品线架构_V1.0.md`](../../04_产品与商业/00_200篇产品线架构_V1.0.md) · [`Remap Gate`](../canon_remap/00_200篇规划正典映射规则_V1.0.md) · [`README.md`](./README.md)  
> **说明**：一行 = 一卷或一案。**A001–A005** = Vol1 五小案（legacy alias EP001–005）。

---

## 汇总

| 指标 | 值 |
|------|-----|
| 规划总篇数 | 200 |
| 已 LOCKED | **0**（见 §LOCK 政策 — 当前无卷过 L1 全门） |
| READY_FOR_SAMPLE | 1（Vol01-A001 样章） |
| DRAFT | 2（Vol01-A001 正文 · Vol01-A002 正文） |
| OUTLINE | 4（Vol01 卷级 · A003–A005 · Vol02 卷级） |
| PENDING_REVIEW | 1（湿椅子素材库） |

---

## LOCK 政策（为何 0 LOCKED）

| 条件 | Vol1 现状 |
|------|-----------|
| 五案 Case Card 齐全 | A001–A005 ✅（2026-06-04） |
| 五案正文 CN + JP | A001 样章 ✅ · A002 CN ✅ · A003–⑤ ⬜ |
| L1 culture / env / fair | 全卷 **N**（未过门） |
| 插图 + 试读 PDF | 样章部分 ✅ · 全卷 ⬜ |

**→ 表内 `LOCKED` 仅在 L1 三门 + 定稿正文 + 卷级验收后写入。** 子案行可先到 `OUTLINE` / `DRAFT`，不提前 LOCK。

---

## 主表 · 卷级

| id | title_cn | title_jp | status | month_nagoya | science_core | fair_clues | experiment_id | characters | l1_culture | l1_env | l1_fair | paths | notes |
|----|----------|----------|--------|--------------|--------------|------------|-----------------|------------|------------|--------|---------|-------|-------|
| Vol01 | 觉得奇怪，就先观察 | おかしいと思ったら、まず観察 | OUTLINE | 4月 | 湿度/黏着·静电·摩擦·动线·核实 | 案①–⑤见任务包 | EXP-V01-observe | 光;慧美;志郎;陸珣;瑆 | N | N | N | `03_…/第1卷_觉得奇怪就先观察/` | **A001–A005** · 方案 B |
| Vol01-A | 总是湿的椅子（素材） | いつも濡れた椅子 | PENDING_REVIEW | 4月 | 结露·传导·湿度 | 窗侧金属;唯一湿椅;晨湿 | EXP-A-condensation | 光;慧美;志郎;陸珣 | Y | Y | Y | `03_…/第1卷_总是湿的椅子/` | **B-3 · 非 Vol1** |
| Vol02 | 谁偷了橡皮 | 消しゴムはどこへ？ | DRAFT | 5月 | 摩擦 · 振动滑出 · 行为链 | 屑走向; 尺背印; 扫除翻机日 | EXP-V02-friction | 光;慧美;志郎;陸珣 | N | N | N | `03_故事内容/第2卷_谁偷了橡皮/` | 接 Vol1 案⑤ L3 |
| Vol03 | 蚂蚁的队列 | — | IDEA | 6月 | TBD | — | — | 陸珣 | N | N | N | — | 前10卷规划 |
| Vol04 | 音乐教室的怪声 | — | IDEA | 7月 | TBD | — | — | — | N | N | N | — | |
| Vol05 | 水龙头里的温水 | — | IDEA | 8月 | TBD | — | — | — | N | N | N | — | |
| Vol06 | 黑板上的印记 | — | IDEA | 9月 | TBD | — | — | — | N | N | N | — | |
| Vol07 | 歪掉的旗杆影子 | — | IDEA | 10月 | TBD | — | — | — | N | N | N | — | |
| Vol08 | 花盆里的白骨 | — | IDEA | 11月 | TBD | — | — | — | N | N | N | — | |
| Vol09 | 不走的钟 | — | IDEA | 12月 | TBD | — | — | — | N | N | N | — | |
| Vol10 | 会咬人的门把手 | — | IDEA | 1月 | TBD | — | — | — | N | N | N | — | |

---

## 主表 · Vol1 子案（A001–A005）

| id | title_cn | status | science_core | case_card | scene_cards | prose_cn | prose_jp |
|----|----------|--------|--------------|-----------|-------------|----------|----------|
| Vol01-A001 | 翘边的海报 | DRAFT | 湿度·黏着·气流 | `样章包/02_case_card_案01` | `样章包/03_scene_cards` | ✅ 样章 | ✅ §4 |
| Vol01-A002 | 错位的泥印 | DRAFT | 动线还原·目击链 | `02_case_card_案02` | `03_scene_cards_案02` | ✅ HybridVoice | ⬜ |
| Vol01-A003 | 空着的那一栏 | OUTLINE | 核实流程·采访伦理 | `02_case_card_案03` | `03_scene_cards_案03-05` §③ | ⬜ | ⬜ |
| Vol01-A004 | 粉笔灰的圆圈 | OUTLINE | 静電·粉尘·清扫动线 | `02_case_card_案04` | `03_scene_cards_案03-05` §④ | ⬜ | ⬜ |
| Vol01-A005 | 橡皮屑的方向 | OUTLINE | 摩擦痕迹·行为链 | `02_case_card_案05` | `03_scene_cards_案03-05` §⑤ | ⬜ | ⬜ |

路径根：`03_故事内容/第1卷_觉得奇怪就先观察/`

---

## 字段说明

| 字段 | 取值 / 格式 |
|------|-------------|
| `status` | IDEA → OUTLINE → DRAFT → PENDING_REVIEW → READY_FOR_SAMPLE → READY_FOR_TRANSLATION → READY_FOR_ARTIST → LOCKED |
| `l1_*` | Y / N / 日期 ISO |
| `paths` | 相对仓库根目录 |
| `fair_clues` | 分号分隔短句 |

---

## Case Card 索引

| id | case_card_path |
|----|----------------|
| Vol01-A001 | `03_故事内容/第1卷_觉得奇怪就先观察/样章包/02_case_card_案01_翘边的海报.md` |
| Vol01-A002 | `03_故事内容/第1卷_觉得奇怪就先观察/02_case_card_案02_错位的泥印.md` |
| Vol01-A003 | `03_故事内容/第1卷_觉得奇怪就先观察/02_case_card_案03_空着的那一栏.md` |
| Vol01-A004 | `03_故事内容/第1卷_觉得奇怪就先观察/02_case_card_案04_粉笔灰的圆圈.md` |
| Vol01-A005 | `03_故事内容/第1卷_觉得奇怪就先观察/02_case_card_案05_橡皮屑的方向.md` |
| Vol02 | `docs/volume_planning/volume_02_eraser_case_card.md` |
| Vol01-A（素材） | `docs/volume_planning/volume_01_wet_chair_case_card.md` · **非 Vol1 正典** |

---

## 变更 log

| 日期 | 变更 |
|------|------|
| 2026-06-02 | 初版模板 + Vol01 示例行 |
| 2026-06-04 | Vol1 remap 方案 B · 湿椅子→素材 |
| 2026-06-04 | **A001–A005 子表 · Case Card 索引修正 · LOCK 政策** |
