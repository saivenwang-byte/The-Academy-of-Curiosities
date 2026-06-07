# 第一单元 MVP · 生产顺序 LOCK · CN → 分镜文字 → JP → 插画 → 排版

> **Status**: **ACTIVE · 生产化段 SSOT** · 2026-06-08  
> **正文期最小路径**：见 [**`24_最小路径_CN正文工作流_V1.0.md`**](./24_最小路径_CN正文工作流_V1.0.md) ★ —— TITLE→SPINE→BODY→REVIEW LOOP **先于** 本文件 §2 Gate  
> **插画路径 LOCK**：[`27_IP裁定_混合插画门禁_LOCK_V0.1.md`](./27_IP裁定_混合插画门禁_LOCK_V0.1.md) · IP APPROVED 2026-06-08  
> **本文件**：**G-JP 门禁**（§3）· **G-MVP 包**（§6）细节 **仍有效** · §2 Gate 表时点以 doc 26 为准  
> **裁决**：IP Owner 确认 · 与首市场 JP 试读 **不矛盾**（中文=创作稿 · 日本語=试读交付语）  
> **依据**：[`篇幅与单位构架_V1.1.md`](../../../../00_项目总览/篇幅与单位构架_V1.1.md) · [`docs/00_JP_TRANSLATION_REVIEW_GATE.md`](../../../../docs/00_JP_TRANSLATION_REVIEW_GATE.md) · [`academy-illustration-pipeline`](../../../../.cursor/skills/academy-illustration-pipeline/SKILL.md)

---

## 0. 结论（可以 · 且应这样做）

**可以，且比「先出 demo 图再改文」更稳。**

最小 MVP 试读（日本語 Reader/PDF）推荐顺序：

```
① 五案中文正文 → IP Owner 逐案确认（CN_OWNER_LOCK）
② 分镜头文字描述（Shot Map · 无 PNG）→ 主编/E06-S 文字审
③ 日译 + jp-voice-editor + E04/E07 专家组 → JP_OWNER_LOCK
④ 分镜插画（G1→精修）· 气泡/屏显/黑板字用 JP 定稿
⑤ 瑆笔记 + 单元插画齐 → E22 排版锁页 → 最小试读样章
```

**原则**：插画 **一次成型** 的前提是 **CN 情节锁 + JP 字锁 + Shot Map 字锁** 三者齐；缺一则只能 G1 探索，不得 PRODUCT。

---

## 1. 与「首市场日本語」的关系

| 文档 | 说法 | 本流程 |
|------|------|--------|
| [`00_首市场与试读语言_LOCK`](../../../../00_项目总览/00_首市场与试读语言_LOCK_2026-06-07.md) | 试读=日本語 | ✅ MVP **交付物** 为 JP |
| [`篇幅与单位构架_V1.1`](../../../../00_项目总览/篇幅与单位构架_V1.1.md) | **中文为创作稿** | ✅ 先写/先审 CN |
| [`00_JP_TRANSLATION_REVIEW_GATE`](../../../../docs/00_JP_TRANSLATION_REVIEW_GATE.md) | 中文定稿 ≠ 可出版日文 | ✅ JP 独立门禁 |

---

## 2. 分阶段 Gate（五案通用）

| Gate | 名称 | 输入 | 输出 | 谁签 |
|:----:|------|------|------|------|
| **G-CN** | 中文正文锁 | Hybrid Voice V2 CN | `CN_OWNER_LOCK` 逐案 | **IP Owner（您）** |
| **G-SHOT-T** | 分镜文字锁 | G-BODY + Case Card | `03_案0X_分镜头与插页地图_V2.0.md` | 主编 + E06-S · **LOCK 时点 = G-KF-REVIEW**（doc 26） |
| **KF-LOCK-T** | 关键帧构图锁 | **G-BODY** + Shot Map V2 **草案** | `07_设计原档/04_样章视觉/KF_LOCK_T/` · 见 [`21`](./21_插画关键帧锁定策略_G-EDITOR前提下_V0.1.md) · [`26`](./26_插画门禁路径判断_正文后关键帧_vs_日译优先_V0.1.md) | **IP Owner** · **∥ G-JP 并行** |
| **G-JP** | 日文正文锁 | G-BODY | `案0X_*_HybridVoice_V2.0_日本語.txt` | E04 + E07 田中 · **∥ G-KF-T 并行** |
| **KF-LOCK-J** | 插画字锁 | G-JP + KF-LOCK-T | brief v0.2 · 气泡/屏显/黑板/DB1 字列 diff | E04 + E07 + IP Owner |
| **G-KF-REVIEW** | 关键帧终审 | KF-LOCK-J | 帧审 PASS · **G-SHOT-T LOCK** · doc 26 §5 | 主编 + E06-S + auditor + IP |
| **G-IMG** | 插画锁 | **G-KF-REVIEW** PASS | depth_anchor PNG v1.0 | visual-auditor |
| **G-MVP** | 试读样章 | G-JP + G-IMG + E22 | Reader/PDF | Gate A/B |

**硬规则**：

- **G-BODY 后 G-JP 与 KF-LOCK-T 并行**（doc 26）· Shot Map V2 **草案** 供 T 阶段 · **G-SHOT-T LOCK** 并入 **G-KF-REVIEW** · **KF-LOCK-J** 汇合后帧审 · 再 **G-IMG**
- **禁止** G-CN 未过 → 正式插画 v1.0
- **允许** G-CN 未过 → 内部 G1 探索（须标 `G1DRAFT`）

