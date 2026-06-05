# Cursor 生图 401 · 说明与替代方案

> **现象**: `Image generation failed` · `Request failed with status code 401`  
> **结论**: **无法在项目仓库内修复** · 属 Cursor 平台 **Unauthorized（未授权）**  
> **更新 2026-06-04**: 部分会话中 `GenerateImage` **可能间歇成功** — 仍 **不可** 作为 L0 定稿依赖  
> **本次实测（2026-06-04）**: SC-L0-001 / SC-L0-DEMO-002 **均生成成功** · 见 [`prompts_L0_探索_v1.md`](./prompts_L0_探索_v1.md) · 输出 `CHAR_lineup_L0_AI探索_v0.png` · `CHAR_lineup_L0_Demo窗邊_AI探索_v0.png` · 审计 **REVISE**（探索可用 · 非定稿）

---

## 1. 原因（常见）

| 可能 | 处理 |
|------|------|
| Cursor 订阅未含图像生成 | Settings → Account / Subscription 确认套餐 |
| 图像功能未开启 | Cursor Settings → Features / Beta → Image generation |
| 会话鉴权过期 | 完全退出 Cursor · 重新登录 |
| 区域/网络限制 | 换网络 · 关闭 VPN 或换节点 · 联系 Cursor Support |
| API 配额/临时故障 | 稍后重试 · 查看 [status.cursor.com](https://status.cursor.com) |

**本项目不等待 401 修复** · 画师管线以 **文字说明书 + 人工绘制** 为准。

### 1.1 为何仓库里「修不了」

401 发生在 Cursor **客户端 → Cursor 云端生图 API** 的鉴权层，与仓库代码、Python 脚本、Git 无关。  
本地脚本 `compose_l0_illustrator_pack.py` 只做 **PNG 合成**，不调用生图 API。

---

## 2. 替代交付（已就绪）

| 优先级 | 文件 | 用途 |
|--------|------|------|
| **P0** | [`05_视觉设定/00_插画师视觉创作说明书_V1.0.md`](../../05_视觉设定/00_插画师视觉创作说明书_V1.0.md) | IP 视觉正典 |
| **P0** | [`05_视觉设定/02_插画创作规范手册_V1.0.md`](../../05_视觉设定/02_插画创作规范手册_V1.0.md) | 技法/场景/光影 |
| **P0** | [`CHAR_lineup_L0_专家共识_画师文字创作说明书.md`](./CHAR_lineup_L0_专家共识_画师文字创作说明书.md) | L0 执行依据 |
| P0 | [`CHAR_lineup_L0_专家共识_画师brief.md`](./CHAR_lineup_L0_专家共识_画师brief.md) | 硬规格摘要 |
| P0 | [`prompts_L0_探索_v1.md`](./prompts_L0_探索_v1.md) | **AI 探索 SC prompt**（SC-L0-001 / DEMO-002） |
| P1 | `CHAR_lineup_L0_AI探索_v0.png` | SC-L0-001 探索成图 · **非定稿** |
| P1 | `CHAR_lineup_L0_Demo窗邊_AI探索_v0.png` | SC-L0-DEMO-002 探索成图 · **非定稿** |
| P1 | `CHAR_lineup_L0_专家共识_画师参照.png` | 纯布局锁定 |

---

## 3. 本地再生 PNG（非 AI）

```powershell
# 全人物发包（春装底 + 共识举牌）
python 07_设计原档/04_样章视觉/tools/compose_l0_illustrator_pack.py

# 纯布局线框
python 07_设计原档/04_样章视觉/tools/gen_char_lineup_l0_consensus.py
```

---

## 4. 给插画师的一句话

> 请按《插画师视觉创作说明书 V1.0》+《插画创作规范手册》+《L0 画师文字创作说明书》绘制定稿；发包 PNG 只看站位和身高，不抄旧脸；成稿回传 PSD+PNG。

---

## 5. 若你必须用 AI 辅助（非项目官方路径）

| 方式 | 说明 |
|------|------|
| 外部工具 | Midjourney / SD / 其他 · **禁** 垫知名 IP · 输出仍须人工精修过 GATE |
| Cursor 重试 | 更新 Cursor · 重新登录 · 确认订阅含 Image · **401 消失时可做草图探索，不可替代定稿** |
| 人工画师 | **推荐** · 见 [`01_画师发包清单.md`](../../05_视觉设定/01_画师发包清单.md) |

---

最后更新：2026-06-04
