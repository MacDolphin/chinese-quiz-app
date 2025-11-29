import asyncio
import edge_tts

async def get_edge_tts_audio(text, voice="zh-TW-HsiaoChenNeural", rate="+20%"):
    print(f"Generating audio for: {text} with voice {voice} and rate {rate}")
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    mp3_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_data += chunk["data"]
    return mp3_data

async def main():
    try:
        data = await get_edge_tts_audio("太棒了")
        print(f"Success! Got {len(data)} bytes")
        with open("test.mp3", "wb") as f:
            f.write(data)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
