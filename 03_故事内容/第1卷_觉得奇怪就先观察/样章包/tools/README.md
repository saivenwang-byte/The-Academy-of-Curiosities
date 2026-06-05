# 样章包 tools

| 脚本 | 用途 |
|------|------|
| `build_sample_reading_pdf.py` | 汇编 HybridVoice + 插页 → HTML/PDF（A5 · Edge headless） |

| `gen_v_s01_tail_placeholder.py` | 生成 `插图/V-S01-TAIL_壁报草稿空栏.png` 试读占位（可换 SC 成图） |

```bash
python build_sample_reading_pdf.py
# → PDF/学堂趣事录_Vol1_样章试读_YYYYMMDD.pdf
```

依赖：Pillow
