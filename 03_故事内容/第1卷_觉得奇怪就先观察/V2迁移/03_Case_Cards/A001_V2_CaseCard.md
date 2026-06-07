# Case Card · A001 · 翘边的海报 · V2.0

> **Schema**: [`06_Case_Card_Schema_V2.0.md`](../../../../00_项目总览/IP重构执行包_20260607/06_Case_Card_Schema_V2.0.md)  
> **Engine**: [`02_单案故事引擎_V2.0.md`](../../../../00_项目总览/IP重构执行包_20260607/02_单案故事引擎_V2.0.md)  
> **Supersedes**: `样章包/02_case_card_案01_翘边的海报.md`（V1.1_STRUCT）  
> **Status**: **V2_STRUCT** · science_validation: **pending**

```yaml
schema_version: V2.0
case_id: A001
status: V2_STRUCT
supersedes: V1.1_STRUCT
engine: 02_单案故事引擎_V2.0.md
unit_title: 五件怪事都指向同一个人
unit_subtitle: 全校都在等他承认
complexity_budget: L
scene_count_target: 9
science_validation_status: pending
guest_character: 水野直人
```

---

## 1. 基础

| 字段 | 值 |
|------|-----|
| `title_cn` | 翘边的海报 |
| `title_jp` | めくれたポスター（工作稿） |
| `hook_one_line` | 报名截止前，海报翘边露旧字——全校等他承认，观察社先查风。 |
| `club_layer` | observe → interview → verify |
| `scene` | 名古屋 · 活动准备室门外侧廊 · 海报板+壁报夹 |
| `month_nagoya` | 4月第2–3周 · 樱尾声 · 午后可能有雨 |
| `char_lead` | 慧美（核对）· 志郎（动手）· 光（问人） |
| `global_seed_ids` | `DS-002` |

---

## 2. 科学层

| 字段 | 值 |
|------|-----|
| `science_core` | 侧廊晨间高湿 → 胶带黏性下降；空调出风/窗缝气流 → **风侧**胶带先开边 |
| `science_cross` | 贴胶带方向习惯（志郎换向）→ 翘边 **换边** 假象 |
| `misread` | 有人恶作剧撕/翘海报；**水野**故意破坏活动 |
| `human_truth` | 志郎想贴牢换方向；水野只想把旧通知摆正确却不敢说清 |
| `儿童实验` | 胶带+电吹风模拟风侧；湿度对照纸角（继承 V1） |

---

## 3. 压力与责任（V2）

| 字段 | 值 |
|------|-----|
| `pressure_primary` | **活动报名截止前撤委员**；5年段议论「水野搅局」 |
| `pressure_secondary` | 报名截止前 **20 分钟**；联络事项「午后可能有雨」 |
| `wrong_responsibility` | 水野直人为阻止春季活动/泄愤，**故意撕翘**观察社海报 |
| `true_responsibility` | **机制**：风侧+湿度+志郎换贴方向；**动机**：水野换贴旧活动通知半句、想参加却怯懦沉默 |

---

## 4. 关系与传播

| 字段 | 值 |
|------|-----|
| `relation_type` | `shared_source` |
| `relation_to` | A002 |
| `relation_hook_text` | 侧廊规矩才刚立下，鞋柜那边也出现了「不该有的痕迹」。 |
| `propagation_layer` | `rumor` |
| `source_resolved` | `no` |
| `next_case_id` | A002 |

```yaml
tail_hook_grade: L1
tail_hook_type: 壁报
tail_hook_text: "壁报草稿第4栏刻意留空；慧美铅笔小问号；光说核实完再写。"
tail_hook_fair_in: "SC-09 光解释空栏规矩+半句旧通知未核实"
```

---

## 5. 公平线索（≥3）

| ID | 线索 | 公平含义 | 曝光场次 |
|----|------|----------|----------|
| FC-1 | 翘边总在 **出风栅/窗缝同侧** | 气流受力侧 | SC-02 |
| FC-2 | **雨天/高湿** 日翘边更明显 | 黏性下降 | SC-04 |
| FC-3 | 志郎 **换胶带方向** 与翘边换边同日 | 人为习惯非恶作剧 | SC-04 |
| FC-4 | 旧活动通知 **半句** 露出（可擦墨印边） | 水野动过但非「撕毁」 | SC-05 |

---

## 6. 陸瑆第二真相

| 字段 | 值 |
|------|-----|
| `kei_note_angle` | 哥哥们查风时，她看的是海报下角谁站过 |
| `kei_second_truth` | 「他把海报换回去了。不是想毁掉——是想把那句话摆到大家能看见的地方。」 |
| `kei_second_truth_test` | 读者对水野产生 **理解** 而非厌恶；误会伤人先于机制 |

---

## 7. 角色场次功能

| 角色 | 本场功能 |
|------|----------|
| 陸珣 | 指风侧；本子记录；拒写目击栏名字 |
| 伊藤光 | 拦「查犯人」；写草稿 |
| 加藤慧美 | 天气/对照表；空栏规矩 |
| 松本志郎 | 换贴习惯；文件夹挡风验证 |
| 水野直人 | 误指焦点；沉默；换贴旧通知 |
| 校工 | 划边界「别撕」 |

---

## 8. Gate

| 项 | 状态 |
|----|:----:|
| Remap G1–G7 | 待 V2 正文后重跑 |
| Card-G1–G6 | ✅ 字段齐 |
| Card-G7 科学签 | ⬜ pending |
| phase2b | 待正文 |

---

## 9. C03b 段落锚（对接分场脚本）

| 线索 | 场次 |
|------|------|
| FC-1 | SC-02 |
| FC-2 | SC-04 |
| FC-3 | SC-04 / SC-07 |
| FC-4 | SC-05 / SC-08 |

---

最后更新：2026-06-07 · A001 V2_STRUCT
