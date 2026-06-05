"""OCR 图片文字提取"""
import sys, pytesseract
from PIL import Image

if len(sys.argv) < 2:
    print("用法: python ocr_image.py <图片路径>")
    sys.exit(1)

img = Image.open(sys.argv[1])
text = pytesseract.image_to_string(img, lang='jpn+chi_sim+eng')
if text.strip():
    print(text)
else:
    print("(未检测到文字)")
