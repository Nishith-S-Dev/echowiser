import os
import tempfile
import requests
import torch
from transformers import pipeline
from gtts import gTTS
import edge_tts
import asyncio
from pathlib import Path
from typing import Optional
import streamlit as st

class TTSEngine:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_audio(self, text: str, tone: str = "neutral", 
                      speed: float = 1.0, pitch: int = 0) -> Optional[str]:
        """Generate audio from text using selected model"""
        
        if self.model_name == "IBM Granite":
            return self._generate_with_ibm_granite(text, tone, speed, pitch)
        elif self.model_name == "Hugging Face Bark":
            return self._generate_with_bark(text, tone)
        elif self.model_name == "Edge TTS":
            return self._generate_with_edge_tts(text, tone, speed, pitch)
        elif self.model_name == "Google TTS":
            return self._generate_with_gtts(text, speed)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
    
    def _generate_with_ibm_granite(self, text: str, tone: str, speed: float, pitch: int) -> str:
        """Enhance text using IBM Granite LLM via Hugging Face, then TTS with Edge"""
        try:
            # Use Hugging Face pipeline for IBM Granite LLM
            granite_model = "ibm-granite/granite-3b-instruct"  # or another Granite model
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            generator = pipeline(
                "text-generation",
                model=granite_model,
                token=hf_token
            )
            prompt = f"Rewrite this text in a {tone} tone:\n{text}"
            result = generator(prompt, max_new_tokens=500)
            enhanced_text = result[0]['generated_text']

            # Now use Edge TTS to convert enhanced text to speech
            return self._generate_with_edge_tts(enhanced_text, tone, speed, pitch)
        except Exception as e:
            st.error(f"IBM Granite LLM error: {str(e)}")
            # Fallback to Edge TTS with original text
            return self._generate_with_edge_tts(text, tone, speed, pitch)
    
    def _generate_with_bark(self, text: str, tone: str) -> str:
        """Generate audio using standard Bark model"""
        try:
            from bark import SAMPLE_RATE, generate_audio, preload_models
            from scipy.io.wavfile import write
            
            # Preload models (this may take a moment on first run)
            preload_models()
            
            # Voice selection based on tone
            voice_presets = {
                "neutral": "v2/en_speaker_6",
                "inspiring": "v2/en_speaker_9", 
                "suspenseful": "v2/en_speaker_3",
                "dramatic": "v2/en_speaker_7",
                "calm": "v2/en_speaker_1",
                "energetic": "v2/en_speaker_8"
            }
            
            voice_preset = voice_presets.get(tone.lower(), "v2/en_speaker_6")
            
            # Generate audio
            audio_array = generate_audio(text, history_prompt=voice_preset)
            
            # Save to file
            output_file = self.output_dir / f"bark_audio_{tone}.wav"
            write(str(output_file), SAMPLE_RATE, audio_array)
            
            return str(output_file)
            
        except Exception as e:
            st.error(f"Bark TTS error: {str(e)}")
            # Fallback to Edge TTS
            return self._generate_with_edge_tts(text, tone, 1.0, 0)

    
    def _generate_with_edge_tts(self, text: str, tone: str, 
                               speed: float, pitch: int) -> str:
        """Generate audio using Edge TTS"""
        try:
            # Voice selection based on tone
            voice_map = {
                "neutral": "en-US-JennyNeural",
                "inspiring": "en-US-AriaNeural",
                "suspenseful": "en-US-GuyNeural",
                "dramatic": "en-US-DavisNeural",
                "calm": "en-US-JennyNeural",
                "energetic": "en-US-AriaNeural"
            }
            
            voice = voice_map.get(tone.lower(), "en-US-JennyNeural")
            output_file = self.output_dir / f"edge_audio_{tone}.wav"
            
            async def generate():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(str(output_file))
            
            # Run async function
            asyncio.run(generate())
            return str(output_file)
            
        except Exception as e:
            st.error(f"Edge TTS error: {str(e)}")
            return self._generate_with_gtts(text, speed)
    
    def _generate_with_gtts(self, text: str, speed: float) -> str:
        """Generate audio using Google TTS (fallback)"""
        try:
            tts = gTTS(text=text, lang='en', slow=(speed < 1.0))
            output_file = self.output_dir / "gtts_audio.mp3"
            tts.save(str(output_file))
            return str(output_file)
            
        except Exception as e:
            raise Exception(f"All TTS methods failed: {str(e)}")
