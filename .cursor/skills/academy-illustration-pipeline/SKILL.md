---
name: academy-illustration-pipeline
version: 1.0.0
description: |
  《学堂趣事录》Vol1+ 插图与分镜完整生产流水线。正文定稿后才出分镜；出图前强制过画风Sheet、角色L0、分镜头规划书、E06-S。
  用户提到分镜头、取景、构图、插画demo、画风、角色造型、scale、M文档、V1.0制作流程、出图前审核时触发。
  与 academy-visual-auditor 配合：本 skill = 流程与门禁；auditor = 单帧审图。
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - GenerateImage
---

# 学堂趣事录 · 插图分镜生产流水线 · Illustration Pipeline

## 何时触发

- 写/改 **分镜头与插页地图**、Shot Map、深度锚点包、demo PNG
- 用户说「出图」「demo」「画风不对」「人物造型」「取景」「构图」
- V2 新案插图 **任何** 正式绘制前
- **禁止**：正文未定 → 直接 GenerateImage demo 并标 PASS

---

## 0. 铁律（违反 = REJECT）

| # | 铁律 |
|---|------|
| 1 | **插图服务已定稿正文** — 分镜 `原文范围` 必须链 **JP V3.8 定稿段落**（CN 仅作对照）；**Phase 4 JP + 翻译部 M0 PASS 前禁止 Phase 5 定稿与 Phase 8/9 GenerateImage** |
| 2 | **角色造型 = V1.0 LOCK** — [`14_角色设计稿创作简报_v2.md`](../../../07_设计原档/03_角色视觉/14_角色设计稿创作简报_v2.md) + L0 排面 · **禁** 通用 anime child |
| 3 | **画风 = V1.0 正篇 Sheet** — [`Vol1_正篇画风Sheet_IP_LOCK_V1.0.md`](../../../07_设计原档/04_样章视觉/Vol1_正篇画风Sheet_IP_LOCK_V1.0.md) · 清晰轻漫画线稿 × 克制水彩 × **电影化空间光影** |
| 4 | **取景 = 分镜头规范 V1.1** — [`Vol1_分镜头电影化构图规范_V1.0.md`](../../../07_设计原档/02_插画与场景/Vol1_分镜头电影化构图规范_V1.0.md) · S/C/E/L/P/H + 景别/机位/六项构图 |
| 5 | **未过 E06-S → 不得 PRODUCT** · demo 仅 **G1 探索** 且须标 `G1DRAFT` |
| 6 | **角色言行** — 写分镜涉及对白/动作时加载 [`academy-character-scale`](../../skills/academy-character-scale/SKILL.md)（characters.yaml） |

---

## 1. 必读正典（出图前 checklist · 全部 Read）

| 优先级 | 文档 | 管什么 |
|:------:|------|--------|
| ★ | [`00_插画师视觉创作说明书_V1.0.md`](../../../05_视觉设定/00_插画师视觉创作说明书_V1.0.md) | IP 气质 · 三层视觉 · 线条/色/符号 |
| ★ | [`13_插画风格规范_v2.md`](../../../07_设计原档/02_插画与场景/13_插画风格规范_v2.md) | 6–7头身 · `#2A1810` · 四月光色 |
| ★ | [`Vol1_正篇画风Sheet_IP_LOCK_V1.0.md`](../../../07_设计原档/04_样章视觉/Vol1_正篇画风Sheet_IP_LOCK_V1.0.md) | Gate A 六测试帧尺度 |
| ★ | [`Vol1_分镜头电影化构图规范_V1.0.md`](../../../07_设计原档/02_插画与场景/Vol1_分镜头电影化构图规范_V1.0.md) | S/C/E/L/P/H · P0/P1/P2 · §4 景别机位 · §11 必填字段 |
| ★ | [`Vol1_插图深度标准_湿椅子抽象_V1.0.md`](../../../07_设计原档/02_插画与场景/Vol1_插图深度标准_湿椅子抽象_V1.0.md) | D1–D6 深度 · A+B 双轨 |
| ★ | [`Vol1_插图深度锚点_IP_LOCK_V1.0.md`](../../../00_项目总览/Vol1_插图深度锚点_IP_LOCK_V1.0.md) | A001=6精修锚点 · 每案6–8+1B-SUM |
| ★ | [`14_角色设计稿创作简报_v2.md`](../../../07_设计原档/03_角色视觉/14_角色设计稿创作简报_v2.md) | Vol1 四人+瑆 · AI prompt 前缀 |
| ★ | [`00_单案分镜头交付模板_V1.0.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/样章包/00_单案分镜头交付模板_V1.0.md) | Shot Map 表格字段 |
| ★ | [`Vol1_五案分镜头核定表_V1.0.md`](../../../00_项目总览/Vol1_五案分镜头核定表_V1.0.md) | 卷级 P0 节点预算 |
| V2 | [`10_五案字段级对照表_V0.2.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/10_五案字段级对照表_V0.2.md) | 机制/主帧矛盾 |
| V2 | [`A002-A005_V2_插图锚点一览_V0.2.md`](../../../05_视觉设定/A002-A005_V2_插图锚点一览_V0.2.md) | V2 主帧 · 废止 V1 物件 |
| 入口 | [`07_设计原档/00_视觉规范正典入口.md`](../../../07_设计原档/00_视觉规范正典入口.md) | 视觉索引 |

