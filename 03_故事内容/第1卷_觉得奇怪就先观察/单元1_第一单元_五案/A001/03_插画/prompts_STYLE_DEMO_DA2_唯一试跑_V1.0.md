# A001 · STYLE DEMO · DA2 · 唯一试跑 · V1.0

> **在 IP 签 DEMO PASS 之前，禁止 GenerateImage 任何其他 A001 帧。**  
> **SSOT**：[`00_画风唯一正典_StyleB_LOCK_V1.0.md`](../../../../07_设计原档/04_样章视觉/00_画风唯一正典_StyleB_LOCK_V1.0.md)

---

## G-TEXT + G-CAST

| 出场 | **具名 4 only**：慧美 · 志郎 · 光 · 珣 |
| 匿名 | **≤2** · 5年2組同学 · **背影/虚化/无 L0 脸** · 禁 seifuku 水手服当主班 |
| 禁止具名 | 瑆 · 理纱 · 中谷 · 葛西 · 父母 · 水野 · 成人 |
| **MAX_BODIES** | **6** |
| 文字 | **なし** |

---

## 垫图（reference_image_paths · 顺序固定）

1. `07_设计原档/04_样章视觉/CHAR_lineup_L0_StyleB_马克笔_V0.2.png` **← 唯一画风 LOCK**

**禁止** 十人排面 `CHAR_lineup_L0_IP确认方向_*` 作场景垫图（会把 8–10 人搬进教室）· REF04 · REF01 · USERSTYLE

**造型**：仅用 prompt 内 slot 描述 + Style B 画风垫 · 成图后 **G-CAST 数人头 ≤6**

**导演审定**：[`00_G-CAST_导演审定表_A001_V1.0.md`](../02_分镜头/00_G-CAST_导演审定表_A001_V1.0.md) 签字前 **禁止出图**

---

## Prompt（全文 · 禁加水彩词）

```
STYLE_B_LOCK:
alcohol marker pen (Copic-like) flat color illustration,
clean warm brown ink outline #2A1810, light paper grain only,
NOT watercolor wash NOT painterly wash NOT wet-on-wet NOT muddy grain,
NOT cel-shaded anime NOT 3D, Nagoya combined classroom April window light,
white uwabaki on wooden floor, ages 10-12 bridge-book 6-7 head.

SCENE DA2 observation club blocks false blame:
Kato Keimi slot7 ~155cm yellow cardigan silver glasses low ponytail arms spread calm blocking classmates,
Matsumoto Shiro slot3 ~145cm stocky round glasses green plaid shirt olive green QUILTED utility vest crouching at grey broadcast cart checking log sample bag on green backpack SAME FACE AS LOCK slot3,
Ito Akira slot4 ~146cm white tee orange-red utility vest pale hand half raised NOT confessing,
Riku Shun slot2 ~142cm shortest navy zip hoodie yellow inner collar aside writing notes NOT center,
classmates gesturing background, ceiling speaker hint, fair-play mood.

MAX 2 anonymous classmates: back view or faceless blur ONLY, same age 5th grade casual clothes, NOT distinct faces NOT L0 lineup slots NOT seifuku sailor uniform as focus,

NEGATIVE: watercolor painting watercolor wash painterly REF04 b169491b cel-shade chibi seifuku sneakers,
English Chinese text adults parents camera crew eight crowd extra named children Risa Mizuho Ki Hikaru sister
```

---

## Output

| 文件 | 用途 |
|------|------|
| `STYLE_DEMO/A001_STYLE_DEMO_DA2_v1.0.png` | DEMO 成图 |
| `STYLE_DEMO/A001_STYLE_DEMO_DA2_对照_LOCK左_DEMO右_v1.0.png` | 交付用对照 |

---

最后更新：2026-06-10
