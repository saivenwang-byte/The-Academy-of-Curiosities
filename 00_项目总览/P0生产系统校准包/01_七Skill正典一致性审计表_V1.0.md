# 现有七 Skill 正典一致性审计表 · V1.0

> **Status**: LOCK · Gate A 校准包 · 2026-06-07  
> **基线**: `00_正典门禁` · `篇幅与单位构架_V1.1` · `00_十人名称_LOCK_2026-06-07` · Plan B Vol1  
> **执行记录**: P0-1 已完成（commit `5a35bd0`）· 本表为正式验收形态

---

## 审计维度（10 项）

| # | 检查项 | 正典答案 |
|---|--------|----------|
| D1 | 目标年龄 | **10–12 岁主读者** · 兼容四年级 |
| D2 | Vol1 结构 | **5 案** · 《觉得奇怪，就先观察》 |
| D3 | 年级班级 | 珣·光 **5年2組** · 瑆 **4年2組** · 慧美 5-1 · 志郎 5-3 |
| D4 | 入社 | **Vol1 A005** · 非 Vol3 |
| D5 | 理紗 / 中谷 Vol1 | **隐藏 / 轻量** · 非主帧 |
| D6 | 瑆 | **笔记层 · 非社员** |
| D7 | 200 案 / 卷 | **200 案 ≈ 40 卷资产** · **A 线 20×5** |
| D8 | 湿椅子 | **素材库** · 非 Vol1 正典 |
| D9 | 输入/输出路径 | Plan B 卷路径 · Reader 20260607 |
| D10 | 职责重叠 | 见 §三 |

---

## §一、逐项裁决

| Skill | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | **状态** | 处置 |
|-------|----|----|----|----|----|----|----|----|----|-----|----------|------|
| academy-series-architect | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 🟡 | **UPDATE→KEEP** | 已同步 2026-06-07 |
| academy-engine | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **KEEP** | — |
| academy-research-editor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **KEEP** | — |
| academy-voice-editor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **KEEP** | — |
| academy-jp-voice-editor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **UPDATE→KEEP** | frontmatter 已修 |
| academy-visual-auditor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 🟡 | **UPDATE→KEEP** | Plan B 机制已对齐 |
| academy-story-database | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **KEEP** | — |
| academy-char-01…10 | ❌ | — | — | — | — | — | — | — | — | 🔴 | **DEPRECATE** | → character-director + soul |
| academy-character-director | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | ✅ | — | **KEEP** | 五人 soul LOCK · engine Phase 2b |
| academy-canon-governor | — | — | — | — | — | — | — | — | ✅ | — | **KEEP** | 首跑 2026-06-08 |
| academy-gate-orchestrator | — | — | — | — | — | — | — | — | ✅ | — | **KEEP** | 任务书 · Gate A 汇总 |
| ACE-B Officer | — | — | — | — | — | — | — | — | ✅ | — | **UPDATE** | 并行轨 · 非替代七 Skill |

**图例**：✅ 已对齐 · 🟡 部分 · ❌ 冲突 · — 不适用

---

## §二、不应重复写入 Skill 的规则（应移入正典单点）

| 规则 | 唯一正典源 | Skill 只引用 |
|------|------------|--------------|
| 读者年龄 / 篇幅 | `篇幅与单位构架_V1.1` | 链接，不复制数字 |
| 年级班级 | `00_年级班级关系表_V1.0` | 链接 |
| 十人读音 | `00_十人名称_LOCK_2026-06-07` | 链接 |
| Vol1 卷名/五案 | `00_正典门禁` | 链接 |
| 角色 never_says | `characters.yaml` + `soul/*.yaml` | character-director 调用 |
| E22 版面 | `E22_书籍形态…LOCK` | visual-auditor 链接 |
| Gate 阶段 | `00_项目现状板` | gate-orchestrator 调用 |

---

## §三、职责边界（重叠风险）

| 重叠对 | 裁决 |
|--------|------|
| engine ↔ voice-editor | engine 结构/科学 · voice 文学节拍 · **不交叉改案卡** |
| jp-voice-editor ↔ E04 | Skill 预审 · E04/蒸馏官 **签核** |
| visual-auditor ↔ E06 | Skill 规范检查 · 画师/总监 **交付** |
| series-architect ↔ engine | architect 卷/阶段 · engine **单案** |
| character-director ↔ characters.yaml | yaml=约束 · soul=灵魂 · director=表演校验 |

**SPLIT 建议（Gate B 后）**：无立即拆分；**gate-orchestrator** 新建以解四栏汇总，不从七 Skill 拆出。

---

## §四、验收

- [x] 七 Skill stale grep 清零（C01/C02）
- [x] char-* DEPRECATE 横幅
- [x] character-director 绑定五人 soul **PASS**（IP LOCK 2026-06-08）
- [x] canon-governor Skill **任务书 + 首跑**（[`canon-governor_首跑报告_20260608.md`](./canon-governor_首跑报告_20260608.md)）
- [x] engine Phase **2b** 挂钩 character-director

关联：[`Skill正典审计报告_20260607.md`](../Skill正典审计报告_20260607.md)
