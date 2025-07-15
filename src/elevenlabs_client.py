"""
ElevenLabs API client for text-to-speech conversion
"""

import requests
import os

class ElevenLabsClient:
    """Client for ElevenLabs text-to-speech API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {"xi-api-key": api_key}
    
    def text_to_speech(self, text, voice_id, output_file, voice_settings=None):
        """Convert text to speech with voice customization"""
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        # Default voice settings
        default_settings = {
            "stability": 0.5,        # 0-1: lower = more expressive
            "similarity_boost": 0.8,  # 0-1: voice consistency
            "style": 0.5,            # 0-1: exaggeration level
            "use_speaker_boost": True
        }
        
        if voice_settings:
            default_settings.update(voice_settings)
        
        data = {
            "text": text, 
            "model_id": "eleven_multilingual_v2",
            "voice_settings": default_settings
        }
        
        print(f"Converting: '{text[:50]}...' to {output_file}")
        response = requests.post(url, json=data, headers=self.headers)
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        # Check if file was created and has content
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"✓ Created {output_file} ({os.path.getsize(output_file)} bytes)")
            return output_file
        else:
            print(f"✗ Failed to create {output_file}")
            return None