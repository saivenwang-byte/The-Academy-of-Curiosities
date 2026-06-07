# Case Card 与数据 Schema V2.0

> 状态：`MIGRATION_SPEC`  
> 对象：程序员、Agent开发、数据维护、主编

## 1. 目标

在现有Case Card基础上增加可机器校验的故事钩子、压力、责任、卷网、学科网、全球母题和复杂度字段；保留原字段兼容性。

## 2. 必填字段

```yaml
case_id: A001
title_cn: ""
title_jp: ""
hook_one_line: ""
hook_image_or_sound: ""
scene: ""
month_nagoya: ""

accused_or_affected_person: ""
stakes_lost_if_fail: ""
countdown_event: ""
countdown_social: ""
pressure_primary: ""
pressure_secondary: ""

science_core: ""
science_cross: ""
science_auxiliary: ""
social_amplifier: ""
mechanism_chain: []
fair_clues: []
misread: ""
main_red_herring: ""

wrong_responsibility: ""
true_responsibility: ""
character_secret: ""
repair_action: ""
human_truth: ""
kei_note_angle: ""

relation_type: []
volume_node: ""
volume_variables_in: []
volume_variables_out: []
volume_meta_question: ""
knowledge_reuse_type: []

source_seed_id: ""
source_grade: ""
localization_notes: ""
ethics_risk: ""

complexity_budget:
  main_mysteries: 1
  accused_persons: 1
  main_countdowns: 1
  primary_pressures: 1
  secondary_pressures: 1
  core_mechanisms: 1
  cross_mechanisms: 1
  auxiliary_mechanisms: 0
  fair_clues: 3
  red_herrings: 1
  character_secrets: 1
  responsibility_reversals: 1

gate:
  hook_pass: false
  pressure_pass: false
  fairplay_pass: false
  mechanism_pass: false
  emotion_pass: false
  responsibility_pass: false
  repair_pass: false
  volume_network_pass: false
```

## 3. 字段枚举建议

### `relation_type`

`causal | common_source | puzzle_piece | mirror | contrast | misapplication | carrier | information_pollution | pressure_field | role_exchange | echo | spatial | probabilistic`

### `pressure_primary / pressure_secondary`

`time | friendship | class_honor | study | responsibility | identity | expectation | rule | family | public_reputation`

### `source_grade`

`R1 | R2 | R3 | R4 | ORIGINAL`

### `knowledge_reuse_type`

`relay | corroboration | conflict | misapplication | convergence | none`

## 4. 自动校验规则

程序必须至少实现：

1. `fair_clues`数量3—4；
2. 主机制=1，交叉机制≤1，辅助机制≤1；
3. 主压力=1，副压力≤1；
4. `wrong_responsibility`与`true_responsibility`不得完全相同；
5. `repair_action`不得为空；
6. A线案件必须有`volume_node`；
7. 每卷跨案变量总数≤4；
8. 每卷关系类型3—5种；
9. A005必须存在`convergence`或多关系汇流；
10. R2/R3/R4禁止自动生成“真实事件改编”宣传语；
11. 若知识明确解释超过正文5%，标记WARN；
12. 若高压连续场景超过35%，标记WARN；
13. 陸瑆笔记若只复述机制，标记FAIL；
14. A005使用的新关键证据若前四案未登记，标记P0 FAIL。

## 5. 卷级数据结构

```yaml
volume_id: VOL1
volume_title: ""
meta_question: ""
pressure_field: ""
cases: [A001, A002, A003, A004, A005]
relation_edges: []
discipline_edges: []
volume_variables: []
character_role_exchange: []
a005_recovery_matrix: []
unresolved_variables: []
```

### `relation_edges`示例

```yaml
- from: A001
  to: A003
  type: mirror
  evidence: ""
  visible_to_child: true
```

## 6. 输出报告

程序应生成：

- 单案复杂度报告；
- 单案Gate报告；
- 五案关系边表；
- 学科网边表；
- 卷级变量进出表；
- A005回收缺口；
- 术语与知识解释密度报告；
- 伦理与来源风险报告。

## 7. 兼容策略

- 原Case Card字段不得删除；
- 新字段先设为可空并输出WARN；
- 完成A001迁移后，再转为强制；
- MIG-G4后更新主Schema与lint；
- 旧案数据必须保留`schema_version: 1.x`，新案使用`2.0`。
