# L0 探索 Prompt · v1

> **Status**: EXPLORATION · AI_DRAFT · 2026-06-04  
> **用途**: Cursor / 外部生图 **草图探索** · **非** L0 定稿 · **非** 画师交付依据  
> **正典**: [`CHAR_lineup_L0_专家共识_画师brief.md`](./CHAR_lineup_L0_专家共识_画师brief.md) · [`05_视觉设定/`](../../05_视觉设定/)  
> **禁**: 任何知名漫画家/动画/插画师/既有 IP 名称 · 侦探 cosplay · Q 版（正篇）

---

## 输出命名

| SC ID | 探索输出文件名 | 定稿目标（人工） |
|-------|----------------|------------------|
| SC-L0-SHEET-001 | `CHAR_lineup_L0_设定Sheet_AI_v1.png` | **7+3+三层面板** · 2026-06-05 |
| SC-L0-003 | `CHAR_lineup_L0_AI探索_v0.3.png` | 用户倾向对齐 · 身高排面 |
| SC-L0-001 | `CHAR_lineup_L0_AI探索_v0.png` | 初版探索 |
| SC-L0-DEMO-002 | `CHAR_lineup_L0_Demo窗邊_AI探索_v0.png` | Vol1 Demo 人工精修 |

---

## SC-L0-001 · 十人身高排面（全幅）

### 中文摘要

横版 3840×2160 · 白底 · Style A 温暖透明水彩 + 暖棕铅笔线（非纯黑）· 10 名角色左→右按身高 · 右侧 100–180 cm 黑色刻度尺 · 顶木牌「学堂趣事录 / 觉得奇怪，就先观察」· 底栏「学校おもしろ観察クラブ · L0 · Nagoya · spring」· 每人脚边黑底白字双行举牌（假名+中文）· 极淡名古屋樱与小学远景 ≤15% · 四月上午侧光 · 零恐怖 · 零侦探道具。

### EN Prompt（主）

```
Horizontal character lineup reference sheet, 3840x2160, pure white background. Warm transparent watercolor children's book illustration with soft warm-brown pencil outlines (not pure black), low-to-medium saturation, gentle April morning side-light from upper left. Japanese Nagoya elementary school slice-of-life mood, calm observational atmosphere, NOT detective, NOT horror, NOT anime action poster, NOT chibi.

Ten characters standing in a row left to right, feet aligned on one ground line, strictly ordered by height (shortest left). Right edge: vertical height scale 100cm to 180cm with black tick marks every 10cm.

Top: small wooden sign "学堂趣事录" subtitle "觉得奇怪，就先观察". Bottom text: "学校おもしろ観察クラブ · L0 · Nagoya · spring". Extremely faint cherry blossom petals and distant grey-green RC school building at 15% opacity, must not cover faces.

Slot 1 (132cm, shortest girl): round child face, peach flower hair clip, oat-beige cardigan, light grey skirt, holding small diary and colored pencils, indoor school slippers.

Slot 2 (142cm, boy protagonist): slightly slouched thin boy, black messy hair, navy blue jacket with yellow inner collar, khaki cargo shorts, route observation notebook, small compass pendant, backpack.

Slot 3 (145cm, stocky boy): spiky hair, round glasses, red T-shirt, dark green cargo pants, green crossbody bag, verification cards, broad shoulders not obese.

Slot 4 (146cm, energetic boy): round eyes smiling, grey hoodie, bright ORANGE scarf around neck (required), blue shorts, small whistle, community keychain on bag.

Slot 5 (147cm, calm girl): straight dark hair, muted purple-grey long dress or cardigan, sketchbook, bookmark ruler, still elementary school face not teen model.

Slot 6 (152cm, lean older boy): messy black hair, slim narrow shoulders NOT chubby, olive green field jacket, dark pants, small camera crossbody, elementary NOT middle school uniform.

Slot 7 (155cm, girl): silver-frame glasses, yellow cardigan, navy knee-length skirt or pants, ponytail, interview notebook, brown shoulder bag.

Slot 8 (158cm, elderly man): grey beard, gentle wrinkles, patterned cloth hat, work apron over brown clothes, rolled old map and notebook, slightly hunched.

Slot 9 (163cm, adult woman mother): clear adult proportions, low bun, beige apron over light dress, lunch box or flower basket, NOT child height.

Slot 10 (175cm, tallest adult man): adult male designer casual shirt, khaki pants, pen or coffee cup, tallest in lineup.

Each character: small black label plaque at feet with two lines Japanese kana name above Chinese name. Realistic Japanese elementary proportions 5.5-7.5 heads tall. Soft watercolor paper texture, visible gentle brush edges, no neon colors, no 3D render, no vector flat fill.
```

### Negative Prompt

```
detective hat, trench coat, magnifying glass pose, crime scene, horror, blood, dark gothic, chibi 2-head body, middle school sailor uniform, neon colors, pure black outlines, 3D CGI, photo collage, generic anime action hero, oversized sparkly eyes, famous character likeness, text gibberish errors acceptable but avoid wrong character count, extra people, crowds
```

### P0 自检（成图后 · academy-visual-auditor）

- [ ] 10 人 · 槽位左→右 · 身高递增（瑆最矮 · 直人最高）
- [ ] 右侧 100–180 cm 身高线可读
- [ ] 光 **橙围巾** · 珣 **路线本**（非探案）· 葛西 **泉藏** 老人态 · 父母 **成人**
- [ ] 中谷 **精瘦** · 理紗 **小学生脸**
- [ ] 无侦探/恐怖/中学制服
- [ ] 画风：温暖水彩 + 暖棕线 · 非霓虹/3D
- [ ] 顶/底栏文案正确或接近（AI 日文常错 → 探索可 REVISE）

