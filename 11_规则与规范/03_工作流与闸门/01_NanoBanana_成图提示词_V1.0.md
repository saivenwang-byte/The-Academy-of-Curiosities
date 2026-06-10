# Nano Banana 成图提示词 · Vol1 案①薄样张 · V1.0

> **Status**: **SUPERSEDED** · 请使用 **[`01_NanoBanana_成图提示词_V1.1.md`](./01_NanoBanana_成图提示词_V1.1.md)**（10–12 岁 · 光=あきら）

> **用途**：8 角色 master ref（L0 槽①–⑧）+ 案① 4 场景 · 直送 Nano Banana / Stable Diffusion  
> **正典**：[`CHAR_lineup_L0_专家共识_画师brief.md`](../../../07_设计原档/04_样章视觉/CHAR_lineup_L0_专家共识_画师brief.md)  
> **禁止**：侦探/探案/犯人 · 制服 · 恐怖 · 泉蔹/全藏错字 · 理紗 Vol1 C 位  
> **最后更新**：2026-06-05

---

## 全局 Style Block（所有 prompt 前缀）

```
[Style] Japanese children's mystery bridge book, warm transparent watercolor,
clear ink line, age 8-11 readable, Nagoya spring, NOT chibi, NOT mature anime,
NOT 3D render, NOT horror, indoor shoes uwabaki when in school
[IP] 学堂奇事録 · 学校おもしろ観察クラブ · observation not detective
```

---

## A. 角色 Master Ref（8 人 · 白底半身 · 私服春装）

> 输出：`薄样张_试读/assets/CHAR_01–08_master.png`（画师/Nano 成图后落盘）

### CHAR-01 · 陸瑆（4年2組 · 132cm）

**正 prompt**
```
[Style block] character reference sheet, single girl, age 9-10, 132cm shortest,
round gentle face, short hair or low ponytail with small flower clip,
oatmeal cardigan over light skirt or pants, holding A5 kraft paper diary and colored pencils,
peach accent color, soft smile, white background, full body front view, height note 132cm
```

**负 prompt**：`detective coat, magnifying glass, boy clothes, mature face, school uniform, けい mislabel`

---

### CHAR-02 · 陸珣（5年2組 · 142cm）

**正 prompt**
```
[Style block] character reference, boy age 10-11, 142cm, slightly hunched posture,
oval face single eyelids dark brown eyes messy black hair,
navy jacket yellow inner layer utility shorts, route observation notebook,
compass pendant on bag strap, blue+yellow accent, quiet focused gaze NOT handsome shonen hero,
white background full body front, 142cm label
```

**负 prompt**：`detective pose, case notebook, magnifying glass hero, cool anime boy, uniform`

---

### CHAR-03 · 松本志郎（5年3組 · 145cm）

**正 prompt**
```
[Style block] character reference, boy age 10-11, 145cm stocky broad shoulders NOT obese,
spiky hair round glasses, red T-shirt work pants or shorts, green worn sports bag,
verification cards in pocket, energetic squat-ready stance, green+red accent,
white background full body, 145cm label
```

**负 prompt**：`fat caricature, violence props, uniform, detective badge`

---

### CHAR-04 · 伊藤光（5年2組 · 146cm）

**正 prompt**
```
[Style block] character reference, boy age 10-11, 146cm balanced build,
round eyes warm smile short soft black hair, gray hoodie bright ORANGE scarf (P0 identity),
shorts, light gray backpack with community badge keychain NOT travel souvenirs,
whistle on strap, orange accent, white background full body, 146cm label
```

**负 prompt**：`sports jersey number detective, uniform, cold expression`

---

### CHAR-05 · 山本理紗（5年4組 · 147cm · Vol11+ 参照用）

**正 prompt**
```
[Style block] character reference, girl age 10-11, 147cm slender, calm straight hair,
morandi long skirt or cardigan, sketchbook and bookmark ruler, navy morandi accent,
elementary school face NOT teen model, white background full body, 147cm label,
note: reference only NOT Vol1 poster center
```

**负 prompt**：`Vol1 main character spotlight, mature idol face, uniform`

---

### CHAR-06 · 中谷琦（6年1組 · 152cm · 远景参照）

**正 prompt**
```
[Style block] character reference, boy age 11-12, 152cm lean narrow shoulders,
fluffy hair, olive field jacket casual clothes NOT middle school uniform,
camera crossbody brown leather strap, B6 black record book, distant observer mood,
olive accent, white background full body, 152cm label
```

