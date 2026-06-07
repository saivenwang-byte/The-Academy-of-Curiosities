# 読者百景 · 数字读者实验室 · Phase 1

> **Status**: **SIMULATION · internal method validation**  
> **Truth**: 合成 Persona · **非真实儿童数据** · **非市场调查**  
> **Phase 1**: **50 人**（12 锚点 + 38 配额生成）· 试读材料 **序+A001 GateA**

---

## 入口

| 文件 | 用途 |
|------|------|
| [`読者百景_Phase1_入口_20260614.md`](./読者百景_Phase1_入口_20260614.md) | 正典入口 · 规格 · 与 E20 关系 |
| [`config/quota_phase1.yaml`](./config/quota_phase1.yaml) | 三面板配额 |
| [`config/eval_dimensions.yaml`](./config/eval_dimensions.yaml) | 维度资格矩阵 · N/A 规则 |
| [`data/anchors_12.json`](./data/anchors_12.json) | 固定锚点读者 |
| [`tools/run_phase1.py`](./tools/run_phase1.py) | 一键 Phase 1（dry-run / live） |

---

## 快速运行

```bash
# 仅生成 50 人格（无 API）
python tools/run_phase1.py --step personas

# 完整 dry-run（人格 + 模拟评价 + 健康度 + 报告）
python tools/run_phase1.py --dry-run

# 需 OPENAI_API_KEY · 结构化 live 评价
python tools/run_phase1.py --live --concurrency 4
```

---

## 五层架构

```
L1 evidence/     公开阅读信号（手工录入 · 非爬虫）
L2 persona/      锚点 12 + 生成 38
L3 eval_worker/  六任务包 · JSON Schema
L4 stats/        聚类 · 分歧 · 面板健康 · 真人校准 hook
L5 report/       四类分报告 · 页码级 P0/P1
```

---

## 与 E20 关系

| 来源 | 用途 |
|------|------|
| **本系统合成 50** | 内审 · 改稿优先级 · 方法验证 |
| [`E20_虚拟读者100`](../E20_虚拟读者/) | 历史 KPI 压测（保留） |
| [`E20_真实读者招募槽位`](../E20_真实读者招募槽位_20260613.md) | **校准真源** · 对外证据 |

**禁止** 将合成输出填入真实槽位表。

---

## 治理

- 符合 [`IP拍板记录_治理冻结令`](../../../../00_项目总览/IP拍板记录_治理冻结令与对外定位_20260612.md) **E20 数据白名单**
- **禁止** persona Agent · 与 ACE 路线一致
- 所有输出文件头标注 **SIMULATION**

| 版本 | 2026-06-14 · Phase 1 · seed=20260614 |
