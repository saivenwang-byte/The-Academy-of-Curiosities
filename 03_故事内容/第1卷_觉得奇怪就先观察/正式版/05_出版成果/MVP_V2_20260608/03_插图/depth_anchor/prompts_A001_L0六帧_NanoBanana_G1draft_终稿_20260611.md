# A001 · L0 六帧 · NanoBanana · G1draft 终稿 · 2026-06-11

> **Status**: **G1DRAFT_PRODUCTION · DA1 画风 PASS** · 2026-06-11  
> **外装 LOCK**: 用户参考 Sheet v1（橙红 utility vest · 绿格+绿 vest）· 已同步 P0-03 / 春装表  
> **产出命名**: `V-S01-{ID}_{描述}_G1draft_c0N.png` → 栏③优选 → `_G1draft.png` → `_v1.0.png`  
> **Shot Map**: [`03_案01_分镜头与插页地图_V1.3_锁页版.md`](../../03_案01_分镜头与插页地图_V1.3_锁页版.md)  
> **人物 LOCK**: [`P0-03_第一话出场人物执行卡`](../../../../../../05_视觉设定/角色模型/P0-03_第一话出场人物执行卡_V1.0.md)  
> **画风 Sheet**: `07_设计原档/04_样章视觉/Vol1_正篇画风_角色设定Sheet_用户参考_v1.png`  
> **CC 源（已勘误）**: `00_项目总览/外部专家评估_CC_仓库评估_行动方案_20260607.md` · `【CC】files/案A001_…_v1.0.md`  
> **勘误摘要**: 身高 P0-03 · 三眼海报 · **Sheet v1 外装 LOCK** · G1draft 流程 · DA1 画风 IP PASS 2026-06-11

---

## 0. 使用说明

1. **STYLE + NEGATIVE** 每条 prompt 头尾必贴。  
2. 出图前加载 **画风 Sheet** 作参考图；每帧复述四人锚点。  
3. 落盘：`样章包/插图/depth_anchor/`  
4. **P0 验收顺序**：DA1 → DA3 → DA4 → DB1 → DA2 → DC1  
5. 每帧 3–4 候选 → 一致性审核 → 科学顾问签 DA3（P0-04）

---

## 1. 全局 STYLE

```
Modern Japanese bridge-book anime illustration for ages 10-12,
clean organic ink line, soft painterly digital coloring with warm golden-hour cinematic lighting,
realistic pre-teen proportions 6-7 heads NOT chibi NOT shonen hero,
large expressive eyes but grounded pre-teen bodies, rich daily-life texture,
Nagoya public elementary school side corridor April afternoon,
gentle fair-play mystery mood, uwabaki indoor shoes, 4:3 horizontal composition,
IP 学堂奇事録 · 学校おもしろ観察クラブ · observation club NOT detective agency
```

## 2. 全局 NEGATIVE

```
watercolor wash only, rough pencil sketch only, chibi SD, horror, ghost, supernatural glow,
Chinese classroom, detective trench coat, dark scary lighting, 3D render,
English or Chinese rendered text in image, watermark, fluorescent neon,
giant textbook answer arrows on poster, wet chair condensation as main clue,
Ito Hikaru wrong name, 4th grade only class, school uniform blazer,
泉蔹 全藏 wrong kanji, Yamamoto Risa center frame, Lu Hikaru younger sister in frame
```

## 3. 四人 · P0-03 LOCK（案① · 5年跨班）

| 角色 | cm | 视觉 LOCK | 禁止 |
|------|-----|-----------|------|
| **伊藤光** Ito Akira | **146** | **橙红 utility vest** · 白T · 刺状暖棕发 · 哨子 · 硬壳本 · 前倾发现脸 | ❌ Hikaru · ❌ 仅围巾无 vest（见 §3.1） |
| **加藤慧美** Kato Keimi | **155** | 黄开衫 · **低侧马尾+耳侧细辫+柔黄发带** · 银框圆镜 · 采访本 · 四人最高 | ❌ 165学姐 · ❌ 推镜抱胸 |
| **松本志郎** Matsumoto Shiro | **145** | **绿格衬衫 + 绿 utility vest** · 圆框镜 · 矮壮 · 查证卡 | ❌ 暴力搜查 · ❌ 肥胖 caricature |
| **陸珣** Riku Shun | **142** | 藏青/蓝卫衣 · 黄内衬露 1–2cm · 乱黑发 · 路线本 · **侧后入口位** · 四人最矮 | ❌ 社牛 C 位 · ❌ 昆虫破案 pose |

**相对身高**：珣(142) < 志郎(145) < 光(146) < 慧美(155)

**不出场**：陸瑆 · 理紗 · 中谷 · 葛西 · 父母

### 3.1 外装 LOCK（Sheet v1 · IP PASS 2026-06-11）

