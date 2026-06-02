# 故事资产总表 · Story Asset Table

> **维护 Skill**：`academy-story-database`  
> **Status**: TEMPLATE · 2026-06-02  
> **说明**：一行 = 一卷（或一篇独立故事）。状态须符合 `docs/00_PROJECT_STARTUP_GATE.md`。

---

## 汇总

| 指标 | 值 |
|------|-----|
| 规划总篇数 | 200 |
| 已 LOCKED | 0 |
| READY_FOR_TRANSLATION | 0 |
| OUTLINE | 0 |
| DRAFT | 1（Vol2） |
| PENDING_REVIEW | 1（Vol1） |

---

## 主表

| id | title_cn | title_jp | status | month_nagoya | science_core | fair_clues | experiment_id | characters | l1_culture | l1_env | l1_fair | paths | notes |
|----|----------|----------|--------|--------------|--------------|------------|-----------------|------------|------------|--------|---------|-------|-------|
| Vol01 | 总是湿的椅子 | いつも濡れた椅子 | PENDING_REVIEW | 4月 | 结露 · 椅背贴アルミ窓枠 | 窗侧日照; 椅背湿非椅座; 4月湿度 | EXP-V01-condensation | 陸珣;陸瑆;慧美 | Y | Y | Y | `03_故事内容/第1卷_总是湿的椅子/` | 正文 v4; 插图 v2; art_review 入库 |
| Vol02 | 谁偷了橡皮 | 消しゴムはどこへ？ | DRAFT | 5月 | 摩擦 · 振动滑出 · 行为链 | 屑走向; 尺背印; 扫除翻机日 | EXP-V02-friction | 光;慧美;志郎;陸珣 | N | N | N | `03_故事内容/第2卷_谁偷了橡皮/` | 第六批初稿 · L1 待过 |
| Vol03 | 蚂蚁的队列 | — | IDEA | 6月 | TBD | — | — | 陸珣 | N | N | N | — | 前10卷规划 |
| Vol04 | 音乐教室的怪声 | — | IDEA | 7月 | TBD | — | — | — | N | N | N | — | |
| Vol05 | 水龙头里的温水 | — | IDEA | 8月 | TBD | — | — | — | N | N | N | — | |
| Vol06 | 黑板上的印记 | — | IDEA | 9月 | TBD | — | — | — | N | N | N | — | |
| Vol07 | 歪掉的旗杆影子 | — | IDEA | 10月 | TBD | — | — | — | N | N | N | — | |
| Vol08 | 花盆里的白骨 | — | IDEA | 11月 | TBD | — | — | — | N | N | N | — | |
| Vol09 | 不走的钟 | — | IDEA | 12月 | TBD | — | — | — | N | N | N | — | |
| Vol10 | 会咬人的门把手 | — | IDEA | 1月 | TBD | — | — | — | N | N | N | — | |

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
| Vol01 | `docs/volume_planning/volume_01_wet_chair_case_card.md` |
| Vol02 | `docs/volume_planning/volume_02_eraser_case_card.md` |

---

## 变更 log

| 日期 | 变更 |
|------|------|
| 2026-06-02 | 初版模板 + Vol01 示例行 |
| 2026-06-02 | Case Card 索引链至 volume_01_wet_chair_case_card.md |
| 2026-06-02 | Vol02 OUTLINE 行 + Case/Scene 卡 |
| 2026-06-02 | Vol2 决策锁定 · 第五批 |
| 2026-06-02 | Vol2 DRAFT 正文 · Vol03–10 IDEA · body_lint · 第六批 |
