"""
Main podcast generator class that orchestrates the entire process
with advanced voice settings support and detailed logging
"""

from .elevenlabs_client import ElevenLabsClient
from .ssml_processor import SSMLProcessor
from .audio_processor import AudioProcessor
from pathlib import Path
import os

class PodcastGenerator:
    """Main class for generating podcasts from scripts with voice-specific settings"""
    
    def __init__(self, config):
        self.config = config
        self.elevenlabs = ElevenLabsClient(config['api_key'])
        self.ssml_processor = SSMLProcessor(config['voice_settings'])
        self.audio_processor = AudioProcessor()
        
        # Voice mapping
        self.voices = config['voices']
        self.voice_aliases = config.get('voice_aliases', {})
        
        # Logging will be setup when create_podcast is called
        self.logger = None
        
        print(f"✓ Initialized with voices: {list(self.voices.keys())}")
        print(f"✓ Voice aliases: {self.voice_aliases}")
    
    def _setup_logging(self, output_name):
        """Setup logging for this podcast generation session"""
        import logging
        from datetime import datetime
        from pathlib import Path
        
        # Create logs directory
        if hasattr(self, 'project_dir'):
            log_dir = Path(self.project_dir) / "logs"
        else:
            log_dir = Path("logs")
        
        log_dir.mkdir(exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        episode_name = Path(output_name).stem
        log_filename = f"{episode_name}_{timestamp}.log"
        log_file = log_dir / log_filename
        
        # Setup logger
        logger = logging.getLogger(f"podcast_{timestamp}")
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        print(f"📋 Logging to: {log_file}")
        return logger, log_file
    
    def _resolve_voice_id(self, voice_name):
        """Resolve voice name/alias to actual voice ID"""
        # Check if it's an alias first
        if voice_name in self.voice_aliases:
            actual_voice = self.voice_aliases[voice_name]
            if actual_voice in self.voices:
                return self.voices[actual_voice], actual_voice
        
        # Check if it's a direct voice name
        if voice_name in self.voices:
            return self.voices[voice_name], voice_name
        
        # Fallback
        print(f"⚠️ Voice '{voice_name}' not found, using default")
        default_voice = list(self.voices.keys())[0]
        return self.voices[default_voice], default_voice
    
    def create_podcast(self, script, output_name, temp_file_folder):
        """Create complete podcast from script with voice-specific settings"""
        # Setup logging for this session
        logger, log_file = self._setup_logging(output_name)
        
        audio_files = []
        temp_files = []
        pause_indices = []
        
        # Ensure output directory exists if we have project info
        if hasattr(self, 'output_dir'):
            import os
            os.makedirs(self.output_dir, exist_ok=True)
            # Make output path relative to output directory
            if not os.path.isabs(output_name):
                output_name = os.path.join(self.output_dir, output_name)
        
        logger.info(f"Starting podcast generation: {output_name}")
        logger.info(f"Script length: {len(script)} characters")
        
        # Parse script for different speakers
        lines = script.split('\n')
        segment_count = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Parse speaker format: [SPEAKER_NAME]: content
            if line.startswith('[') and ']:' in line:
                speaker_end = line.find(']:')
                speaker_name = line[1:speaker_end].lower()  # Convert to lowercase for matching
                text = line[speaker_end + 2:].strip()
                
                # Resolve voice ID and name
                voice_id, actual_voice_name = self._resolve_voice_id(speaker_name)
                
                # Get emotion settings specific to this voice
                emotion_settings = self.ssml_processor.extract_emotion(line, actual_voice_name)
                
                # Get default voice settings
                default_settings = self.ssml_processor.get_default_voice_settings(actual_voice_name)
                
                # Merge settings (emotion overrides defaults)
                final_settings = {**default_settings, **emotion_settings}
                
                # Process SSML markup
                processed_text = self.ssml_processor.process_text(text)
                
                # Log processing step
                log_entry = f"""
=== PROCESSING: {speaker_name} ({actual_voice_name}) ===
Original text: {text}
Detected emotions: {emotion_settings}
Voice settings: {final_settings}
Processed text: {processed_text}
=============================================
"""
                logger.info(log_entry)
                
                # Console output
                print(f"🎭 {speaker_name}: emotions={emotion_settings}")
                print(f"📝 Processed: '{processed_text[:60]}...'")
                
                if processed_text:
                    file = os.path.join(temp_file_folder, f"temp_{actual_voice_name}_{i}.mp3")
                    # file = os.path.join(self.output_name, f"temp_{actual_voice_name}_{i}.mp3")
                    # file = f"temp_{actual_voice_name}_{i}.mp3"
                    
                    # Log API call
                    api_log = f"""
=== ELEVENLABS API CALL ===
Text sent to API: {processed_text}
Voice ID: {voice_id}
Model: {self.config['audio']['model']}
Voice settings: {final_settings}
Output file: {file}
===========================
"""
                    logger.info(api_log)
                    
                    # Console output for API call
                    settings_summary = f"stability={final_settings['stability']:.1f}, style={final_settings['style']:.1f}"
                    print(f"🔊 Converting with {settings_summary}: '{processed_text[:40]}...'")
                    
                    result = self.elevenlabs.text_to_speech(
                        processed_text, 
                        voice_id, 
                        file, 
                        final_settings,
                        self.config['audio']['model']
                    )
                    
                    if result:
                        audio_files.append(file)
                        temp_files.append(file)
                        segment_count += 1
                        logger.info(f"SUCCESS: Created {file}")
                    else:
                        error_msg = f"FAILED: TTS conversion for: {processed_text[:50]}..."
                        logger.error(error_msg)
                        print(f"❌ {error_msg}")
            
            elif '[PAUZE]' in line:
                # Mark this position for a longer pause
                pause_indices.append(segment_count - 1)
                logger.info(f"Added pause marker after segment {segment_count - 1}")
        
        if not audio_files:
            error_msg = "No audio files generated!"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            return None
        
        # Get voice-specific volume adjustments
        voice_volumes = {}
        for voice_name in self.voices.keys():
            voice_volumes[voice_name] = self.ssml_processor.get_voice_volume_adjustment(voice_name)
        
        # Log audio combination
        audio_log = f"""
=== AUDIO COMBINATION ===
Audio files: {audio_files}
Voice volumes: {voice_volumes}
Final output: {output_name}.mp3
=========================
"""
        logger.info(audio_log)
        
        # Combine all audio files with smart gaps and voice-specific volumes
        output_file = f"{output_name}.mp3"
        
        # Check if audio_processor supports voice_volumes
        try:
            result = self.audio_processor.combine_audio_segments(
                audio_files, 
                output_file, 
                pause_indices=pause_indices,
                voice_volumes=voice_volumes,
                normal_gap=int(self.config['podcast']['default_pause_duration'] * 1000),
                pause_gap=int(self.config['podcast']['long_pause_duration'] * 1000)
            )
        except TypeError:
            # Fallback to old method without voice_volumes
            fallback_msg = "Using legacy audio processor without voice volume support"
            logger.warning(fallback_msg)
            print(f"⚠️ {fallback_msg}")
            result = self.audio_processor.combine_audio_segments(
                audio_files, 
                output_file, 
                pause_indices=pause_indices,
                normal_gap=int(self.config['podcast']['default_pause_duration'] * 1000),
                pause_gap=int(self.config['podcast']['long_pause_duration'] * 1000)
            )
        
        # Cleanup temp files
        # self.audio_processor.cleanup_temp_files(temp_files)
        
        if result:
            # Get file size for logging
            import os
            if os.path.exists(result):
                file_size = os.path.getsize(result)
                success_msg = f"SUCCESS: Generated {result} ({file_size:,} bytes)"
            else:
                success_msg = f"SUCCESS: Generated {result}"
            
            logger.info(success_msg)
            print(f"✅ {success_msg}")
            print(f"📋 Detailed log saved to: {log_file}")
        
        return result