**负 prompt**：`round chubby face, headphones hype boy, uniform tie`

---

### CHAR-07 · 加藤慧美（5年1組 · 155cm）

**正 prompt**
```
[Style block] character reference, girl age 10-11, 155cm girl proportions NOT high school,
silver round glasses low ponytail neat, yellow cardigan light skirt or pants,
interview notebook brown shoulder bag, yellow accent, thoughtful push-glasses gesture,
white background full body, 155cm label
```

**负 prompt**：`165cm senpai, blazer uniform, thesis expression`

---

### CHAR-08 · 葛西泉藏（~70岁 · 158cm）

**正 prompt**
```
[Style block] character reference, elderly man ~70, 158cm spirited NOT severely hunched,
gray beard deep eye sockets patterned cap work apron samue style,
old map and worn notebook, community elder warm eyes, white background full body,
name 泉藏 NOT 泉蔹, 158cm label
```

**负 prompt**：`ghost, horror, 全藏 wrong kanji, evil wizard`

---

## B. 案① 场景（4 张 · 薄样张必用）

### SC-V-S01 · 侧廊海报翘边

```
[Style block] half-page interior illustration, elementary school side corridor Nagoya spring afternoon,
students in uwabaki, hand-drawn club poster on board Japanese text 学校おもしろ観察クラブ
and three simple doodle eyes, LEFT edge curling upward (windward clue),
AC vent grille above poster subtle, four 5th graders ~140-155cm band:
bright boy orange scarf (Hikaru Ito), girl notebook glasses (Keimi), squatting boy red shirt (Shiro),
transfer boy quiet with sketchbook behind (Riku Shun POV entry)
```

**负 prompt**：`horror night, Chinese poster, Yamamoto Risa, chibi, photo realistic`

**成图**：`样章包/插图/V-S01_侧廊海报.png`

---

### SC-V-S01-TAIL · 壁报草稿空栏

```
[Style block] quarter-page illustration, bulletin draft on clipboard pencil grid,
three filled columns Japanese handwriting, fourth column intentionally EMPTY with small ? in margin,
title about curled poster club wall newspaper, warm corridor light uwabaki at bottom edge,
readable empty box, no character close-up
```

**负 prompt**：`horror, Chinese plaques, named character face, submission slip case2`

**成图**：`样章包/插图/V-S01-TAIL_壁报草稿空栏.png`

---

### SC-V-S02 · 陸瑆日记页

```
[Style block] diary page illustration, horizontal ruled notebook pencil drawing,
simple poster with wind arrow from top curling corner, minimal decoration Yoshitake-style,
one gentle question at bottom in Japanese mood, peach accent margin, age 9-10 handwriting feel,
陸瑆 4年2組 NOT club member, warm desk lamp evening
```

**负 prompt**：`filled scrapbook, horror, named Risa, lesson summary text`

**成图**：`样章包/插图/V-S02_陸瑆日记页.png`

---

### SC-V-S03 · 风侧示意图（案①机制图）

```
[Style block] educational diagram for children, simple top-down corridor cross-section,
poster on wall with one edge lifting, arrows showing airflow from AC vent above,
left/right curl variants small inset, warm colors clear labels optional Japanese,
NOT textbook dense, bridge book clarity age 8-10
```

**负 prompt**：`horror wind ghost, complex physics equations, dark palette`

**成图**：`样章包/插图/V-S03_风侧示意图.png`

---

## C. 成图验收（案①薄样张）

- [ ] 8 角色 cm / 年级 / 道具与 L0 brief 一致  
- [ ] 葛西 **泉藏** · 瑆 **ひかる** · 珣 **しゅん**  
- [ ] 场景无恐怖 · 海报日文 **学校おもしろ観察クラブ**  
- [ ] V-S01 珣在侧后 · 理紗零出镜  
- [ ] 薄样张 PDF 可嵌入 4 场景（占位可接受 v0.9）

---

## D. 参考路径

| 资产 | 路径 |
|------|------|
| L0 发包图 | `07_设计原档/04_样章视觉/CHAR_lineup_L0_专家共识_画师发包.png` |
| 样章 SC 详表 | `样章包/06_插图brief_案01.md` |
| Cursor 401 替代 | `07_设计原档/04_样章视觉/Cursor生图401_说明与替代方案.md` |

---

最后更新：2026-06-05
