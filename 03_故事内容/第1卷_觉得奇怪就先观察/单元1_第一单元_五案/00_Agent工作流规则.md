# Agent 工作流规则 · 第一单元

> **强制执行** · 违反 = 浪费算力 + 无效交付  
> **流程 SSOT**：[../../11_规则与规范/00_全流程标准作业手册_V1.0.md](../../11_规则与规范/00_全流程标准作业手册_V1.0.md) ★  
> 更新：2026-06-11

## 核心规则：一案一时

| # | 规则 |
|---|------|
| R1 | 同时只 **ACTIVE** 一个单元文件夹（当前：**A001**） |
| R2 | **Phase 1 样张** 做完并 PASS 后，才进入 **Phase 2 排版** |
| R3 | A001 样张未 PASS → **禁止** A002–A005 的插画、样张、排版 |
| R4 | **禁止** 五案批量：批量出图、批量日译、批量 PDF、`vol1_auto_pipeline --full-auth` 跨案 |
| R5 | 新版本写入 `A00X/对应子目录`，更新 `00_正典指针.md`，旧文件进 `_archive/` |
| R6 | **Agent 执行纪律**：按本表 Phase 与三部门文档 **自动走流程** · **不逐步请示**「要不要做 X」· 闸门 FAIL → **从该 Phase 重跑**（修脚本/修稿/重审）直至 PASS 或触达 **仅人类可签** 的硬门 · 汇报 **状态与阻塞项**，不把流程决策抛回主编 |

## Phase 顺序 LOCK（2026-06-11 · produce / deliver 双轨）

```
编辑部 CN 定稿
  → 编+导 分镜文字 brief（editorial_verdict: PASS）
  → 译部 分镜审核（translation_verdict: PASS | RETURN）
  → 设计部出图（--mode produce）→ 成图双审
  → 04_样张 PDF 试读（--mode deliver：M0-B + G-AB-JP + COUNT_PASS）
  → 【G-AB-FULL】→ 05_排版
```

**M0-B / G-AB-JP 不挡 produce 出图** · **译部须 PASS 或 RETURN，禁止 pending 卡线** · 见 [`00_硬拦截说明_V1.0.md`](./00_硬拦截说明_V1.0.md)

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

## 硬拦截（2026-06-11 · produce / deliver）

```bash
# 出图 / prompt
python ".../tools/workflow_preflight.py" --mode produce --case A001
python ".../tools/workflow_preflight.py" --mode produce --phase generate-image --prompt A001/02_分镜头/prompts/DA2.md --case A001

# 试读审阅包
python ".../tools/workflow_preflight.py" --mode deliver --phase review-pack --case A001
```

| 结果 | Agent 动作 |
|------|------------|
| exit **0** | 继续 |
| exit **1** RETURN/FAIL | 按 RETURN 代码退回上一工位 · 修完重跑 · **禁止 pending 空等** |
| exit **2** | produce 模式不产生 · deliver 极少用 |

裁决 SSOT：[`00_译部分镜审核_单元1_V1.0.md`](./00_译部分镜审核_单元1_V1.0.md) · 分案 G-BRIEF · [`00_硬拦截说明_V1.0.md`](./00_硬拦截说明_V1.0.md)

## 闸门 FAIL 时 · Agent 默认动作（R6 细则）

| 结果 | Agent 动作（不问主编） |
|------|------------------------|
| `lint_jp_corruption` / M0 脚本 FAIL | 修脚本或正文 → 重跑 lint/M0 → 更新登记册 |
| G-TEXT / G-CAST FAIL | 修分镜 brief 或 DEMO → 重审 → 未 PASS 不出图 |
| STYLE DEMO / 画风审计 FAIL | 按 Style B LOCK 重出 DEMO → 再批量 |
| AI-DESK PASS 但真人主编 REJECT | **以真人结论为准** · 回到对应 Phase 重跑 · AI PASS **不算** M0-B |
| **G-AB-JP FAIL** | RETURN → **翻译部**修稿 · **仅 deliver 前必过** · 不挡 produce |
| **G-AB-FULL FAIL** | 分轨 RETURN · 未 PASS 不进排版 |
| 译部 pending | **RETURN** 译部出 PASS/RETURN · **不** 全线 BLOCKED_HUMAN |
