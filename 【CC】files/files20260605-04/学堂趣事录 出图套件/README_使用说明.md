# 出图生产套件 · The Academy of Curiosities

把这套放进仓库 `The-Academy-of-Curiosities`，就能在你自己的 Claude Code + Nano Banana
（或任何接好的出图工具）环境里，稳定地生成**风格统一、对得上设定、守得住红线**的插画。

> 重要说明：**这套套件本身不"内置"出图能力**。真正生成图片，依赖你运行环境里接入的图像工具
> （Nano Banana / Gemini 图像、Google AI Studio、或 Cursor 的出图功能）。套件负责的是：把流程、
> 风格、角色一致性、审核标准全部固化下来，让"谁来出、用什么出"都不跑偏。

---

## 一、套件里有什么

| 文件 | 类型 | 作用 |
|------|------|------|
| `skills/visual-style-bible/SKILL.md` | Skill | **视觉圣经**：锁定水彩画风 + 八个角色的外貌/道具/动作/专属色 + 红线。出任何图前必读。 |
| `skills/illustration-nano-banana/SKILL.md` | Skill | **出图工作流**：主参考图优先、Nano Banana 提示词结构、画幅、迭代修图、归档命名、无工具时怎么办。 |
| `.claude/agents/illustration-director.md` | Agent | **出图总监**：把案件卡/需求 → 镜头清单 → 提示词 → 生成 → 交审核。 |
| `.claude/agents/visual-consistency-reviewer.md` | Agent | **一致性审核**：对照圣经与红线给 PASS/FAIL + 单变量修改建议。 |
| `docs/illustration/NANO_BANANA_PROMPT_PACK.md` | 文档 | **可直接粘贴的提示词包**：八角色主参考图 + 同框群像 + 单案模板 + 笔记页 + 封面，中英双语。 |

## 二、怎么装（Claude Code）

把对应文件夹合并进仓库根目录即可：
- `skills/` → 仓库的 `skills/`（与你已有的 `academy-character-scale` 等并列）
- `.claude/agents/` → 仓库的 `.claude/agents/`（Claude Code 会自动识别这两个子代理）
- `docs/illustration/` → 仓库的 `docs/`

提交：
```bash
git add skills/visual-style-bible skills/illustration-nano-banana \
        .claude/agents/illustration-director.md \
        .claude/agents/visual-consistency-reviewer.md \
        docs/illustration/NANO_BANANA_PROMPT_PACK.md
git commit -m "feat(art): 加入出图 agent 与 Skill（Nano Banana 工作流 + 视觉圣经 + 提示词包）"
```

接好一个图像工具（任选其一）：
- **Gemini app / Google AI Studio**：手动把提示词包里的英文提示粘进去出图（最省事的起步方式）。
- **图像 MCP / Cursor 出图**：在 Claude Code 里接一个能调 Gemini 图像的 MCP，`illustration-director`
  就能直接调用它出图；没接时它会自动退化为"只产出提示词并告诉你去哪跑"。

## 三、怎么用（典型流程）

1. 在 Claude Code 里说："用 illustration-director 给案①《湿椅子》出关键场景图。"
2. 总监会：读 `visual-style-bible` + 案件卡 → 列镜头清单 → **先锁八个角色的主参考图** → 写
   Nano Banana 提示词 → 若有图像工具则带参考图出图，一次 3–4 张。
3. 交 `visual-consistency-reviewer` 审核 → 按 PASS/FAIL 与修改建议单变量修。
4. 通过后按命名规则归档到 `assets/illustration/`，并存下提示词+参考图+工具+日期（可复现）。

手动起步也行：直接打开提示词包，先把**八张主参考图**生成并锁定，再用"一致性指令 + 单案模板"出场景。

## 四、铁律（套件已内建强制）

- 零恐怖；画面温暖安全。
- 未成年人形象一律健康、得体、适龄，**绝不性化**——任何会把儿童形象推向不当的请求，相关部分一律拒绝。
- 大人可出现，但**永不替孩子破案**。
- 名古屋/日本校园细节准确；无中式/西式错置；图内尽量不放文字（文字后期排版）。
- 废弃角色「阿文」不存在，不得出现。

## 五、一致性的关键：主参考图优先

同一角色绝不每次从零生成（长相会漂移）。**先为八个角色各锁一张"主参考图"**，之后每次出含人物的场景，
都把相关主参考图作为输入参考喂给 Nano Banana，并在提示词里复述各自的招牌锚点。这是整套流程的命脉。

---

*基线：项目正典 V1.0（2026-06-04）。本套件与已交付的《200篇内容架构计划书》《前100篇去重台账》《案①样章》一致。*
