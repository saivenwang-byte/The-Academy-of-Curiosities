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

## 同音防撞（CC 报告 C 步 · 2026-06-10）

**断言**：在册角色 **不得共用同一 furigana 读音**。

| 正确 | 废止 | 说明 |
|------|------|------|
| 陸瑆 → **ひかる** | — | 妹妹 · 4年 |
| 伊藤光 → **あきら**（いとう あきら） | ひかる · `ito_hikaru` | 俱乐部成员 · 5年 |
| 陸珣 → **りくじゅん** / しゅん | — | 转学生 · 5年 |

审计时 grep：`ひかる` 不得同时标注光与瑆；`ito_hikaru` / `Ito Hikaru` 为废止残留。见 [`00_十人名称_LOCK_2026-06-07.md`](../../01_角色设定/00_十人名称_LOCK_2026-06-07.md)。

## 状态
PLANNED — 校准包 P0-2 实现首跑 · 同音断言已入任务书
