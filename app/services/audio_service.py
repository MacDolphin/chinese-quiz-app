# Service for Audio/TTS operations
# 音訊處理服務

import requests
import base64
from urllib.parse import quote
import streamlit.components.v1 as components
import logging

def get_audio_bytes_from_google_tts(text: str) -> bytes:
    """
    從 Google Translate TTS 下載音頻字節。
    Fetch audio bytes from Google TTS.

    Args:
        text: Text to speak

    Returns:
        Audio bytes or None
    """
    try:
        encoded_text = quote(text)
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-TW&client=tw-ob&q={encoded_text}"
        
        # 添加 User-Agent 避免被阻擋
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        logging.error(f"TTS Error: {e}")
        return None

def generate_audio_html(text: str) -> None:
    """
    在 Streamlit 中生成隱藏的 Audio 播放器 HTML (支援 iOS)。
    Generate hidden HTML audio player for Streamlit (iOS compatible).
    
    Args:
        text: Text to speak
    """
    # 獲取音頻字節
    audio_bytes = get_audio_bytes_from_google_tts(text)
    
    if not audio_bytes:
        logging.warning("TTS generation failed")
        return
    
    # 轉換為 base64
    audio_base64 = base64.b64encode(audio_bytes).decode()
    
    # 使用 HTML5 Audio API 播放
    html_code = f"""
    <div style="text-align: center; padding: 10px; display: none;">
        <audio id="audioPlayer" controls autoplay style="width: 100%; max-width: 500px;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            您的瀏覽器不支援音頻播放
        </audio>
    </div>
    <script>
        // 確保音頻能在 iOS 上播放
        // Ensure audio plays on iOS
        const audio = document.getElementById('audioPlayer');
        if (audio) {{
            audio.play().catch(e => console.log('Autoplay prevented:', e));
        }}
    </script>
    """
    
    components.html(html_code, height=0)
