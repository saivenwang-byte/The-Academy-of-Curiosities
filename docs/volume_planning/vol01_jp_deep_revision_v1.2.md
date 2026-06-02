# Vol1 日文深修清单 · v1.2（2026-06-02）

> 依据：外部样章审读 82/100 · 红线修正 + 工作流入库  
> 对象：`03_故事内容/第1卷_总是湿的椅子/完整文字稿_日本語.txt`  
> 状态：**JP_CULTURE_REVIEW_PARTIAL_PASS** → 深修中 → 目标 `READY_FOR_SAMPLE_DRAFT`

---

## 采纳 / 不采纳（Agent 判断）

| # | 审读意见 | 决定 | 理由 |
|---|----------|------|------|
| R1 | 第三月曜 vs 水曜冲突 | ✅ 采纳 | 本格时间线硬错误 |
| R2 | 删除「一点五」章节号 | ✅ 采纳 | 改为「二、火曜日のしみ」，后续章顺延 |
| R3 | 載玻片→スライドガラス | ✅ 采纳 | 中文术语红线 |
| R4 | 卷末实验儿童安全 | ✅ 采纳 | IP 红线 · 6–14 岁 |
| R5 | 椅背→窓側金属接触 | ✅ 采纳 | 教室几何+传导物理更稳；同步中文正典 |
| R6 | 椅面21℃结露矛盾 | ✅ 采纳 | 改测点+湿度计 |
| R7 | 温湿度计 | ✅ 采纳 | 露点需可观察湿度 |
| R8 | 对照组 A/B/C | ✅ 部分 | 正文保留铁板/スライド；笔记层可写三对照 |
| R9 | ランドセル新→名札新 | ✅ 采纳 | 4年转学生常识 |
| R10 | 予備鈴→チャイム | ✅ 采纳 | 小学语感 |
| R11 | 三時限目→3時間目 | ✅ 采纳 | 全文统一 |
| R12 | きしめん底→つゆ | ✅ 采纳 | |
| R13 | 昼歯磨き学校差异 | ✅ 采纳 | 加「この学校では…」 |
| R14 | イス面→座面等 | ✅ 采纳 | 见 `docs/JP_PROSE_LEXICON.md` |
| R15 | 伊藤光/陸ひかる混淆 | ⚠️ 部分 | **不改** `人物名称定稿` 读音（陸瑆=ひかる）；**改**正文表记：`陸瑆`/`瑆` vs `光`；禁「陸ひかる」旁白 |
| R16 | 陸珣台词改「假设非答案」 | ✅ 采纳 | 保留结构，加一句 |
| R17 | 压缩重复科学解释 | ✅ 部分 | 正文瘦一句；详表留陸瑆笔记 |
| R18 | 怪事→ふしぎ | ✅ 部分 | 叙事用ふしぎ；品牌/文件名保留「奇事録」 |
| R19 | 志郎轻微道歉 | ✅ 采纳 | 一句 |
| R20 | 慧美/光儿童感 | ✅ 部分 | 各加一处 |
| R21 | 解答略早需大改结构 | ❌ 不采纳 | R16 已够；全文结构不动 |
| R22 | 妹妹改读法（あかり等） | ❌ 暂不 | 需 `人物名称定稿` 正式修订；先用漢字 disambiguation |

---

## 工作流影响

| 模块 | 更新 |
|------|------|
| `academy-jp-voice-editor` | 引用 `docs/JP_PROSE_LEXICON.md` |
| `00_JP_TRANSLATION_REVIEW_GATE.md` | 增加 v1.2 深修检查项 |
| `00_character_canon_index.md` | 同音 disambiguation 规则 |
| `body_lint.py` | 可后续加 載玻片/一点五 禁词（中文侧） |
| `volume_01_scorecard.yaml` | jp_status 字段 |
| 中文 `完整文字稿.txt` | 几何机制同步（窗侧金属） |

---

## 深修后状态标记

```
status_zh: PENDING_REVIEW (L1 passed, v4)
status_jp: JP_DEEP_REVISION_v1.2
gates:
  jp_culture: PARTIAL_PASS → re-review after v1.2
  science_geometry: REVISED
  language: REVISED
  experiment_safety: REVISED
target: READY_FOR_SAMPLE_DRAFT (JP)
```
