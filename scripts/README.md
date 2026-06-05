# scripts/

## 一键

```bash
python scripts/pre_push_check.py
```

## 分卷 / 正文

```bash
python scripts/volume_lint.py --all
python scripts/body_lint.py --vol 2
```

| 脚本 | 用途 |
|------|------|
| `case_card_lint.py` | Case / 故事表 / Vol1 图 |
| `scene_card_lint.py` | Scene Cards |
| `volume_lint.py` | 按卷统一 lint + body |
| `body_lint.py` | 完整文字稿禁直译/结构 |
| `pre_push_check.py` | 推送前全套 |
| `import_reference_library.py` | 09_ 盘点 |
| `archive_vol1_duplicate_pngs.py` | PNG 归档 |
| `run_tanaka_calibration.py` | 田中 HTML · CALIBRATION_DB 五维批量扫描 |
| `canon_sweep_4-2.py` | 4年2組 漂移扫描 → `docs/canon_remap/4年2組_漂移扫描清单.md` |
| `audit_phase_package.py` | 阶段交付包门禁 · P0–P3（薄样张/正式版等） |
| `build_ledger_v02.py` | 200 篇故事资产台账 v0.2 生成 |
| `build_ledger_v03.py` | 200 篇故事资产台账 v0.3 生成 |

**田中 HTML**：`japan_campus_consultant_agent.html`（v1.2 · 五维默认全开）

**CI**：`.github/workflows/planning-lint.yml`
