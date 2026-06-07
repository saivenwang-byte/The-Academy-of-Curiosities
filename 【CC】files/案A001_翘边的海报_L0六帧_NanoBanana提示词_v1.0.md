# 案 A001《翘边的海报 / めくれたポスター》· L0 六帧 · Nano Banana 出图提示词 v1.0

> **目标**：闭合 Gate A 的视觉瓶颈——把现状板上标「未交付」的 **L0 六帧 v1.0**（与 G1 PNG）做出来。
> **基线**：`06_A001_L0六帧_v1.0_生产清单.md` + `P0-01_第一话正典摘要卡_V1.0`（IP LOCK）+ 现有 `prompts_A001_深度锚点_v2_正篇画风.md`（本文为其 v1.0 升级，承接 v0.2 探索稿）。
> **画风（LOCK，非水彩）**：Modern Japanese **bridge-book anime**, clean organic line art, soft painterly **digital** coloring, warm golden-hour cinematic lighting, realistic 10–12yo 6–7 heads **NOT chibi**。参考 Sheet：`07_设计原档/04_样章视觉/Vol1_正篇画风_角色设定Sheet_用户参考_v1.png`。
> **人名（LOCK）**：伊藤光 = **Ito Akira**（非 Hikaru）· 陸珣 = **Riku Shun**（非 Jun）· 加藤慧美 = Kato Keimi · 松本志郎 = Matsumoto Shiro。图内不渲染人名文字。
> **注意**：本案 = **翘边的海报**（侧廊·风侧·湿度·胶带），**非湿椅子**（湿椅子仅作插图深度参照）。此前那份「湿椅子逐镜」不用于 Gate A。

---

## 0. 全帧共用

**STYLE（每条开头）**
```
Modern Japanese bridge-book anime illustration, clean organic line art, soft painterly digital coloring with warm golden-hour cinematic lighting, realistic 10-12 year old proportions 6-7 heads NOT chibi, large expressive eyes but grounded pre-teen bodies, rich daily-life texture, Nagoya public elementary school April afternoon, gentle fair-play mystery mood, no horror.
```
**NEGATIVE（每条结尾）**
```
watercolor wash, rough pencil sketch only, chibi SD, horror, ghost, supernatural glow, Chinese classroom, detective trench coat, dark scary lighting, English or any rendered text in image, watermark, fluorescent colors, giant textbook arrows
```
**分辨率**：A 轨 DA1–DA4 长边 **3200px**；B/C 轨 DB1·DC1 长边 **2400px**。
**P0 验收顺序**：**DA1 → DA3 → DA4 → DB1 → DA2 → DC1**。

**主参考图优先**：先用画风 Sheet 锁定四人春装定妆图，再带参考图出场景，并每帧复述锚点：
- **Ito Akira（光·155）**：橙红运动外套 · 刺猬棕发 · 哨子 · 硬壳本 · 行动发起
- **Kato Keimi（慧美·145）**：黄开衫 · **低侧马尾+耳侧短辫+柔黄发带（LOCK）** · 银框镜 · 采访本
- **Matsumoto Shiro（志郎·142）**：红T+绿背心 · 圆框镜 · 矮壮 · 查证卡
- **Riku Shun（珣·146）**：蓝卫衣+黄内搭 · 乱黑发 · 路线地图本 · **侧后冷静位**
- **G1 灰模 LOCK**：DA1–DA4 为同一条侧廊，门/窗朝向与海报位置**像素级一致**。

---

## DA1 · 侧廊发现（P0 · 主钩子）— MS · G1 机位A 东向平视 · 4:3 · 3200px

