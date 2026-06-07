# Case Card · A002 · 没有人写过的道歉 · V2.0

> **母纲**: V0.2 · **Schema**: V2.0 · **Status**: V2_STRUCT · science: pending

```yaml
schema_version: V2.0
case_id: A002
complexity_budget: L
scene_count_target: 9
science_validation_status: pending
guest_character: —
```

| 字段 | 值 |
|------|-----|
| `title_cn` | 没有人写过的道歉 |
| `hook_one_line` | 黑板上每天一句「对不起」——可没人看见志郎写过。 |
| `science_core` | 透明展示膜残留 · 清洁液+湿度+粉尘使字迹再现 |
| `science_cross` | 黑板表面微结构 · 清扫顺序 |
| `pressure_primary` | 志郎被指破坏广播设备相关现场 · 须公开「认错」 |
| `pressure_secondary` | 早自习前字迹再现 |
| `wrong_responsibility` | 志郎秘密写道歉并反复擦除 |
| `true_responsibility` | 机制：膜+清洁显字；动机：志郎未报备材料测试改变现场 |
| `relation_type` | `shared_source` |
| `relation_to` | A003 |
| `relation_hook_text` | 黑板安静了，壁报上却有人「记得」从没贴过的海报。 |
| `global_seed_ids` | DS-009 |
| `kei_second_truth` | 志郎说不是他写的。可黑板记得他来过。 |
| `repair_action` | 实验记录补写：「实验也会制造新的现场。」 |

**FC**: 膜边缘反光 · 字迹与志郎握笔角度不符 · 清洁后再现时序 · 展示膜样品袋标签

---

# Case Card · A003 · 每个人都记得的海报 · V2.0

```yaml
case_id: A003
complexity_budget: L
scene_count_target: 9
science_validation_status: pending
```

| 字段 | 值 |
|------|-----|
| `title_cn` | 每个人都记得的海报 |
| `hook_one_line` | 全班都记得那张海报——学校却找不到。 |
| `science_core` | 视觉碎片+版式暗示 · 记忆重构 · 传言组合 |
| `science_cross` | 采访核实 · 不同目击者复述差异 |
| `pressure_primary` | 慧美被疑删稿包庇 · 失壁报编辑资格 |
| `pressure_secondary` | 壁报张贴前 |
| `wrong_responsibility` | 慧美删除「水野不得参加」海报 |
| `true_responsibility` | 无实体完整海报；慧美为保护排练照片沉默 |
| `relation_type` | `mirror` + `info_pollution` |
| `relation_to` | A001 / A005 |
| `global_seed_ids` | DS-010 |
| `kei_second_truth` | 大家记得的同一张海报，画出来却不一样。 |
| `repair_action` | 壁报三标识：已确认 / 听说 / 仍不知道 |

**FC**: 口述版式不一致 · 正式照片无该海报 · 草稿夹页尺寸不符 · 远处标题+占位视觉连线

---

# Case Card · A004 · 只出现在她抽屉里的失物 · V2.0

```yaml
case_id: A004
complexity_budget: M
scene_count_target: 9
science_validation_status: pending
guest_character: 水野真帆
```

| 字段 | 值 |
|------|-----|
| `title_cn` | 只出现在她抽屉里的失物 |
| `hook_one_line` | 失物全在她抽屉里——她没有别人的钥匙。 |
| `science_core` | 临时柜倾斜 · 柜后连通缝 · 器材车振动使轻物滑入 |
| `science_cross` | 校园动线 · 失物招领流程 |
| `pressure_primary` | 水野被疑偷窃 · 取消展示 · 通知家长 |
| `pressure_secondary` | 公开日物资清点前 |
| `wrong_responsibility` | 水野逐一偷走展示物资 |
| `true_responsibility` | 机制：振动转移；动机：她藏起含朋友哭泣声的录音卡 |
| `relation_type` | `puzzle_piece` |
| `relation_to` | A005 |
| `global_seed_ids` | DS-011 |
| `kei_second_truth` | 抽屉里不只有失物。还有她不想让人听的那张卡。 |
| `repair_action` | 归还录音卡 · 公开说明不播放内容 |

**FC**: 无撬锁痕 · 柜体倾斜水泡/水平仪 · 振动与器材车时刻重合 · 最下抽屉先有物

---

# Case Card · A005 · 午休后消失的影子 · V2.0

```yaml
case_id: A005
complexity_budget: H
scene_count_target: 10
science_validation_status: pending
```

| 字段 | 值 |
|------|-----|
| `title_cn` | 午休后消失的影子 |
| `hook_one_line` | 合照里五个人在——脚下却没有影子。 |
| `science_core` | 平板全景逐段拼接 · 阴影/地面时间错位 |
| `science_cross` | 光学 · 时间戳 · 数字影像 metadata |
| `pressure_primary` | 20分钟后预展取消 · 观察社停活动 · 五人退出展示 |
| `pressure_secondary` | 体育馆大屏投屏 |
| `wrong_responsibility` | 五人+观察社策划五案掩盖破坏 |
| `true_responsibility` | 照片真但未保存完整同时过程；各人承担传播/沉默/实验/藏卡/未及时说明 |
| `relation_type` | `info_pollution` + `puzzle_piece` |
| `relation_to` | —（卷终） |
| `global_seed_ids` | DS-012 |
| `kei_second_truth` | 重新拍照后每人都有影子。真正回来的，是他们愿意再站在一起。 |
| `repair_action` | 全班重拍 · 慧美四栏壁报 · 水野名字并列写回 |

**FC**: 全景模式 icon · 分段曝光 metadata · 器材车经过时间线 · 单次快门对照组有影 · 误推静电失败

**跨案回收**: A001时间/文件 · A002表面痕迹 · A003版本 · A004路线 · ≤4 变量

---

最后更新：2026-06-07 · A002–A005 批量 STRUCT
