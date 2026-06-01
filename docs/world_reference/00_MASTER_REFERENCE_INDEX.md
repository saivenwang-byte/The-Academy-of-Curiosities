# 00 · Master Reference Index · 世界参考总索引

> **Status**: ACTIVE  
> **Project**: The Academy of Curiosities / 学堂趣事录  
> **Stage**: 名古屋 · 小学4年2组 · 本格儿童推理  
> **Import status**: **SECOND_PASS_COMPLETE**（01–07 第二轮 08 打标 + 09 顾问复核）

---

## 1. 写作标准文档地图

| # | 标准文档 | 决定什么 |
|---|----------|----------|
| 01 | [01_JAPAN_CAMPUS_CULTURE_STANDARD.md](./01_JAPAN_CAMPUS_CULTURE_STANDARD.md) | 学校制度、空间动线、行为边界 |
| 02 | [02_GEO_CLIMATE_LIGHT_STANDARD.md](./02_GEO_CLIMATE_LIGHT_STANDARD.md) | 经纬度、气候、日照、光影、影长 |
| 03 | [03_WATER_TIDE_WEATHER_STANDARD.md](./03_WATER_TIDE_WEATHER_STANDARD.md) | 水迹、湿度、冷凝、潮汐、风 |
| 04 | [04_FOOD_DAILY_LIFE_STANDARD.md](./04_FOOD_DAILY_LIFE_STANDARD.md) | 給食、饮食、气味、污渍 |
| 05 | [05_FLORA_FAUNA_PHENOLOGY_STANDARD.md](./05_FLORA_FAUNA_PHENOLOGY_STANDARD.md) | 花、虫、物候、花粉 |
| 06 | [06_LANGUAGE_PUNS_SOUND_STANDARD.md](./06_LANGUAGE_PUNS_SOUND_STANDARD.md) | 口语、谐音、拟声、称呼 |
| 07 | [07_MYSTERY_FAIR_PLAY_EVIDENCE_STANDARD.md](./07_MYSTERY_FAIR_PLAY_EVIDENCE_STANDARD.md) | 本格公平、线索、可验证 |
| 08 | [08_SOURCE_RELIABILITY_RULES.md](./08_SOURCE_RELIABILITY_RULES.md) | 来源分级、禁用规则 |

**并行 L1（中文工作区）**  
- `02_创作原则与世界观/名古屋写作硬指标_本格科学参考.md`  
- `02_…/日本校园文化顾问_田中みどり.txt`  
- `docs/00_REDLINE_JP_CULTURAL_CALIBRATION.md`  
- `docs/00_PROJECT_STARTUP_GATE.md`

---

## 2. 09_ 资料库 → 标准文档映射

| 09_ 文件 | 目标标准 | 可靠度 |
|----------|----------|--------|
| `01_校园制度与日程/日本小学学年历与日常制度.txt` | 01 | VERIFIED_SOURCE |
| `02_校园空间与建筑/*.txt` | 01, 02 | VERIFIED_SOURCE |
| `03_人际与社交规则/*.txt` | 01, 06 | CONSULTANT_CONFIRMED |
| `03_人际社交用语/语言方言谐音梗与儿童口语.txt` | 06 | VERIFIED_SOURCE |
| `04_儿童文化与怪谈/*.txt` | 05, 06 | VERIFIED_SOURCE |
| `04_儿童文化与亚文化/日语_谚语_惯用语_拟声拟态词.txt` | 06 | VERIFIED_SOURCE |
| `05_名古屋气候与自然/*.txt` | 02, 03 | VERIFIED_SOURCE |
| `05_地域与民俗_名古屋/名古屋地方文化综合参考.md` | 02, 04, 05 | VERIFIED_SOURCE |
| `06_家庭与住宅/*.txt` | 01, 04 | VERIFIED_SOURCE |
| `07_学校怪谈*/` | 07（外壳） | LOCAL_VARIATION |
| `08_給食与文化/*.txt` | 04 | VERIFIED_SOURCE |
| `08_気候辞典.md` | 02, 03 | VERIFIED_SOURCE |
| `11_写作素材速查/按卷可用的元素清单.txt` | 全部 | CONSULTANT_CONFIRMED |
| `12_L类八大主题_完整素材库.txt` | 01, 02, 06 | VERIFIED_SOURCE |
| `00_来源索引_全站URL清单.txt` | 08 | VERIFIED_SOURCE |

