import csv
import os
import asyncio
import edge_tts

# Configuration
VOCAB_FILE = 'vocabulary.csv'
AUDIO_DIR = 'audio'
VOCAB_AUDIO_DIR = os.path.join(AUDIO_DIR, 'vocab')
PRAISE_AUDIO_DIR = os.path.join(AUDIO_DIR, 'praises')

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
    if os.path.exists(filepath):
        print(f"Skipping existing: {filepath}")
        return

    print(f"Generating: {text} -> {filepath}")
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(filepath)
    except Exception as e:
        print(f"Error generating {text}: {e}")

async def main():
    # Create directories
    os.makedirs(VOCAB_AUDIO_DIR, exist_ok=True)
    os.makedirs(PRAISE_AUDIO_DIR, exist_ok=True)

    # 1. Generate Praise Audio
    print("--- Generating Praise Audio ---")
    for p in praises:
        filepath = os.path.join(PRAISE_AUDIO_DIR, f"{p['filename']}.mp3")
        await generate_audio(p['text'], filepath)

    # 2. Generate Vocabulary Audio
    print("\n--- Generating Vocabulary Audio ---")
    if not os.path.exists(VOCAB_FILE):
        print(f"Error: {VOCAB_FILE} not found!")
        return

    with open(VOCAB_FILE, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            char = row.get('char', '').strip()
            if char:
                # Use character as filename (handle special chars if needed, but Chinese chars are usually fine in modern FS)
                # For safety, maybe hash it or just use it if FS supports. 
                # Let's use the char directly for readability, assuming standard OS support.
                filepath = os.path.join(VOCAB_AUDIO_DIR, f"{char}.mp3")
                
                # Generate audio for the character (or char + zhuyin if preferred? Usually just char is enough for "Correct answer is X")
                # The app says: "哎呀答錯了，正確答案是 {target['char']}" -> We probably want to record "正確答案是 X" or just "X"?
                # The current app logic plays: f"哎呀答錯了，正確答案是 {target['char']}"
                # This is dynamic. To pre-generate, we can't pre-generate every combination.
                # Strategy: 
                # Option A: Just play the character sound "X". The user hears "X".
                # Option B: Generate "Correct answer is" separately and play two audios? Streamlit doesn't support queuing easily.
                # Decision: Just play the character pronunciation. It's faster and cleaner.
                
                await generate_audio(char, filepath)

    print("\nAll audio generation complete!")

if __name__ == "__main__":
    asyncio.run(main())
