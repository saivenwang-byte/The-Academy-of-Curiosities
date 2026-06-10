# 用户确认风格参照 · 历史 mood 库 · 2026-06-09

> **⚠ SUPERSEDED for AI 出图 · 2026-06-10**  
> **GenerateImage / Cursor 出图唯一 SSOT** → [`00_画风唯一正典_StyleB_LOCK_V1.0.md`](../00_画风唯一正典_StyleB_LOCK_V1.0.md) · 垫图 `CHAR_lineup_L0_StyleB_马克笔_V0.2.png`  
> **本目录五图**：保留作 **氛围/版式 mood 参考** · **禁止** 再作 PRIMARY 画风垫图（尤其 REF04 水彩）

> **Status**: **USER LOCK（历史）** · 五图定锚 · 已被 Style B 正典取代  
> **链**：[`Vol1_正篇画风Sheet_IP_LOCK_V1.0.md`](../Vol1_正篇画风Sheet_IP_LOCK_V1.0.md) · [`13_插画风格规范_v2.md`](../../02_插画与场景/13_插画风格规范_v2.md)

---

## 0. 一句话合成

**正篇** = REF04（主）+ REF03（角色氛围）+ 2026-06-03 会议「温暖水彩」  
**机制/SUM** = REF01（信息图水彩）+ REF05（铅笔网格涂鸦）  
**氛围辅** = REF02（田野手账拼贴）· 仅尾钩/特展 · 非主帧默认

---

## 1. 五图索引

| ID | 文件 | 用途 | 权重 |
|----|------|------|:----:|
| **REF01** | `REF01_水彩教学信息图_机制页方向.png` | 机制页 · DB1 · 教学信息图版式 · 柔和粉彩面板 | 机制 |
| **REF02** | `REF02_田野手账拼贴_氛围辅参照.png` | 尾钩特展 · 手账拼贴 · 科学好奇符号 | 辅 |
| **REF03** | `REF03_陆珣走廊单人_角色氛围.png` | 陸珣单人 · 名古屋走廊 · 樱瓣四月光 · 沉思 mood | 角色 |
| **REF04** | `REF04_观察社四人组_正篇主参照.png` | **正篇主画风 PRIMARY** · 四人组 · 纸纹水彩 · 暖窗光 | **★** |
| **REF05** | `REF05_铅笔网格涂鸦_SUM页方向.png` | SUM/笔记插入 · 石墨铅笔 · 方格纸涂鸦 | SUM |

---

## 2. 正篇主画风（LOCK）

| 维度 | LOCK | REJECT |
|------|------|--------|
| **线** | 软棕/炭笔感 `#2A1810` · 手绘轻漫画轮廓 · 留白呼吸 | 纯黑硬墨线 · 赛璐璐硬边 · 矢量平涂 |
| **色** | 画家水彩晕染 · 纸纹/水痕 · 低饱和暖调 · 纸质感 | 数码平涂 · 荧光色 · 厚涂游戏感 · cel-shade |
| **光** | 四月暖斜光 · 窗雾 `ひんやり` vs 暖室 · 电影侧光 | 舞台顶光 · 夜景侦探 · 泛光无层次 |
| **人物** | 6–7 头身 · 10–11 岁体感 · P0-03 服道 LOCK | Q版 · 成熟 anime · 通用 anime child |
| **环境** | 名古屋公立小学 · **私服 + 上履き** · 铝窗走廊/教室 | 中式教室 · 制服/seifuku · 运动鞋室内 |
| **气质** | 观察社日常 · 公平本格 · 温和好奇 | 推理番张力脸 · 恐怖 mob · 3D render |

**合成句**（每条 prompt Global STYLE 必贴）：

> Painterly watercolor bridge-book illustration with soft brown charcoal pencil lines (#2A1810), visible paper grain, warm April window light, 6-7 head pre-teens in casual clothes and uwabaki — match REF04 group scene PRIMARY, REF03 character mood SECONDARY; NOT flat anime, NOT cel-shaded, NOT hard black ink.

---

## 3. 分轨映射

### 3.1 正篇深度锚点（DA1–DA6 · TAIL 主帧）

- **垫图顺序**：REF04 → REF03 →（同案 continuity 帧如 c06）
- **对齐**：[`Vol1_正篇画风Sheet_IP_LOCK_V1.0.md`](../Vol1_正篇画风Sheet_IP_LOCK_V1.0.md) 六测试帧
- **四人色码**（REF04）：蓝/红(橙)/绿/黄 — 与 P0-03 外装一致

### 3.2 机制页 / DB1

- **垫图**：REF01 为主 · REF04 人物比例为辅
- 柔和粉彩教学面板 · 水彩信息图 · 非教辅 PPT 风

### 3.3 SUM / 笔记插入（B 轨 · 瑆页）

- **垫图**：REF05 为主 · REF01 版式节奏为辅
- 石墨铅笔 · 方格纸 · 手账涂鸦 aesthetic · **非** 正篇主帧画风

### 3.4 氛围辅（尾钩特展 · 偶发）

- **垫图**：REF02 · 田野手账拼贴 · 大地色水彩
- **禁** 用作 DA1–DA6 默认画风（会稀释 REF04 主锚）

---

## 4. GenerateImage 引用规范

```
正篇 DA/TAIL: reference_image_paths = [REF04, REF03]
机制 DB1:      reference_image_paths = [REF01, REF04]
SUM 插入:      reference_image_paths = [REF05, REF01]
尾钩特展:      reference_image_paths = [REF02] (+ REF04 若含人物)
```

**命名**：`*_V3.6.3_USERSTYLE_G1draft.png` · 仍 **G1DRAFT** · 非 PRODUCT

---

## 5. 与旧锚关系

| 旧锚 | 新地位 |
|------|--------|
| `G1draft_c06` 广播帧 | 同案 continuity · 次于 REF04 |
| `CHAR_lineup_L0_*` | 服道/身高 LOCK · 风格以 REF04 为准 |
| V3.6.1 / V3.6.2 批次 | 对照保留 · 试读 PDF 优先 V3.6.3 |

---

*用户 2026-06-09 确认 · 归档于本目录*
