---
name: academy-gate-orchestrator
version: 0.1.0
description: 阶段门禁与专家汇总官。汇总四栏/ACE/E06；去重排序；输出 PASS/HOLD。P0-2 任务书。
allowed-tools: [Read, Write, Grep]
---

# academy-gate-orchestrator · V0.1 任务书（非自治）

## 输入
- 四栏回传 · P0-04 · E04/E07 · visual-auditor 报告 · ACE-B 草案

## 输出
- `GateA_E06_汇总表` 填充分栏
- 单一 Gate 报告：P0/P1/P2 · IP 待决 ≤5 条

## 禁止
- 冒充专家签字
- 覆盖 IP Owner E06 终签

## 状态
PLANNED — Gate A 6/13 后可首跑