**academy-visual-auditor**：单帧 PASS/REVISE/REJECT · P0 清单（上履き、四月、机制可见）

---

## 2. 全链路 Phase（卷 → 案 → 场 → 镜头）

```
Phase 0  单元母纲 + Case Card（题名·机制·关系·science）
Phase 1  Scene Cards / 分场脚本（9–10场 · 节拍表）
Phase 2  CN Hybrid Voice 正文（规范达标 · 体感 7k–8k/案 · 见 V1.2 弹性指引）
Phase 3  文学/角色审计（academy-voice-editor · character-scale · literary-audit）
Phase 4  JP 定稿（翻译部 · academy-jp-tanaka-desk · M0-A/B 全绿）← **G-JP · 未 PASS 阻断 Phase 5/8/9**
Phase 5  Shot Map / 分镜头与插页地图（**须 JP V3.8 锚句 · M0 PASS 后定稿字字段**）
Phase 5b **空间资产查表** · 新场则建筑专家组 brief（[`16_V2空间资产复用…`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/16_V2空间资产复用与建筑插画专家组_V0.1.md)）· **禁重画教室/侧廊**
Phase 5.5 **G-TEXT + G-CAST 文字专家审核关** — 每帧 §11 + **出场白名单** + **禁止出场** + **`MAX_BODIES` 人数算术** · 角色 scale/空间/科学专家 **文字 PASS** · **未过禁止 GenerateImage**（见 `V2迁移/103_*` · `106_G-CAST_*`）
Phase 6  画风 Sheet 测试帧 / 深度锚点 brief（机制+服道化+连续性）
Phase 7  Prompt 包（Global Style + 角色前缀 + 分镜 §11 全字段）
Phase 8  G1 灰模 / AI 探索稿 → E06-S 分镜审
Phase 9  精修上色 v1.0 → visual-auditor → depth_anchor PNG
Phase 10 排版锁页（Reader / E22 五层标注）→ PRODUCT-GATE
```

**V2 与 V1 唯一顺序差异**：Phase 0–1 用 V2 母纲/Case Card/锐利标题；**Phase 5–10 流程与 V1.0 相同**。

对照详表：[`13_V1到V2插图生产工作流对照_V0.1.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/13_V1到V2插图生产工作流对照_V0.1.md)

---

## 3. 哪一步产出「分镜头」？

| 产出 | 时机 | 路径模式 |
|------|------|----------|
| **分场脚本** | Phase 1 · 与正文并行起草 | `V2迁移/04_分场脚本/A00X_V2_分场脚本_V0.2.md` |
| **分镜头与插页地图** | Phase 5 · **正文 CN 主干 + JP 工作稿齐** 后 | `样章包/03_案0X_分镜头与插页地图_V2.0.md` |
| **深度锚点 6 帧** | Phase 6 · Shot Map 中 P0 节点锁定 | `07_设计原档/04_样章视觉/A00X_V2_深度锚点包_*` |
| **补充分镜** | Phase 6 · L1 inset 条件启用 | `样章包/A00X_补充分镜候选_V*.md` |

**每一案** 独立一份 Shot Map · 张数不必相同 · 以 P0 节点为准。

V1 范例（流程结构，叙事已 SUPERSEDED）：[`03_案01_分镜头与插页地图_V1.2_完整分镜.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/样章包/03_案01_分镜头与插页地图_V1.2_完整分镜.md)

---

## 4. 出图前 · 分镜规划书必填（§11 · 缺一不得 prompt）

| 字段 | 关键词/要求 |
|------|-------------|
| 镜头编号 | `V-S0X-A1` / `DA1` |
| 原文范围 | §n 或 SC-xx 对应句 |
| 镜头功能 | **S/C/E/L/P/H**（可组合 S+L） |
| 强制级 | **P0/P1/P2** |
| 景别 | EWS/WS/MS/MCU/CU/ECU |
| 机位 | 平视/略俯/略仰/过肩/框中框 |
| 构图 | 三分/引导线/框中框/深浅景/留白呼吸 |
| 视觉中心 | 第一眼看哪里 |
| 第二信息 | 二刷才发现什么 |
| 人物 | 出场+站位（珣侧后/慧美拦/志郎蹲查…） |
| **出场白名单** | 本帧 **仅** 允许出现的具名角色 |
| **禁止出场** | 本帧 **不得** 出现的角色（A001 校内：**葛西·父母·瑆·理纱·中谷** 等） |
| 服道化 | 上履き · 四月光 · 道具标签 |
| 线索公平性 | 揭晓前是否已可见 |
| 连续性参照 | L0 / 上一帧 PNG ID |
| 文字留白 | 气泡/正文区 |