---

## 3. 场景作战卡（写任何场景前必填）

```text
卷目：
场景编号：
地点：名古屋 / L格（探索地图）/ 具体房间
年级：小学4年
月份：
时刻：HH:MM（对照 02 §日出日落）
天气 / 气温 / 湿度：（对照 02 §月别）
光线：太阳方位 / 是否低角度 / 窗朝向
人物为何在此：（01 §留校许可）
涉及制度：（01 当番/係/部活）
涉及物候：（05 若有关）
可能水迹来源：（03 清单）
可能线索物件：上履き、雑巾、引き戸、ランドセル…
文化风险项：（01/06 禁止清单）
科学机制：（07 可验证？）
来源标签：（08）
顾问复核：YES/NO
```

---

## 4. 线索快查（你的问题 → 查哪份标准）

| 问题 | 查 |
|------|-----|
| 椅子为什么湿？ | 03 §结露 · 02 §4月湿度 |
| 窗边为什么有影子？ | 02 §太阳高度角 · 02 §教室朝向 |
| 气味为什么出现？ | 04 §食物 · 05 §花粉/霉 |
| 某种花为什么开了？ | 05 §物候 |
| 几点阳光照到黑板？ | 02 §时刻+高度角+窗向 |
| 梅雨能否造成冷凝？ | 03 §梅雨湿度 · 02 §6月 |
| 海风/潮汐影响？ | 03 §潮汐（L4）；L1–L3 校内通常 **否** |
| 孩子为何此时留校？ | 01 §放学后边界 |
| 谐音梗是否成立？ | 06 §ダジャレ规则 |
| 行为在小学校是否成立？ | 01（**本IP=小学校**，非中学校） |

---

## 5. 维护流程

1. 新素材入 `09_/` → 更新本索引 §2  
2. 提取事实 → 写入 01–07 对应节 → 打 08 标签  
3. `academy-research-editor` 执行 · 冲突标 `NEEDS_VERIFICATION`  
4. 同步 `02_/名古屋写作硬指标_本格科学参考.md`（L1 蒸馏层）  
5. 定稿前：Startup Gate + 双 L1 门禁

---

## 6. 第一卷可直接引用（Vol1 · 总是湿的椅子）

| 维度 | 标准 | 要点 |
|------|------|------|
| 时间 | 02, 05 | 4月 · 桜散 · 昼温升夜冷 |
| 空间 | 01, 02 | 南向教室 · 靠窗椅触窗框 |
| 机制 | 03 | 结露 · 传导冷却 · 湿度 |
| 文化 | 01 | 転校生 · 理科室借片 · 当番后短留 |
| 公平 | 07 | 三线索 + 玻璃杯实验 |
| 来源 | 08 | 05_名古屋气候 · 02_校舍 · VERIFIED |

---

## 7. 标准文档完成状态

| 文档 | 状态 |
|------|------|
| 00 总索引 | ✅ ACTIVE |
| 01 校园文化 | ✅ FIRST_PASS |
| 02 地理气候光影 | ✅ FIRST_PASS |
| 03 水文潮汐天气 | ✅ FIRST_PASS |
| 04 饮食日常 | ✅ FIRST_PASS |
| 05 物候 | ✅ FIRST_PASS |
| 06 语言谐音 | ✅ FIRST_PASS |
| 07 本格公平 | ✅ SECOND_PASS |
| 09 顾问复核 | ✅ ACTIVE |
| 08 来源规则 | ✅ ACTIVE |
| 09 顾问复核日志 | ✅ [09_CONSULTANT_REVIEW_LOG.md](./09_CONSULTANT_REVIEW_LOG.md) |

---

最后更新：2026-06-02
