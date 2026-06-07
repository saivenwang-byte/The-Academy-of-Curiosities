# Case Card · A001 · 全班都听见了他的声音 · V2.0

> **Schema**: [`06_Case_Card_Schema_V2.0.md`](../../../../00_项目总览/IP重构执行包_20260607/06_Case_Card_Schema_V2.0.md)  
> **Engine**: [`02_单案故事引擎_V2.0.md`](../../../../00_项目总览/IP重构执行包_20260607/02_单案故事引擎_V2.0.md)  
> **母纲**: [`Vol1_V2_第一单元_MVP母纲_V0.2.md`](../01_五案关系网/Vol1_V2_第一单元_MVP母纲_V0.2.md)  
> **Supersedes**: 同路径旧 Card（翘边的海报 · V0.1 归档）  
> **Status**: **MIGRATION_CANDIDATE** · science_validation: **working_draft_pending_human_sign**  

```yaml
schema_version: V2.0
case_id: A001
status: V2_STRUCT
supersedes: A001_V0.1_翘边的海报
engine: 02_单案故事引擎_V2.0.md
unit_title: 待定（工作名：全校都认错了人）
unit_subtitle: 五件怪事，五次指认，最后连观察社也成了嫌疑人
complexity_budget: L
scene_count_target: 9
science_validation_status: working_draft_pending_human_sign
guest_character: 水野真帆（卷级 · 本案被提及）
```

---

## 1. 基础

| 字段 | 值 |
|------|-----|
| `title_cn` | 全班都听见了他的声音 |
| `title_jp` | クラス全員が、彼の声を聞いた（工作稿） |
| `hook_one_line` | 广播里是他的声音——可 **他今天根本说不出话**。 |
| `club_layer` | observe → interview → verify |
| `scene` | 名古屋 · 5年段教室 + 校内广播室/器材车接口 · 公开日准备周 |
| `month_nagoya` | 4月下旬 · 公开日前 · 樱季末 |
| `char_lead` | 光（被疑）· 慧美（拦定罪）· 志郎（查设备） |
| `global_seed_ids` | `DS-008`（声学/录音类 · 待 remap 登记） |

---

## 2. 科学层

| 字段 | 值 |
|------|-----|
| `science_core` | 旧排练录音误播 · 数字音频压缩/跳播 · 句子边界截断 |
| `science_cross` | 听觉声纹熟悉度 · 语境缺失（只听半句） |
| `misread` | 光当面恶意说「水野不该参加」 |
| `human_truth` | **失声日**（保健室登记）+ 旧录音误播；光曾转述未经确认的排练片段 |
| `儿童实验` | 两段录音拼接/跳播对比 · 「 familiar 声音 ≠ 同一句原话」（禁伤害性内容） |

---

## 3. 压力与责任（V2）

| 字段 | 值 |
|------|-----|
| `pressure_primary` | 光失去 **广播协助/公开日导播** 资格；班级议论「排斥同学」 |
| `pressure_secondary` | 公开日彩排前 **40 分钟**；器材车下一班轮转 |
| `wrong_responsibility` | 伊藤光通过广播 **故意** 羞辱水野、破坏公开日团结 |
| `true_responsibility` | **机制**：旧卡/排练文件误触播放+压缩跳播；**动机**：光传播过未核实排练消息且未及时澄清 |

---

## 4. 关系与传播

| 字段 | 值 |
|------|-----|
| `relation_type` | `shared_source` |
| `relation_to` | A002 |
| `relation_hook_text` | 广播安静了，黑板上却开始每天出现一句「对不起」。 |
| `propagation_layer` | `broadcast` |
| `source_resolved` | `partial`（误播源可定位 · 恶意意图不可） |
| `next_case_id` | A002 |

```yaml
tail_hook_grade: L1
tail_hook_type: 广播/器材车
tail_hook_text: "志郎在广播日志里发现展示膜测试记录——与黑板有关。"
tail_hook_fair_in: "SC-09 器材车清单+志郎一句「黑板那边也有怪事」"
```

---

## 5. 公平线索（≥3）

| ID | 线索 | 公平含义 | 曝光场次 |
|----|------|----------|----------|
| FC-0 | **保健室登记** · 咽头发炎 · 当日 **禁声** | 生理不可能 | SC-01 |
| FC-1 | 播放时 **光唇未动** / 与现场不同步 | 非现场发言 | SC-02 |
| FC-2 | 日志 **文件时间** 早于当日 · 标签「排练_0328」 | 旧录音 | SC-05 |
| FC-3 | 波形在「不该参加」前 **硬切/压缩断点** | 跳播拼接 | SC-06 |
| FC-4 | 完整排练句为「……**迟到者**不该参加 **彩排**」· 广播只播中间段 | 语境截断 | SC-07 |

---

## 6. 陸瑆第二真相

| 字段 | 值 |
|------|-----|
| `kei_note_angle` | 哥哥们查文件时，她看的是光 **有没有躲开** 大家的眼睛 |
| `kei_second_truth` | 「大家都听见他的声音了。可没有人听见，**他今天说不出话**。」 |
| `kei_second_truth_test` | 读者对 **光** 产生「被误会」的同情，而非「传谣者活该」 |

---

## 7. 角色场次功能

| 角色 | 本场功能 |
|------|----------|
| 陸珣 | 先看 **屏幕时间/日志** · 不先站队 |
| 伊藤光 | 被疑焦点 · 修复句「我说过一句很像的话…」 |
| 加藤慧美 | 拦「犯人」· 记录不同版本说法 |
| 松本志郎 | 查器材车/广播链 · 幽默 relief |
| 水野真帆 | 被提及 · 未出场主帧 · 沉默承受误传 |
| 班主任 | 制度钟 · 要求「午休前说明」 |

---

## 8. Gate

| 项 | 状态 |
|----|:----:|
| Remap G1–G7 | 待 V2 正文 |
| Card-G1–G6 | ✅ |
| Card-G7 科学签 | 🟡 working_validated · 见 `P0_科学顾问签核记录_V0.1.md` |
| phase2b | 待正文 |

---

## 9. C03b 段落锚

| 线索 | 场次 |
|------|------|
| FC-1 | SC-02 |
| FC-2 | SC-05 |
| FC-3 | SC-06 |
| FC-4 | SC-07 / SC-08 |

---

最后更新：2026-06-07 · A001 V2_STRUCT · 标题优先版
