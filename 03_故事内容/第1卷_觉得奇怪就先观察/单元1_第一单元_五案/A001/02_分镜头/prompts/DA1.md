# A001 · DA1 · Prompt · V3.6

> **Status**: G1DRAFT_PRODUCTION · 试读 PDF 用  
> **Shot Map**: [`03_分镜头_插页地图_V3.9_JP.md`](../03_分镜头_插页地图_V3.6_JP.md)  
> **正文锚**: [`../01_正文/案01_全班都听见了他的声音_HybridVoice_V3.9_日本語.txt`](../01_正文/案01_全班都听见了他的声音_HybridVoice_V3.9_日本語.txt)

## 画面内容提示词 · V3.9

| 字段 | 内容 |
|------|------|
| 画面瞬间 | 四月上午，合班教室里天花板喇叭正在响；讲台上光站着，嘴刚张开，气息还没成句，但全校已经「听见他的声音」。 |
| G-CAST MAX | 6 |
| 画中文字 | **なし**（PLAY 屏可抽象波形+播放图标，**不可读**英文/中文句） |
| 重绘 | ⚪ |
| JP V3.9 锚句 | 「合同教室（ごうどうきょうしつ）で、光は教壇に立ち、口はまだ開いている……息しか出ない。保健室の指示ははっきりしていた。今日は発声禁止。それなのに天井の放送スピーカーは明るく、はっきりしていた。」 |

## 文化锁 · 田中みどり · 教壇（2026-06-10）

| 项 | 结论 |
|----|------|
| **学生能否站教壇？** | **✅ 成立** — 仅限制度性场合：日直（起立/礼）、被点名**発表/说明**、**公開日·学習発表会彩排** |
| **本案** | 正文：光「名前を呼ばれ、教壇に**上がって**放送の流れを説明」→ **合同教室彩排** · PASS |
| **❌ 禁止** | 站**机の上**（课桌）· 无点名随意占教壇 · 手持麦克风（本校用天井 PA + 教壇横放送卓） |
| **画内执行** | 光**双脚在教壇台阶上**（黑板前低台）· 嘴微张仅气声 · 无手持麦 |

> 内容层描述（非 Style 词块）。Style B 见下方 Global STYLE。

## 出图硬锁 · g_cast_prompt_gate

> **引用**：[`00_PROMPT_HARD_LOCK_V1.0.md`](./00_PROMPT_HARD_LOCK_V1.0.md) · PROMPT_HARD_LOCK

| LOCK | 词块 |
|------|------|
| 珣发色 | soft messy BLACK hair `#1A1818` |
| 光发色 | spiky WARM BROWN hair `#6A4830` |
| 禁 | NO Chinese text · NO 学堂趣事录 · NO 葛西泉藏 · NO nameplates |
| 群众 | anonymous faceless classmates — no extra L0 faces beyond G-CAST MAX |
| 具名 | 光 · 珣 · 慧美 · 志郎（按 G-CAST 表） |
| 鞋 | white uwabaki · 上履き · NO sneakers |

## §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **DA1** |
| 所属 | Vol1 · A001 · SC-02 |
| 原文范围 | V3.9 JP · 见 Shot Map JP 锚点句 |
| 镜头功能 | **S+L** |
| 强制级 | **P0** |
| 景别 | **MS** |
| 机位 | 合班教室·东向平视·三分构图 |
| 视觉中心 | 天井放送スピーカーが鳴っている |
| 第二信息 | 教壇の光·唇がまだ動いていない·PLAY屏 |
| 服道化 | 上履き·四月光·器材車·発声禁止届 |
| JP 锚点句 | 合同教室（ごうどうきょうしつ）で、光は教壇に立ち、口はまだ開いている……息しか出ない。保健室の指示ははっきりしていた。今日は発声禁止。それなのに天井の放送スピーカーは明るく、はっきりしていた。 |

## Global STYLE

```
STYLE_B_LOCK:
alcohol marker pen (Copic-like) flat color illustration,
clean warm brown ink outline #2A1810, light paper grain only,
NOT watercolor wash NOT painterly wash NOT wet-on-wet NOT muddy grain,
NOT cel-shaded anime NOT 3D NOT flat vector UI,
Nagoya public elementary classroom April slanted window light,
Japanese children ages 10-12 bridge-book 6-7 head, casual clothes white uwabaki,
IP 学堂奇事録 observation club fair-play mystery
```

## Global NEGATIVE

```
NEGATIVE_STYLE_B:
watercolor painting, watercolor wash, painterly digital-anime, wet paper texture,
heavy grain, REF04 style, b169491b mood, cel-shade, chibi, seifuku, sneakers,
English text, Chinese text, adults parents Kasai in classroom, character spec cards
```

## 合成 Prompt

```
[STYLE] MS 合班教室·东向平视·三分构图,
VISUAL CENTER: 天井放送スピーカーが鳴っている,
SECOND READ: 教壇の光·唇がまだ動いていない·PLAY屏,
characters and props per 14_v2 L0 and Vol1画风Sheet,
fair-play clue readable without text arrows, Nagoya elementary April uwabaki,
scene context: 合同教室で、光は教壇に立ち、口はまだ開いている……息しか出ない。それなのに天井の放送スピーカーは明るく、はっきりしていた。...
[NEGATIVE]
```
