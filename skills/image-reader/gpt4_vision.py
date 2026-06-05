"""GPT-4o Vision 图片分析。依次尝试多个 Key，自动限流重试。"""
import sys, base64, json, time, urllib.request, urllib.error

if len(sys.argv) < 2:
    print("用法: python gpt4_vision.py <图片路径>")
    sys.exit(1)

with open(sys.argv[1], 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

keys = [
    open(r"D:\【私人】\【KEY】\openai-api-key.txt").read().strip(),
    open(r"D:\【私人】\【KEY】\openai-api-key (1).txt").read().strip(),
    open(r"D:\【私人】\【KEY】\密钥.txt").read().split('\n')[21].strip(),  # Codex-CC line
]

def try_key(key, attempt=0):
    body = {
        "model": "gpt-4o",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "请详细描述这个截图/图片的内容。如果是UI界面，逐行列出所有按钮、选项、数值。如果是表格，逐列读出所有内容。"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
            ]
        }],
        "max_tokens": 1000
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        if e.code == 429:
            wait = 5 * (attempt + 1)
            print(f"[Key {attempt+1} 限流，等待{wait}秒...]", file=sys.stderr)
            time.sleep(wait)
            return try_key(key, attempt + 1) if attempt < 3 else None
        else:
            return f"[HTTP {e.code}]"
    except Exception as e:
        return f"[错误: {e}]"

for i, key in enumerate(keys):
    print(f"[尝试 Key {i+1}]", file=sys.stderr)
    result = try_key(key)
    if result and not result.startswith("[HTTP"):
        print(result)
        sys.exit(0)
    print(f"Key {i+1}: {result[:80] if result else 'failed'}", file=sys.stderr)

print("所有 Key 均不可用。请稍后重试。")
