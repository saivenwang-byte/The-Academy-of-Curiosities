---
editorial_verdict: PASS
editorial_date: 2026-06-11
translation_verdict: PASS
translation_date: 2026-06-05
return_to:
return_notes:
case: A001
updated: 2026-06-11
---

# A001 · G-BRIEF · 编+导提交 + 译部审核 · V1.0

> **单元审定**：[`00_导演组编辑组_分镜插画文字版审定_V1.0.md`](../../00_导演组编辑组_分镜插画文字版审定_V1.0.md)  
> **译部台账**：[`00_译部分镜审核_单元1_V1.0.md`](../../00_译部分镜审核_单元1_V1.0.md)  
> **绑定**：分镜文字 [`00_插画师分镜文字稿_V1.0.md`](./00_插画师分镜文字稿_V1.0.md) · G-CAST [`00_G-CAST_导演审定表_A001_V1.0.md`](./00_G-CAST_导演审定表_A001_V1.0.md)

## 裁决（机器可读 · 只 PASS / RETURN）

| 部门 | verdict | 日期 | 说明 |
|------|:-------:|------|------|
| 编+导 | **PASS** | 2026-06-11 | 36 P0 文字稿已齐 |
| 译部 | **PASS** | | 须 48h 内改为 PASS 或 RETURN |

**frontmatter 写法**：

```yaml
translation_verdict: PASS   # 或 RETURN
return_to: editorial        # RETURN 时
return_notes: "DA3 屏显日文须改"
```

- **PASS** → `workflow_preflight.py --mode produce` 放行该案出图  
- **RETURN** → exit 1 · 退回编+导 · 该案暂停  
- **pending** → exit 1 · `TRANSLATION_REVIEW_REQUIRED` · 退回译部出结论（不卡全线其他工位）

**试读 PDF** 另需 `--mode deliver`：M0-B + G-AB-JP + COUNT_PASS