| 角色 | Gate A A001 出图 LOCK |
|------|------------------------|
| 光 | 白T + **橙红 utility vest** + 哨子 + 硬壳本 |
| 志郎 | **绿格衬衫 + 绿 utility vest** + 圆框镜 + 查证卡 |
| 慧美 | 黄开衫 + 低侧马尾/耳侧细辫/柔黄发带 + 银框镜 |
| 珣 | 蓝 zip 卫衣 + 黄内衬 + 卡其短/九分 + 路线本 · 侧后 |

> 已回写 `P0-03` · `Vol1_春装执行表` · `Vol1_正篇画风Sheet`。L0 排面 watercolor 轨不变。

---

## 4. 分辨率

| 轨 | 帧 | 长边 |
|----|-----|------|
| A | DA1–DA4 | **3200px** |
| B/C | DB1 · DC1 | **2400px** |

---

## 5. 逐帧 Prompt

### DA1 · 侧廊发现 · P0 · MS · G1机位A东向 · R8–9

**输出**: `V-S01-A1_侧廊发现_G1draft.png`

```
[STYLE] 4:3 horizontal high detail. OUTSIDE side-corridor of Nagoya elementary activity-preparation room, April afternoon, optional cherry petals, west light through aluminium-sash windows, cool corridor air. Handmade wall poster Japanese text 学校おもしろ観察クラブ with THREE simple hand-drawn doodle eyes beneath the title — entire RIGHT edge curls upward peeling. On that SAME side just above/beside poster: air-conditioner vent grille AND aluminium window gap — fair clue by composition ONLY, absolutely NO explanatory arrows. Four 5th graders in uwabaki with correct height order: Kato Keimi tallest ~155cm yellow cardigan low side ponytail short braid by ear soft yellow hairband silver-rim glasses interview notebook voice recorder; Ito Akira ~146cm spiky warm-brown hair white tee bright ORANGE-RED UTILITY VEST whistle hardcover notebook energetic discovery pose pointing at poster; Matsumoto Shiro ~145cm stocky green plaid shirt green utility vest round glasses reference cards active; Riku Shun shortest ~142cm messy black hair blue zip hoodie yellow inner shirt khaki shorts route-map book standing slightly BEHIND at corridor entrance quiet observer. At least 3 corridor prop types: pushpins clipboard slot grid magnet aluminium sash vent grille. Cozy fair-play discovery mood cinematic. [NEGATIVE]
```

**必见**：三只简笔眼 · 右缘翘 · vent/窗缝同侧 · 上履き · 珣侧后 · 慧美最高  
**验收**：画风 Sheet T1 · G1背景LOCK · 环境道具≥3类

---

### DA3 · 风侧线索 · P0 · CU · G1机位B框中框 · R12–13

**输出**: `V-S01-A3_风侧线索_G1draft.png`

```
[STYLE] close-up educational beat 4:3 high detail. Tight FRAME-IN-FRAME linking on SAME side: AC vent grille, aluminium window gap, curling edge of 学校おもしろ観察クラブ poster — fair clue by composition only NO arrows of any kind. Kato Keimi ~155cm focus: yellow cardigan, low side ponytail short ear-side braid soft yellow hairband, silver-rim glasses, leaning to write in interview notebook or lightly indicating the spot. Ito Akira ~146cm orange-red utility vest white tee and Matsumoto Shiro ~145cm green plaid green vest partly at frame edges. Fine quiet details: faint moisture few water droplets near window gap gentle rainy-day mist never scary, magnet pin pencil mark on tape edge. Soft cinematic light Nagoya corridor April. [NEGATIVE]
```

**必见**：vent+窗缝+翘边同侧 · 慧美主体 · 无答案箭头  
**验收**：T3 · P0-04 DA3 PASS

---

### DA4 · 验证收束 · P0 · MS · G1机位A略低 · R14–17

**输出**: `V-S01-A4_验证收束_G1draft.png`

```
[STYLE] resolution beat warm golden light 4:3 high detail same side-corridor as DA1 consistent door windows poster position. Matsumoto Shiro ~145cm stocky green plaid shirt green utility vest round glasses re-sticking poster NEW direction OR placing clear file folder as wind shield — action STEP-READABLE. Ito Akira ~146cm orange-red utility vest white tee hardcover notebook; Kato Keimi ~155cm yellow cardigan side braid soft yellow hairband silver glasses; Riku Shun ~142cm blue hoodie route-map book relaxed nearby. Shiro looks relieved friendly non-mockery C04 human habit not malice. Wall-newspaper draft nearby shows three columns filled pencil writing fourth column still empty in background. NO caption text explaining because of wind. [NEGATIVE]
```

**必见**：换贴/文件夹挡风可读 · 壁报三栏满（第四栏空可在背景） · 四人放松  
**验收**：T4 · 换贴动作可读

---

