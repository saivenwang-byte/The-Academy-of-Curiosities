#!/usr/bin/env python3
"""Send Vol1 sample CN/JP text via SMTP. Requires env: SMTP_HOST, SMTP_USER, SMTP_PASS."""
from __future__ import annotations

import os
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/样章包"
FILES = [
    SAMPLE / "04_样章_序+案01_正文_HybridVoice.txt",
    SAMPLE / "04_样章_序+案01_正文_日本語.txt",
    ROOT / "00_项目概览/00_归档/2026-06-04_工作日清单.md",
]
TO = ["saivenwang@126.com", "saivenwang@gmail.com"]


def main() -> int:
    host = os.environ.get("SMTP_HOST", "smtp.126.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    user = os.environ.get("SMTP_USER") or os.environ.get("EMAIL_USER")
    password = os.environ.get("SMTP_PASS") or os.environ.get("EMAIL_PASS")

    if not user or not password:
        print("SKIP: SMTP_USER and SMTP_PASS (or EMAIL_USER/EMAIL_PASS) not set.", file=sys.stderr)
        return 2

    msg = MIMEMultipart()
    msg["From"] = user
    msg["To"] = ", ".join(TO)
    msg["Subject"] = "《学堂趣事录》Vol1 样章 · 序+案① 中/日正文 · 2026-06-04"

    body = """王赛文 您好，

附件为《学堂趣事录》第1卷样章包正文（2026-06-04）：

1. 04_样章_序+案01_正文_HybridVoice.txt — 中文 Hybrid Voice v1（试读 PDF 用稿）
2. 04_样章_序+案01_正文_日本語.txt — 日文初稿 JP_VOICE_v1
3. 2026-06-04_工作日清单.md — 今日工作调整/优化/删改清单

范围：序 + 案①《翘边的海报》
状态：待田中 · 待 E07/E20 · PDF 未导出

— Academy of Curiosities · 自动发送
"""
    msg.attach(MIMEText(body, "plain", "utf-8"))

    for path in FILES:
        if not path.exists():
            print(f"MISSING: {path}", file=sys.stderr)
            return 1
        part = MIMEApplication(path.read_bytes(), Name=path.name)
        part["Content-Disposition"] = f'attachment; filename="{path.name}"'
        msg.attach(part)

    with smtplib.SMTP_SSL(host, port) as server:
        server.login(user, password)
        server.sendmail(user, TO, msg.as_string())

    print(f"OK: sent to {', '.join(TO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
