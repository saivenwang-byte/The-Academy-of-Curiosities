# A003 · G1 Prompts · MVP · R7 · V0.7

> **Status**: **Gate 3 R7 · V0.7 空栏+uwabaki 同帧 · 禁 c06 运动鞋** · 2026-06-08  
> **SSOT**: [`分镜拆解/A003_分镜拆解_R17_V0.1.md`](../分镜拆解/A003_分镜拆解_R17_V0.1.md)  
> **STYLE_LOCK**: [`65_V1.0参考图与V2规范对照_V0.1.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/65_V1.0参考图与V2规范对照_V0.1.md) §3  
> **空间**: **侧廊 G1** · 四栏壁报 · 引き戸 · doc16 §1.2 · **禁 6-2/4-2 门牌** · **禁 Panel3 lineup 海报**  
> **输出命名**: `V-S03-V2-A*_G1draft_c04.png`

---

## Global STYLE_LOCK / NEGATIVE / L0

同 A001 **Global STYLE_LOCK + NEGATIVE** · 侧廊场景追加：瓷砖干灰 · 四月侧光框中框 · 器材车轮迹 · **NOT character lineup poster**。

---

## DA1 · 空海报位 · SC-01 · P0

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S03-V2-DEMO / DA1**（G1: `V-S03-V2-A1_空海报位`） |
| 所属 | Vol1 · A003 · SC-01 |
| 镜头功能 | **S+L** |
| 景别 | **MS** |
| 机位 | 壁报平视 · 四栏构图 |
| 视觉中心 | **空海报位** · 钉印可见 · 无 A3 残胶矩形 |
| 第二信息 | 三人口述版式分叉气泡（留空区） |
| 人物 | 慧美银框镜 · 光橙vest · 低年级 · 侧廊 |
| 场景 | 名古屋侧廊 · 四栏壁报 · **上履き** · G1 尺度锁 |
| 禁项 | 完整实体海报 · **6-2/4-2门牌** · 制服 · 图书馆背影 |
| 正文锚点 | 「每个人都记得——可记得的版式，不一样。」 |
| G-BODY锚 | 四月侧廊·四栏·空位可读·私服 |

### 合成 Prompt（G1 · c04 · R4 STYLE_LOCK + L0 垫图）

```
Soft cinematic anime children's mystery illustration ages 10-12,
clear light-manga ink warm brown outline #2A1810 restrained watercolor NOT chibi NOT seifuku,
MS corridor bulletin wall four-column layout Nagoya elementary side hallway,
empty poster slot with visible pin holes tape residue NO complete A3 poster entity,
Kato Keimi ~155cm yellow cardigan silver-rim glasses low ponytail ear braid interview notebook,
Ito Akira ~146cm white tee orange-red utility vest spiky warm-brown hair,
younger students casual clothes uwabaki pointing conflicting directions blank speech areas NO text,
spring cherry-gray corridor slanted light equipment cart wheel tracks,
fair-play memory conflict clue NOT horror NOT bullying NOT character lineup poster,
NOT seifuku NOT 6-2 door plate NOT 4-2 door plate NOT complete red-black poster
[NEGATIVE] chibi SD seifuku blazer gakuran sneakers character lineup board height chart,
English Chinese text rendered in image watermark High School text,
6年2組 door plate 4年2組 door plate leather shoes
```

**Output**: `V-S03-V2-DEMO_空海报位_G1draft_c04.png`

---

## DA1 · R6 c06 · 空海报位 · EXPERT_LOCK · SC-01 · P0 ⚠️

> **R4 REVISE**: 空栏弱（空白纸非钉印空位）· 气泡 P1 · R6 **L0 垫图 + 钉印空位机制**

### EXPERT_LOCK（A003 DA1 · R6）

| 必须 | 禁止 |
|------|------|
| 四栏壁报 · **一空栏** 钉印/胶带残痕 · 无 A3 实体 | 完整海报 · 五张空白纸 |
| 三人口述分叉（**无气泡无字**） | 可读 speech bubbles |
| 侧廊 G1 尺度 · 四月侧光 | 6-2/4-2 门牌 · lineup 海报 |

### 合成 Prompt（G1 · c06 · R6 L0 face ref + EXPERT_LOCK）

```
Match character faces to attached L0 lineup reference:
Kato Keimi 155cm yellow cardigan silver-rim glasses low ponytail ear braid interview notebook,
Ito Akira 146cm white tee orange-red utility vest spiky warm-brown hair,
younger students casual clothes white uwabaki.
Soft cinematic anime children's mystery ages 10-12, clear light-manga ink #2A1810 watercolor NOT chibi NOT seifuku,
MS corridor bulletin wall four-column layout Nagoya elementary side hallway G1 scale,
VISUAL CENTER: one empty poster slot with visible pin holes tape residue torn paper edges,
other columns have partial papers but NO complete A3 poster entity,
students pointing conflicting directions toward empty slot blank mouth areas NO speech bubbles NO text,
spring cherry-gray corridor slanted April light equipment cart wheel tracks on tile,
fair-play memory conflict clue NOT horror NOT character lineup poster,
NOT seifuku NOT 6-2 door plate NOT 4-2 door plate NOT complete red-black poster
[NEGATIVE] chibi SD seifuku blazer gakuran sneakers speech bubbles caption overlay,
readable text watermark five identical blank tan sheets character lineup board
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S03-V2-DEMO_空海报位_G1draft_c06.png`

---

## DA1 · R7 c07 · 空栏+uwabaki · EXPERT_LOCK · SC-01 · P0 ⚠️

> **R6 c04 near-PASS** · c06 运动鞋 REJ · R7 **钉印空位 + 全员 uwabaki 入画 + 禁气泡**

### EXPERT_LOCK（A003 DA1 · R7）

| 必须 | 禁止 |
|------|------|
| 四栏壁报 · **一空栏** 钉印/胶带残痕 · 无 A3 实体 | 五张空白 tan 纸 · 完整海报 |
| **全员 white uwabaki** 地板可见 · 禁运动鞋 | sneakers · outdoor shoes · speech bubbles |
| 三人口述分叉（**无气泡无字**） | puffer vest 替 orange utility vest |
| L0 脸互认 · 侧廊 G1 尺度 | 6-2/4-2 门牌 · lineup 海报 |

### 合成 Prompt（G1 · c07 · R7 L0 + 空栏 uwabaki EXPERT_LOCK）

```
Match character faces to attached L0 lineup reference:
Kato Keimi 155cm yellow cardigan silver-rim glasses low ponytail ear braid interview notebook,
Ito Akira 146cm white tee orange-red utility vest spiky warm-brown hair NOT puffer vest,
younger students casual clothes.
Soft cinematic anime children's mystery ages 10-12, clear light-manga ink #2A1810 watercolor NOT chibi NOT seifuku,
MS corridor bulletin wall four-column layout Nagoya elementary side hallway G1 scale,
VISUAL CENTER: one empty poster slot with visible pin holes tape residue torn paper edges NO complete A3 poster,
other columns partial papers, students pointing conflicting directions toward empty slot,
MANDATORY all students white uwabaki indoor shoes 上履き clearly visible on green corridor floor in frame,
feet and uwabaki NOT sneakers NOT outdoor shoes, blank mouth areas NO speech bubbles NO text,
spring cherry-gray corridor slanted April light equipment cart wheel tracks,
fair-play memory conflict clue NOT horror NOT character lineup poster,
NOT seifuku NOT 6-2 door plate NOT 4-2 door plate
[NEGATIVE] chibi SD seifuku blazer gakuran sneakers speech bubbles caption overlay,
readable text watermark five identical blank tan sheets orange puffer vest
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S03-V2-DEMO_空海报位_G1draft_c07.png`

---

## DA2 · 正式照无海报 · SC-03 · P0

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S03-V2-A2 / DA2** |
| 镜头功能 | **L+C** |
| 景别 | **MS** |
| 机位 | 折叠桌略俯 |
| 视觉中心 | 慧美四栏格 + 平板 **正式活动照无该海报** |
| 第二信息 | 背景空栏位可读 · 珣速写远标题 |
| 正文锚点 | 「正式活动照里——那一栏是空的。」 |

### 合成 Prompt（G1 · c02）

```
[STYLE] MS corridor folding table Kato Keimi four-column notebook silver-rim glasses yellow cardigan,
tablet showing official event photo WITHOUT missing poster slot entity,
empty bulletin slot pin holes background, Riku Shun ~142cm blue hoodie sketching distant sign uwabaki,
spring Nagoya corridor fair clue NOT horror, casual clothes NOT seifuku bridge-book watercolor
[NEGATIVE] complete poster villain Mizuno poster curl sneakers
```

**Output**: `V-S03-V2-A2_正式照无海报_G1draft_c04.png`

---

## DA4 · 远标题连线 · SC-04 · P0

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S03-V2-A4 / DA4** |
| 镜头功能 | **L+P** |
| 景别 | **MS** |
| 机位 | 侧廊 **远摄** · 占位连线 |
| 视觉中心 | FC-4 **远标题**「我们眼中的学校」可读 · 钉印占位 |
| 第二信息 | 器材车背景 · 学生 uwabaki 指不同方向 |
| 禁项 | **6-2/4-2门牌** · 完整海报 · 皮鞋袜 · 制服 |
| 正文锚点 | 「远一点的标题，和近处说的，对不上。」 |
| G-BODY锚 | 侧廊尺度锁·禁门牌漂移·L0 |

### 合成 Prompt（G1 · c04 · R4 STYLE_LOCK + L0 垫图）

```
Soft cinematic anime children's mystery illustration ages 10-12,
clear light-manga ink warm brown outline #2A1810 restrained watercolor NOT chibi NOT seifuku,
MS distant corridor shot bulletin wall empty slot pin holes,
distant bulletin title area placeholder visual line connecting empty slot NOT full poster entity,
equipment cart background students casual clothes uwabaki pointing conflicting directions,
Riku Shun ~142cm blue zip hoodie Keimi ~155cm yellow cardigan silver-rim glasses low ponytail,
Shiro ~145cm green plaid green vest round glasses,
spring Nagoya elementary side corridor G1 scale locked fair-play memory fragment,
NOT seifuku NOT 6-2 door plate NOT 4-2 door plate NOT leather shoes
[NEGATIVE] chibi SD seifuku blazer gakuran sneakers character lineup board,
English Chinese text rendered in image watermark High School text,
6年2組 door plate 4年2組 door plate complete poster entity
```

**Output**: `V-S03-V2-A4_远标题连线_G1draft_c04.png`

---

## DA4 · R5 c05 · 上履き修复 · SC-04 · P0 ⚠️

> **R4 REJECT**: c04 **运动鞋 C7 P0** · R5 强制 uwabaki

### KF-LOCK-J NEGATIVE（R5 必贴）

```
NOT speech bubbles with readable text, NOT caption overlay bars, NOT UI HUD boxes,
NOT manga panel borders with text, NOT phone screen with legible text,
NOT English Chinese Japanese rendered text in image, NOT watermark subtitle,
NOT sneakers, NOT outdoor athletic shoes, NOT leather shoes, NOT running shoes
```

### 合成 Prompt（G1 · c05 · R5 uwabaki LOCK + L0 垫图）

```
Soft cinematic anime children's mystery illustration ages 10-12,
clear light-manga ink warm brown outline #2A1810 restrained watercolor NOT chibi NOT seifuku,
MS distant corridor shot Nagoya elementary CLASS_5-2 side hallway G1 scale locked,
bulletin wall empty poster slot pin holes tape residue NO complete A3 poster entity,
distant bulletin title area placeholder visual line connecting empty slot NOT full poster,
equipment cart background spring cherry-gray corridor slanted April light,
Riku Shun ~142cm blue zip hoodie yellow inner at corridor-side,
Kato Keimi ~155cm yellow cardigan silver-rim glasses low ponytail ear braid,
Matsumoto Shiro ~145cm green plaid green vest round glasses,
MANDATORY all students wearing white uwabaki indoor shoes 上履き clearly visible on green corridor floor,
feet and uwabaki in frame NOT sneakers NOT outdoor shoes NOT leather shoes,
students casual clothes pointing conflicting directions blank areas NO readable text,
fair-play memory fragment NOT horror NOT bullying NOT character lineup poster,
NOT seifuku NOT 6-2 door plate NOT 4-2 door plate
[NEGATIVE] chibi SD seifuku blazer gakuran sneakers outdoor athletic shoes leather shoes,
speech bubbles caption overlay UI boxes readable text watermark,
English Chinese Japanese text rendered in image,
6年2組 door plate 4年2組 door plate complete poster entity character lineup board
```

**Output**: `V-S03-V2-A4_远标题连线_G1draft_c05.png`

---

*A003 G1 prompts R5 · V0.5 · doc65 STYLE_LOCK · KF-LOCK-J · 侧廊 G1 · 禁门牌/lineup*
