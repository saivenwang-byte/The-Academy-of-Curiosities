# A005 · G1 Prompts · MVP · R2 · V0.2

> **Status**: **Gate 2 refresh · R2 spec-aligned** · 2026-06-08  
> **SSOT**: [`分镜拆解/A005_分镜拆解_R17_V0.1.md`](../分镜拆解/A005_分镜拆解_R17_V0.1.md)  
> **空间**: **体育馆 brief** · doc16 §2 · 穹顶 · 投屏白墙 · 侧门器材车 · 灯杆长影  
> **EXPERT_LOCK**: **仅水野** 脚下无影 · 车/灯杆 **有影** · 重拍 **五影全在**  
> **输出命名**: `V-S05-V2-A*_G1draft_c02.png`

---

## Global STYLE / NEGATIVE / L0

同 A001 · Plan B 五人正典名：**陸珣 · 伊藤光 · 加藤慧美 · 松本志郎 · 水野真帆**  
**禁**：山本/佐藤/田中 错名 · 五人全无影 · 橡皮屑 · 运动鞋

---

## DA1 · 投屏无影 · SC-01 · P0 · EXPERT_LOCK ⚠️

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S05-V2-A1 / DA1** |
| 镜头功能 | **S+L** |
| 景别 | **MS** |
| 机位 | 体育馆投屏平视 |
| 视觉中心 | 五人合照投屏 · **仅水野脚边无影** |
| 第二信息 | 器材车/灯杆 **长影仍在** · 四人影正常 |
| 人物 | 珣·光·慧美·志郎·水野 · L0 私服 · **上履き** |
| 场景 | 体育馆预展 · doc16 brief · 四月 |
| 禁项 | 五人全无影 · 错 cast 名 · chibi · 制服 · 运动鞋 |
| 正文锚点 | 「合照里——只有她的影子不见了。」 |
| G-BODY锚 | EXPERT_LOCK·Plan B五人·A004承接 |

### 合成 Prompt（G1 · c02）

```
[STYLE] MS gymnasium projection screen group photo five students shoulder to shoulder uwabaki white indoor shoes,
ONLY Mizuno Maho shadow missing under her feet other four shadows normal on floor,
equipment cart and light pole long shadows still visible on gym floor,
Riku Shun blue hoodie Ito Akira orange vest white tee Keimi yellow cardigan silver glasses
Shiro green plaid green vest round glasses Mizuno slim shoulders casual clothes,
Nagoya elementary gymnasium April overhead light pre-exhibition screen,
fair-play panorama stitch clue NOT curse NOT all five shadowless,
NOT seifuku NOT sneakers NOT wrong names NOT chibi bridge-book watercolor #2A1810
[NEGATIVE]
```

**Output**: `V-S05-V2-A1_仅水野无影_G1draft_c02.png`

---

## DA3 · 拍摄信息三帧 · SC-05 · P0

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S05-V2-A3 / DA3** |
| 镜头功能 | **L+C** |
| 景别 | **MCU** |
| 机位 | 平板 POV 框中框 |
| 视觉中心 | **分段曝光三帧** · 水野侧让帧高亮 |
| 第二信息 | 时间戳 10:52:03/05/07 可读 |
| 正文锚点 | 「十四秒拼成一张——她侧让的那一帧，没有影。」 |
| 禁项 | 五人全无影 · 诅咒 · metadata 术语入叙事 |

### 合成 Prompt（G1 · c02）

```
[STYLE] MCU tablet POV frame-in-frame three exposure segments timeline readable,
Mizuno side-step frame highlighted timestamp 10:52:03 10:52:05 10:52:07,
gymnasium projection soft background Riku Shun blue hoodie studying NOT curse,
Keimi yellow cardigan notebook edge silver glasses Shiro green vest edge,
fair-play panorama stitch clue casual clothes NOT seifuku bridge-book watercolor
[NEGATIVE] all five shadowless horror curse rubber eraser crumbs villain lighting
```

**Output**: `V-S05-V2-A3_metadata三帧_G1draft_c02.png`

---

## DA6 · 重拍有影 · SC-08 · P0 · EXPERT_LOCK ⚠️

### §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **V-S05-V2-A6 / DA6** |
| 镜头功能 | **L+P** |
| 景别 | **MS** |
| 机位 | 重拍区 · **单次快门** moment |
| 视觉中心 | **五影全在** · 水野影回来 |
| 第二信息 | 相机可见 · 与 DA1 投屏 inset 对照可选 |
| 禁项 | 五人全无影 · 检修场景 · 运动鞋 · 英文 UI 块 |
| 正文锚点 | 「单次快门——五个影子，都在。」 |
| G-BODY锚 | EXPERT_LOCK验证帧·L0五人私服上履き |

### 合成 Prompt（G1 · c02）

```
[STYLE] MS gymnasium reshoot five students queue single shutter moment ALL five shadows
on floor including Mizuno Maho shadow returned clearly visible,
camera on tripod visible bright overhead gymnasium light,
Riku Shun blue hoodie Ito Akira orange vest Keimi yellow cardigan silver glasses
Shiro green plaid green vest Mizuno casual clothes all uwabaki white indoor shoes,
contrast optional small projection screen inset showing previous missing shadow,
repair fair-play NOT supernatural NOT seifuku NOT sneakers NOT maintenance scene
Nagoya elementary gymnasium April bridge-book watercolor #2A1810
[NEGATIVE] five shadowless horror English text blocks outdoor shoes
```

**Output**: `V-S05-V2-A6_重拍有影_G1draft_c02.png`

---

*A005 G1 prompts R2 · V0.2 · 体育馆 brief · EXPERT_LOCK*
