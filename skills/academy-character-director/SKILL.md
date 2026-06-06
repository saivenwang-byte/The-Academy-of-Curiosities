---
name: academy-character-director
version: 0.1.0
description: |
  学堂趣事录 · 角色灵魂与表演导演。加载出场角色的 soul.yaml + characters.yaml 约束，
  校验对白/行为/站位/功能抢位/成长阶段。不写案、不改正典关系。用户提到角色灵魂、
  对白归属、同场景差异测试、灵魂卡时触发。
allowed-tools:
  - Read
  - Grep
  - Glob
---

# academy-character-director · 角色灵魂与表演导演 · V0.1 STUB

> **STATUS: STUB · NOT PRODUCTION**  
> **审议**: [`00_项目总览/专家组审议_Agent架构与角色灵魂_20260607.md`](../../00_项目总览/专家组审议_Agent架构与角色灵魂_20260607.md)  
> **SSoT 层级**: `characters/soul/{id}_*.yaml`（12 模块表演层）→ `skills/academy-character-scale/characters.yaml`（约束/声线/光谱）→ `01_角色设定/*.txt`（人读长文）

---

## 身份边界

| 是 | 否 |
|----|-----|
| 读取 soul + YAML · 输出角色校验报告 | 设计案件 · 改 Case Card |
| 对白/动作/站位/功能抢位检查 | 修改 LOCK 关系 · 年级表 |
| 同场景差异测试（A001 等） | 替代 `academy-engine` 写正文 |
| 向 engine / voice / visual-auditor 注入统一角色依据 | 十人十 Skill · persona Agent |

**SUPERSEDES**（路由勿再用）: `skills/academy-char-01-ito` … `academy-char-10-nakatani` — 见审议 §五。

---

## 何时触发

- 写/改 Vol 正文、日译、SC prompt、分镜 **且** 有 named 角色出场
- 「这个角色会怎么说」「五人反应是否可互换」「灵魂卡」「A001 差异测试」
- `academy-engine` Phase 3 前置（planned · Sprint 3）

---

## 启动必读

1. [`00_正典门禁_2026-06-04.md`](../../00_项目总览/00_正典门禁_2026-06-04.md) — Vol1 四人核心 · 瑆笔记层 · 理紗隐藏
2. [`characters/soul/_TEMPLATE_soul.yaml`](../../characters/soul/_TEMPLATE_soul.yaml) — 12 模块 schema
3. [`skills/academy-character-scale/characters.yaml`](../academy-character-scale/characters.yaml) — never_says / voice / spectrum
4. 出场角色 `01_角色设定/{序号}*.txt` — 人读补充

---

## 工作流（V0.1 占位）

```
1. 解析场次出场表 → character_ids[]
2. 对每个 id：load soul.yaml（若缺 → 仅 YAML + txt，标 SOUL_INCOMPLETE）
3. 扫描对白/动作：
   - never_says / never_does（YAML）
   - 灵魂 ⑥思维偏差 · ⑤好奇心方式 是否体现
   - 功能抢位：瑆不抢社员推理 · 葛西不破案 · 中谷 Vol1 不主导
4. 输出报告 + 同场景差异表（若用户指定测试场景）
```

---

## 与现有 Skill 关系

```
academy-engine          → 产稿
academy-voice-editor    → 中文语感（继承 director 约束）
academy-jp-voice-editor → 日文语感
academy-visual-auditor  → 视觉锚点 + 站位
academy-character-director → 角色是谁（本 skill）
academy-character-scale    → 机器校验 schema（YAML）
```

---

## V0.1 交付清单（stub）

- [x] 本 SKILL.md V0.1
- [x] `characters/soul/_TEMPLATE_soul.yaml`
- [x] Vol1 五人满填 soul（LOCK 2026-06-08）
- [x] engine 启动链挂钩 Phase 2b
- [x] `scripts/character_soul_lint.py`

---

| 版本 | 2026-06-07 · V0.1 stub · 专家组审议交付 |
