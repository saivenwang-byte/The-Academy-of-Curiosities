# A002 · G1 Prompts · MVP · R4 · V0.4

> **Status**: **Gate 3 R4 · doc65 STYLE_LOCK** · 2026-06-08  
> **SSOT**: [`分镜拆解/A002_分镜拆解_R17_V0.1.md`](../分镜拆解/A002_分镜拆解_R17_V0.1.md)  
> **STYLE_LOCK**: [`65_V1.0参考图与V2规范对照_V0.1.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/65_V1.0参考图与V2规范对照_V0.1.md) §3  
> **空间**: **5年2組教室** · CLASS_5-2 · 绿黑板 · 板槽 · 珣 **R3·C1**  
> **输出命名**: `V-S02-V2-A*_G1draft_c04.png`

---

## Global STYLE_LOCK / NEGATIVE / L0

同 [`A001_G1_prompts.md`](./A001_G1_prompts.md) **Global STYLE_LOCK + NEGATIVE**（doc65 §3 · 禁 chibi · 禁 seifuku · 禁 lineup board）。  
**A002 追加**：志郎 **5年3組扫除当番** 时穿 **绿格+绿vest 私服 L0** · **NOT** 学校扫除网 vest 替代 L0 · **NOT** 秘密写字 pose。

**A002 R3 追加 NEGATIVE**（DA3 专用 · 禁错帧）:
```
character lineup board, height chart, portrait grid, student photo slots,
身長測定, height measurement backdrop, acrylic name card grid,
11-slot character board, roster display, class photo wall,
6年2組 door plate, wrong grade label
```

---

## DA1 · 黑板对不起 · SC-02 · P0

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S02-V2-A1 / DA1** |
| 所属 | Vol1 · A002 · SC-02 |
| 镜头功能 | **S+L** |
| 景别 | **MS–CU** |
| 机位 | 黑板平视 · 三分构图 |
| 视觉中心 | 绿黑板居中 **「对不起。」** 圆钝粉笔白字 |
| 第二信息 | 志郎 **绿格+绿vest** 持抹布 **NOT 写字 pose** · 珣 R3C1 观察 |
| 场景 | **5年2組** 本班教室 · 四月早自习窗缝光 · **上履き** |
| 禁项 | 下駄箱泥印 · **制服/seifuku** · 志郎 secret 写字 · 翘边 |
| 正文锚点 | 「黑板上写着三个字：对不起。」 |
| G-BODY锚 | 5-2教室·CLASSROOM_4-2·四月光·私服上履き |

### 合成 Prompt（G1 · c04 · R4 STYLE_LOCK + L0 垫图）

```
Soft cinematic anime children's mystery illustration ages 10-12,
clear light-manga ink warm brown outline #2A1810 NOT pure black,
restrained watercolor paper texture 6-7 head NOT chibi NOT seifuku,
MS-CU 5年2組 classroom green chalkboard three characters 对不起 period
white rounded chalk strokes center board,
Matsumoto Shiro ~145cm stocky green plaid shirt green utility vest round glasses
holding cleaning cloth NOT writing pose NOT secret writer,
Kato Keimi ~155cm yellow cardigan silver-rim glasses low ponytail ear braid blocking trial gesture,
Riku Shun ~142cm blue zip hoodie yellow inner at R3-C1 corridor-side observing stroke angle,
students casual clothes uwabaki white indoor shoes on floor NOT gakuran NOT blazer,
spring slanted aluminum window light equipment cart corridor door seed,
fair clue readable apology text, Nagoya RC school bridge-book watercolor
[NEGATIVE] chibi SD seifuku blazer gakuran sneakers mud prints ghost writing,
character lineup board height chart portrait grid,
English Chinese text rendered in image watermark,
6年2組 door plate 4年2組 door plate Chinese classroom
```

**Output**: `V-S02-V2-A1_黑板对不起_G1draft_c04.png`

---

## DA3 · 膜边反光 · SC-05 · P0 · R3 ⚠️

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S02-V2-A3 / DA3** |
| 所属 | Vol1 · A002 · SC-05 |
| 镜头功能 | **L+C** |
| 景别 | **MCU · ECU** |
| 机位 | **板槽 POV 近距** · 四月斜光 · **NOT 全身 lineup** |
| 视觉中心 | 绿黑板 **板槽内** 透明展示膜 **膜边反光细线** 斜光亮一下 |
| 第二信息 | 清洁液瓶缘 · 样品袋「未登记」标签 · 珣手指指向板槽边缘 |
| 禁项 | **character lineup board** · **height measure** · portrait grid · FC标签入叙事 · 鬼怪 · 制服 |
| 正文锚点 | 「膜边有一条细线，像有人贴过又揭。」 |
| G-BODY锚 | 板槽POV自C1侧·四月光移动·展示膜非人物墙 |

### EXPERT_LOCK（R3 · 禁错帧）

| 必须 | 禁止 |
|------|------|
| 绿黑板板槽 **单条透明膜边** 反光 | 11格人物 lineup · 身長測定 |
| 清洁液瓶 + 未登记样品袋 | 学生肖像卡网格 · 身高尺 backdrop |
| POV 近距 · 膜边 ECU | 6年2組门牌 · 全身五人排队 |

### 合成 Prompt（G1 · c03 · R3）

```
[STYLE] MCU ECU first-person POV close-up at green chalkboard BOARD SLOT only,
NOT character lineup NOT height chart NOT portrait grid,
VISUAL CENTER: thin reflective glint line on transparent display film edge
where film meets chalkboard slot, April slanted window light catching film edge,
SECOND READ: cleaning fluid spray bottle label edge on shelf below,
small sample plastic bag with handwritten unregistered tag,
Riku Shun blue zip hoodie finger pointing at film edge uwabaki visible at bottom,
5年2組 classroom Nagoya April fair-play film clue NOT ghost writing,
bridge-book watercolor restrained ink #2A1810 6-7 head NOT chibi
[NEGATIVE] character lineup board height measurement chart portrait slots grid,
student photo wall acrylic name cards 身長測定 backdrop 11 slots,
6年2組 door plate seifuku horror ghost Chinese classroom sneakers
```

**Output**: `V-S02-V2-A3_膜边反光_G1draft_c04.png`

---

## DA4 · 对照实验 · SC-07 · P0

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S02-V2-A4 / DA4** |
| 所属 | Vol1 · A002 · SC-07 |
| 镜头功能 | **L+P** |
| 景别 | **MS** |
| 机位 | 折叠桌 · 备课本双格 |
| 视觉中心 | 湿擦→清洁液→ **旧痕再显** 对照序列 |
| 第二信息 | FC-4 样品袋 · 志郎演示非 guilty pose |
| 正文锚点 | 「不是幽灵写字——是膜和清洁液的时间差。」 |
| G-BODY锚 | 对照实验儿童可读·L0 四人私服 |

### 合成 Prompt（G1 · c02 · 未改）

```
[STYLE] MS folding table experiment wet wipe cleaning fluid old trace reappears sequence,
Matsumoto Shiro green plaid green vest demonstrating NOT guilty pose round glasses,
Keimi yellow cardigan sample bag label unregistered silver glasses,
Riku Shun recording notebook blue hoodie uwabaki,
green board edge film continuity, Nagoya classroom April fair-play bridge-book watercolor
NOT ghost apology NOT seifuku NOT horror
[NEGATIVE]
```

**Output**: `V-S02-V2-A4_对照实验_G1draft_c04.png`

---

*A002 G1 prompts R4 · V0.4 · doc65 STYLE_LOCK · DA3 board-slot POV*
