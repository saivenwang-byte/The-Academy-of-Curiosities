# 《学堂趣事录》项目启动前置检查门 V0.1

Status: ACTIVE  
Priority: HIGHEST PROJECT RULE  
Applies to: every story, outline, scene, dialogue, visual prompt, sample chapter

---

## 0. Core Decision

**教室正典（LOCKED）**：主人公团队 = **`4年2組 · 窗=校庭`** — 禁止写为 5年2組。  
详：`docs/world_reference/00_SCHOOL_CLASS_CANON_LOCKED.md`

《学堂趣事录》不是凭感觉写日本校园，也不是把中国校园故事翻译成日文。

每一卷正式写作前，必须同时通过 **L1 三并列** 与三道检查门：

| L1 | 门 | 入口 |
|----|-----|------|
| 日本校园文化顾问 | 文化校准门 | `japan_campus_consultant_agent.html` |
| **Project World Metrics** | 名古屋环境指标门 | `docs/world_reference/00_MASTER_ENVIRONMENT_INDEX.md` |
| 本格推理公平规则 | 本格推理公平门 | `docs/world_reference/04_MYSTERY_SCIENCE_CASE_STANDARD.md` |

1. **日本文化校准门**：制度、空间、行为、语言、儿童文化、情感分寸。  
2. **名古屋环境指标门**：地理、气候、日照、湿度、物候、水迹、科学机制。  
3. **本格推理公平门**：线索提前出现、可验证、儿童可推理。

任何一项未通过，文本状态只能标记为：

`PENDING_REVIEW`

不得标记为：

`READY_FOR_SAMPLE` / `READY_FOR_TRANSLATION` / `READY_FOR_ARTIST`

**日文版**：`READY_FOR_TRANSLATION` 额外要求 — 见 `docs/00_JP_TRANSLATION_REVIEW_GATE.md`（田中みどり **全文**五维督查 + J1–J7，产出 `文化校准报告_日本語.txt`）。中文 L1 不能替代。

---

## 1. Required Reference Files

写作前必须查阅以下文件：

**红线与协议**
- `docs/world_reference/00_SCHOOL_CLASS_CANON_LOCKED.md` — **4年2組 · 窗=校庭（LOCKED）**
- `docs/00_REDLINE_JP_CULTURAL_CALIBRATION.md`
- `docs/02_REFERENCE_LIBRARY_IMPORT_PROTOCOL.md`
- `02_创作原则与世界观/创作红线与原则.txt`

**Project World Metrics（世界环境指标库）**

- `docs/world_reference/00_MASTER_ENVIRONMENT_INDEX.md` — **正典入口**
- Writer Quick Ref：`01`–`08`（见总索引 §1）
- Maintenance 细则：`docs/world_reference/maintenance/`（09_ 蒸馏 · 08 打标）
- 每卷执行卡：`docs/volume_planning/`

**L1 硬指标（名古屋数值蒸馏层）**
- `02_创作原则与世界观/名古屋写作硬指标_本格科学参考.md`
- `02_创作原则与世界观/日本校园文化顾问_田中みどり.txt`
- `japan_campus_consultant_agent.html`

**L2 素材库（查原文，不直接当规则）**
- `09_日本参考资料库/INDEX.md`

---

## 2. Mandatory Scene Card

每一场正式写作前，必须先写一张 Scene Card：

```text
卷目：
场景编号：
class_canon: 4年2組 · 窗=校庭（必填 · LOCKED）
地点：名古屋 / 具体校内或通学路空间
月份：
时间：
天气：
气温：
湿度：
光线方向：
日出 / 日落参考：
人物为什么在这里：
涉及校园制度：
涉及日本称呼 / 口语：
涉及自然或科学机制：
可被儿童观察到的线索：
禁止触碰的红线：
需要顾问复核：YES / NO
```

---

## 3. Mandatory Case Card

每一卷正式写作前，必须先写一张 Case Card：

```text
卷目：
class_canon: 4年2組 · 窗=校庭（必填 · LOCKED）
核心异常：
表层误会：
真实机制：
核心知识：
交叉知识：
公平线索 1：
公平线索 2：
公平线索 3：
儿童可复现实验：
日本校园成立理由：
名古屋环境成立理由：
最终解释是否零超自然：YES / NO
```

---

## 4. Review Order

1. Case Card
2. Scene Card
3. Japan Cultural Calibration Agent
4. Environment Metrics Review
5. Science and Fair-play Review
6. Drafting
7. Second review
8. Archive（中文 L4）
9. **日文翻译 → 田中みどり全文督查**（见 `docs/00_JP_TRANSLATION_REVIEW_GATE.md`）
10. READY_FOR_TRANSLATION（仅日文督查 PASSED 后）

---

## 5. Editorial Principle

本项目的创作方式等同于建立一张“故事作战地图”。

经纬度、海拔、光影、气温、湿度、学校动线、称呼、饮食、方言、物候、风、雨、水迹、声音和儿童行为，都不是装饰，而是推理证据系统的一部分。