**EN PROMPT**
```
[STYLE] 4:3 horizontal, high detail. The OUTSIDE side-corridor of a Nagoya elementary school activity-preparation room, April, a few cherry petals optional, west light slanting through aluminium-sash windows, cool corridor air. On the wall a handmade recruitment poster reads 学校おもしろ観察クラブ with a simple eye doodle — its entire RIGHT edge curls/peels upward. On that SAME side, just above/beside the poster, are an air-conditioner vent grille and a gap in the aluminium window: the curl is on the same side as the vent and the window gap (fair clue, but NO explanatory arrows of any kind). Four kids in indoor shoes (uwabaki): Ito Akira (taller ~155cm, spiky brown hair, orange-red athletic jacket, whistle, hardcover notebook, just spotted it, energetic); Kato Keimi (~145cm, low side ponytail plus a short braid by the ear and a soft yellow hairband, yellow cardigan, silver-rim glasses, interview notebook); Matsumoto Shiro (~142cm, stocky, red tee under green utility vest, round glasses, reference cards); Riku Shun (~146cm, messy black hair, blue hoodie over yellow shirt, route-map book, standing slightly BEHIND and to the side as a quiet observer at the corridor entrance). At least 3 kinds of corridor props clearly visible: pushpins, a clip-board with slot grid, a magnet, the aluminium sash, the vent grille. Cozy fair-play discovery mood. [NEGATIVE]
```
**图内必见**：海报右缘上翘 + vent/窗缝同侧；四人；珣侧后入口位。 **必避**：任何"指向答案"的箭头；恐怖。 **v1.0 验收**：画风 Sheet T1 · G1 背景 LOCK · 环境道具≥3类 · 身高比 155/145/142/146。

---

## DA3 · 风侧线索（P0 · 公平线索 CU）— CU · G1 机位B · 框中框 · 4:3 · 3200px

**EN PROMPT**
```
[STYLE] close-up educational beat, 4:3 horizontal, high detail. A tight FRAME-IN-FRAME composition that links three things on the SAME side: the air-conditioner vent grille, the gap in the aluminium window, and the curling edge of the 学校おもしろ観察クラブ poster — this co-location IS the fair clue, shown by composition only, with absolutely NO arrows. Kato Keimi is the focus (yellow cardigan, low side ponytail + short braid by the ear + soft yellow hairband, silver-rim glasses), leaning in to write in her interview notebook or lightly indicating the spot. Ito Akira (orange-red jacket) and Matsumoto Shiro (green vest) are partly visible at the edges. Fine, quiet details: faint moisture / a few water droplets near the window gap, a misty rainy-day feel (optional, gentle, never scary), a magnet, a pin, a pencil mark. Soft cinematic light. [NEGATIVE]
```
**图内必见**：vent+窗缝+翘边**同侧**(框中框)；慧美主体。 **必避**：巨型教辅箭头、任何暗示性箭头;恐怖湿痕。 **v1.0 验收**：画风 Sheet T3 · P0-04 DA3 行 PASS · 框中框加严。

---

## DA4 · 验证收束（P0 · C04 人的原因）— MS · G1 机位A变体略低 · 4:3 · 3200px

**EN PROMPT**
```
[STYLE] resolution beat, warm golden light, 4:3 horizontal, high detail, same side-corridor as DA1 (consistent door/window). Matsumoto Shiro (stocky, red tee + green utility vest, round glasses) is re-sticking the poster in a NEW direction, OR placing a clear file folder beside it as a wind shield — the action is STEP-READABLE (you can tell what he is doing). Ito Akira (orange-red jacket, hardcover notebook) and Kato Keimi (yellow cardigan, side braid + soft yellow hairband, silver glasses) and Riku Shun (blue hoodie, route-map book) stand relaxed nearby; Shiro looks relieved. Near them a wall-newspaper draft shows three columns already filled in with pencil writing. Calm, friendly, post-solved mood. NO caption text explaining "because of wind". [NEGATIVE]
```
**图内必见**：志郎换向贴/文件夹挡风(分步可读)；壁报草稿三栏 pencil；四人放松。 **必避**："因为风"之类解谜 caption。 **v1.0 验收**：画风 Sheet T4 · 换贴动作可读。

---

## DB1 · 风侧机制 SUM（P0 · B 轨机制信息图）— 信息图 · 非透视 · 4:3 横 · 2400px

**EN PROMPT**
```
A hand-drawn children's-notebook style infographic (NOT a perspective scene, NO human characters), 4:3 horizontal, on a light paper texture background color #F7F3EE, soft painterly digital coloring, gentle and friendly. Three labelled cells arranged left to right: (1) an air-conditioner vent grille + a window gap, with a light hand-drawn arrow showing air flow lifting the poster's edge; (2) a rainy-day / humidity symbol with a strip of tape losing its stickiness; (3) a poster being re-stuck in a new direction next to a clear file folder acting as a wind shield. Use simple LIGHT hand-drawn arrows (never heavy), leave clean space for JAPANESE main labels only, no formulas, no textbook or PowerPoint look, no clutter. Information density on par with a polished picture-book explainer page. No spoiler about any next case. [NEGATIVE]
```
**图内必见**：三格①出风/窗缝 ②湿度/雨日 ③贴法/文件夹；日文主标注位；浅底纸纹。 **必避**：公式堆砌、PPT/教辅风、人物主视觉、剧透 A002。 **v1.0 验收**：画风 Sheet T5 · 对标湿椅子09 · 日文字 E04 LOCK。

