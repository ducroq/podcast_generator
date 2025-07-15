"""
Main podcast generator class that orchestrates the entire process
"""

from .elevenlabs_client import ElevenLabsClient
from .ssml_processor import SSMLProcessor
from .audio_processor import AudioProcessor

class PodcastGenerator:
    """Main class for generating podcasts from scripts"""
    
    def __init__(self, api_key, host_a_voice, host_b_voice, host_a_volume=0, host_b_volume=0):
        self.elevenlabs = ElevenLabsClient(api_key)
        self.ssml_processor = SSMLProcessor()
        self.audio_processor = AudioProcessor()
        
        self.host_a_voice = host_a_voice
        self.host_b_voice = host_b_voice
        self.host_a_volume = host_a_volume
        self.host_b_volume = host_b_volume
        
        # Host personalities
        self.host_a_settings = {
            "stability": 0.7,     # More stable/professional
            "similarity_boost": 0.8,
            "style": 0.3          # Less dramatic
        }
        
        self.host_b_settings = {
            "stability": 0.4,     # More expressive/curious
            "similarity_boost": 0.7,
            "style": 0.6          # More animated
        }
    
    def create_podcast(self, script, output_name):
        """Create complete podcast from script"""
        audio_files = []
        temp_files = []
        pause_indices = []  # Track where pauses should be
        
        # Parse script for different speakers
        lines = script.split('\n')
        segment_count = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for emotion markers
            emotion_settings = self.ssml_processor.extract_emotion(line)
            
            if line.startswith('[HOST A]:'):
                text = line.replace('[HOST A]:', '').strip()
                text = self.ssml_processor.process_text(text)
                if text:
                    settings = {**self.host_a_settings, **emotion_settings}
                    file = f"temp_a_{i}.mp3"
                    result = self.elevenlabs.text_to_speech(text, self.host_a_voice, file, settings)
                    if result:
                        audio_files.append(file)
                        temp_files.append(file)
                        segment_count += 1
                    else:
                        print(f"Skipping failed conversion: {text}")
            
            elif line.startswith('[HOST B]:'):
                text = line.replace('[HOST B]:', '').strip()
                text = self.ssml_processor.process_text(text)
                if text:
                    settings = {**self.host_b_settings, **emotion_settings}
                    file = f"temp_b_{i}.mp3"
                    result = self.elevenlabs.text_to_speech(text, self.host_b_voice, file, settings)
                    if result:
                        audio_files.append(file)
                        temp_files.append(file)
                        segment_count += 1
                    else:
                        print(f"Skipping failed conversion: {text}")
            
            elif '[PAUZE]' in line:
                # Mark this position for a longer pause
                pause_indices.append(segment_count - 1)  # After current segment
        
        # Combine all audio files with smart gaps
        output_file = f"{output_name}.mp3"
        result = self.audio_processor.combine_audio_segments(
            audio_files, output_file, pause_indices=pause_indices,
            host_a_volume=self.host_a_volume, host_b_volume=self.host_b_volume
        )
        
        # Cleanup temp files
        self.audio_processor.cleanup_temp_files(temp_files)
        
        return result