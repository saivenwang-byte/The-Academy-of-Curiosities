# 儿童日语绘本翻译 · Cursor 工作流

在 Cursor 里把日语绘本页面（截图、扫描图、视频）转成**带假名的儿童日语 + 中文对照**，并可组装双语 Markdown/PDF。

本目录是**独立工具包**，不修改《学堂趣事录》正文；可复制整个文件夹到你的绘本项目根目录使用。

---

## 前置条件

### 1. Cursor Nightly（推荐）

1. 打开 [Cursor 下载页](https://cursor.com/) 或设置中的 **Beta / Nightly** 通道。
2. 安装并切换到 **Nightly**  builds，以获得更稳定的**聊天内贴图**与 Agent 技能发现。

> 稳定版也可用；若贴图后模型「看不见」图片，请先升级 Nightly 并确认已选视觉模型。

### 2. DeepSeek 视觉模型（推荐 OCR）

1. Cursor → **Settings → Models**。
2. 添加 **DeepSeek** API Key（[DeepSeek 开放平台](https://platform.deepseek.com/)）。
3. 在 Agent / Chat 默认模型中选择 **DeepSeek-VL** 或当前可用的 **多模态** 模型（如 GPT-4o、Qwen-VL 等）。
4. **用户须自行开通 API、充值与合规使用**——本仓库不包含密钥。

### 3. 全局技能（已安装于用户目录）

确认以下目录存在（由安装脚本或手动创建）：

```
C:\Users\Lenovo\.cursor\skills\
├── image-ocr-jp\
├── vision-understand-kids\
├── japanese-kids-translate\
├── bilingual-pdf-maker\
├── screenshot-to-cursor\
└── video-storyboard-analyzer\
```

每个文件夹内应有 **`SKILL.md`**（大写，Cursor 官方约定）。

### 4. 可选：ffmpeg（视频分镜）

```powershell
winget install Gyan.FFmpeg
# 或 choco install ffmpeg
ffmpeg -version
```

### 5. 可选：Pandoc（导出 PDF）

```powershell
winget install JohnMacFarlane.Pandoc
```

---

## 三种使用场景

| 场景 | 说明 | 详细步骤 |
|------|------|----------|
| **A · 单页截图** | Win+Shift+S → 粘贴到 Cursor | [workflow.md](./workflow.md#场景-a单页截图最快) |
| **B · 批量扫描图** | 文件夹多页 JPG/PNG | [workflow.md](./workflow.md#场景-b批量扫描图) |
| **C · 绘本视频** | 读绘本视频 → 分镜 + 字幕 | [workflow.md](./workflow.md#场景-c绘本视频分镜) |

---

## 快速开始（场景 A）

1. 打开 Cursor，新建或打开**绘本专用文件夹**（建议复制本目录的 `.cursorrules` 到项目根）。
2. 选中 **DeepSeek-VL**（或视觉模型）。
3. `Win + Shift + S` 截图 → 在聊天里 `Ctrl + V` 粘贴。
4. 发送：`翻译这页绘本`
5. Agent 将依次输出：【画面解读（儿童版）】→【日语原文】→【儿童日语（汉字+假名）】→【中文对照】

---

## 项目目录建议

```
my-picturebook/
├── .cursorrules          ← 从本工具包复制
├── images/               ← 原图或扫描
├── output/
│   ├── book_bilingual.md
│   ├── storyboard.md     ← 视频场景
│   └── frames/           ← ffmpeg 抽帧
└── input.mp4             ← 可选
```

---

## 故障排除

| 现象 | 处理 |
|------|------|
| 模型说看不到图 | 换 Nightly；换 DeepSeek-VL / GPT-4o；重新截图粘贴 |
| OCR 乱序 | 消息里注明「縦書き」或「横書き」；裁剪只含文字区域 |
| 没有振假名 | 确认触发 **japanese-kids-translate**，勿用通用翻译 |
| 技能未生效 | 检查 `~/.cursor/skills/*/SKILL.md` 是否存在；重启 Cursor |
| ffmpeg 找不到 | 重开终端；把 ffmpeg 加入 PATH |
| PDF 假名排版差 | Markdown PDF 适合试读；商业排版请用 InDesign 等 |

---

## 与《学堂趣事录》的关系

- 本工具包位于 `tools/儿童日语绘本翻译/`，**仅供通用绘本翻译流程**。
- 丛书日文正稿请继续用 `academy-jp-voice-editor`、`academy-jp-tanaka-desk` 等项目技能。
- 项目级规则：`.cursor/rules/kids-picturebook-translate.mdc`（在本仓库内打开本目录时生效）。

---

## 许可与隐私

- 截图/绘本内容可能含版权材料，请仅用于个人学习或已获授权用途。
- API 调用将发送图像到所选模型提供商，请自行阅读其隐私政策。
