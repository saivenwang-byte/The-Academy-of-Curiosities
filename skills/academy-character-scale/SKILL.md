---
name: academy-character-scale
version: 1.0.0
description: 学堂趣事录角色约束系统。在创作或校验任何故事内容时，加载角色蒸馏卡作为言行校验器。每个角色由不可变锚点+约束边界+光谱坐标定义。违反约束 = 红线级错误。
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
---
# 角色蒸馏系统 · Character Scale System

## 架构

```
characters.yaml    ← 唯一真相源（Single Source of Truth）
     ↓
  加载到创作上下文 → 每句对话/每个动作校验
     ↓
  违反 constraint？→ 标记 + 建议替换
```

## 触发规则

- 写任何一卷故事正文时 → 必须加载
- 修改角色档案时 → 必须对照 YAML 检查 consistency
- 校验已写好的故事 → 扫描全部对话和动作，报告违规
- 设计新角色时 → 参照现有角色的 spectrum 定位，检查功能重叠

## 每个角色的约束模型

```yaml
角色ID:
  identity:          # 不可变标识
  anchors:           # 不可变锚点（声音/动作/视觉）
  constraints:       # 约束边界（绝不说/绝不做）
    never_says: []   # 说出这些→直接违规
    never_does: []   # 做出这些→直接违规
  spectrum:           # 光谱坐标（0.0-1.0）
    extroversion:     # 外向度
    action_bias:      # 行动倾向
    focus_depth:      # 专注深度
    social_warmth:    # 社交温度
  voice:
    tempo:            # 语速
    register:         # 声调
    sentence_length:  # 句子长度
    filler:           # 惯用语气词
    catchphrase:      # 口头禅
  triggers:           # 例外条件（什么会打破他平时的 pattern）
  relations:          # 关系参数（对每个队友的不同模式）
```

## 校验工作流

### Step 1：加载 YAML
读 `skills/academy-character-scale/characters.yaml`

### Step 2：逐角色扫描
对故事中出场的每个角色：
1. 检查所有对话 → 是否违反 `never_says`
2. 检查所有动作 → 是否违反 `never_does`
3. 检查对话风格 → 是否匹配 `voice`
4. 检查与其他角色互动 → 是否匹配 `relations`

### Step 3：输出校验报告
```
[角色名] detected:
  ✓ 对话 12 句，全部通过 voice 检查
  ⚠ 第7句 "你太厉害了！" 接近 never_says 边界（建议改为 "すごい"）
  ✗ 第15句 使用了感叹号，违反 sentence_length
```

## 输出格式

校验完成后输出报告，格式：

```
【角色校验报告 · 第X卷】

伊藤光：
  ✓ 对话 18 句，无违规
  ✓ 动作 5 处，符合标志动作
  - 无警告

加藤慧美：
  ✓ 对话 14 句，无违规
  ⚠ 第3句过长（建议拆短）

[汇总]
✓ 通过：6/8 角色
⚠ 警告：2/8 角色
✗ 违规：0/8 角色
```
