---
name: academy-canon-governor
version: 0.1.0
description: 正典治理与变更控制器。检查 Skill/正文/索引与 LOCK 冲突；输出变更影响；不写故事。P0-2 任务书。
allowed-tools: [Read, Grep, Glob]
---

# academy-canon-governor · V0.1 任务书（非自治）

## 输入
- `00_正典门禁` · `正典文件索引` · `characters.yaml` · 目标 diff 范围

## 输出
- `Skill正典一致性审计表` 更新行
- 冲突矩阵（文件A vs 文件B）
- CHANGE IMPACT：可自动修 / 须 IP 裁决

## 禁止
- 修改 LOCK 文件无 IP 批准
- 代替 gate-orchestrator 汇总四栏

## 状态
PLANNED — 校准包 P0-2 实现首跑
