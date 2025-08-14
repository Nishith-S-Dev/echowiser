import requests
import json
import os
import streamlit as st
from pathlib import Path
import tempfile
from typing import Optional
import base64

class HuggingFaceTTS:
    def __init__(self):
        self.api_token = os.getenv('HUGGINGFACE_API_TOKEN')
        self.api_url_base = "https://api-inference.huggingface.co/models/"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Voice descriptions for Parler TTS based on tone
        self.parler_voices = {
            "neutral": "A clear female voice speaks with normal pace and neutral emotion.",
            "inspiring": "An enthusiastic female speaker with a warm, uplifting tone delivers words with passion.",
            "suspenseful": "A mysterious male voice with a slightly low pitch speaks slowly with dramatic pauses.",
            "dramatic": "An expressive female speaker with dynamic intonation conveys intense emotion.",
            "calm": "A gentle female voice speaks softly with a peaceful, relaxing tone.",
            "energetic": "An excited male speaker with high energy and fast pace delivers words enthusiastically."
        }
    
    def generate_audio(self, text: str, model: str, tone: str = "neutral", 
                      voice_description: Optional[str] = None) -> Optional[str]:
        """Generate audio using Hugging Face TTS models"""
        
        try:
            # Handle different model types
            if "parler" in model.lower():
                return self._generate_with_parler(text, model, tone, voice_description)
            elif "speecht5" in model.lower():
                return self._generate_with_speecht5(text, model)
            elif "mms-tts" in model.lower():
                return self._generate_with_mms(text, model)
            else:
                # Generic TTS approach
                return self._generate_generic(text, model)
                
        except Exception as e:
            st.error(f"TTS Generation Error: {str(e)}")
            return None
    
    def _generate_with_parler(self, text: str, model: str, tone: str, 
                             voice_description: Optional[str]) -> str:
        """Generate audio using Parler TTS[1][7]"""
        
        # Use custom voice description or tone-based default
        voice_desc = voice_description or self.parler_voices.get(tone, self.parler_voices["neutral"])
        
        api_url = f"{self.api_url_base}{model}"
        
        payload = {
            "inputs": text,
            "parameters": {
                "description": voice_desc
            }
        }
        
        response = requests.post(api_url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            # Save audio file
            output_file = self.output_dir / f"parler_audio_{tone}.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            return str(output_file)
        else:
            raise Exception(f"Parler TTS API error: {response.status_code}")
    
    def _generate_with_speecht5(self, text: str, model: str) -> str:
        """Generate audio using Microsoft SpeechT5[6][9]"""
        
        api_url = f"{self.api_url_base}{model}"
        
        payload = {"inputs": text}
        
        response = requests.post(api_url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            output_file = self.output_dir / "speecht5_audio.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            return str(output_file)
        else:
            raise Exception(f"SpeechT5 API error: {response.status_code}")
    
    def _generate_with_mms(self, text: str, model: str) -> str:
        """Generate audio using Facebook MMS TTS[19]"""
        
        api_url = f"{self.api_url_base}{model}"
        
        payload = {"inputs": text}
        
        response = requests.post(api_url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            output_file = self.output_dir / "mms_audio.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            return str(output_file)
        else:
            raise Exception(f"MMS TTS API error: {response.status_code}")
    
    def _generate_generic(self, text: str, model: str) -> str:
        """Generic TTS generation for other models"""
        
        api_url = f"{self.api_url_base}{model}"
        
        payload = {"inputs": text}
        
        response = requests.post(api_url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            output_file = self.output_dir / "generic_audio.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            return str(output_file)
        else:
            raise Exception(f"Generic TTS API error: {response.status_code}")
    
    def _handle_api_errors(self, response, model_name: str):
        """Handle common API errors"""
        if response.status_code == 503:
            st.warning(f"⏳ {model_name} model is loading. This may take a few minutes...")
            return False
        elif response.status_code == 429:
            st.error("🚫 Rate limit exceeded. Please wait a moment and try again.")
            return False
        elif response.status_code == 401:
            st.error("🔑 Invalid API token. Please check your Hugging Face token.")
            return False
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")
            return False
