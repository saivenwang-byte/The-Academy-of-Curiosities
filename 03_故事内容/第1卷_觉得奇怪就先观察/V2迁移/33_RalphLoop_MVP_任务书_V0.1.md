# Ralph Loop · MVP 任务书 · Vol1 Unit1 · V0.1

> **SSOT**：本文件 + `tools/ralph-loop/workspace/prompt.md` + `progress.txt`  
> **基线**：commit `f95da38` · doc 32 · 综合 **~78%**  
> **机器门**：`03_故事内容/tools/validate_mvp_v2_unit1.py` exit 0  
> **最后更新**：2026-06-08 · Ralph bootstrap

---

## 0. 范围

| 在环 | 不在环 |
|------|--------|
| CN G-BODY R6+ 抛光 · FC 标签清理 | 重做 R5（f95da38 已落地） |
| JP MoA-lite 四视角记录 | G-JP LOCK · J10 田中签 |
| scores_mvp_latest.json 诚实模拟分 | 伪造 ≥9.0 专家分 |
| PDF/PPT 随正文重建 | E06 PASS · 印厂母版 |
| doc 33 终态 % 更新 | 科学 P0 人类 lab 宣称完成 |

---

## 1. MVP DONE 门槛（ALL）

| # | 检查项 | 目标 |
|---|--------|------|
| 1 | `validate_mvp_v2_unit1.py` | exit 0 |
| 2 | CN 五案 | 卷专家 **≥9.0** · 卷读者 **≥8.5** · P0_jump **≤8%** |
| 3 | JP 五案 | MVP-JP FULL + `mvp_jp_moa_lite.json` 每案 recorded |
| 4 | 插图 | ≥10 PNG · `03_插图/案0X/` 每案 ≥2 |
| 5 | 交付 | PDF×2 + PPT · `00_MVP交付清单.md` v4+ |
| 6 | 文档 | 本文件终态 % + G-LOCK 诚实缺口 |

---

## 2. 基线缺口（f95da38）

| 维度 | 当前 | 目标 | 动作 |
|------|------|------|------|
| G-BODY 专家 | 8.7 | ≥9.0 | R6+ CN · FC 清理 · A004 扩写 |
| G-BODY 读者 | 8.1 | ≥8.5 | 跳读段 trim · 案③节奏 |
| P0 跳读 | ~8% | ≤8% | ✅ 边界 · 维持 |
| A004 字数 | 2661 | ≥3000 | 恢复 R4 误删叙事 |
| FC 标签 | 3 处 | 0 | R6 strip → 叙事句 |
| scores JSON | 无 | 有 | 每轮专家板更新 |
| JP MoA | 无 | 5 案 | `mvp_jp_moa_lite.json` |

---

## 3. 每轮迭代协议

1. 读 `progress.txt` · `git log -3` · 本文件  
2. `python 03_故事内容/tools/validate_mvp_v2_unit1.py`  
3. 按 `weakest` 维度选动作（见 prompt.md）  
4. 五席专家板 → 写 progress + scores  
5. `git commit -m "ralph-mvp iter N: …"`  
6. 每 2 轮 `git push`

---

## 4. 路径

| 类型 | 路径 |
|------|------|
| Validator | `03_故事内容/tools/validate_mvp_v2_unit1.py` |
| Scores | `V2迁移/scores_mvp_latest.json` |
| JP MoA | `V2迁移/mvp_jp_moa_lite.json` |
| R6+ CN | `03_故事内容/tools/_review_loop_r6_cn_body.py` |
| Build | `正式版/05_出版成果/tools/build_mvp_v2_unit1.py` |
| MVP 包 | `正式版/05_出版成果/MVP_V2_20260608/` |

---

## 5. 完成度追踪（迭代中更新）

| 维度 | 基线 f95da38 | **Ralph 终态** | 目标 |
|------|:------------:|:--------------:|:----:|
| CN G-BODY | ~97% | **~98%** | R6–R9 · FC clean · A004 3486字 |
| JP | ~88% | **~90%** | MoA-lite 5/5 recorded |
| 插图 | ~48% | **~48%** | bundle 32 PNG · PH 未换 production |
| PDF/PPT | ~82% | **~84%** | rebuild iter 4 |
| **综合** | **~78%** | **~86%** | validator **BLOCKED** expert 8.9<9.0 |

**Ralph 结果**：8 iterations (0–7) · `<promise>BLOCKED</promise>` · see `tools/ralph-loop/workspace/BLOCKERS.md`

---

## 6. G-LOCK 诚实缺口（不可 Ralph 消除）

1. **科学 P0 人类 lab**（A001 波形 · A002 膜 · A005 全景）  
2. **G-BODY IP 签**  
3. **G-IMG PRODUCT**（PH ≠ production · 无 E06-S auditor PASS）

若 20 轮后仍因上列 human-only 项导致 expert <9.0 → `<promise>BLOCKED</promise>`

---

*Ralph Loop SSOT · 2026-06-08*
