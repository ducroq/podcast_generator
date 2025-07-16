"""
ElevenLabs API client for text-to-speech conversion
with advanced voice settings support
"""

import requests
import os

class ElevenLabsClient:
    """Client for ElevenLabs text-to-speech API with advanced configuration"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {"xi-api-key": api_key}
        self.logger = None  # Will be set by PodcastGenerator
    
    def text_to_speech(self, text, voice_id, output_file, voice_settings=None, model_id=None):
        """Convert text to speech with advanced voice customization"""
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        # Use provided model_id or default
        if model_id is None:
            model_id = "eleven_multilingual_v2"
        
        # Default voice settings (fallback)
        default_settings = {
            "stability": 0.7,
            "similarity_boost": 0.8,
            "style": 0.4,
            "use_speaker_boost": True
        }
        
        # Use provided settings or defaults
        final_settings = default_settings.copy()
        if voice_settings:
            final_settings.update(voice_settings)
        
        data = {
            "text": text, 
            "model_id": model_id,
            "voice_settings": final_settings
        }
        
        # Log API call details
        if self.logger:
            self.logger.log_api_call(text, voice_id, final_settings, model_id, output_file)
        else:
            # Fallback to console logging
            settings_summary = f"stability={final_settings['stability']:.1f}, style={final_settings['style']:.1f}"
            print(f"🔊 Converting with {settings_summary}: '{text[:40]}...'")
        
        response = requests.post(url, json=data, headers=self.headers)
        
        if response.status_code != 200:
            print(f"✗ API Error: {response.status_code} - {response.text}")
            return None
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        # Verify file creation
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            file_size = os.path.getsize(output_file)
            print(f"✓ Created {output_file} ({file_size:,} bytes)")
            return output_file
        else:
            print(f"✗ Failed to create {output_file}")
            return None