---
name: illustration-nano-banana
description: >
  How to actually generate canonical illustrations for 《学堂趣事录 / The Academy of
  Curiosities》 using Nano Banana (Google Gemini 2.5 Flash Image) or a compatible
  text-to-image / image-editing tool. Use this skill whenever the user wants to
  generate, produce, render, or create images, character art, picture-book pages,
  covers, or promotional visuals — and whenever they mention Nano Banana, Gemini
  image, Imagen, Midjourney, or "出图/生成图片/插图". It covers the master-reference-first
  consistency workflow, how to structure prompts for Nano Banana specifically,
  aspect ratios, batching, iterative editing, and the QA hand-off. Always pair this
  with the visual-style-bible skill (the look) and the prompt pack (the wording).
---

# Nano Banana 出图工作流 · The Academy of Curiosities

This skill assumes an image tool is connected in the runtime (e.g. a Gemini-image
MCP server, the Google AI Studio / Gemini app, Cursor's image tooling, or any
text-to-image + image-edit endpoint). If **no image tool is available in the current
session**, do NOT pretend to generate. Instead: produce the finished prompts (from
the prompt pack), tell the user exactly which tool to paste them into, and stop.

Always read `visual-style-bible` first — it defines the look and the locked character
anchors. This skill defines the *process*.

---

## 0. 为什么用 Nano Banana

Nano Banana = Gemini 2.5 Flash Image。本项目选它的理由：
- **角色一致性强**：能以一张参考图为锚，在新场景里保持同一个角色的长相。
- **对话式编辑**：可以"保留这个角色，只改背景/动作/光线"地迭代。
- **多图融合**：可把"角色参考图 + 场景参考图"合成一张。
- **强自然语言遵循**：吃"像跟人描述画面"那样的整段描述，而不是关键词堆。

## 1. 黄金法则：主参考图优先（master-reference-first）

绝不要每次从零生成同一个角色——长相会漂移。流程恒为两步：

**第一步 · 锁主参考图（每个角色一次）**
1. 用 `NANO_BANANA_PROMPT_PACK.md` 里该角色的"主参考图提示词"生成。
2. 一次出 3–4 张，挑最符合 `visual-style-bible` 锚点的一张。
3. 命名归档（见 §5），标注 `LOCKED`。这张就是该角色之后所有图的"长相基准"。
4. 八个主要角色都各锁一张后，再进入场景生成。

**第二步 · 用参考图生成场景**
- 生成任何含人物的场景时，**把相关角色的主参考图作为输入参考喂给 Nano Banana**，并在提示词里明确：
  > 使用所提供参考图中的这些确切角色（同一长相、发型、专属道具），把他们放进下面的场景：……
- 多角色场景：同时提供多张主参考图（多图融合），并点名谁是谁。
- 即便给了参考图，提示词里**仍要复述每个人的招牌锚点**（光的橙围巾、珣的侧袋手势+蚂蚁……）作为冗余保险。

## 2. 提示词结构（Nano Banana 友好）

写成**一整段自然语言描述**，不要关键词逗号流。按以下顺序覆盖（缺项可省）：

1. **媒介与风格**：soft watercolor Japanese ehon illustration, semi-realistic, warm painterly, visible watercolor texture, soft edges, natural light（明确 not anime/chibi/3D）。
2. **主体与身份**：谁、年龄、关系（如 "the quiet transfer student Riku Shun"）。
3. **外貌与服装**：发型、神情、衣着（取自风格圣经）。
4. **招牌道具/动作**：至少一项（保证可辨识）。
5. **动作与情绪**：在做什么、什么心情。
6. **场景**：名古屋校园的具体元素（窗側、引き戸、上履き、樱花……），季节与卷次月份吻合。
7. **构图与机位**：全身/半身/特写、视角、景别、留白。
8. **光线与色调**：晨光/午后斜光/暖黄；温暖低饱和。
9. **负面约束（务必写）**：no horror, no scary elements, no text or garbled letters, no logos, not anime/chibi, not 3D, no modern Chinese or Western school elements, age-appropriate and wholesome。
10. **画幅比例**：见 §3。

> 提示：Nano Banana 对**英文**提示通常更稳；提示词包提供中英双语，出图用英文版、存档可留中文版对照。

## 3. 画幅比例（按用途）

- 绘本跨页内文：**3:2 横**（landscape spread）
- 单页竖图 / 角色立绘：**2:3 竖**
- 封面 KV：**2:3 竖**（留出书名位，但**图内不写字**，文字后期排版上）
- 角色设定参考图：**2:3 竖** 或 **1:1**
- 社媒方图：**1:1**

## 4. 迭代与修图（对话式）

锁定构图后，用编辑指令微调，**保持同一张的其余部分不变**：
- "保持这张画面与角色不变，只把光线改成黄昏暖光。"
- "同一张，把陸珣的左手改成搭在书包侧袋上。"
- "保留三个孩子，去掉背景里那块写错的板书，改成干净的绿色黑板。"
- 脸崩/手崩：用局部编辑"只修复这张里这个孩子的脸/手，其余不动"。

每轮改动尽量**单一变量**，便于回退与对照。

## 5. 归档与命名（接入仓库）

建议存入仓库 `assets/illustration/` 下：

```
assets/illustration/
├── character_refs/                 # 主参考图（LOCKED）
│   ├── 04_riku_shun_REF_v1_LOCKED.png
│   └── ...
├── vol01_wet_chair/                # 按卷/案归档场景图
│   ├── sc01_classroom_morning_v3.png
│   └── ...
└── covers/
```

文件名规则：`{案号或类别}_{内容}_{版本}[_LOCKED].png`。每张图旁建议附一个同名 `.txt`/`.md` 记录**使用的提示词 + 参考图 + 工具/模型 + 日期**，便于复现（与 xlsx 台账同理）。

## 6. 流程清单（每次出图照走）

1. 读 `visual-style-bible`（看锚点与红线）。
2. 确认该角色**主参考图**已 `LOCKED`；没有则先锁。
3. 从 `NANO_BANANA_PROMPT_PACK.md` 取/改提示词；多角色场景准备好多张参考图。
4. 生成（带参考图 + 英文提示 + 比例 + 负面约束），一次 3–4 张。
5. 自检：风格✓ 锚点✓ 红线✓ 文化细节✓ 线索可视✓。
6. 交 `visual-consistency-reviewer` 子代理做独立审核（PASS/FAIL + 修改建议）。
7. FAIL → 按建议用编辑指令单变量修；PASS → 归档命名 + 记录提示词。

## 7. 双层叙事的"笔记页"是另一种画风

陸瑆的笔记页**不是水彩写实**，而是**儿童手账涂鸦风**：铅笔/彩铅线条、稚拙的小图解、箭头与手写感文字框（文字仍建议后期排版，图内不写正式字）。生成时单独切换风格描述，不要套用主水彩风。

## 8. 没有图像工具时

若当前环境无出图工具：
- 不要假装生成或描述"已生成"的图。
- 直接交付**最终英文提示词 + 比例 + 参考图策略**，并告知用户粘贴到 Nano Banana（Gemini app / Google AI Studio）或其 Cursor 出图工具中执行。
- 可同时产出矢量占位（设定群像）供排版占位，但须注明"非水彩定稿"。
