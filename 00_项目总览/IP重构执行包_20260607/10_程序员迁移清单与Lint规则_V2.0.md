# 程序员迁移清单与 Lint 规则 · V2.0

> **Status**: **EXECUTION** · 分支 `reframe/ip-v2-campus-ripple`  
> **脚本**: `scripts/audit_phase_package.py` · 待扩 V2 lint

---

## 1. 目录清单（须存在）

| 路径 | 用途 |
|------|------|
| `00_项目总览/IP重构执行包_20260607/00_README.md` | 包入口 |
| `00_项目总览/IP重构执行包_20260607/01_`…`11_*.md` | 方法正典 |
| `03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/00_V2迁移总览.md` | 卷迁移入口 |
| `03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/01_五案关系网/` | MVP 母纲 |
| `03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/02_资产对照表/` | V1→V2 映射 |
| `03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/03_Case_Cards/` | V2 Cards |
| `03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/04_分场脚本/` | Scene scripts |
| `03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/05_科学验证/` | Science checklist |

**勿删**: `03_故事内容/00_校园趣事观察社_单篇故事引擎_V1.0.md`

---

## 2. 权威源切换规则

| 资产 | V1 权威（基线 tag 前） | V2 权威（G4-10 后） |
|------|------------------------|---------------------|
| 创作引擎 | `单篇故事引擎_V1.0.md` | `02_单案故事引擎_V2.0.md` |
| A001 Case Card | `样章包/02_case_card_案01_*.md` | `V2迁移/03_Case_Cards/A001_V2_CaseCard.md` |
| A001 正文 CN | `正式版/01_正文/案01_*V1.2*.txt` | `正式版/01_正文/案01_*V2*.txt`（待写） |
| 正典门禁 引擎引用 | 指向 V1 | **追加** V2 supersede 注记（不删 V1 链） |

---

## 3. Lint 规则（V2-CARD）

```yaml
# 建议实现：scripts/lint_case_card_v2.py（待建）
rules:
  - id: V2-CARD-001
    check: required_fields_present
    fields: [pressure_primary, wrong_responsibility, true_responsibility, relation_type, global_seed_ids, kei_second_truth, scene_count_target]
  - id: V2-CARD-002
    check: fair_clues_min
    min: 3
  - id: V2-CARD-003
    check: scene_count_range
    min: 8
    max: 10
  - id: V2-CARD-004
    check: complexity_budget_enum
    values: [L, M, H]
  - id: V2-CARD-005
    check: relation_type_enum
    values: [causal, shared_source, puzzle_piece, mirror, misuse, info_pollution]
  - id: V2-CARD-006
    check: kei_second_truth_no_science_keywords
    blocklist: [湿度, 静电, 摩擦, 可擦, 结露, 胶带]
  - id: V2-ENGINE-001
    check: v1_engine_not_referenced_in_new_cards
    message: "新 Card 须引 engine V2.0"
```

---

## 4. story_database 同步（G4-10 后）

| 文件 | 动作 |
|------|------|
| `docs/story_database/00_story_asset_table.md` | A001 status → `V2_STRUCT` |
| `docs/volume_planning/volume_01_scorecard.yaml` | 增 `narrative_ip: v2` |

---

## 5. CI / 审计挂钩

| 现有 | V2 |
|------|-----|
| `audit_phase_package.py` | 增 `--v2-migration` 检查目录齐 |
| `canon_sweep_4-2.py` | HOLD · V2 正文前不扫 |
| Gate A E06 | V2 正文后 **重跑** |

---

## 6. 合并前 Checklist

- [ ] `reframe/ip-v2-campus-ripple` 上 Lint 全绿  
- [ ] IP Owner + 科学签核 commit 注记  
- [ ] `00_正典门禁` 增 V2 引擎 supersede 单行（非替换整节）  
- [ ] `baseline/v1-narrative-20260607` 不可 force 改  
- [ ] 无 V2 正文时不标 `PRODUCT-GATE`

---

最后更新：2026-06-07
