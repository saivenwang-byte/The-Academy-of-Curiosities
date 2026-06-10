---
name: academy-jp-tanaka-desk
version: 1.0.0
description: >-
  田中みどり「助手复合体」日文翻译终审台：MoA 四视角 + 出版编辑 + 科学术语 + 田中五维汇总。
  一人不够时用蒸馏专家/出版社编辑人格并行补位，产出可执行 JP 版本文件夹与复合体报告。
  用户提到田中助手、JP 复合审、MoA 日译、出版社编辑润色、G-JP 门禁时触发。
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Shell
---

# 田中助手复合体 · JP Translation Desk

## 问题

- **田中みどり一人**无法覆盖：标日语法 · 児童文学文体 · 公平推理 · 出版节奏 · 理科术语 · 全文五维文化。
- 真人出版社编辑/儿童文库编辑的审阅意见（如 doc81）需 **结构化接入**，而非每次口头重复。

## 解法

**TANAKA-DESK（田中终审台）** = 1 主审 + 5 助手 **顺序跑、报告合并**。

| 代号 | 映射 | 职责 |
|------|------|------|
| **TANAKA** | E07 · `日本校园文化顾问_田中みどり.txt` | 五维文化 · 校园叫法 · **汇总签核** |
| **HERMES-RONRI** | E05 · MoA #1 · Sobol/Hayamine | 公平线索 JP 可见 · 揭晓前无剧透 |
| **HERMES-BUNPO** | E04 · MoA #2 · あさば/はやみね | 均句 ≤40 假名 · 留白 · L09 |
| **HERMES-GOUI** | E04 · MoA #3 · J1–J10 | 直译腔 · 词汇 · 标点 · L10 |
| **HERMES-DOKUSHA** | E03 · MoA #4 | 10–12 可读 · ふりがな策略 · L11 |
| **EDITOR-SHO** | E16 · 真人编辑/青鸟文库型 | 娱乐性 · 审判腔 · 信息密度 · doc81 |
| **SCI-RIKA** | engine 科学 · P06 | 結露/振动/全景等术语一致 |

**主审仍是田中** — 助手只产出 **分报告 + 修改建议**，不替代 `READY_FOR_TRANSLATION` 签字。

---

## 何时触发

- CN 已定稿（如 V3.1）需 **整卷或逐案** 日译终审
- V3.x JP MoA-lite 后仍 **自然度 <8**
- E20 日文 pilot 前需 **复合体 PASS**
- IP 要求「像出版社过稿一样」过日文

**不触发**：仅改中文 · 仅 glossary 替换无全文读稿。

---

## 可执行入口（Agent / CLI）

```bash
# 单案
python "03_故事内容/第1卷_觉得奇怪就先观察/tools/jp_tanaka_desk/run_desk.py" \
  --case A001 --cn-version V3.1 --jp-in-version V3.3 --jp-out-version V3.4

# 全卷五案 · kids simplify V3.5
python ".../jp_kids_simplify_pass.py" --all --cn-version V3.1 --jp-in-version V3.4 --jp-out-version V3.5
```

**产出**（每案）：

```
单元1_第一单元_五案/正文/V3.4/
  01_中文/          ← 从 CN 版本拷贝（不变）
  02_日本語/        ← 复合体润色后 JP
  03_版本意见/
    00_TANAKA-DESK_复合体报告_A001.md
    文化校准报告_日本語_A001.txt    ← 归档用 · 对接 09_CONSULTANT_REVIEW_LOG

单元1_第一单元_五案/正文/V3.5/   ← kids simplify 后
  03_版本意见/00_KIDS-SIMPLIFY_报告_A001.md
```

**SSOT 工作流**：`V2迁移/86_田中助手复合体_JP翻译工作流_V0.2.md`

---

## Agent 执行步骤（无 CLI 时）

1. 读 `tools/jp_tanaka_desk/desk_roster.yaml`
2. 读 CN 定稿 + JP 输入稿 + `doc81` ADOPT 项 + `00_JP_TRANSLATION_REVIEW_GATE.md`
3. **按 roster 顺序** 逐助手过稿（每助手输出：PASS/CONDITIONAL/FAIL + 修改清单）
4. 合并修改 → 写入 `--jp-out-version` 新文件夹（**不覆盖**输入版本）
5. 写 `00_TANAKA-DESK_复合体报告_A00X.md` + 更新 `scores_*_jp.json`
6. TANAKA 汇总判定：`G-JP DRAFT` / `DESK_PASS` / `BLOCK（须人类）`

---

## 与现有 Skill 关系

```
CN 定稿
  → academy-jp-voice-editor（MoA-lite 初润 · V3.2）
  → jp_tanaka_j10_pass（V3.3）
  → 【本 skill · TANAKA-DESK 复合体 · V3.4】
  → jp_kids_simplify_pass（V3.5 · doc81 3.5 自然度）
  → TANAKA-DESK 可选复跑（V3.6）
  → 真人田中 J10 签字（若有人）
  → E20 试读
  → G-JP LOCK
```

| 上游 | 本 skill | 下游 |
|------|----------|------|
| `jp_v32_expert_polish.py` / V3.2 | 复合体 7 席 · V3.4 | `jp_kids_simplify_pass.py` → V3.5 |
| doc81 真人编辑 | EDITOR-SHO 席吸收 | doc84/85/86 分数更新 |

---

## 人类替补（RACI）

| 助手 | 优先真人 | 无真人时 |
|------|----------|----------|
| TANAKA | E07 日本顾问 | Agent + `japan_campus_consultant_agent.html` |
| EDITOR-SHO | E16 出版编辑 · **本次 doc81 真人** | Agent 模拟 + doc81 checklist |
| HERMES-* | E04 日童编辑 | MoA-lite 规则 + novel2hermes 检查表 |
| SCI-RIKA | 科学 P0 签核人 | engine FC/P06 对照 · **BLOCK 直至 Lab** |

---

## 门禁

- **DESK_PASS**：7 席无 FAIL · CONDITIONAL ≤2 · TANAKA 汇总 YES
- **不得** 仅跑 HERMES-GOUI（glossary）即标 DESK_PASS
- **不得** Agent DESK_PASS 替代真人田中 **G-JP LOCK**（仅升到 `G-JP DRAFT` 或 `DESK_PASS_PENDING_HUMAN`）

触发语：「跑田中助手复合体 A001」「TANAKA DESK 全卷」「JP 复合审 V3.4」
