# A001 · TAIL · Prompt · V3.6

> **Status**: G1DRAFT_PRODUCTION · 试读 PDF 用  
> **Shot Map**: [`03_分镜头_插页地图_V3.9_JP.md`](../03_分镜头_插页地图_V3.6_JP.md)  
> **正文锚**: [`../01_正文/案01_全班都听见了他的声音_HybridVoice_V3.9_日本語.txt`](../01_正文/案01_全班都听见了他的声音_HybridVoice_V3.9_日本語.txt)

## 画面内容提示词 · V3.9

| 字段 | 内容 |
|------|------|
| 画面瞬间 | 安静下来的教室；器材车旁展示膜一角掀起；黑板上「ごめんなさい」测试字半句；珣写路线笔记。 |
| G-CAST MAX | 4 |
| 画中文字 | **なし** · 黑板上若有字：仅 **`ごめんなさい`** 测试（半句可）· **禁** 英文 checklist / Name: Shiro / STOCKY |
| 重绘 | 🔴 |
| JP V3.9 锚句 | 「機材ワゴンのリストが側門に貼られる。次は：5年2組黒板・展示膜テスト記録。」 |

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
| 镜头编号 | **TAIL** |
| 所属 | Vol1 · A001 · SC-08–09 |
| 原文范围 | V3.9 JP · 见 Shot Map JP 锚点句 |
| 镜头功能 | **H+P** |
| 强制级 | **P0** |
| 景别 | **¼–半** |
| 机位 | 分格·侧门清单 |
| 视觉中心 | 器材車下一站·黒板 |
| 第二信息 | FC-4完整句 vs 半句 |
| 服道化 | 清单·膜卷·A002种子 |
| JP 锚点句 | 機材ワゴンのリストが側門に貼られる。次は：5年2組黒板・展示膜テスト記録。 |

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
[STYLE] ¼–半 分格·侧门清单,
VISUAL CENTER: 器材車下一站·黒板,
SECOND READ: FC-4完整句 vs 半句,
characters and props per 14_v2 L0 and Vol1画风Sheet,
fair-play clue readable without text arrows, Nagoya elementary April uwabaki,
scene context: 次は黒板。展示膜のテストが、まだ終わっていない。...
[NEGATIVE]
```