---

## DA2 · 误导搜查（P1 · 误导节拍）— MS · G1 机位A 同轴 · 4:3 · 3200px

**EN PROMPT**
```
[STYLE] 4:3 horizontal, the SAME Nagoya side-corridor as DA1 with pixel-level continuity of the door, windows and the curling poster in the same position. Misdirection beat: Matsumoto Shiro (red tee + green utility vest, round glasses) crouches in an exaggerated, playful floor-search pose, proposing a prank theory — clearly NON-violent and a little comedic. Ito Akira (orange-red jacket) shakes his head, a bit tense. Kato Keimi (yellow cardigan, side braid + soft yellow hairband, silver glasses) stops Shiro with her notebook. Riku Shun (blue hoodie, route-map book) stands aside, quietly recording, NOT joining the hype. The curled poster and the vent/window are visible in the background (same side). April, uwabaki, warm cinematic light. [NEGATIVE]
```
**图内必见**：志郎夸张蹲查(非暴力)；光摇头；慧美制止；珣侧记录不跟风；背景海报与 DA1 连续。 **必避**：暴力搜查；走廊不连续。 **v1.0 验收**：画风 Sheet T2 · 同走廊像素级可识别。

---

## DC1 · 壁报空栏尾钩（P1 · L1 尾钩）— CU/¼页 · G1 机位C · 暖光 · 2400px

**EN PROMPT**
```
[STYLE] warm cozy close-up, ¼-page crop, 4:3 or vertical. The bulletin/wall-news draft board at the END of the side-corridor — clearly a SEPARATE board from the recruitment poster (spatial separation, the poster board is not this board). The draft has FOUR columns: three columns are filled with neat pencil writing, and the FOURTH column is deliberately left BLANK, with a tiny pencil "？" in it (clear contrast so the empty column reads instantly). A small handwritten witness note reads 陸珣・風側. Optionally only a child's hand and a pencil enter the frame. Warm afternoon light, gentle hopeful mood. No next-case submission strip, no spoiler. [NEGATIVE]
```
**图内必见**：草稿四栏(三栏 pencil + 第4栏空 + tiny ？)；witness 小字「陸珣・風側」；壁报板≠海报板。 **必避**：A002 投稿窄条、剧透。 **v1.0 验收**：画风 Sheet T6 · 海报板与壁报栏空间分离。

---

## 科学线索 → Shot 映射（图内必见对照）

| 公平线索 | 主 Shot | 图内必见 |
|---|---|---|
| 翘边 = 出风/窗缝同侧 | DA1 + DA3 | vent 与翘边同侧构图 |
| 雨天/湿度加重 | DA3 + DB1 | 湿痕/薄雾 · DB1 格② |
| 志郎换贴方向（C04 非恶意） | DA4 | 换向贴/文件夹挡风 |
| 壁报空栏规矩（L1 尾钩） | DC1 | 第4栏空 + ？ |

## 出图后流程
1. 一帧出 3–4 张候选；P0 顺序 **DA1→DA3→DA4→DB1→DA2→DC1**。
2. 交 `visual-consistency-reviewer` 审核——重点：四人锚点（Akira 橙外套/Keimi 发带 LOCK/Shiro 红绿/Shun 蓝卫衣侧后）· **画风=bridge-book 非水彩** · vent 与翘边同侧 · **无答案箭头** · 零恐怖 · 图内无文字（DB1/DC1 仅日文标注位留白）· G1 同走廊一致。
3. 科学顾问签 **P0-04**（DA3 行优先）。
4. PASS → 存入 `样章包/插图/depth_anchor/ → 正式版/02_插画/assets/`，记录提示词+参考图+seed/工具+日期。
5. 四栏签核齐 → **E06 终签**，Gate A 闭合。
