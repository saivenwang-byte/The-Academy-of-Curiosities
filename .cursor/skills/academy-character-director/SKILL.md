---
name: academy-character-director
version: 1.0.0
description: |
  学堂趣事录 · 角色灵魂与表演导演 V1.0。加载 soul.yaml + characters.yaml，
  执行对白/行为/功能抢位/同场景差异校验；对接 engine Phase 2b。不写案、不改正典。
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# academy-character-director · 角色灵魂与表演导演 · V1.0

> **STATUS: PRODUCTION** · Gate A 起强制前置（engine Phase 2b）  
> **审议**: [`专家组审议_Agent架构与角色灵魂_20260607.md`](../../00_项目总览/专家组审议_Agent架构与角色灵魂_20260607.md)  
> **SSoT**: `characters/soul/{id}_soul.yaml` → `characters.yaml` → `01_角色设定/*.txt`

---

## 身份边界

| 是 | 否 |
|----|-----|
| 加载 soul · 输出 **角色校验报告** / 差异测试表 | 设计案件 · 改 Case Card |
| 对白归属 · never_says · 功能抢位 · 站位 | 修改 LOCK 关系/年级 |
| 同场景五人差异测试（A001 等） | 替代 engine 写正文 |
| 为 voice / jp-voice / visual-auditor 注入角色约束 | persona Agent · 十人十 Skill |

**SUPERSEDES**: `academy-char-01` … `academy-char-10`

---

## 何时触发

- `academy-engine` **Phase 2b**（写正文前）
- 改 Vol 正文/日译/SC prompt/分镜且有 named 角色
- 「谁会怎么说」「五人可互换吗」「A001 差异测试」「灵魂偏移」

---

## 启动链

```powershell
python scripts/character_soul_lint.py --vol1-core
# 对每个出场 id：Read characters/soul/{id}_soul.yaml
# 交叉 Read skills/academy-character-scale/characters.yaml
```

**Lint FAIL** → 正文 Phase 3 最高 `DRAFT` · 报告列缺失模块。

---

## 工作流

### Step 1 · 出场表

从 Scene Card / 分镜解析 `character_ids[]`。Vol1 核心五人：

| id | 角色 | tier |
|----|------|------|
| ito_hikaru | 伊藤光 | vol1_core |
| kato_keimi | 加藤慧美 | vol1_core |
| matsumoto_shiro | 松本志郎 | vol1_core |
| riku_shun | 陸珣 | vol1_core |
| riku_hikaru | 陸瑆 | note_layer |

### Step 2 · 加载灵魂

- `characters/soul/{id}_soul.yaml`（LOCK 优先）
- 缺 soul → 仅 `characters.yaml` + txt，标 **SOUL_INCOMPLETE**

### Step 3 · 扫描（每场/每段）

| 检查 | 来源 |
|------|------|
| `forbidden_patterns` / `never_write` | soul + yaml constraints |
| `curiosity_first_move` 是否体现 | soul §05 |
| `thinking_bias` 是否可识别 | soul §06 |
| 功能抢位 | 瑆不抢社员推理 · 葛西不破案 · 中谷 Vol1 轻量 |
| 对白句长/语气 | `language_fingerprint` vs yaml voice |

### Step 4 · 同场景差异（验收）

引用 [`P0生产系统校准包/06_A001角色一致性回测报告_V1.0.md`](../../00_项目总览/P0生产系统校准包/06_A001角色一致性回测报告_V1.0.md) 五场景：

1. 第一次发现异常  
2. 第一次错误假设  
3. 团队分歧  
4. 验证实验  
5. 瑆笔记  

**PASS**：去名后仍可判断说话者。

### Step 5 · 输出报告

```markdown
# 角色导演报告 · {案/场次} · {date}
STATUS: {PASS|HOLD|DRAFT}

## 出场
- ids · soul 版本 · lint

## 偏移项（P0/P1）
| 行/场景 | 角色 | 问题 | 建议 |

## 差异测试（若适用）
| 场景 | 预期 first_move | 正文是否符合 |

## 下游
- voice-editor: …
- visual-auditor: 站位/道具 …
```

---

## 与 Skill 关系

```
academy-engine Phase 2b     → 本 skill（强制）
academy-voice-editor        → 继承 forbidden + 句长
academy-jp-voice-editor     → 继承 register · あきら/ひかる
academy-visual-auditor      → behavior_fingerprint · key_props
academy-character-scale     → never_says 机器 schema
```

---

## V1.0 交付

- [x] PRODUCTION（非 STUB）
- [x] Vol1 五人 soul LOCK · KarfWang IP
- [x] `character_soul_lint.py` strict + cross-yaml
- [x] engine Phase 2b 挂钩
- [ ] Vol2+ soul 扩展（Gate B 后）

---

| 版本 | 2026-06-08 · V1.0 · STUB→PRODUCTION |
