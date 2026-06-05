---
name: image-reader
version: 1.0.0
description: 图片内容读取与分析。抓取图片中的文字（OCR）并分析画面内容。当用户提供截图但模型不支持图像输入时触发。支持本地OCR和GPT-4o Vision双通道。
allowed-tools:
  - Read
  - Bash
---

# 图片读取器 · Image Reader

## 核心定位

双通道读取图片内容：本地 OCR 提取文字 + GPT-4o Vision 分析画面。当模型不支持图像输入时，用此外挂读取截图、照片、图表。

## 触发场景

- 用户分享截图/图片文件路径
- 用户说"看一下这张图"
- ERROR: Cannot read "image.png"

## 工作流

### 通道 1：本地 OCR（提取文字，离线可用）

调用 Python 脚本 `ocr_image.py <文件路径>`，使用 pytesseract 提取图片中的文字。

### 通道 2：GPT-4o Vision（分析画面内容，需要 API Key）

调用 Python 脚本 `gpt4_vision.py <文件路径>`，将图片编码发送到 GPT-4o，获取详细描述。

会依次尝试三个 OpenAI Key，自动处理限流重试。
