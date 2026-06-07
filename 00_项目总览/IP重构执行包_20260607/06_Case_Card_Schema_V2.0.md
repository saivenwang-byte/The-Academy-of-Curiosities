# Case Card Schema · V2.0

> **Status**: **LOCKED · Schema** · 取代 V1 Card 新建写作  
> **样例**: [`03_故事内容/.../V2迁移/03_Case_Cards/A001_V2_CaseCard.md`](../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/03_Case_Cards/A001_V2_CaseCard.md)

---

## 1. 元数据头（Markdown 必填）

```yaml
schema_version: V2.0
case_id: A001
status: DRAFT | STRUCT | VOICE | GATE_A | GATE_B | PRODUCT
supersedes: V1.1_STRUCT   # 若有
engine: 02_单案故事引擎_V2.0.md
```

---

## 2. 字段全表

### 2.1 继承 V1（保留）

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `case_id` | string | ✅ | A001–A200 |
| `title_cn` / `title_jp` | string | ✅ | 题名 |
| `hook_one_line` | string | ✅ | 一句话钩子 |
| `club_layer` | enum | ✅ | interview / observe / verify |
| `scene` | string | ✅ | 名古屋场景 |
| `month_nagoya` | string | ✅ | 季节锚 |
| `science_core` | string | ✅ | 主原理 |
| `science_cross` | list | ✅ | ≥1 交叉 |
| `fair_clues` | list | ✅ | ≥3 · 每条可定位段落 |
| `misread` | string | ✅ | 第一误判 |
| `propagation_layer` | enum | ✅ | none / rumor / broadcast / submission / title_distortion / wall_post |
| `source_resolved` | enum | ✅ | yes / no / partial |
| `human_truth` | string | ✅ | 温柔人际锤 |
| `char_lead` | string | ✅ | 主导角色 |
| `kei_note_angle` | string | ✅ | 笔记层角度 |
| `foreshadow_id` | string | — | Lxx 或 — |
| `gate_pass` | map | ✅ | Remap G1–G7 |
| `tail_hook_grade` | enum | ✅ | L1–L4 |
| `tail_hook_type` | string | ✅ | |
| `tail_hook_text` | string | ✅ | |
| `tail_hook_fair_in` | string | ✅ | |
| `next_case_id` | string | ✅ | |
| `day_mon`…`day_fri` | map | — | 周节拍 |

### 2.2 V2 新增（必填 unless 注明）

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `unit_title` | string | 卷首案 | Vol1 单元题 |
| `complexity_budget` | enum | ✅ | L / M / H |
| `pressure_primary` | string | ✅ | 主社交/制度压 |
| `pressure_secondary` | string | — | 事件钟文案 |
| `wrong_responsibility` | string | ✅ | 错误归咎叙事 |
| `true_responsibility` | string | ✅ | 机制+真实动机 |
| `relation_type` | enum | ✅ | causal / shared_source / puzzle_piece / mirror / misuse / info_pollution |
| `relation_to` | string | ✅ | 下案或 A005 |
| `relation_hook_text` | string | — | Step⑬ 一句 |
| `global_seed_ids` | list | ✅ | DS-xxx |
| `kei_second_truth` | string | ✅ | 瑆第二真相 · 禁新机制 |
| `kei_second_truth_test` | string | ✅ | 验收：读者学到什么 **情感** |
| `scene_count_target` | int | ✅ | 8–10 |
| `science_validation_status` | enum | ✅ | pending / signed |
| `guest_character` | string | — | 卷级客座出场标记 |

---

## 3. YAML 块模板

```yaml
case_id: A001
complexity_budget: L
pressure_primary: "活动报名截止前撤委员；全校指认破坏海报"
pressure_secondary: "报名截止前20分钟；午后雨将至"
wrong_responsibility: "水野直人为搅乱春季活动故意撕翘海报"
true_responsibility: "侧廊风侧翘边+志郎换贴习惯；水野仅换贴旧通知半句且未说出口"
relation_type: shared_source
relation_to: A002
global_seed_ids: [DS-002]
propagation_layer: rumor
source_resolved: no
kei_second_truth: "瑆：他把海报换回去了——不是想毁掉，是想把话说清楚。"
kei_second_truth_test: "读者感到被误指者的怯懦可理解，非恶人"
scene_count_target: 9
science_validation_status: pending
guest_character: 水野直人
```

---

## 4. C03b 线索曝光表（继承）

| 线索 ID | 描述 | 最早场次 | 段落锚 |
|---------|------|----------|--------|
| FC-1 | … | SC-03 | … |

---

## 5. Gate 附表

| Gate | 检项 |
|------|------|
| Card-G1 | 必填字段非空 |
| Card-G2 | fair_clues ≥3 且 exposure 填 |
| Card-G3 | pressure + wrong/true 不矛盾 |
| Card-G4 | relation_type 在 03_五案一网 登记 |
| Card-G5 | kei_second_truth 零新机制（人工扫） |
| Card-G6 | complexity_budget 不超标 |
| Card-G7 | science_validation_status = signed（进 PRODUCT 前） |

---

最后更新：2026-06-07
