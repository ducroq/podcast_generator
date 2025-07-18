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
    
    def text_to_speech(self, text, voice_id, output_file, voice_settings=None, model_id=None, enable_logging=False):
        """
        Convert text to speech with advanced voice customization.
        
        Args:
            text (str): The text to convert to speech.
            voice_id (str): The ID of the voice to use.
            output_file (str): The path to save the generated audio file.
            voice_settings (dict, optional): Dictionary of voice settings (stability, similarity_boost, etc.).
            model_id (str, optional): The ID of the model to use. Defaults to "eleven_multilingual_v2".
            enable_logging (bool, optional): If False, "Zero Retention Mode" is used for this request,
                                            meaning history features are unavailable and data is not logged.
                                            Defaults to False.
        """
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
            "voice_settings": final_settings,
            "enable_logging": enable_logging 
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
        

def main():
    import datetime
    from config_loader import load_config

    """
    Main function to load configuration and demonstrate ElevenLabs text-to-speech
    with minimal data retention. This function runs when the script is executed directly.
    """
    print("--- Running ElevenLabs Client Test with Zero Retention ---")
    
    try:
        config = load_config()
    except FileNotFoundError as e:
        print(f"Configuration error: {e}")
        print("Please ensure 'config/credentials/secrets.ini' and 'config/config.ini' exist and are correctly configured.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while loading config: {e}")
        return

    api_key = config['api_key']
    voices = config['voices']
    audio_settings = config['audio']

    if not api_key:
        print("Error: ElevenLabs API key not found in secrets.ini.")
        return
    if not voices:
        print("Error: No voices configured in config.ini. Please add at least one voice under the [voices] section.")
        return

    elevenlabs_client = ElevenLabsClient(api_key=api_key)

    text_to_convert = "This audio is generated directly from the elevenlabs_client.py script itself, using `enable_logging=False` for minimal data retention. It should not appear in your API history."
    
    # Use the first voice found in config.ini as the test voice
    test_voice_name = next(iter(voices)) 
    test_voice_id = voices[test_voice_name]

    # Create an output directory for audio files
    output_dir = "generated_audio"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a timestamped filename for uniqueness
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(output_dir, f"test_audio_{timestamp}.mp3")

    print(f"Using voice: '{test_voice_name}' (ID: {test_voice_id})")
    print(f"Using model: {audio_settings['model']}")
    print(f"Saving to: {output_filename}")

    generated_file = elevenlabs_client.text_to_speech(
        text=text_to_convert,
        voice_id=test_voice_id,
        output_file=output_filename,
        model_id=audio_settings['model'],
        enable_logging=False, # <--- THIS IS THE CRUCIAL SETTING FOR MINIMUM RETENTION
        # You can pass voice_settings from config if you define them:
        voice_settings=config['voice_settings'].get(test_voice_name) # Pass settings if they exist for the voice
    )

    if generated_file:
        print("\nTest completed: Audio file generated.")
        print("To verify minimal retention, check your ElevenLabs API history dashboard online.")
        print("This particular generation *should not* appear there because enable_logging was set to False.")
    else:
        print("\nTest failed: Audio file could not be generated.")

if __name__ == "__main__":
    main()        