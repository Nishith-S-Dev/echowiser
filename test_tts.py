import streamlit as st
import edge_tts
import asyncio
import tempfile

async def test_edge_tts():
    text = "Hello! This is a test of our audiobook system."
    voice = "en-US-JennyNeural"
    
    output_file = "test_audio.wav"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"✅ Audio saved to {output_file}")

# Test Edge TTS
asyncio.run(test_edge_tts())
print("🎉 TTS system is working!")
