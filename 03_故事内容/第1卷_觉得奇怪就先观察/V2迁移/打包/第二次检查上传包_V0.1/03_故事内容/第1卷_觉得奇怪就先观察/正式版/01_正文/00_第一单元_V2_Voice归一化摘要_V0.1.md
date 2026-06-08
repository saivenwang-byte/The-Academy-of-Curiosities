# 第一单元 V2 · Hybrid Voice 归一化摘要 · V0.1

> **日期**：2026-06-08  
> **范围**：A001–A005 · `HybridVoice_V2.0.txt`  
> **工具**：[`03_故事内容/tools/normalize_hybrid_voice_bold.py`](../../tools/normalize_hybrid_voice_bold.py)  
> **Skill**：`academy-voice-editor`（第三遍 · 机械间距清理 · 未改情节/LOCK）

---

## 1. 处理内容

| 项 | 说明 |
|----|------|
| **问题** | V1.1 扩写「续」段遗留 `**字** **字**` 逐字加粗与 CJK 间多余空格 |
| **处理** | 合并机械加粗 run · 清理标点旁空格 · 保留元数据/FC/已确认/EXPERT_LOCK 行 |
| **未改** | EXPERT_LOCK 机制 · 场号 SC-XX · FC 标注 · 瑆笔记 · P06 实验块 |

---

## 2. 逐案

| 案 | 脚本归一化行数* | 手工 | 汉字(CJK) | 状态行 |
|:--:|:--------------:|:----:|:---------:|--------|
| A001 | 23 | — | 3,354 | Hybrid Voice v3 · normalized |
| A002 | 71+ | — | 3,908 | 同上 |
| A003 | 56+ | — | 4,304 | 同上 |
| A004 | 50+ | 1 | 4,300 | 同上 |
| A005 | 83+ | — | 6,508 | 同上 |

\* 多轮累计（collapse + heavy-bold + spacing）

---

## 3. §7 自评（归一化后）

| ID | 项 | 评 |
|----|-----|:--:|
| 7.1 | 留白 | 续段可读性恢复 · 仍有多空行（扩写体例 · 可后删） |
| 7.2 | 句长 | 机械拆字已去 · 均句回到 Hybrid Voice |
| 7.3 | 陸珣声线 | 未增台词 |
| 7.4 | 金句 | 未删原有金句 |
| 7.5 | 回响 | 未动 |

---

## 4. 仍待（非本次）

- A005 卷末部分「归档」重复句段 · 属扩写厚度 · 可选人工删冗
- 读者群试读 · G-CN 勾选
- G-SHOT-T

---

## 5. 复跑命令

```bash
python 03_故事内容/tools/normalize_hybrid_voice_bold.py
```

仅处理指定案：

```bash
python 03_故事内容/tools/normalize_hybrid_voice_bold.py "路径/案02_….txt"
```

---

最后更新：2026-06-08
