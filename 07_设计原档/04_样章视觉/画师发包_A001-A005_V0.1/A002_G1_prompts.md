# A002 · G1 Prompts · MVP · R7 · V0.7

> **Status**: **Gate 3 R8 · V0.8 E06-S per-slot face lock c04→c08** · 2026-06-08  
> **SSOT**: [`分镜拆解/A002_分镜拆解_R17_V0.1.md`](../分镜拆解/A002_分镜拆解_R17_V0.1.md)  
> **STYLE_LOCK**: [`65_V1.0参考图与V2规范对照_V0.1.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/65_V1.0参考图与V2规范对照_V0.1.md) §3  
> **空间**: **5年2組教室** · CLASS_5-2 · 绿黑板 · 板槽 · 珣 **R3·C1**  
> **输出命名**: `V-S02-V2-A*_G1draft_c04.png`

---

## Global STYLE_LOCK / NEGATIVE / L0

同 [`A001_G1_prompts.md`](./A001_G1_prompts.md) **Global STYLE_LOCK + NEGATIVE**（doc65 §3 · R5 KF-LOCK-J · 禁 chibi · 禁 seifuku · 禁 lineup board）。  
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

## DA1 · R5 c05 · CLASS_5-2 座席 · SC-02 · P0

> **R4 REVISE**: 珣 R3C1🟡 · R5 显式廊下侧观察位

### 合成 Prompt（G1 · c05 · R5 座席 + KF-LOCK-J）

```
Soft cinematic anime children's mystery illustration ages 10-12,
clear light-manga ink warm brown outline #2A1810 restrained watercolor 6-7 head NOT chibi NOT seifuku,
MS-CU 5年2組 classroom green chalkboard three characters 对不起 period white rounded chalk strokes,
Matsumoto Shiro ~145cm stocky green plaid shirt green utility vest round glasses
holding cleaning cloth NOT writing pose at board center,
Kato Keimi ~155cm yellow cardigan silver-rim glasses low ponytail ear braid blocking trial gesture,
Riku Shun ~142cm blue zip hoodie yellow inner at R3-C1 corridor-side observing stroke angle NOT at window,
students casual clothes white uwabaki indoor shoes clearly visible on floor NOT sneakers,
spring slanted aluminum window light equipment cart corridor door seed,
fair clue readable apology text Nagoya RC school bridge-book watercolor
[NEGATIVE] chibi SD seifuku blazer gakuran sneakers speech bubbles caption overlay UI boxes,
readable text watermark English Chinese Japanese text in image,
Riku at window side C6 wrong seat character lineup board height chart
```

**Output**: `V-S02-V2-A1_黑板对不起_G1draft_c05.png`

---

## DA1 · R6 c06 · L0 face · SC-02 · P0

> **R4 PASS candidate c04** · R6 L0 脸库强化 · 保留 c04/c05 若 c06 回归

### 合成 Prompt（G1 · c06 · R6 L0 face ref）

```
Match character faces exactly to attached L0 lineup reference:
Matsumoto Shiro 145cm green plaid green utility vest round glasses stocky,
Kato Keimi 155cm yellow cardigan silver-rim glasses low ponytail ear braid,
Riku Shun 142cm blue zip hoodie yellow inner at R3-C1 corridor-side.
Soft cinematic anime children's mystery ages 10-12, clear light-manga ink #2A1810 watercolor NOT chibi NOT seifuku,
MS-CU 5年2組 classroom green chalkboard three white rounded chalk characters 对不起 period center board,
Shiro holding cleaning cloth NOT writing pose, Keimi blocking trial gesture,
Riku observing stroke angle NOT at window, all white uwabaki clearly visible on floor NOT sneakers,
spring slanted aluminum window light equipment cart corridor door, fair clue readable apology text on board,
Nagoya RC school bridge-book watercolor
[NEGATIVE] chibi SD seifuku blazer gakuran sneakers speech bubbles caption overlay,
readable watermark English text Riku at window C6 wrong seat character lineup board
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S02-V2-A1_黑板对不起_G1draft_c06.png`

---

## DA1 · R7 c07 · L0 face lock only · SC-02 · P0

> **R6 near-PASS c04** · R7 **minimal change**: L0 3840 垫图 + 脸互认 · 保留 c04 构图/机制

### 合成 Prompt（G1 · c07 · R7 L0 face lock · c04 baseline）

```
Match character faces exactly to attached L0 lineup reference sheet:
Matsumoto Shiro 145cm green plaid green utility vest round glasses stocky,
Kato Keimi 155cm yellow cardigan silver-rim glasses low ponytail ear braid,
Riku Shun 142cm blue zip hoodie yellow inner at R3-C1 corridor-side.
Soft cinematic anime children's mystery ages 10-12, clear light-manga ink #2A1810 restrained watercolor NOT chibi NOT seifuku,
MS-CU 5年2組 classroom green chalkboard three white rounded chalk characters 对不起 period center board,
Shiro holding cleaning cloth NOT writing pose, Keimi blocking trial gesture,
Riku observing stroke angle NOT at window, all white uwabaki clearly visible on floor NOT sneakers,
spring slanted aluminum window light equipment cart corridor door, fair clue readable apology text on board,
Nagoya RC school bridge-book watercolor
[NEGATIVE] chibi SD seifuku blazer gakuran sneakers speech bubbles caption overlay,
readable watermark English text Riku at window C6 wrong seat character lineup board
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S02-V2-A1_黑板对不起_G1draft_c07.png`

---

## DA1 · R8 c08 · E06-S face lock · c04 baseline · SC-02 · P0 ⚠️

> **R7 near-PASS c04** · c07 英文 clue 便签回归 · R8 **E06-S per-slot 脸签 + KF-LOCK-J++** · 零场景变更

### E06-S FACE LIBRARY LOCK（per-slot · 3840 sheet · c04 composition frozen）

```
Slot ② Riku Shun 142cm: oval face messy black hair navy zip hoodie yellow inner khaki shorts — left near balcony door observing
Slot ③ Matsumoto Shiro 145cm: round glasses stocky green plaid green utility vest — center at board holding cleaning cloth NOT writing
Slot ⑦ Kato Keimi 155cm: silver-rim glasses low ponytail ear braid yellow cardigan — right profile blocking trial gesture
Match face geometry exactly to attached L0 3840 reference per slot. Minimal scene change from c04.
```

### 合成 Prompt（G1 · c08 · R8 E06-S · c04 frozen）

```
E06-S FACE LIBRARY LOCK from CHAR_lineup_L0_3840 per slots ②③⑦ listed above.
Soft cinematic anime children's mystery ages 10-12, clear light-manga ink #2A1810 restrained watercolor NOT chibi NOT seifuku,
MS-CU 5年2組 classroom green chalkboard three white rounded chalk characters 对不起 period center board,
Shiro slot③ holding cleaning cloth NOT writing pose, Keimi slot⑦ blocking trial gesture,
Riku slot② observing stroke angle near balcony door NOT at window, all white uwabaki clearly visible on floor NOT sneakers,
spring slanted aluminum window light equipment cart corridor door, fair clue readable apology text on board ONLY,
Nagoya RC school bridge-book watercolor
[NEGATIVE KF-LOCK-J++] chibi SD seifuku blazer gakuran sneakers speech bubbles caption overlay UI boxes,
readable watermark English sticky notes clue cards Japanese text Riku at window C6 wrong seat character lineup board,
manga panel borders phone screen legible text name tags on clothing
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S02-V2-A1_黑板对不起_G1draft_c08.png`

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

## DA3 · R6 c06 · 膜边 ECU · EXPERT_LOCK · SC-05 · P0 ⚠️

> **R3 baseline c03** 膜边✅ · 日文字 P1 · R6 **无字 ECU 强化** · 仅 c06> c03 时替换

### EXPERT_LOCK（A002 DA3 · R6 · 禁错帧）

| 必须 | 禁止 |
|------|------|
| 绿黑板 **板槽 POV ECU** · **膜边反光细线** 斜光一闪 | lineup 11格 · 身長測定 |
| 清洁液瓶缘 · 未登记样品袋（**无可读字**） | 学生肖像卡网格 · 6-2门牌 |
| 珣手指指向膜边 · uwabaki 底缘 | 全身五人排队 · 错帧 height chart |

### 合成 Prompt（G1 · c06 · R6 L0 + EXPERT_LOCK ECU）

```
MCU ECU first-person POV close-up green chalkboard BOARD SLOT only,
NOT character lineup NOT height chart NOT portrait grid,
VISUAL CENTER: thin bright reflective glint line on transparent display film edge
where film meets chalkboard slot, April slanted window light catching film edge sharply,
SECOND READ: cleaning fluid spray bottle silhouette on shelf below,
small sample plastic bag with blank handwritten tag shape NO readable letters,
Riku Shun blue zip hoodie finger pointing at film edge uwabaki visible at bottom frame edge,
5年2組 classroom Nagoya April fair-play film clue NOT ghost writing,
bridge-book watercolor restrained ink #2A1810 6-7 head NOT chibi NOT seifuku
[NEGATIVE] character lineup board height measurement chart portrait slots grid,
student photo wall acrylic name cards 身長測定 backdrop 11 slots readable Japanese text,
6年2組 door plate seifuku horror ghost Chinese classroom sneakers speech bubbles
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S02-V2-A3_膜边反光_G1draft_c06.png`

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

*A002 G1 prompts R5 · V0.5 · doc65 STYLE_LOCK · KF-LOCK-J · DA3 board-slot POV*
