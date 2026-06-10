# A001 · STYLE DEMO · DA2 · 审计 · V1.0

> **对照图**：[`A001_STYLE_DEMO_DA2_对照_LOCK左_DEMO右_v1.0.png`](./A001_STYLE_DEMO_DA2_对照_LOCK左_DEMO右_v1.0.png)  
> **DEMO 单张**：[`A001_STYLE_DEMO_DA2_v1.0.png`](./A001_STYLE_DEMO_DA2_v1.0.png)

---

## IP 签字（请对照左图 LOCK）

| 项 | v1.0 | 说明 |
|----|:----:|------|
| 媒介像马克笔平涂 | ✅ | **IP 2026-06-10 签画风 PASS** |
| 线稿 #2A1810 干净 | △ | 偏软棕水彩线 · 非 L0 硬边马克 |
| 四人脸与 L0 槽位 | △ | 慧美/志郎/光/珣 在 · 脸不完全同 slot |
| 志郎 矮壮+圆镜+绿格+橄榄 vest | △ | vest 有 · 脸/体型待对齐 |
| 教室无成人 | ✅ | |
| 无英文中文 | ✅ | 白板日文 OK |
| **G-CAST 人头 ≤6** | ❌ | **~8 全设计角色** · 含 seifuku 女生等 L0 式多样填充 |
| 同学为匿名背景 | ❌ | 4 个额外角色像准主角 · 非 5-2 匿名群众 |

**裁决**：**画风 IP 可签 PASS** · **G-CAST FAIL** · **整帧 REJECT 须 v1.1 重出** · 7 P0 **继续冻结**

---

## 为何 prompt 对了仍像水彩

Cursor `GenerateImage` 对「儿童绘本 + 日本小学」有 **默认 painterly 偏置**；旧 REF04 训练痕迹 + 无真正 ControlNet 锁画风 → 垫 Style B 仍漂。

**下一步（选一）**：
1. v1.1：prompt 首句 `EXACT same art medium as reference image 1 marker pen only` + 提高垫图权重（若 API 支持）
2. 外部：ComfyUI / SD + Style B L0 作 IP-Adapter（见 `Cursor生图401_说明与替代方案.md`）
3. 人类画师按 LOCK 手绘 DA2 → 作新 DEMO 母图

---

最后更新：2026-06-10
