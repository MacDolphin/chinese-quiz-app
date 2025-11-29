import os
import asyncio
import edge_tts

# Praises list (must match the app)
praises = [
    {"text": "太棒了！", "filename": "praise_01"},
    {"text": "完全正確！", "filename": "praise_02"},
    {"text": "你真厲害！", "filename": "praise_03"},
    {"text": "水啦！答對了！", "filename": "praise_04"},
    {"text": "Excellent!", "filename": "praise_05"},
    {"text": "你是漢字小天才！", "filename": "praise_06"},
    {"text": "好聰明喔！", "filename": "praise_07"},
    {"text": "答得好！繼續保持！", "filename": "praise_08"},
    {"text": "沒錯！就是這個！", "filename": "praise_09"},
    {"text": "你的中文越來越好了！", "filename": "praise_10"},
    {"text": "太神了！", "filename": "praise_11"},
    {"text": "給你一個大拇指！", "filename": "praise_12"}
]

async def generate_audio(text, filepath, voice="zh-TW-HsiaoChenNeural", rate="+20%"):
    print(f"Generating: {text} -> {filepath}")
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(filepath)
    except Exception as e:
        print(f"Error generating {text}: {e}")

async def main():
    # Create directory
    os.makedirs('audio_minimal', exist_ok=True)

    # Generate Praise Audio
    print("--- Generating Praise Audio (12 files only) ---")
    for p in praises:
        filepath = os.path.join('audio_minimal', f"{p['filename']}.mp3")
        await generate_audio(p['text'], filepath)

    print("\n✅ All 12 praise audio files generated in 'audio_minimal' folder!")
    print("📁 You can now upload this folder to GitHub (only 12 files)")

if __name__ == "__main__":
    asyncio.run(main())
