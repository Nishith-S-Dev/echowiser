import requests
import json
import os
import streamlit as st
from typing import Optional

class HuggingFaceTextEnhancer:
    def __init__(self):
        self.api_token = os.getenv('HUGGINGFACE_API_TOKEN')
        self.api_url_base = "https://api-inference.huggingface.co/models/"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        
        # Tone-based enhancement prompts
        self.tone_prompts = {
            "inspiring": "Rewrite this text in an inspiring and motivational tone that uplifts the reader:",
            "suspenseful": "Rewrite this text with suspenseful and mysterious elements that create tension:",
            "dramatic": "Rewrite this text in a dramatic and emotionally intense style:",
            "calm": "Rewrite this text in a calm, peaceful, and soothing manner:",
            "energetic": "Rewrite this text with high energy and enthusiasm:",
            "neutral": "Improve the clarity and flow of this text while maintaining a neutral tone:"
        }
    
    def enhance_text(self, text: str, tone: str, model: str) -> str:
        """Enhance text using Hugging Face Granite models"""
        try:
            # Use appropriate prompt based on tone
            prompt = self.tone_prompts.get(tone.lower(), self.tone_prompts["neutral"])
            
            # Create the full prompt
            full_prompt = f"{prompt}\n\nOriginal text: {text}\n\nEnhanced text:"
            
            # API endpoint
            api_url = f"{self.api_url_base}{model}"
            
            # Request payload
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": min(len(text.split()) * 2, 1000),  # Reasonable limit
                    "temperature": 0.7,
                    "do_sample": True,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
            }
            
            # Make API request
            response = requests.post(api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the generated text
                if isinstance(result, list) and len(result) > 0:
                    enhanced_text = result[0].get('generated_text', '')
                    
                    # Extract only the enhanced part (after "Enhanced text:")
                    if "Enhanced text:" in enhanced_text:
                        enhanced_text = enhanced_text.split("Enhanced text:")[-1].strip()
                    
                    # Fallback: if enhancement seems incomplete, return original with tone markers
                    if len(enhanced_text) < len(text) * 0.5:
                        return self._add_tone_markers(text, tone)
                    
                    return enhanced_text
                else:
                    st.warning("Enhancement model returned unexpected format, using original text")
                    return self._add_tone_markers(text, tone)
            
            elif response.status_code == 503:
                st.warning("⏳ Model is loading, using simple tone enhancement...")
                return self._add_tone_markers(text, tone)
            else:
                st.warning(f"Enhancement API error ({response.status_code}), using original text")
                return self._add_tone_markers(text, tone)
                
        except Exception as e:
            st.warning(f"Enhancement failed: {str(e)}, using original text with tone markers")
            return self._add_tone_markers(text, tone)
    
    def _add_tone_markers(self, text: str, tone: str) -> str:
        """Fallback: Add simple tone markers to text"""
        tone_prefixes = {
            "inspiring": "With hope and determination: ",
            "suspenseful": "In a moment of tension: ",
            "dramatic": "With great emotion: ",
            "calm": "In peaceful reflection: ",
            "energetic": "With boundless energy: ",
            "neutral": ""
        }
        
        prefix = tone_prefixes.get(tone.lower(), "")
        return f"{prefix}{text}" if prefix else text
