# Agent 工作流规则 · 第一单元

> **强制执行** · 违反 = 浪费算力 + 无效交付  
> 更新：2026-06-10

## 核心规则：一案一时

| # | 规则 |
|---|------|
| R1 | 同时只 **ACTIVE** 一个单元文件夹（当前：**A001**） |
| R2 | **Phase 1 样张** 做完并 PASS 后，才进入 **Phase 2 排版** |
| R3 | A001 样张未 PASS → **禁止** A002–A005 的插画、样张、排版 |
| R4 | **禁止** 五案批量：批量出图、批量日译、批量 PDF、`vol1_auto_pipeline --full-auth` 跨案 |
| R5 | 新版本写入 `A00X/对应子目录`，更新 `00_正典指针.md`，旧文件进 `_archive/` |
| R6 | **Agent 执行纪律**：按本表 Phase 与三部门文档 **自动走流程** · **不逐步请示**「要不要做 X」· 闸门 FAIL → **从该 Phase 重跑**（修脚本/修稿/重审）直至 PASS 或触达 **仅人类可签** 的硬门 · 汇报 **状态与阻塞项**，不把流程决策抛回主编 |

## Phase 顺序 LOCK（2026-06-10）

```
编辑部 CN 定稿
  → 翻译部 JP + M0-A/B 全绿
  → 【G-AB-JP】翻译部专家组 + 读者群 AB 盲测 → 未达标回翻译部修稿重测
  → 编+译 分镜文字 brief（G-BRIEF 双签）→ G-TEXT + G-CAST
  → 设计部出图（Style B only）→ 编+译 成图双审
  → 04_样张 PDF
  → 【G-AB-FULL】专家组 + 读者群 AB 盲测（含 E20）→ 未达标分轨退回重测
  → 05_排版 → 正式版通告
```

分工见 [`00_三部门总览_V1.0.md`](./00_三部门总览_V1.0.md) · [`00_翻译部与编辑部_分工_V1.0.md`](./00_翻译部与编辑部_分工_V1.0.md) · [`00_设计部_插画画工流程_V1.0.md`](./00_设计部_插画画工流程_V1.0.md) · [`00_AB盲测闸门_V1.0.md`](./00_AB盲测闸门_V1.0.md) ★

**G-AB-JP 未 PASS → 禁止 G-BRIEF / 设计部出图** · **G-AB-FULL 未 PASS → 禁止 05_排版 / 正式版通告**

## Phase 1 · 样张（单案）

```
01_正文 CN+JP 锁版 → 02_分镜头 §11 文字 → G-TEXT + G-CAST 专家审 → 03_插画（本案 only）→ 04_样张（试读 PDF）→ 验收
```

| 关卡 | 说明 |
|------|------|
| **G-TEXT** | 每帧出场白名单 + 禁止出场 · **未 PASS 禁止 GenerateImage** |
| **G-CAST** | 每帧 `MAX_BODIES` + 具名/匿名算术 · 成图 **数人头** · 见 `V2迁移/106_G-CAST_出场人数算术关_V1.0.md` · **未 PASS 禁止出图/进 PDF** · **导演审定表签字** 见 `A001/02_分镜头/00_G-CAST_导演审定表_A001_V1.0.md` |
| **M0-JP** | 日文 PDF 试读前：**M0 验收全绿** · 见 `00_M0-M5_试读合规验收标准_V1.0.md` |
| **E06-S** | 分镜 8 项 · visual-auditor 流程 |
| **L0 群像** | `CHAR_lineup_L0_修正_V0.4` IP 签后再 embed |

验收门：E20 / 读者试读 / PRODUCT-GATE 清单

## Phase 2 · 排版（单案）

前置：本案 `04_样张/` 已签字  
产出：`05_排版/` 全页排版 PDF

## 活跃单元切换条件

- A001 `04_样张/` PASS → 更新 `00_单元导航.md` 活跃单元为 A002  
- 以此类推 A003 → A004 → A005

## 工具调用

| 工具 | 适用范围 |
|------|----------|
| `build_a001_e20_pilot_pdf.py` | 仅 A001 |
| `build_unit1_trial_pdf.py` | **暂停** 五案批量；单案 PDF 待拆 |
| `vol1_auto_pipeline/run.py` | **禁止** `--full-auth` 跨案；仅 DESK/KIDS 等文稿步骤可按案调用 |

## 读路径顺序

1. [`00_正本登记册_V1.0.md`](./00_正本登记册_V1.0.md) ★  
2. `A00X/00_正典指针.md`  
3. `A00X/01_正文/`  
4. `00_单元导航.md`

**门禁**：交付前 `python scripts/vol1_ssot_gate.py` 须全绿

## 硬拦截（2026-06-10 · 技术门禁）

**GenerateImage / 写 prompt / 组装审阅包 / 写 PRODUCT 路径之前**，Agent **必须**跑：

```bash
python "03_故事内容/第1卷_觉得奇怪就先观察/tools/workflow_preflight.py" --phase generate-image --prompt A001/02_分镜头/prompts/DA2.md
python "03_故事内容/第1卷_觉得奇怪就先观察/tools/workflow_preflight.py" --phase review-pack
```

| 结果 | Agent 动作 |
|------|------------|
| exit **0** | 继续 |
| exit **1** FAIL | 修脚本/修稿/修 prompt → 重跑 · **禁止**问主编「要不要继续」 |
| exit **2** BLOCKED_HUMAN | 汇报 **BLOCK 代码** + 待签人 · **停止** · 禁止写 `03_插画成片` / `06_主编审阅包` / `PRODUCT_*` |

签核 SSOT：[`A001/02_分镜头/00_G-CAST_导演审定表_A001_V1.0.md`](./A001/02_分镜头/00_G-CAST_导演审定表_A001_V1.0.md) · [`00_G-BRIEF_双签_A001_V1.0.md`](./A001/02_分镜头/00_G-BRIEF_双签_A001_V1.0.md) · 说明 [`00_硬拦截说明_V1.0.md`](./00_硬拦截说明_V1.0.md)

## 闸门 FAIL 时 · Agent 默认动作（R6 细则）

| 结果 | Agent 动作（不问主编） |
|------|------------------------|
| `lint_jp_corruption` / M0 脚本 FAIL | 修脚本或正文 → 重跑 lint/M0 → 更新登记册 |
| G-TEXT / G-CAST FAIL | 修分镜 brief 或 DEMO → 重审 → 未 PASS 不出图 |
| STYLE DEMO / 画风审计 FAIL | 按 Style B LOCK 重出 DEMO → 再批量 |
| AI-DESK PASS 但真人主编 REJECT | **以真人结论为准** · 回到对应 Phase 重跑 · AI PASS **不算** M0-B |
| **G-AB-JP FAIL** | 修改清单 → **翻译部**修稿 → 重跑 M0 + **G-AB-JP** · 未 PASS 不进 G-BRIEF |
| **G-AB-FULL FAIL** | 按主因分轨退回（文/图/画风/E20）→ 修完 **重跑 G-AB-FULL** · 未 PASS 不进排版 |
| 仅人类硬门 pending | 汇报阻塞（如田中 M0-B · IP 签 · E20 招募）· **不** 越门 |
