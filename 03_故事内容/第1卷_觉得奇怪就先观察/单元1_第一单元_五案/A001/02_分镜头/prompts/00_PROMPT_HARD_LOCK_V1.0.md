# A001 · Prompt 硬锁 · 出图前必读 · V1.0

> **引用**：各 `prompts/DAx.md` 合成 Prompt 前 **必须** 包含本文件词块  
> **门禁**：`g_cast_prompt_gate.py` · `illustration_post_gate.py` · `workflow_preflight --phase generate-image`

---

## 垫图（仅画风 · 禁十人中文顶栏泄漏）

| 用 | 不用 |
|----|------|
| `CHAR_lineup_L0_StyleB_马克笔_V0.2.png` | `CHAR_lineup_L0.png` · 十人排面带「学堂趣事录」顶栏 |

---

## 发色 · 脸库（slot LOCK）

```
Riku Jun 陸珣: soft messy BLACK hair #1A1818, navy zip #3A5080 yellow inner collar, compass pendant, gray backpack — NO silver white gray hair
Ito Akira 伊藤光: spiky WARM BROWN hair #6A4830, white T-shirt orange-red utility vest — NO blonde silver white hair
Matsumoto Shiro 松本志郎: short STOCKY, round glasses, green plaid olive utility vest
Kato Keimi 加藤慧美: silver glasses, low ponytail, yellow cardigan
```

---

## 文化 · G-CAST 硬禁

```
NO Chinese text in scene NO 学堂趣事录 on wall NO simplified Chinese
NO character name plates NO desk labels NO 葛西泉藏 NO Kasai Senzo NO spec cards
NO parents NO adults in classroom
MAX_BODIES per shot map — count visible L0 faces
all children white uwabaki indoor shoes NO sneakers NO outdoor shoes
```

---

## Style B（唯一）

```
STYLE_B_LOCK: alcohol marker pen flat color, warm brown outline #2A1810, NOT watercolor wash
NEGATIVE_STYLE_B: watercolor, Chinese text, English text, name labels, Kasai, character spec cards, chibi, seifuku, sneakers
```

---

最后更新：2026-06-10