---

## 5. Prompt 组装顺序（禁跳步）

```
1. Global Style Block（画风 Sheet + 13_v2 + 04_视觉说明书 §2）
2. 角色前缀（14_v2 §3 · 逐人追加 · 6-7头身 #2A1810）
3. 本分镜 §11 字段（景别+机位+视觉中心+第二信息）
4. V2 机制 Must-see（visual-auditor Vol1 V2 表）
5. Negative（禁 chibi · 禁制服 · 禁 Plan B 废止主帧 · 禁 generic anime classroom）
```

**Demo 主帧** = Shot Map 中 **P0 首帧** 的完整 §11 行 · **不是** 仅 hook 一句话。

---

## 6. 角色 Scale（M 文档）

| Skill/文件 | 用途 |
|------------|------|
| [`academy-character-scale`](../../skills/academy-character-scale/SKILL.md) | 对白/动作 never_says · voice · relations |
| [`characters.yaml`](../../skills/academy-character-scale/characters.yaml) | 唯一真相源 |
| [`14_角色设计稿创作简报_v2`](../../../07_设计原档/03_角色视觉/14_角色设计稿创作简报_v2.md) | **视觉** scale · 体态 · 服装 |
| L0 排面 | `CHAR_lineup_L0_*` · 3840×2160 · 100–180cm 身高尺 |

**光**：橙/黄围巾 · 运动私服 · **公开日可 orange utility vest**（Sheet 定）  
**慧美**：银框镜 · 低马尾+耳侧细辫+柔黄发带 · 黄开衫  
**志郎**：绿格+绿 vest · 矮壮 · 圆框镜  
**珣**：蓝黄 · 路线本 · **侧后/观察位** · 非 C 位抢戏  

---

## 7. E06-S 分镜审（出厂前 · 8 项）

见 [`Vol1_分镜头电影化构图规范`](../../../07_设计原档/02_插画与场景/Vol1_分镜头电影化构图规范_V1.0.md) §13：

S1 P0 全覆盖 · S2 L 公平 · S3 功能类型已填 · S4 六项构图 · S5 角色动作 · S6 连续+科学 · S7 双轨边界 · S8 D1–D6 深度

**Verdict**：全部 S1–S8 → 才可 G1 探索稿；探索稿仍须 **visual-auditor** 单帧审。

---

## 8. V2 当前批次状态（2026-06-08）

| 项 | 状态 |
|----|------|
| V2 五案 CN 正文 | INTERNAL_DRAFT ✅ |
| V2 分场脚本 | ✅ |
| V2 Shot Map（03_案0X_V2） | ⬜ **未建** |
| `prompts_A00X_V2_demo_v0.1` | 🟡 缺 §11 字段 · **REJECT 探索** |
| `V-S0X-V2-DEMO_*.png` | 🟡 **REJECT** — 跳过 Phase 5–8 |
| 下一步 | 先 V2 Shot Map → 改 prompt → 重出 G1 |

---

## 9. 与 sibling skills

| Skill | 分工 |
|-------|------|
| `academy-engine` | Phase 0–4 正文 |
| **本 skill** | Phase 5–10 分镜+插图 |
| `academy-visual-auditor` | 单帧 P0/P1 审计 |
| `academy-jp-voice-editor` | Phase 4 JP 定稿 → 插图锚文本 |
| `academy-character-scale` | 角色言行 scale |

---

## 10. V3.6 试读批次（Unit1 · 2026-06-09）

五案 JP V3.6 → Shot Map JP 锚定 → `绑定正文_V3.6` G1DRAFT → 试读 PDF。

| 文档 | 路径 |
|------|------|
| 工作流 | [`88_单元1_V3.6_分镜插画试读PDF工作流_V0.1.md`](../../../03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/88_单元1_V3.6_分镜插画试读PDF工作流_V0.1.md) |
| Shot Map | `单元1…/正文/V3.6/04_分镜插画/A00X/03_分镜头_插页地图_V3.6_JP.md` |
| PDF 脚本 | `tools/build_unit1_trial_pdf.py` |

**诚实边界**：试读 PDF 用 G1DRAFT；PRODUCT-GATE 后替换绑定并重跑。

---

最后更新：2026-06-09 · V3.6 试读链路追加
