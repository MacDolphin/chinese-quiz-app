from urllib.parse import quote
import requests

# 测试 Google TTS
text = "你好"
encoded_text = quote(text)
url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-TW&client=tw-ob&q={encoded_text}"

print(f"Testing URL: {url}")

try:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.headers.get('Content-Type')}")
    print(f"Content Length: {len(response.content)} bytes")
    
    if response.status_code == 200:
        # 保存音频文件
        with open('test_audio.mp3', 'wb') as f:
            f.write(response.content)
        print("✅ Audio saved to test_audio.mp3")
    else:
        print(f"❌ Failed: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