---

## 3. 日译门禁要点（G-JP 必查）

| 来源 | 要点 |
|------|------|
| [`academy-jp-voice-editor`](../../../../.cursor/skills/academy-jp-voice-editor/SKILL.md) | 中文定稿后 · MoA 四视角 · 去直译腔 |
| [`日文读音标注策略_V1.1`](../../../../00_项目总览/日文读音标注策略_V1.1.md) | 标日字符密度 · 选择性ルビ · 禁「全振假名」 |
| [`00_十人名称_LOCK`](../../../../01_角色设定/00_十人名称_LOCK_2026-06-07.md) | 光=**あきら** · 瑆=**ひかる** |
| [`Vol1_声线验收清单`](../../../../00_项目总览/Vol1_声线验收清单_V1.0.md) | 对话口语 · 珣台词≤5/卷 |
| [`E07_田中文化门禁_Vol1_V0.2_MVP`](../07_文化门禁/E07_田中文化门禁_Vol1_V0.2_MVP.md) | 上履き/保健室/公开日/名古屋 |
| [`00_JP_TRANSLATION_REVIEW_GATE`](../../../../docs/00_JP_TRANSLATION_REVIEW_GATE.md) | 全文五维 · 0 实质红项 |
| [`09_日本校园文化顾问`](../../../../08_日本校园文化顾问/日本校园文化校准手册.md) | 推拉门/换鞋/给食等 |

**篇幅**：E04 日译 **改写至 JP 预算**（非 CN 1:1）· 见 [`篇幅与单位构架_V1.1`](../../../../00_项目总览/篇幅与单位构架_V1.1.md) §3。

---

## 4. 分镜文字描述（G-SHOT-T 交付物）

每案一份 · 模板 [`00_单案分镜头交付模板_V1.0.md`](../样章包/00_单案分镜头交付模板_V1.0.md)：

- Scene Cards 表（链 SC）
- Shot Map 全字段（S/C/E/L/P/H · 景别 · 机位 · 视觉中心 · **原文范围**）
- **不含 PNG** 阶段即可您审「画什么、谁在哪、线索是否公平」

A001 范例：[`03_案01_分镜头与插页地图_V2.0.md`](../样章包/03_案01_分镜头与插页地图_V2.0.md)（DA1 G1 探索 **不等同** G-IMG 过门）

---

## 5. 当前批次状态（2026-06-08 · doc 27 supersede）

> **口径**：**G-BODY 未签** · 生产化 **冻结** · 2026-06-08 G-EDITOR/KF-LOCK-T 签 = **PRE-G-BODY** · 见 [`27_IP裁定_混合插画门禁_LOCK_V0.1.md`](./27_IP裁定_混合插画门禁_LOCK_V0.1.md)

| 案 | G-BODY | G-EDITOR† | G-CN | G-SHOT-T | KF-LOCK-T† | G-JP | G-KF-REVIEW | G-IMG | 说明 |
|:--:|:------:|:---------:|:----:|:--------:|:----------:|:----:|:-----------:|:-----:|------|
| A001 | ⬜ | ✅ PRE-G-BODY | ⬜ | 🟡 草案 | ✅ PRE-G-BODY | ⬜ | ⬜ | 🟡 DA1 G1 only | 器材车 **direct** |
| A002 | ⬜ | ✅ PRE-G-BODY | ⬜ | 🟡 草案 | ✅ PRE-G-BODY | ⬜ | ⬜ | ⬜ | 展示膜 · 车 **间接** |
| A003 | ⬜ | ✅ PRE-G-BODY | ⬜ | 🟡 草案 | ✅ PRE-G-BODY | ⬜ | ⬜ | ⬜ | 壁报 · 车 **间接** |
| A004 | ⬜ | ✅ PRE-G-BODY | ⬜ | 🟡 草案 | ✅ PRE-G-BODY | ⬜ | ⬜ | ⬜ | 振动 · 车 **间接** |
| A005 | ⬜ | ✅ PRE-G-BODY | ⬜ | 🟡 草案 | ✅ PRE-G-BODY | ⬜ | ⬜ | ⬜ | 卷终 · 车 **direct** |

† **PRE-G-BODY**：历史签保留 · **不** 解锁 G-JP / G-KF-T 修订 / G-KF-REVIEW / G-IMG · G-BODY 后重签或 diff

**CN 篇幅**：五案合计 **21,843** CJK · 逐案均 ≥3,200 · A005 卷末瘦圈 −531 · **不强制 7k–8k**（C7）

---

## 6. MVP 试读最小包（G-MVP）

| 项 | 内容 |
|----|------|
| 文字 | 序 + A001–A005 **JP 定稿**（或 Gate A 先 序+A001） |
| 图 | 每案 P0 深度锚点 + 1 B-SUM + 瑆 |
| 排版 | E22 五层 · A5 · Reader HTML/PDF |
| 试读 | E20 真实 10–12 岁 · JP 材料 |

---

最后更新：2026-06-08 · **G-BODY 未签 · 生产冻结** · doc 27 IP APPROVED hybrid · PRE-G-BODY 历史签不解锁
