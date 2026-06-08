---
name: academy-xing-diary-b-track
version: 0.1.0
description: 《学堂趣事录》陸瑆笔记 B 轨插图生产。触发：陆瑆笔记、B轨、scrapbook、贴纸、观察日记、SUM页。暖黄手账风 #F5EDE0，流程借鉴 ian-xiaohei 认知锚点/shot list，视觉完全项目自有；禁小黑、禁 A 轨、禁纯白默认。
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - GenerateImage
---

# 学堂趣事录 · 陸瑆笔记 B 轨 · Illustration Skill

> **NOT** ian-xiaohei clone · **partial adopt 流程 only**（见 doc74）  
> **A 轨零接触** · 仅 `03_笔记/` · `.diary-page` · 卷末 spread · SUM 机制页

## 何时触发

- 用户说：**陆瑆笔记** · **B轨** · **scrapbook** · **贴纸** · **观察日记** · **SUM页**
- 从 `陆瑆笔记_VolN.md` 或案末笔记正文出 **1 机制 1 图**
- Vol1 配额：全卷 **1 篇总笔记** + 样章级单页 · **禁** shot list 扩成 4–8 全页

## 启动必读

1. [`01_角色设定/06陆瑆.txt`](../../../01_角色设定/06陆瑆.txt)
2. [`05_视觉设定/00_插画师视觉创作说明书_V1.0.md`](../../../05_视觉设定/00_插画师视觉创作说明书_V1.0.md) §1.2B · §10
3. [`05_视觉设定/02_插画创作规范手册_V1.0.md`](../../../05_视觉设定/02_插画创作规范手册_V1.0.md) §6.2
4. [`CHAR_lineup_L0_专家共识_画师brief.md`](../../../07_设计原档/04_样章视觉/CHAR_lineup_L0_专家共识_画师brief.md) **§7 瑆 SD 二头身**（贴纸轨 · 与 A 轨 L0 分离）
5. [`G-BODY_插画一致性门禁_V0.1.md`](../../../07_设计原档/04_样章视觉/G-BODY_插画一致性门禁_V0.1.md) · KF-LOCK-J
6. [`74_陆瑆笔记_ian-xiaohei…`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/74_陆瑆笔记_ian-xiaohei-illustrations_可行性评估_V0.1.md)

---

## Visual Lock（B 轨 SSOT）

| 维度 | LOCK |
|------|------|
| **底纸** | 微黄横线/方格 **`#F5EDE0`** · 手账拼贴 · **非纯白** |
| **线条/色** | 暖棕 `#2A1810` · 粉/桃/橙点缀 · 水彩/彩铅 · 低–中饱和 |
| **比例** | **二头身 Q 版陸瑆** · 更圆更简 · **仅此轨** · 与 A 轨 6–7 头分离 |
| **元素** | 贴纸 · 胶带 · 便签 · 拍立得小插图 · 修正痕 · 拟人小物（圆圆 · 无恐怖） |
| **角色** | **陸瑆本人** · A5 牛皮纸线圈本 · 彩铅 · 银色自动铅笔 · 花夹 |
| **瑆 SD** | 单独贴纸轨 · 见 L0 brief §7 · **不得** 与 A 轨 L0 正页 Q 版混用 |

**Negative（prompt 必含）**：

```
NOT xiaohei, NOT black blob character, NOT pure white background default,
NOT 16:9 editorial layout forced, NOT A-track cinematic watercolor,
NOT seifuku, NOT chibi in main SC frames, NOT simplified Chinese big titles,
NOT 5年2组, NOT 陆瑆/陆珣 name mix, NOT detective pose
```

---

## 工作流（借 ian-xiaohei 结构 · 换 IP 视觉）

```
1. READ    笔记正文 / Case 机制段（≤8 句）
2. ANCHOR  提炼 1 个认知锚点（观察 · 状态变化 · 简单因果）
3. SHOT    输出 shot list：1 concept → 1 image（Vol1 严控张数）
4. TYPE    选结构类型（见下表）
5. PROMPT  填 B 轨 template → GenerateImage
6. QA      checklist → visual-auditor 可选
```

### 结构类型（1 图 1 机制）

| 类型 | 用途 | 例 |
|------|------|-----|
| **map route** | 路径/动线/风的方向 | 案① 风→海报角翘箭头 |
| **before/after** | 状态对比 | 贴前/贴后 · 干/湿 |
| **simple experiment diagram** | 机制简图 | 箭头+简笔物件 · 无长文 |
| **sticker collage** | 贴纸页/角标 | 瑆 SD + 拟人小物 + 胶带 |

---

## 红线（P0）

| ID | 规则 |
|----|------|
| **NO 小黑 IP** | 禁 helloianneo「小黑」任何变体 |
| **NO 白底默认** | 底纸必须 `#F5EDE0` 横线本气质 |
| **NO A 轨接触** | 禁用于 SC/DA/PRODUCT/L0/封面 |
| **KF-LOCK-J** | 画内文字：日文正典或不可读 · 禁简体乱入 · CN 阅读层≠成图层 |
| **名称 LOCK** | **陸瑆** / **陸珣** / **4年2組**（瑆）· 禁 tag 混名 · SSOT [`00_十人名称_LOCK`](../../../01_角色设定/00_十人名称_LOCK_2026-06-07.md) |
| **配额** | Vol1 总笔记 1 页 · 不自动扩页 |

---

## Prompt 骨架

见 [`references/b-track-prompt-template.md`](./references/b-track-prompt-template.md)

```text
[B-TRACK · 陸瑆日记 · Vol1 案__]
Paper: #F5EDE0 lined notebook, warm brown ink #2A1810, peach/pink accents, watercolor/colored pencil
Subject: ONE mechanism only — [anchor]
陸瑆: 2-head SD sticker style, flower clip, coil notebook edge, colored pencils — SEPARATE from A-track
Structure: [map route | before/after | diagram | sticker collage]
FORBIDDEN: xiaohei, pure white bg, simplified Chinese poster text, A-track style, wrong names
```

---

## QA Checklist（出图前）

- [ ] 底纸 `#F5EDE0` 横线本 · 非纯白编辑风
- [ ] **一机制一图** · 无大段正文塞入
- [ ] 陸瑆 **二头身 SD** · 非 A 轨脸库
- [ ] 无小黑 · 无 A 轨电影水彩
- [ ] KF-LOCK-J · 名称正典
- [ ] 未超 Vol1 笔记配额

---

## 输出

```markdown
## B-Track · [案ID] · [结构类型]

**认知锚点**: …
**Shot**: 1/1 · [文件名].png
**Prompt SSOT**: references/b-track-prompt-template.md 实例
**QA**: ☐ 待 visual-auditor
```

---

*V0.1 · doc74 partial adopt · 项目 B 轨专用*
