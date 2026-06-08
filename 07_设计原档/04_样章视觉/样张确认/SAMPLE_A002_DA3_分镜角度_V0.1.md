# SAMPLE · A002 · DA3 · 分镜角度 · V0.1-SAMPLE

> **Status**: **SAMPLE-GATE · 待 IP 签** · 2026-06-08  
> **用途**: Vol1 Unit1 插画 batch **第二** 试跑帧 · 验证 **机位/景别/POV** 纪律（非重复 DA1）  
> **案**: A002 · SC-05 · **V-S02-V2-A3 / DA3**  
> **输出**: `03_故事内容/第1卷_觉得奇怪就先观察/样章包/插图/样张确认/SAMPLE_A002_DA3_分镜角度_V0.1.png`  
> **前版样张**: [`SAMPLE_A002_DA1_修正_V0.1.md`](./SAMPLE_A002_DA1_修正_V0.1.md) · 风格 partial PASS · 角度 off  
> **根因计划**: [`72_插画第三次跑偏_根因与样张修正计划_V0.1.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/72_插画第三次跑偏_根因与样张修正计划_V0.1.md)

---

## 0. 帧选择理由

| 候选 | R17 机位块 | 为何不选 / 为何选 |
|------|-----------|------------------|
| A002 DA1 | MS–CU · 黑板平视·三分 | ✅ 已出样张 · 用户反馈 **角度/取景 off** · 不重复 |
| **A002 DA3** | **MCU · 板槽POV斜光** | ✅ **选用** — R17 + §11 + CLASS_5-2 均有 **POV/ECU 硬规格**；机制曾 G-BODY PASS（膜边）；与 DA1 景别/机位 **完全不同** |
| A001 DA1 | PA 广播 MS | 唇不同步机制强 · 但教室合班机位不如 DA3 POV 硬 |
| A003 DA1 | 走廊空海报位 | 机位有定义 · 无 ECU/POV 深度锚 · 第二样张优先测 **板槽 POV** |

**结论**: DA3 = doc62 MVP 帧 · doc65 R3 唯一 G-BODY 机制 PASS 候选 · **机位块最清晰** → 本样张专测 **分镜角度纪律**。

---

## 1. 分镜 §11（R17 · 冻结 · 逐字引用）

> SSOT: [`A002_分镜拆解_R17_V0.1.md`](../分镜拆解/A002_分镜拆解_R17_V0.1.md) · DA3 行

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S02-V2-A3 / DA3** |
| 所属 | Vol1 · A002 · **SC-05** |
| 镜头功能 | **L+C** |
| 强制级 | **P0** |
| 景别 | **MCU** |
| 机位 | **板槽POV斜光** |
| 视觉中心 | **FC-1膜边反光** |
| 第二信息 | 清洁液·FC-3时序 |
| 人物 | **珣·志郎** |
| 服道化 | 透明膜边·窗缝光 |
| 禁项 | — |
| 正文锚点 | 「膜边有一条细线，像有人贴过又揭。」 |
| G-BODY锚 | **板槽POV自C1侧合理** |
| MVP | ✅ |

### 1.1 §11 扩展（G1 prompt · doc62 必填六列）

| 字段 | 值 |
|------|-----|
| 景别（执行） | **MCU → ECU**（膜边微距 · doc65 §7 科学 ECU 许可：膜边=不可替代 FC-1） |
| 机位（执行） | **板槽 POV 近距** · 自 **R3·C1 廊下侧** 仰视板槽 · 四月窗缝 **斜光 45°** · **NOT 全身 lineup** |
| 构图 | **框中框**（绿板槽金属边 = 内框）· **引导线**（膜边反光线 → 珣指尖）· **浅景深**（膜边 sharp / 板面 soft） |
| 视觉中心 | 绿黑板 **板槽内** 透明展示膜 **膜边反光细线** 斜光亮一下 |
| 第二信息 | 清洁液瓶缘 · 样品袋「未登记」形（**无可读字**）· 珣手指指向板槽边缘 · 志郎袖/手在槽缘演示（partial） |
| 禁项 | character lineup board · height measure · portrait grid · 鬼怪 · 制服 · 6年2組门牌 |

**座席 SSOT**: [`CLASS_5-2_教室插图表_V0.1.md`](../CLASS_5-2_教室插图表_V0.1.md) — A002 DA3–DA4 · **板槽 POV 自 C1 侧合理**

---

## 2. 机位纪律 · P0（本样张核心）

```
CAMERA BLOCK (P0 · angle discipline · NOT ad-hoc):

Shot size:    MCU base frame, ECU on film-edge glint (CU minimum for L-frame per doc65 §4.1)
POV:          Subjective near-POV from Riku at R3·C1 corridor-side, camera height ~120cm child eye level
Angle:        Slight low angle 15° looking UP at board-slot ledge (NOT flat blackboard MS like DA1)
Axis:         Camera on C1 corridor side facing north blackboard (CLASS_5-2 grid)
Depth:        FOREGROUND sharp: film-edge glint + Riku index finger
              MID: board-slot metal lip, cleaning bottle silhouette
              BACKGROUND soft: green chalkboard surface, April window light streak
Framing:      NO full-body characters · NO lineup grid · crop to board-slot ledge horizontal band
              Bottom 10%: white uwabaki toe edge only · Top 60%: green board + slot
Light:        Single source April slanted window light from upper-left 45°, dust motes optional
```

**与 DA1 差异（用户反馈修正点）**:

| 维度 | DA1 样张 | DA3 本样张 |
|------|----------|------------|
| 景别 | MS–CU 黑板平视 | **MCU–ECU 板槽 POV** |
| 机位 | 三分构图平视整板 | **C1 侧 POV · 15° 略仰 · 框中框槽缘** |
| 视觉中心 | ごめんなさい。粉笔字 | **膜边反光细线** |
| 人物占比 | 三人 MS 全身倾向 | **仅手/袖/鞋缘 partial** |

---

## 3. STYLE_LOCK · A 轨（继承 DA1 V0.1 PASS · doc65 §3）

**主 mood ref**: `assets/…b169491b…png` — Nagoya 活动室内 · 温暖电影水彩 · 私服 · 上履き  
**辅助 mood**（肌理/光 · 禁构图复制）: `f2069ebd` scrapbook 纸纹 · `cb5c48e7` 走廊侧光  
**B 轨 only**: `d6564b40` instructional — **禁入本帧**

### 3.1 Global STYLE_LOCK（embed 首部）

```
A-TRACK Vol1 SAMPLE A002 DA3 board-slot POV ECU,
Nagoya public elementary school Japanese peers NOT Chinese aesthetic NOT generic anime classroom,
casual clothes day white uwabaki indoor shoes toe edge visible NOT sneakers NOT outdoor shoes,
aluminum window frames April late cherry new green slanted cinematic side light 45 degrees dust motes,
clear light-manga ink warm brown outline #2A1810 NOT pure black,
restrained watercolor paper texture gentle wash NOT flat vector NOT 3D NOT thick oil,
6-7 head pre-teen proportions ages 10-12 bridge-book NOT chibi NOT SD NOT instructional infographic,
warm golden cinematic observation-club daily mystery fair-play clue readable zero horror zero supernatural
```

---

## 4. L0 角色锁（E06-S · 本帧 partial 出场）

**垫图 mandatory**: [`CHAR_lineup_L0_专家共识_画师发包_3840.png`](../CHAR_lineup_L0_专家共识_画师发包_3840.png)

| Slot | 角色 | 本帧可见部位 | L0 P0（含 V0.2 珣手术块） |
|:----:|------|-------------|---------------------------|
| **②** | **陸 珣** Riku Shun | 右手/前臂 · 鞋缘 · 可选背包带角 | **142cm** · 藏青 **zip 外套 NO hood** `#3A5080` · 黄内衬袖缘 `#E8C848` · **白袜+纯白上履き** 禁蓝带 · 食指指向膜边 · 手 **不插兜** |
| **③** | **松本 志郎** Matsumoto Shirō | 左缘 partial 前臂/袖（演示边） | **145cm 矮壮** · **绿格衬衫 + 绿 utility vest**（A002 当番服道 · 非扫除网 vest）· 圆框镜可虚化 · 持清洁布角 |

**本帧不出**: 慧美⑦（清洁液仅作道具 silhouette）· 光④ · 瑆① · 全班

**名称锁**: 画内若出现标签 → 禁 **陆瑆** · **陆** 简体 · **5年2组** · 任何中文

---

## 5. 场景 · CLASS_5-2 · 板槽区

| 项 | 规格 |
|----|------|
| 空间 | 5年2組 本班 · **绿黑板北墙** · **板槽金属唇** 居中画幅 · 非整板 MS |
| 光 | 四月上午铝窗斜光 · 窗缝光打在膜边 · 单光源 |
| 道具 | 板槽内透明展示膜 · 清洁液喷瓶 · 样品塑封袋（空白标签形）· 板擦可选远景 |
| 鞋 | 珣 **白上履き** 画幅底缘 10% · 贴地可见 · 禁运动鞋 · 禁蓝色彩带 |
| 机制 | **膜边反光细线** = FC-1 · 清洁液 = FC-3 时序种子 · **禁** ごめんなさい。占满画幅（DA1 专属） |

SSOT: [`CLASS_5-2_教室插图表_V0.1.md`](../CLASS_5-2_教室插图表_V0.1.md)

---

## 6. 画内文字 · KF-LOCK-J（P0）

| 必须 | 禁止 |
|------|------|
| **无可读文字**（膜边/清洁液/袋标签均 blur 或空白形） | ごめんなさい。 · 对不起 · 未登録 可读日文 · 任何中文 |
| 样品袋 = 空白手写标签 **形状** only | 学堂趣事录 · 5年2组 · 身長測定 |

---

## 7. HARD NEGATIVE（必贴 prompt 尾部）

```
[NEGATIVE KF-LOCK-J++ SAMPLE GATE DA3 ANGLE]
simplified Chinese text, traditional Chinese, 对不起, ごめんなさい, 未登録 legible, 学堂趣事录, 学堂奇事录 Chinese title,
5年2组, 5年2班, wrong name 陆瑆, 陆 Liu, 陆珣 simplified 陆,
character lineup board, height chart, portrait grid, roster poster, 身長測定, 11 slots student wall,
MS flat blackboard full classroom view like DA1, hero three-shot composition, full body five students queue,
6年2組 door plate, 4年2組 homeroom plate, seifuku, gakuran, school uniform, sneakers, outdoor shoes,
chibi, SD, Q-version, instructional infographic, textbook diagram panels, manga panel borders,
English UI, sticky notes, speech bubbles, caption overlay, watermark,
generic Chinese classroom, fluorescent neon, horror, ghost writing, detective magnifying glass pose,
Riku hoodie hood visible, hands in pockets, spiky hair, blue uwabaki strap, dark crew socks,
Matsumoto in green cleaning mesh vest instead of L0 plaid, full blackboard apology text stealing frame
```

---

## 8. 合成 Prompt · V1.0-SAMPLE（一键复制）

```
A-TRACK Vol1 SAMPLE A002 DA3 board-slot POV ECU angle discipline,
CAMERA: MCU to ECU subjective near-POV from R3-C1 corridor side child eye level 120cm,
slight low angle 15 degrees looking UP at green chalkboard BOARD SLOT ledge only NOT full blackboard MS,
frame-in-frame metal slot lip horizontal band, shallow depth film-edge sharp board soft,
April slanted window light 45 degrees upper-left catching transparent display film edge glint line,
VISUAL CENTER: thin bright reflective glint on transparent film where film meets chalkboard slot,
SECOND READ: cleaning fluid spray bottle silhouette on ledge, small sample plastic bag blank tag shape NO letters,
Riku Shun slot2 partial: navy zip jacket sleeve #3A5080 NO hood yellow inner cuff #E8C848,
index finger pointing at film glint NOT in pockets, plain white uwabaki toe edge bottom frame white socks,
Matsumoto Shirou slot3 partial left edge: green plaid shirt green utility vest sleeve demonstrating at slot NOT writing pose,
5年2組 Nagoya RC classroom April fair-play film clue NOT ghost writing NOT lineup NOT height chart,
clear light-manga ink #2A1810 restrained watercolor paper texture cinematic warm 6-7 head NOT chibi NOT seifuku,
observation club daily mystery bridge-book illustration b169491b mood

Match Riku sleeve and Shirou vest to CHAR_lineup_L0_3840 slots 2 and 3 partial only.

[NEGATIVE KF-LOCK-J++ DA3] simplified Chinese 对不起 ごめんなさい 学堂趣事录 lineup board height chart portrait grid,
MS flat blackboard three-shot full body queue 6年2組 seifuku chibi SD infographic English UI speech bubbles,
hoodie hood hands in pockets blue uwabaki strap Chinese classroom ghost writing apology text full frame
```

---

## 9. 验收 · G-BODY（样张 · 角度优先）

| Gate | 检查 |
|------|------|
| **ANGLE P0** | MCU–ECU · 板槽 POV 自 C1 · 15° 略仰 · 非 DA1 平视 MS · 非 lineup/身長 |
| S1–S5 | A 轨 b169491b mood · 非 chibi · 水彩纸纹 |
| C1–C2 | 珣袖/指/上履き L0（V0.2：无帽·白袜·无蓝带）· 志郎绿格+绿 vest partial |
| C6–C7 | 5年2組 板槽区 · 上履き缘 · 非 4-2/6-2 |
| C9 | POV 自 R3·C1 合理 · 非窗 C6 · 非 C 位全身 |
| E1 | RC 教室绿板 · 四月铝窗斜光 |
| §4 A002 | **膜边反光** readable · 非整板对不起 |
| **KF-LOCK-J** | **零中文** · 零可读错名 · 零 lineup |

**Verdict 栏**: ☐ PASS → 解锁 batch · ☐ REVISE · ☐ REJECT

---

## 10. 用户确认清单（签前必答）

| # | 确认项 | Pass 标准 |
|---|--------|-----------|
| 1 | **机位/景别** | 板槽 POV ECU · C1 侧 · 略仰 · **非** DA1 平视三分 MS |
| 2 | **A 轨画风** | b169491b 温暖电影水彩 · 非 chibi 教辅 |
| 3 | **日本同辈感** | 名古屋 RC · 铝窗斜光 · 私服+白上履き |
| 4 | **L0 partial** | 珣藏青无帽袖+白上履き · 志郎绿格+绿 vest 缘 |
| 5 | **画内文字** | 零可读字 · 零中文 |
| 6 | **机制** | 膜边反光细线清晰 · 非 ghost · 非 lineup |
| 7 | **流程** | 与 DA1 样张双签后解锁 batch |

**签栏**: IP Owner ☐ · visual-auditor ☐ · 日期 ______

---

*V0.1-SAMPLE · 分镜角度专测帧 · A002 DA3 板槽 POV · batch 仍冻结待 IP 签。*
