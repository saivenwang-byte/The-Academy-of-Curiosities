# 专家池 · ACE 蒸馏注册表 · V1.0

> **Status**: ACTIVE · **2026-06-08 就位**  
> **取代**: 虚拟专家假名 Agent（`academy-expert-*`）· 见 [`虚拟专家增补计划_20260607.md`](./虚拟专家增补计划_20260607.md) SUPERSEDED  
> **机器正本**: [`skills/ace-experts/README.md`](../skills/ace-experts/README.md)

---

## 1. Gate A 缺口 → ACE 映射（已就位）

| 原缺口 | E 编号 | ACE Officer | 蒸馏卡 ID | 状态 |
|--------|--------|-------------|-----------|------|
| 日文母语/出版编辑 | **E04** | ACE-A | `LNG-jp-vol1-readability` | ✅ active |
| 日本校园/文化顾问 | **E07** | ACE-A | `CUL-nagoya-campus-five-layer` | ✅ active |
| 科学/线索公平 · P0-04 | **E09** | ACE-A | `SCI-a001-clue-fairness` | ✅ active |
| Gate A 合规扫描 | **E25** | ACE-A | `CMP-gate-a-compliance` | ✅ active |
| 线稿 brief / PNG 对齐 | **G1** | ACE-B | `G1-brief-png-alignment` | ✅ active |
| 深度锚点线索可见 | **G1/E06** | ACE-B | `VIS-fair-clue-frame` | ✅ active |
| 试读 band / 组织者口径 | **E20** | ACE-C | `TRI-vol1-reader-band` | ✅ active |

**仍须 👤**：**E06 终签** · **IP Owner** · 画师 **G1 PNG 产出**（ACE 签 brief 对齐，不产图）

---

## 2. 旧虚拟专家名 → ACE（归档对照）

| 原拟虚拟名 | 原 Agent 名 | 现映射 |
|------------|-------------|--------|
| 吉田文子 | academy-expert-jp-literary | ACE-A · `LNG-jp-vol1-readability` |
| 田中みどり（蒸馏） | 文化 HTML 工具 | ACE-A · `CUL-nagoya-campus-five-layer` + 既有 `japan_campus_consultant_agent.html` |
| 佐藤健一 | academy-expert-science-lab | ACE-A · `SCI-a001-clue-fairness` |
| 渡辺理 | academy-expert-mystery-qc | ACE-B · `VIS-fair-clue-frame` + engine C03 |
| 小林由美 | academy-expert-jp-readability | ACE-C · `TRI-vol1-reader-band` |
| 鈴木版 | academy-expert-prepress | ACE-D（Gate D · 未建） |

---

## 3. 签核路径（蒸馏就绪后）

1. 调用对应 ACE Officer Skill → 加载蒸馏卡  
2. 对目标文件跑 `checks[]` → 产出报告（头：`STATUS: DRAFT · NOT SIGNOFF`）  
3. `python scripts/ace_distill_lint.py` PASS  
4. Gate 包标注：`signoff_type: ace_distilled` · `distill_card_id: …`  
5. **E06 / IP Owner** 收齐后终签  

过渡：6/13 前人类四栏 **仍可并行**；未切换项走 👤。

---

## 4. 验收

- [x] ACE-A / ACE-B / ACE-C Officer SKILL.md  
- [x] 蒸馏卡 ≥7 · lint PASS  
- [x] `docs/ace-distill/` 知识源索引  
- [x] 专家库盘点互链  
- [ ] IP 启用 `ace_distilled` 路径（可选 · 逐 E 编号切换）

---

| 版本 | 2026-06-08 · Gate A 缺口专家蒸馏就位 |
