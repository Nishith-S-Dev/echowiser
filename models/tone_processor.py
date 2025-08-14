import re
from typing import Dict, List

class ToneProcessor:
    def __init__(self):
        self.tone_modifications = {
            "inspiring": {
                "prefix_phrases": [
                    "With determination and hope, ",
                    "Embracing the journey ahead, ",
                    "With unwavering spirit, "
                ],
                "emphasis_words": ["amazing", "incredible", "extraordinary", "powerful"],
                "pace_markers": ["... ", " ... "],  # Add pauses for effect
            },
            "suspenseful": {
                "prefix_phrases": [
                    "In the shadows of uncertainty, ",
                    "As tension builds, ",
                    "With each passing moment, "
                ],
                "emphasis_words": ["suddenly", "mysteriously", "unexpectedly", "ominously"],
                "pace_markers": ["...", " ... ", "..."],
            },
            "dramatic": {
                "prefix_phrases": [
                    "In a moment of profound significance, ",
                    "With overwhelming emotion, ",
                    "At this crucial juncture, "
                ],
                "emphasis_words": ["dramatically", "intensely", "powerfully", "profoundly"],
                "pace_markers": [" -- ", "... "],
            },
            "calm": {
                "prefix_phrases": [
                    "In peaceful reflection, ",
                    "With gentle understanding, ",
                    "Softly and serenely, "
                ],
                "emphasis_words": ["gently", "peacefully", "serenely", "quietly"],
                "pace_markers": [" ... ", "..."],
            },
            "energetic": {
                "prefix_phrases": [
                    "With boundless energy, ",
                    "Bursting with enthusiasm, ",
                    "With vibrant excitement, "
                ],
                "emphasis_words": ["energetically", "dynamically", "vibrantly", "enthusiastically"],
                "pace_markers": ["! ", " ! "],
            }
        }
    
    def apply_tone(self, text: str, tone: str) -> str:
        """Apply tone-specific modifications to text"""
        if tone.lower() == "neutral":
            return text
        
        tone_config = self.tone_modifications.get(tone.lower(), {})
        if not tone_config:
            return text
        
        # Split text into paragraphs
        paragraphs = text.split('\n\n')
        processed_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                processed = self._process_paragraph(paragraph, tone_config, i)
                processed_paragraphs.append(processed)
            else:
                processed_paragraphs.append(paragraph)
        
        return '\n\n'.join(processed_paragraphs)
    
    def _process_paragraph(self, paragraph: str, tone_config: Dict, paragraph_index: int) -> str:
        """Process individual paragraph with tone modifications"""
        # Add prefix phrase to first few paragraphs
        if paragraph_index < 3 and tone_config.get("prefix_phrases"):
            prefix = tone_config["prefix_phrases"][paragraph_index % len(tone_config["prefix_phrases"])]
            paragraph = prefix + paragraph
        
        # Add emphasis words
        if tone_config.get("emphasis_words"):
            for word in tone_config["emphasis_words"]:
                # Randomly add emphasis words (simple implementation)
                if paragraph_index % 2 == 0:  # Add to every other paragraph
                    sentences = paragraph.split('. ')
                    if len(sentences) > 1:
                        sentences[0] = sentences[0] + f", {word},"
                        paragraph = '. '.join(sentences)
        
        # Add pace markers
        if tone_config.get("pace_markers"):
            # Add pauses at sentence boundaries for effect
            paragraph = re.sub(r'\.(\s+)', lambda m: f'.{tone_config["pace_markers"][0]}{m.group(1)}', paragraph)
        
        return paragraph
