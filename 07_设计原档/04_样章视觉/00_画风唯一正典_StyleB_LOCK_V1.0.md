# Vol1 · 画风 · 唯一正典 · Style B LOCK · V1.0

> **Status**: **SINGLE TRUTH · 2026-06-10**  
> **废止**：REF04 水彩主锚 · A轨 b169491b · USERSTYLE · G1「restrained watercolor」· Vol1画风Sheet 水彩句（作历史，不再用于出图）

---

## 1. 为什么一直跑偏（根因）

| 错误来源 | 里面写了什么 | 后果 |
|----------|--------------|------|
| `用户确认风格参照/README.md` | **REF04 纸纹水彩 = PRIMARY** | GenerateImage 垫水彩 → 出 watercolor |
| `A001_G1_prompts.md` | `restrained watercolor` × 全文 | 与 Style B 冲突 |
| `prompts_*_USERSTYLE.md` | `painterly watercolor wash` | v1.2 成图偏水彩 |
| `人类插画师_开工包` | **A轨 b169491b 电影水彩** | Agent 读开工包回水彩 |
| `Vol1_正篇画风Sheet_IP_LOCK` | **克制水彩肌理** | Gate 文档仍指水彩 |
| `academy-illustration-pipeline` SKILL | 画风=克制水彩 | Cursor Skill 默认水彩 |
| `CHAR_lineup_A001` §0 | Tier-0 Style B **和** Tier-0 REF04 水彩 **并列** | 双重正典 |

**结论**：不是模型「纠正不过来」，是 **引导词文件互相打架**。在 DEMO PASS 之前 **禁止** 再批量换图。

---

## 2. 唯一 LOCK（全项目只认这一张 + 这一段话）

### 2.0 画风命名对照（避免「马克笔 vs 动画线稿」误判）

| 说法 | 关系 |
|------|------|
| **Style B LOCK**（本文件 · 仓库技术名） | **正典** |
| **桥梁书动画线稿 + 数字厚涂**（产品/画师沟通） | **同一目标** — 干净线 + 暖色平涂，对标桥梁书品类 |
| **马克笔平涂**（Copic-like · IP「马克笔更重」） | **同一 LOCK 词块** — 防模型漂向 watercolor |
| **废止** | G1DRAFT 水彩混用 · REF04 主锚 · `restrained watercolor` |

详表：[`00_A001-A005_插画师分镜补充规范_V1.0.md` §0.1](./00_A001-A005_插画师分镜补充规范_V1.0.md)

### 2.1 锁定垫图（左图 · 永远附在发包旁）

| 项 | 路径 |
|----|------|
| **画风 LOCK** | [`CHAR_lineup_L0_StyleB_马克笔_V0.2.png`](./CHAR_lineup_L0_StyleB_马克笔_V0.2.png) |
| **造型 LOCK** | [`CHAR_lineup_L0_IP确认方向_20260610.png`](./CHAR_lineup_L0_IP确认方向_20260610.png) |
| **brief** | [`CHAR_lineup_L0_StyleB_日文举牌_V0.2_brief.md`](./CHAR_lineup_L0_StyleB_日文举牌_V0.2_brief.md) |

### 2.2 唯一 STYLE 词块（复制即用 · 禁改 watercolor）

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

### 2.3 唯一 NEGATIVE 词块

```
NEGATIVE_STYLE_B:
watercolor painting, watercolor wash, painterly digital-anime, wet paper texture,
heavy grain, REF04 style, b169491b mood, cel-shade, chibi, seifuku, sneakers,
English text, Chinese text, adults parents Kasai in classroom, character spec cards
```

---

## 3. 出图流程（DEMO 门）

```
1. 只读本文件 + StyleB brief + 分镜文字稿
2. 只跑 STYLE_DEMO（DA2）→ 生成 DEMO
3. 自动拼对照图：左=LOCK 右=DEMO（见 tools/compose_style_demo_compare.py）
4. IP 签字 DEMO PASS
5. 才允许换 DA1/3/4/5/TAIL/DB1
```

**DEMO 路径**：[`A001/03_插画/STYLE_DEMO/`](../../03_故事内容/第1卷_觉得奇怪就先观察/单元1_第一单元_五案/A001/03_插画/STYLE_DEMO/)

---

## 4. 废止清单（已移入 `_archive_废止画风引导/`）

见该目录 `00_废止说明.md` · **勿再引用**

---

最后更新：2026-06-10