---

## SC-L0-DEMO-002 · Vol1 案① 窗边四人 Demo

### 中文摘要

Vol1 探索 Demo：5年2組教室 · 四月下午 15:00–16:00 暖金黄斜光 · 四人（陆珣、伊藤光、加藤慧美、松本志郎）窗边互动 · **仅一把椅子椅背** 贴铝窗框有 **微结露/细水珠** · 窗框略冷 · 室内暖 · 私服+上履き · 温暖水彩 · 平视小学生眼高 · 非侦探。

### EN Prompt（主）

```
Interior Japanese elementary school classroom, April afternoon in Nagoya, warm golden sunlight slanting through aluminum window frames, soft watercolor illustration with warm-brown pencil lines, low saturation, calm observational mood.

Four fifth-grade children in casual spring clothes and white indoor slippers (uwabaki), NOT outdoor shoes, NOT detective outfits:

Boy A (thin, slightly slouched, navy jacket yellow inner collar, route notebook): standing rear row looking toward window.

Boy B (energetic, orange scarf, grey hoodie): sitting on chair by window, chair BACKREST touching aluminum window frame, thin condensation droplets on chair back only, NOT puddle on seat.

Girl C (silver glasses, yellow cardigan, interview notebook): standing nearby listening.

Boy D (spiky hair, round glasses, red shirt, green bag): leaning forward checking something with verification cards.

Deep green chalkboard, wooden desks with metal legs, pale green PVC floor, fluorescent lights. One chair back shows fine dew condensation from cold window contact; neighboring chairs dry. April cherry blossom glimpse outside window with soft air perspective (distant bluish-grey). Eye-level view as elementary student height. Warm, quiet, scientific observation scene, zero horror, zero anime action.
```

### Negative Prompt

```
detective, magnifying glass, wet floor flood, all chairs wet, pouring water, horror, night scene, autumn leaves, summer intense sun, middle school uniforms, outdoor sneakers on desk, chibi, neon, 3D render
```

### P0 自检

- [ ] 仅 **椅背** 结露 · 邻椅干
- [ ] 上履き · 私服
- [ ] 4月名古屋下午暖光
- [ ] 光 **橙围巾** · 珣藏青+黄 · 四人脸可辨
- [ ] 非侦探场景

---

## 使用说明

1. **探索**：Cursor `GenerateImage` 或外部 API 粘贴 EN Prompt + Negative  
2. **审图**：用上方 P0 清单 · 正式格式见 `academy-visual-auditor`  
3. **定稿**：人工画师按 `05_视觉设定` + L0 文字说明书 · 回传 PSD+PNG  
4. AI 成图 **不得** 直接标为 ILLUSTRATOR-READY 或进 GATE PASS

---

## 附录 A · 2026-06-04 探索成图审计

### SC-L0-001 → `CHAR_lineup_L0_AI探索_v0.png`

**Verdict**: **REVISE**（探索参考 ✓ · 定稿 ✗）

| P0 项 | 结果 | 说明 |
|-------|------|------|
| 10 人槽位 | ✅ | 10 人 · 左→右递增 |
| 身高 cm 正典 | ⚠️ | 刻度有，但标注 132–175 与槽位 cm **部分偏移**（如 ⑧⑨⑩ 165/168/175 非 158/163/175 严格对应） |
| 身高线 100–180 | ✅ | 右侧刻度可见 |
| 举牌假名+中文 | ❌ | 仅数字+cm，**无**黑底双行假名/汉字 |
| 光橙围巾 | ✅ | 槽④可见 |
| 珣路线本 | ⚠️ | 有本，标签非正典「路线观察本」 |
| 葛西泉藏老人 | ✅ | 花帽+地图 |
| 父母成人 | ✅ | ⑨⑩ 明显成人 |
| 中谷精瘦 | ⚠️ | ⑥ 相机少年，体型接近但 **cm/槽位** 需核对 |
| 无侦探 | ✅ | 无风衣/放大镜 |
| 画风水彩暖棕 | ✅ | 气质接近 Style A |
| 顶/底栏 | ⚠️ | 顶栏中文有 · 底栏日文有 · 副标/底栏 **不完整** |

**定稿结论**: **REJECT** — 不可替代 `CHAR_lineup_L0_定稿_v1` · 可作 **站位/气质** 草图参考。

### SC-L0-DEMO-002 → `CHAR_lineup_L0_Demo窗邊_AI探索_v0.png`

**Verdict**: **REVISE**（Vol1 Demo 氛围 ✓ · 机制图 ✗）

| P0 项 | 结果 | 说明 |
|-------|------|------|
| 四人可辨 | ✅ | 珣/光/慧美/志郎 主色与道具大体对 |
| 光橙围巾 | ✅ | 居中坐者 |
| 四月下午暖光 | ✅ | 斜照进窗 |
| 教室日本感 | ✅ | 黑板日文 · 4月17日 · 木桌 |
| 仅椅背结露 | ❌ | 黑板写「水模様」主题 ✓ · **椅背贴铝窗框+微结露** 不清晰 |
| 上履き | ⚠️ | 未明确白室内鞋 |
| 非侦探 | ✅ | |

**定稿结论**: **REJECT** — 适合 **氛围/四人互动** 参考 · 结露机制须人工重绘或迭代 prompt。

---

最后更新：2026-06-04
