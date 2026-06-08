# Ralph Agent Instructions · Vol1 Unit1 MVP V2

> SSOT: `03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/33_RalphLoop_MVP_任务书_V0.1.md`
> Baseline: commit `f95da38` · doc 32 · ~78% MVP · **do NOT redo R5/CN/G1 PH work**

## Task

Push Vol1 Unit1 A001–A005 MVP from ~78% to machine-verified COMPLETE:
G-BODY scores · JP MoA-lite · editor-pollution clean · honest scores JSON.

## FROZEN → R17 UNFROZEN (IP 2026-06-08)

- **R17 ACTIVE** · M1′/M2′ merged · doc45 audit complete
- **Do NOT** run R18+ on A001 without new IP agenda
- E20 pilot continues · 0/12 slots · do not fake
- SSOT: `V2迁移/40_A001迭代冻结_E20门禁_V0.1.md` · `45_A001_R17_…`
- Prior anchor: `11cf625` (R16)

## Constraints

- Do **not** revert or re-run `_review_loop_r5_cn_body.py` / `_mvp_g1_placeholders.py` unless doc 33 says so
- Do **not** fake G-BODY metrics or claim G-IMG PRODUCT / science P0 human lab done
- Do **not** git push unless every 2 iterations or loop end
- Each iteration: read `progress.txt` + `git log -3` + doc 33

## Verification（每轮必跑）

```powershell
Set-Location "D:\【AI Project】\【The Academy of Curiosities】"
python "03_故事内容/tools/validate_mvp_v2_unit1.py"
```

## Iteration playbook

1. Run validator → note `weakest` dimension
2. **CN/G-BODY** → `_review_loop_r6+_cn_body.py` or targeted edits (academy-voice-editor)
3. **JP** → record MoA-lite in `V2迁移/mvp_jp_moa_lite.json` + fix weak case
4. **Scores** → update `V2迁移/scores_mvp_latest.json` via honest expert panel (doc 23)
5. **PDF** → `python …/05_出版成果/tools/build_mvp_v2_unit1.py` when bodies change
6. Expert panel (5 roles) → append to `progress.txt`
7. `git commit -m "ralph-mvp iter N: …"`

## Done（ALL required）

| # | Gate | Target |
|---|------|--------|
| 1 | validate_mvp_v2_unit1.py | exit 0 |
| 2 | CN 五案 | 卷专家≥9.0 · 读者≥8.5 · P0_jump≤8% |
| 3 | JP 五案 | MVP-JP FULL + MoA-lite per case |
| 4 | 插图 | ≥10 PNG · ≥2/案 in 03_插图/ |
| 5 | PDF/PPT | rebuilt · 00_MVP交付清单 v4+ |
| 6 | doc 33 | final % + honest G-LOCK gaps |

Output **only when validator exit 0**:

<promise>COMPLETE</promise>

## If stuck（≥20 iter or human-only blockers）

Write `tools/ralph-loop/workspace/BLOCKERS.md` · deliver best achievable MVP · output:

<promise>BLOCKED</promise>

Human-only: science P0 lab · real child trial · G-IMG production PNG · IP G-BODY sign.