### DB1 · 风侧机制 SUM · P0 · 信息图 · R19–20

**输出**: `V-S01-B1_风侧机制图_G1draft.png`

```
Hand-drawn children's bridge-book infographic NOT perspective scene NO human characters, 4:3 horizontal, light paper texture background #F7F3EE soft painterly digital coloring gentle friendly. Three labelled cells left to right: (1) AC vent grille plus window gap light hand-drawn airflow arrow lifting poster edge; (2) rainy-day humidity symbol tape losing stickiness paper curl; (3) poster re-stuck new direction clear file folder wind shield. Simple LIGHT hand-drawn arrows only never heavy, clean space for JAPANESE main labels only, no formulas no PowerPoint no clutter, picture-book explainer density, no spoiler next case. [NEGATIVE]
```

**必见**：三格机制 · 日文标注位 · 浅底 #F7F3EE  
**验收**：T5 · E04 日文字 LOCK

---

### DA2 · 误导搜查 · P1 · MS · G1机位A同轴 · R10–11

**输出**: `V-S01-A2_误导搜查_G1draft.png`

```
[STYLE] 4:3 horizontal SAME Nagoya side-corridor as DA1 pixel-level continuity door windows curling poster same position. Misdirection: Matsumoto Shiro ~145cm green plaid green vest round glasses crouches exaggerated playful floor-search prank theory NON-violent comedic. Ito Akira ~146cm orange-red utility vest white tee shakes head tense. Kato Keimi ~155cm yellow cardigan side braid soft yellow hairband silver glasses stops Shiro with interview notebook. Riku Shun ~142cm blue hoodie route-map book stands aside quietly recording NOT joining hype. Curled poster vent window visible background same side. April uwabaki warm cinematic light. [NEGATIVE]
```

**必见**：同走廊连续 · 志郎蹲查非暴力 · 珣不跟风  
**验收**：T2 · 同廊可识别

---

### DC1 · 壁报空栏尾钩 · P1 · CU¼页 · G1机位C · §4末

**输出**: `V-S01-TAIL_壁报空栏_G1draft.png`

```
[STYLE] warm cozy close-up quarter-page crop 4:3. Bulletin wall-news DRAFT board at END of side-corridor — clearly SEPARATE board from recruitment poster spatial separation. Draft FOUR columns: three filled neat pencil Japanese writing fourth column deliberately BLANK tiny pencil question mark high contrast. Small witness handwriting 陸珣・風側 optional. Child hand pencil bottom edge optional. Warm afternoon light gentle hopeful L1 hook no next-case submission strip no spoiler. [NEGATIVE]
```

**必见**：四栏·第4空+？ · 壁报≠海报 · witness小字  
**验收**：T6 · 海报板与壁报栏空间分离

---

## 6. 科学线索 · Shot 映射

| 公平线索 | 主 Shot | 图内必见 |
|----------|---------|----------|
| 翘边 = vent/窗缝同侧 | DA1 + DA3 | 同侧构图 · 无答案箭头 |
| 雨天/湿度加重 | DA3 + DB1 | 湿痕/薄雾 · DB1格② |
| 志郎换贴/文件夹（C04） | DA4 | 分步可读 |
| 壁报空栏（L1） | DC1 | 第4栏空 + ？ |

---

## 7. CC 勘误对照（本终稿已吸收）

| CC 原稿 | 终稿校正 |
|---------|----------|
| 身高 155/145/142/146 绑错人 | 光146 · 慧155 · 志145 · 珣142 |
| simple eye doodle | **THREE** doodle eyes |
| orange athletic jacket / scarf only | **Sheet v1: orange-red utility vest + white tee** |
| 文件名 v1.0 | **G1draft** 流程 |
| CC 套件 watercolor bible | 本包 **bridge-book** · 禁 watercolor wash |

---

| 版本 | G1draft 终稿 · DA1 画风 PASS · 六帧候选 c01 齐 · 2026-06-11 |

---

## 8. 候选产出索引 · **G1DRAFT LOCKED**（2026-06-11）

| 帧 | 正式文件 | 来源 |
|----|----------|------|
| DA1 | `V-S01-A1_侧廊发现_G1draft.png` | c01 |
| DA3 | `V-S01-A3_风侧线索_G1draft.png` | c01 |
| DA4 | `V-S01-A4_验证收束_G1draft.png` | c02 |
| DA2 | `V-S01-A2_误导搜查_G1draft.png` | c01 |
| DB1 | `V-S01-B1_风侧机制图_G1draft.png` | v0.2 日文 × G1draft 画风重绘 |
| DC1 | `V-S01-TAIL_壁报空栏_G1draft.png` | v0.2 四栏 × G1draft 重绘 |

详见 [`06_A001_G1draft_优选与v0.2吸收清单_20260611.md`](../../06_A001_G1draft_优选与v0.2吸收清单_20260611.md)
