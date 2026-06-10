# A005 · DA3 · Prompt · V3.6

> **Status**: G1DRAFT_PRODUCTION · 试读 PDF 用  
> **Shot Map**: [`03_分镜头_插页地图_V3.9_JP.md`](../03_分镜头_插页地图_V3.6_JP.md)  
> **正文锚**: [`../01_正文/案05_午休后消失的影子_HybridVoice_V3.9_日本語.txt`](../01_正文/案05_午休后消失的影子_HybridVoice_V3.9_日本語.txt)

## 画面内容提示词 · V3.9

| 字段 | 内容 |
|------|------|
| 画面瞬间 | 平板 POV 框中框：十四秒照片 stitched 成一张；分段曝光三帧并排；水野侧让帧高亮。 |
| G-CAST MAX | 2 |
| 画中文字 | **なし** 或 时间戳 **`0:14`** 等数字 · **禁** 英文 `stitched` / `segment` UI |
| 重绘 | 🟡 |
| JP V3.9 锚句 | 「タブレットの中、集合写真はパノラマ（全景）のつなぎ撮影……レンズが左から右へ掃き、十数秒の画面を一枚にした。撮影は昼休み後の一点十二分ごろから、約十四秒。一瞬の写真じゃない。」 |

> 内容层描述（非 Style 词块）。Style B 见下方 Global STYLE。


## §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **DA3** |
| 所属 | Vol1 · A005 · SC-05 |
| 原文范围 | V3.9 JP · 见 Shot Map JP 锚点句 |
| 镜头功能 | **L+C** |
| 强制级 | **P0** |
| 景别 | **MCU** |
| 机位 | 平板POV·框中框 |
| 视觉中心 | FC-2分段曝光三帧 |
| 第二信息 | 水野侧让帧高亮 |
| 服道化 | 平板·时间戳 |
| JP 锚点句 | タブレットの中、集合写真はパノラマ（全景）のつなぎ撮影……レンズが左から右へ掃き、十数秒の画面を一枚にした。撮影は昼休み後の一点十二分ごろから、約十四秒。一瞬の写真じゃない。 |

## Global STYLE

```
Modern Japanese bridge-book illustration ages 10-12,
clear light-manga ink line warm brown outline #2A1810 NOT pure black,
soft painterly coloring restrained watercolor paper texture NOT flat vector,
6-7 head pre-teen proportions NOT chibi NOT shonen hero,
warm golden April morning cinematic side light Nagoya public elementary school,
gentle fair-play mystery observation club NOT detective agency,
uwabaki indoor shoes on floor, IP 学堂奇事録 Campus Ripple V2
```

## Global NEGATIVE

```
chibi SD, horror mob trial, supernatural glow, Chinese classroom layout,
detective magnifying glass pose, 3D render, fluorescent neon,
English or Chinese text rendered in image, watermark,
school uniform blazer sailor suit, sneakers on classroom floor,
generic anime child, villain spotlight
```

## 合成 Prompt

```
[STYLE] MCU 平板POV·框中框,
VISUAL CENTER: FC-2分段曝光三帧,
SECOND READ: 水野侧让帧高亮,
characters and props per 14_v2 L0 and Vol1画风Sheet,
fair-play clue readable without text arrows, Nagoya elementary April uwabaki,
scene context: 十四秒分の写真が、一枚に stitched されている。...
[NEGATIVE]
```
