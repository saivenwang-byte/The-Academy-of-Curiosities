# 儿童日语绘本翻译 · 三步工作流

配套全局技能：`image-ocr-jp` · `vision-understand-kids` · `japanese-kids-translate` · `bilingual-pdf-maker` · `screenshot-to-cursor` · `video-storyboard-analyzer`

---

## 场景 A：单页截图（最快）

**适用：** 电子版绘本、PDF 单页、手机屏摄。

### 步骤

1. **截图** — `Win + Shift + S`，框选页面。
2. **粘贴** — Cursor 聊天 `Ctrl + V`。
3. **提示词**（任选）：
   - `翻译这页绘本` → 全自动链式处理
   - `只提取日语原文` → 仅 OCR
   - `截图翻译，并追加到双语 Markdown` → OCR + 翻译 + 写入文件
4. **核对输出格式**：
   ```
   【画面解读（儿童版）】…
   【日语原文】…
   【儿童日语（汉字+假名）】…
   【中文对照】…
   ```
5. **（可选）导出** — 让 Agent「按 bilingual-pdf-maker 追加到 output/book_bilingual.md」。

### 多页

每页截图一次，在消息里写 `第5页`；最后说：`生成完整 bilingual markdown`。

---

## 场景 B：批量扫描图

**适用：** 已扫好的 `page_01.jpg` … `page_NN.jpg`。

### 步骤

1. 把图片放入 `images/`，文件名 zero-pad（`page_01`）。
2. 在 Cursor Agent 中说：
   ```
   按顺序处理 images/ 下所有页面：画面解读、OCR、儿童日语翻译，输出到 output/book_bilingual.md
   ```
3. Agent 对每页执行技能链（若上下文不够，可分批「处理 page_01 到 page_10」）。
4. **导出 PDF**：
   ```powershell
   pandoc output/book_bilingual.md -o output/book_bilingual.pdf `
     --pdf-engine=xelatex `
     -V CJKmainfont="Microsoft YaHei" `
     -V geometry:margin=1in
   ```
   或使用 **make-pdf** 技能（若已安装 gstack）。

### 验收

- [ ] 页序与文件名一致
- [ ] 每页含原文 + 假名日语 + 中文
- [ ] 图片链接可本地预览

---

## 场景 C：绘本视频分镜

**适用：** 他人读绘本的 MP4、录屏。

### 步骤

1. 视频放到项目根，如 `input.mp4`。
2. **抽帧**（终端）：
   ```powershell
   mkdir output\frames -Force
   ffmpeg -i input.mp4 -vf "fps=0.5,scale=1280:-1" -q:v 2 output/frames/frame_%04d.jpg
   ```
3. 在 Cursor 中说：
   ```
   用 video-storyboard-analyzer 处理 output/frames，生成 output/storyboard.md
   ```
4. 得到表格或分块 Markdown：帧号、时间戳、画面简述、OCR、字幕、中文。
5. **（可选）SRT** — `请根据 storyboard 生成 subtitles_zh.srt`
6. **（可选）双语书** — 把关键帧当作插图，走 **bilingual-pdf-maker**。

### 参数提示

| 需求 | ffmpeg 调整 |
|------|-------------|
| 帧更密 | `fps=1` 或 `fps=2` |
| 少重复 | `select='gt(scene,0.3)'` 场景检测 |
| 更高 OCR 精度 | 去掉 scale 或提高到 `1920:-1` |

---

## 技能链一览

```
场景 A:  screenshot-to-cursor
           → vision-understand-kids
           → image-ocr-jp
           → japanese-kids-translate
           → [bilingual-pdf-maker]

场景 B:  批量读图 → 同上（无 screenshot 步骤）

场景 C:  ffmpeg 抽帧
           → video-storyboard-analyzer
           → [bilingual-pdf-maker / SRT]
```

---

## 输出质量标准

- 句子 ≤ 8 词，ですます体
- 汉字全部带假名：`今日（きょう）`
- 不翻译装饰性花纹；不臆造画面里没有的台词
- 画面解读最多 2 句简单中文，不讲剧情道理
