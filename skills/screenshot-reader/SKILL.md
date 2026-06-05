---
name: screenshot-reader
version: 1.0.0
description: 读取截图内容并转为文字描述。当用户提供截图文件路径时，调用GPT-4o Vision API识别图片内容，返回文字描述。适用于模型本身不支持图像输入的场景。
allowed-tools:
  - Read
  - Bash
---

# 截图阅读器 · Screenshot Reader

## 核心定位

通过 GPT-4o Vision API 将截图转换为文字描述。当用户分享截图但当前模型不支持图像输入时，用此 skill 作为外挂眼睛。

## 触发场景

- 用户说"看一下这张图"并提供了文件路径
- 用户分享截图 PNG/JPG 文件
- 需要识别图片中的 UI / 文字 / 选项

## 工作流

### Step 1: 读取截图文件并编码

```powershell
$imgPath = "用户提供的文件路径"
$base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($imgPath))
```

### Step 2: 调用 GPT-4o Vision

使用 OpenAI Chat Completions API，将 base64 图片作为 image_url 传入：

```json
{
  "model": "gpt-4o",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "text", "text": "请详细描述这张截图的内容。如果是UI界面，列出所有可见的按钮、选项、文字。如果有表格或列表，逐行读出。"},
      {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
    ]
  }],
  "max_tokens": 1000
}
```

### Step 3: 返回文字描述

将 GPT-4o 返回的文本内容展示给用户。
