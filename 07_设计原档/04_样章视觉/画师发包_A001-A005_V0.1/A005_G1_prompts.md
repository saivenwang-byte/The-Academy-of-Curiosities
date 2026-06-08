# A005 · G1 Prompts · MVP · R7 · V0.7

> **Status**: **Gate 3 R8 · V0.8 EXPERT_LOCK shadow gap + KF-LOCK-J++ no text** · 2026-06-08  
> **SSOT**: [`分镜拆解/A005_分镜拆解_R17_V0.1.md`](../分镜拆解/A005_分镜拆解_R17_V0.1.md)  
> **STYLE_LOCK**: [`65_V1.0参考图与V2规范对照_V0.1.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/65_V1.0参考图与V2规范对照_V0.1.md) §3  
> **空间**: **体育馆 brief** · doc16 §2 · 穹顶 · 投屏白墙 · 侧门器材车 · 灯杆长影  
> **EXPERT_LOCK**: **仅水野** 脚下无影 · 四人+器材车+灯杆 **有影** · 重拍 **五影全在**  
> **输出命名**: `V-S05-V2-A*_G1draft_c04.png`

---

## Global STYLE_LOCK / NEGATIVE / L0

同 A001 **Global STYLE_LOCK + NEGATIVE** · Plan B 五人正典名：**陸珣 · 伊藤光 · 加藤慧美 · 松本志郎 · 水野真帆**  
**禁**：山本/佐藤/田中 错名 · 五人全无影 · 橡皮屑 · 运动鞋 · **chibi · Panel4 教辅体**

**A005 R3 追加 NEGATIVE**:
```
live photoshoot queue, height measurement scene, 身長測定 backdrop,
school name banner with height lines, five students posing for height chart,
studio portrait setup without projection screen, all five shadowless,
wrong names Yamamoto Sato Tanaka, sneakers outdoor shoes, chibi
```

---

## EXPERT_LOCK · A005 全局（R3 · 必检）

| 帧 | 必须可见 | 禁止 |
|----|----------|------|
| **DA1** | 投屏上五人合照 · **仅水野脚边无影** · 地板器材车/灯杆 **长影仍在** · 四人影正常 | 现场排队拍照 · 五人全无影 · 无投屏 |
| **DA6** | 体育馆重拍 · **单次快门** · **五影全在含 water野** · 相机三脚架 | 身高测量 · 身長測定 banner · 五人全无影 |

**L0 五人 LOCK**（私服+上履き）:
- 陸珣 Riku Shun 142cm blue zip hoodie khaki pants route notebook
- 伊藤光 Ito Akira 146cm white tee orange-red utility vest spiky hair
- 加藤慧美 Kato Keimi 155cm yellow cardigan silver glasses low ponytail
- 松本志郎 Matsumoto Shiro 145cm green plaid green vest round glasses stocky
- 水野真帆 Mizuno Maho slim shoulders casual clothes NOT wrong name

---

## DA1 · 投屏无影 · SC-01 · P0 · EXPERT_LOCK ⚠️

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S05-V2-A1 / DA1** |
| 镜头功能 | **S+L** |
| 景别 | **MS** |
| 机位 | 体育馆 · **平视投屏** · NOT 现场摄影 |
| 视觉中心 | **投影白屏上** 五人合照 · **仅水野脚边无影** |
| 第二信息 | 真实地板：器材车+灯杆 **长影横在地上** · 四人影在投屏/地板正常 |
| 人物 | 投屏内五人 L0 · 馆内地面上履き可边缘入画 |
| 场景 | 体育馆预展 · doc16 brief · 四月 |
| 禁项 | 现场排队 · 五人全无影 · 错 cast · chibi · 制服 · 运动鞋 · 身高测量 |
| 正文锚点 | 「合照里——只有她的影子不见了。」 |
| G-BODY锚 | EXPERT_LOCK·Plan B五人·投屏非live shoot |

### 合成 Prompt（G1 · c03 · R3）

```
[STYLE] MS Nagoya elementary gymnasium eye-level viewing large white PROJECTION SCREEN,
VISUAL CENTER on screen: group photo of five students shoulder to shoulder in casual clothes,
ONLY Mizuno Maho shadow missing under her feet on the projected photo floor,
other four Riku Ito Keimi Shiro shadows clearly visible normal on projected floor,
SECOND READ on real gym wooden floor: metal equipment cart long shadow,
tall light pole long diagonal shadow still on floor NOT missing,
Riku blue hoodie Ito orange vest Keimi yellow cardigan Shiro green plaid Mizuno slim casual,
uwabaki white indoor shoes fair-play panorama stitch clue NOT curse NOT supernatural,
NOT live photoshoot queue NOT height measurement NOT studio lineup,
bridge-book watercolor #2A1810 6-7 head NOT chibi NOT seifuku NOT sneakers
[NEGATIVE] all five shadowless live queue height chart 身長測定 backdrop,
wrong names Yamamoto Sato Tanaka horror curse rubber eraser villain lighting
```

**Output**: `V-S05-V2-A1_仅水野无影_G1draft_c04.png`

---

## DA1 · R6 c06 · 投屏无影 · EXPERT_LOCK · SC-01 · P0 ⚠️

> **R3 baseline c03** 机制✅ · 字幕/衣字 P1 · R6 **L0 五人 + 无字 EXPERT_LOCK** · 仅 c06> c03 时替换

### 合成 Prompt（G1 · c06 · R6 L0 face ref + EXPERT_LOCK）

```
Match all five character faces to attached L0 lineup reference:
Riku Shun 142cm blue zip hoodie, Ito Akira 146cm white tee orange-red utility vest,
Kato Keimi 155cm yellow cardigan silver glasses low ponytail,
Matsumoto Shiro 145cm green plaid green vest round glasses stocky,
Mizuno Maho slim shoulders casual clothes NOT villain lighting.
MS Nagoya elementary gymnasium eye-level viewing large white PROJECTION SCREEN,
VISUAL CENTER on screen: group photo five students shoulder to shoulder casual clothes,
ONLY Mizuno Maho shadow missing under her feet on projected photo floor,
other four shadows clearly visible normal on projected floor,
SECOND READ on real gym wooden floor: metal equipment cart long shadow,
tall light pole long diagonal shadow still on floor NOT missing,
uwabaki white indoor shoes fair-play panorama stitch clue NOT curse NOT supernatural,
NOT live photoshoot queue NOT height measurement NOT studio lineup,
bridge-book watercolor #2A1810 6-7 head NOT chibi NOT seifuku NOT sneakers
[NEGATIVE] all five shadowless live queue height chart 身長測定 backdrop,
wrong names Yamamoto Sato Tanaka horror curse caption bar subtitle overlay,
readable text on clothing English Chinese Japanese text in image speech bubbles
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S05-V2-A1_仅水野无影_G1draft_c06.png`

---

## DA1 · R7 c07 · 投屏无影 · EXPERT_LOCK · SC-01 · P0 ⚠️

> **R3 baseline c03** 机制✅ · 字幕/衣字 P1 · R7 **L0 五人 + 无字无 caption** · 仅 c07> c03 时替换

### 合成 Prompt（G1 · c07 · R7 L0 + EXPERT_LOCK no text）

```
Match all five character faces to attached L0 lineup reference:
Riku Shun 142cm blue zip hoodie, Ito Akira 146cm white tee orange-red utility vest,
Kato Keimi 155cm yellow cardigan silver glasses low ponytail,
Matsumoto Shiro 145cm green plaid green vest round glasses stocky,
Mizuno Maho slim shoulders casual clothes NOT villain lighting NO text on clothing.
MS Nagoya elementary gymnasium eye-level viewing large white PROJECTION SCREEN,
VISUAL CENTER on screen: group photo five students shoulder to shoulder casual clothes,
ONLY Mizuno Maho shadow missing under her feet on projected photo floor,
other four shadows clearly visible normal on projected floor,
SECOND READ on real gym wooden floor: metal equipment cart long shadow,
tall light pole long diagonal shadow still on floor NOT missing,
uwabaki white indoor shoes fair-play panorama stitch clue NOT curse NOT supernatural,
NOT live photoshoot queue NOT height measurement NOT studio lineup,
bridge-book watercolor #2A1810 6-7 head NOT chibi NOT seifuku NOT sneakers
[NEGATIVE] all five shadowless live queue height chart 身長測定 backdrop,
wrong names Yamamoto Sato Tanaka horror curse caption bar subtitle overlay,
readable text on clothing English Chinese Japanese text in image speech bubbles
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S05-V2-A1_仅水野无影_G1draft_c07.png`

---

## DA1 · R8 c08 · EXPERT_LOCK shadow gap · KF-LOCK-J++ · SC-01 · P0 ⚠️

> **R3 baseline c03** 机制✅ · 字幕/衣字/馆名牌 P1 · R8 **仅 c08 若 shadow gap 保留** · 禁 batch

### EXPERT_LOCK（A005 DA1 · R8 · c03 shadow gap preserved)

| 必须 | 禁止 |
|------|------|
| 投屏五人合照 · **仅水野脚边无影** · 四人影正常 | 五人全无影 · 现场排队 |
| 真实地板：器材车+灯杆 **长影仍在** | caption bar · 底部字幕条 |
| E06-S 五人脸 slot ②③④⑦+水野 | 衣上可读名 · 馆名牌汉字 |
| uwabaki 白 indoor shoes | MIZUNO MAHO text · 英文 UI |

### E06-S FACE LIBRARY LOCK（五人 · 3840 + Mizuno)

```
Slot ② Riku Shun blue zip hoodie, Slot ④ Ito Akira orange-red utility vest,
Slot ⑦ Kato Keimi yellow cardigan silver glasses, Slot ③ Matsumoto Shiro green plaid green vest,
Mizuno Maho slim shoulders casual white top NO text on clothing
Match all five face geometry to attached L0 3840 reference.
CRITICAL MECHANISM: ONLY Mizuno shadow missing under feet on projected photo; other four shadows visible; cart and light pole long shadows on real gym floor.
```

### 合成 Prompt（G1 · c08 · R8 EXPERT_LOCK no text)

```
E06-S FACE LIBRARY LOCK all five from CHAR_lineup_L0_3840 per slots above.
MS Nagoya elementary gymnasium eye-level viewing large white PROJECTION SCREEN,
VISUAL CENTER on screen: group photo five students shoulder to shoulder casual clothes,
ONLY Mizuno Maho shadow missing under her feet on projected photo floor,
other four Riku Ito Keimi Shiro shadows clearly visible normal on projected floor,
SECOND READ on real gym wooden floor: metal equipment cart long shadow,
tall light pole long diagonal shadow still on floor NOT missing,
uwabaki white indoor shoes fair-play panorama stitch clue NOT curse NOT supernatural,
plain gym wall NO readable school name banner NO caption strip at bottom,
NOT live photoshoot queue NOT height measurement NOT studio lineup,
bridge-book watercolor #2A1810 6-7 head NOT chibi NOT seifuku NOT sneakers
[NEGATIVE KF-LOCK-J++] all five shadowless live queue height chart 身長測定 backdrop,
wrong names Yamamoto Sato Tanaka horror curse caption bar subtitle overlay,
readable text on clothing MIZUNO MAHO English Chinese Japanese text in image speech bubbles,
gymnasium name sign banner UI HUD boxes bottom metadata strip
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S05-V2-A1_仅水野无影_G1draft_c08.png`

---

## DA3 · 拍摄信息三帧 · SC-05 · P0

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S05-V2-A3 / DA3** |
| 镜头功能 | **L+C** |
| 景别 | **MCU** |
| 机位 | 平板 POV 框中框 |
| 视觉中心 | **分段曝光三帧** · 水野侧让帧高亮 |
| 第二信息 | 时间戳 10:52:03/05/07 可读 |
| 正文锚点 | 「十四秒拼成一张——她侧让的那一帧，没有影。」 |
| 禁项 | 五人全无影 · 诅咒 · metadata 术语入叙事 |

### 合成 Prompt（G1 · c02 · 未改）

```
[STYLE] MCU tablet POV frame-in-frame three exposure segments timeline readable,
Mizuno side-step frame highlighted timestamp 10:52:03 10:52:05 10:52:07,
gymnasium projection soft background Riku Shun blue hoodie studying NOT curse,
Keimi yellow cardigan notebook edge silver glasses Shiro green vest edge,
fair-play panorama stitch clue casual clothes NOT seifuku bridge-book watercolor
[NEGATIVE] all five shadowless horror curse rubber eraser crumbs villain lighting
```

**Output**: `V-S05-V2-A3_metadata三帧_G1draft_c04.png`

---

## DA6 · 重拍有影 · SC-08 · P0 · EXPERT_LOCK ⚠️

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S05-V2-A6 / DA6** |
| 镜头功能 | **L+P** |
| 景别 | **MS** |
| 机位 | 重拍区 · **单次快门** moment · NOT 身高测量 |
| 视觉中心 | **五影全在** · 水野影回来 · 地板影可读 |
| 第二信息 | 相机三脚架可见 · 可选小 inset 对照 DA1 投屏 |
| 禁项 | 身高测量 · 身長測定 banner · 五人全无影 · 检修场景 · 运动鞋 |
| 正文锚点 | 「单次快门——五个影子，都在。」 |
| G-BODY锚 | EXPERT_LOCK验证帧·L0五人私服上履き·与DA1对照 |

### 合成 Prompt（G1 · c03 · R3）

```
[STYLE] MS gymnasium reshoot area five students standing in line for single shutter photo,
ALL five shadows clearly visible on polished gym floor INCLUDING Mizuno Maho shadow returned,
camera on tripod in foreground LCD showing same five-person frame,
Riku Shun blue hoodie Ito Akira orange vest Keimi yellow cardigan silver glasses
Shiro green plaid green vest Mizuno Maho casual clothes all uwabaki white indoor shoes,
bright overhead gymnasium April light equipment cart edge visible,
contrast optional small projection screen inset showing previous missing shadow moment,
repair fair-play NOT supernatural NOT seifuku NOT sneakers NOT maintenance scene,
NOT height measurement NOT 身長測定 NOT school banner with cm lines,
Nagoya elementary gymnasium bridge-book watercolor #2A1810
[NEGATIVE] height chart backdrop 身長測定 measuring lines school name banner,
five shadowless live studio queue wrong names horror English text blocks outdoor shoes
```

**Output**: `V-S05-V2-A6_重拍有影_G1draft_c04.png`

---

## DA6 · R7 c07 · 五影全在 · EXPERT_LOCK · SC-08 · P0 ⚠️

> **R3 baseline c03** 五影✅ · 英文 UI P1 · R7 **无字 reshoot + 全员 uwabaki**

### 合成 Prompt（G1 · c07 · R7 L0 + five shadows no text）

```
Match all five character faces to attached L0 lineup reference:
Riku Shun 142cm blue zip hoodie, Ito Akira 146cm white tee orange-red utility vest,
Kato Keimi 155cm yellow cardigan silver glasses low ponytail,
Matsumoto Shiro 145cm green plaid green vest round glasses stocky,
Mizuno Maho slim shoulders casual clothes.
MS gymnasium reshoot area five students standing in line for single shutter photo,
ALL five shadows clearly visible on polished gym floor INCLUDING Mizuno Maho shadow returned,
camera on tripod in foreground LCD showing same five-person frame NO readable text on screen,
all five wearing white uwabaki indoor shoes NOT sneakers NOT outdoor shoes,
bright overhead gymnasium April light equipment cart edge visible,
contrast optional small projection screen inset showing previous missing shadow moment NO caption text,
repair fair-play NOT supernatural NOT seifuku NOT maintenance scene,
NOT height measurement NOT 身長測定 NOT school banner with cm lines,
Nagoya elementary gymnasium bridge-book watercolor #2A1810
[NEGATIVE] height chart backdrop 身長測定 measuring lines school name banner,
five shadowless live studio queue wrong names horror English text blocks speech bubbles caption overlay
```

**L0 ref**: `CHAR_lineup_L0_专家共识_画师发包_3840.png` **mandatory**  
**Output**: `V-S05-V2-A6_重拍有影_G1draft_c07.png`

---

*A005 G1 prompts R7 · V0.7 · doc65 STYLE_LOCK · EXPERT_LOCK*
