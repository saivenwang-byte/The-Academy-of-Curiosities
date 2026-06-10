---
name: academy-vol1-auto-pipeline
version: 1.0.0
description: >-
  Vol1 单元1 全自动阶段累进流水线：DESK → KIDS → 打分 → V3.6 → 分镜 → 绑图 → 试读 PDF。
  须 `.cursor/authorization/vol1_full_auto.json` 授权。用户说全自动、批量阶段、累进优化、试读 PDF 时触发。
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Shell
---

# Vol1 Unit1 · 全自动阶段累进流水线

## 一键执行

```bash
cd "03_故事内容/第1卷_觉得奇怪就先观察"
python tools/vol1_auto_pipeline/run.py --auto --full-auth
```

断点续跑：

```bash
python tools/vol1_auto_pipeline/run.py --auto --full-auth --from shot_maps
python tools/vol1_auto_pipeline/run.py --list
```

## 阶段（累进叠加）

| # | Phase | 产出 |
|---|-------|------|
| 1 | desk | V3.4 + TANAKA-DESK 报告 |
| 2 | kids | V3.5 + KIDS-SIMPLIFY 报告 |
| 3 | score | scores_v35_jp.json |
| 4 | v36_body | V3.6 正文文件夹 |
| 5 | shot_maps | `setup_unit1_v36_pipeline.py` → 分镜+prompt |
| 6 | bind_illustrations | （同上，一并执行） |
| 7 | build_pdf | `build_unit1_trial_pdf.py` |

## 授权

- 文件：`.cursor/authorization/vol1_full_auto.json`
- **不替代**：真人田中 G-JP LOCK · E20 真人试读 · PRODUCT-GATE 精修图

## SSOT

- `V2迁移/89_单元1全自动阶段累进工作流_V0.1.md`
- `tools/vol1_auto_pipeline/manifest.yaml`
- `tools/vol1_auto_pipeline/pipeline_state.json`（运行状态）

## 关联 Skill

- `academy-illustration-pipeline` — Phase 5–10 规范
- `academy-jp-tanaka-desk` — Phase desk
- `academy-jp-voice-editor` — JP 上游
