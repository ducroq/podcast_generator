"""
Main podcast generator class that orchestrates the entire process
with advanced voice settings support and detailed logging
ENHANCED VERSION - Compatible with improved SSML processor
"""

from .elevenlabs_client import ElevenLabsClient
from .ssml_processor import SSMLProcessor
from .audio_processor import AudioProcessor
from pathlib import Path
import os
import re

class PodcastGenerator:
    """Main class for generating podcasts from scripts with voice-specific settings"""
    
    def __init__(self, config):
        self.config = config
        self.elevenlabs = ElevenLabsClient(config['api_key'])
        
        # Initialize SSML processor with detailed logging option
        enable_ssml_logging = config.get('enable_detailed_logging', False)
        self.ssml_processor = SSMLProcessor(
            config['voice_settings'], 
            enable_detailed_logging=enable_ssml_logging
        )
        
        self.audio_processor = AudioProcessor()
        
        # Voice mapping
        self.voices = config['voices']
        self.voice_aliases = config.get('voice_aliases', {})
        
        # Logging will be setup when create_podcast is called
        self.logger = None
        
        print(f"✓ Initialized with voices: {list(self.voices.keys())}")
        print(f"✓ Voice aliases: {self.voice_aliases}")
        if enable_ssml_logging:
            print(f"📋 SSML detailed logging: ENABLED")
    
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
    
    def _process_speaker_line(self, line, line_number, actual_voice_name):
        """Enhanced processing of a speaker line with multi-emotion support"""
        
        # Extract all emotions from the line
        emotions_found = self.ssml_processor.extract_all_emotions(line)
        
        # Check for multi-emotion scenarios
        if len(emotions_found) > 1:
            self.logger.info(f"MULTI-EMOTION LINE DETECTED at line {line_number}: {emotions_found}")
            print(f"🎭 Multi-emotion detected: {emotions_found}")
            
            # For now, use primary emotion but log the complexity
            primary_emotion = emotions_found[0]
            self.logger.warning(f"Using primary emotion {primary_emotion} for complex line")
            
            # Future enhancement: could split into segments here
            # segments = self.ssml_processor.process_text_with_emotion_splits(line, actual_voice_name)
        
        # Get emotion settings using enhanced method
        emotion_settings = self.ssml_processor.extract_emotion(line, actual_voice_name)
        
        # Get default voice settings
        default_settings = self.ssml_processor.get_default_voice_settings(actual_voice_name)
        
        # Merge settings (emotion overrides defaults)
        final_settings = {**default_settings, **emotion_settings}
        
        return emotions_found, final_settings
    
    def _parse_speaker_line(self, line):
        """Parse speaker line and extract speaker name and text"""
        # Enhanced parsing to handle various formats
        line = line.strip()
        
        # Format: [SPEAKER_NAME]: content
        speaker_match = re.match(r'\[(\w+)\]:\s*(.*)', line)
        if speaker_match:
            speaker_name = speaker_match.group(1).lower()
            text = speaker_match.group(2).strip()
            return speaker_name, text
        
        return None, None
    
    def _should_skip_line(self, line):
        """Check if line should be skipped"""
        line = line.strip()
        
        # Skip empty lines
        if not line:
            return True
        
        # Skip comment lines
        if line.startswith('#') or line.startswith('//'):
            return True
        
        # Skip section headers
        if line.startswith('===') or line.startswith('---'):
            return True
        
        return False
    
    def create_podcast(self, script, output_name, temp_file_folder):
        """Create complete podcast from script with enhanced voice-specific settings"""
        # Setup logging for this session
        logger, log_file = self._setup_logging(output_name)
        self.logger = logger  # Store for use in other methods
        
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
        
        # Enhanced script preprocessing
        script_lines = self._preprocess_script(script)
        logger.info(f"Processed script into {len(script_lines)} segments")
        
        segment_count = 0
        
        for i, line in enumerate(script_lines):
            # Skip lines that shouldn't be processed
            if self._should_skip_line(line):
                continue
            
            # Handle special pause markers
            if '[PAUZE]' in line or '(lange stilte)' in line:
                pause_indices.append(segment_count - 1)
                logger.info(f"Added pause marker after segment {segment_count - 1}")
                continue
            
            # Parse speaker line
            speaker_name, text = self._parse_speaker_line(line)
            
            if not speaker_name or not text:
                logger.warning(f"Could not parse line {i}: {line}")
                continue
            
            # Resolve voice ID and name
            voice_id, actual_voice_name = self._resolve_voice_id(speaker_name)
            
            # Enhanced processing with multi-emotion support
            emotions_found, final_settings = self._process_speaker_line(line, i, actual_voice_name)
            
            # Process SSML markup with enhanced processor
            processed_text = self.ssml_processor.process_text(text, actual_voice_name)
            
            # Enhanced logging entry
            log_entry = f"""
=== PROCESSING: {speaker_name} ({actual_voice_name}) ===
Line {i}: {line[:100]}{'...' if len(line) > 100 else ''}
Original text: {text}
Detected emotions: {emotions_found}
Emotion settings: {final_settings}
Processed text: {processed_text}
Voice ID: {voice_id}
=============================================
"""
            logger.info(log_entry)
            
            # Enhanced console output
            emotions_str = ', '.join(emotions_found) if emotions_found else 'none'
            print(f"🎭 {speaker_name}: emotions=[{emotions_str}]")
            print(f"📝 Processing: '{processed_text[:60]}{'...' if len(processed_text) > 60 else ''}'")
            
            if processed_text:
                file = os.path.join(temp_file_folder, f"temp_{actual_voice_name}_{segment_count}.mp3")
                
                # Enhanced API call logging
                api_log = f"""
=== ELEVENLABS API CALL ===
Text sent to API: {processed_text}
Voice ID: {voice_id}
Model: {self.config['audio']['model']}
Voice settings: {final_settings}
Output file: {file}
Emotions applied: {emotions_found}
===========================
"""
                logger.info(api_log)
                
                # Enhanced console output for API call
                settings_summary = f"stability={final_settings.get('stability', 0.7):.2f}, style={final_settings.get('style', 0.4):.2f}"
                print(f"🔊 TTS with {settings_summary}")
                
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
                    
                    # Get file size for detailed logging
                    try:
                        file_size = os.path.getsize(file)
                        logger.info(f"SUCCESS: Created {file} ({file_size:,} bytes)")
                        print(f"✅ Generated segment {segment_count}")
                    except:
                        logger.info(f"SUCCESS: Created {file}")
                        print(f"✅ Generated segment {segment_count}")
                else:
                    error_msg = f"FAILED: TTS conversion for line {i}: {processed_text[:50]}..."
                    logger.error(error_msg)
                    print(f"❌ {error_msg}")
        
        if not audio_files:
            error_msg = "No audio files generated!"
            logger.error(error_msg)
            print(f"❌ {error_msg}")
            return None
        
        # Get voice-specific volume adjustments
        voice_volumes = {}
        for voice_name in self.voices.keys():
            voice_volumes[voice_name] = self.ssml_processor.get_voice_volume_adjustment(voice_name)
        
        # Enhanced audio combination logging
        audio_log = f"""
=== AUDIO COMBINATION ===
Audio files: {audio_files}
Voice volumes: {voice_volumes}
Pause indices: {pause_indices}
Final output: {output_name}.mp3
Total segments: {len(audio_files)}
=========================
"""
        logger.info(audio_log)
        
        print(f"🎵 Combining {len(audio_files)} audio segments...")
        
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
        
        # Enhanced final logging and cleanup
        if result:
            # Get final file size and duration info
            try:
                import os
                if os.path.exists(result):
                    file_size = os.path.getsize(result)
                    success_msg = f"SUCCESS: Generated {result} ({file_size:,} bytes)"
                    
                    # Estimate duration (rough calculation)
                    estimated_duration = len(audio_files) * 3  # Rough estimate of 3 seconds per segment
                    success_msg += f", estimated duration: ~{estimated_duration}s"
                else:
                    success_msg = f"SUCCESS: Generated {result}"
            except:
                success_msg = f"SUCCESS: Generated {result}"
            
            logger.info(success_msg)
            logger.info(f"Processing complete. Total segments processed: {segment_count}")
            
            print(f"✅ {success_msg}")
            print(f"📊 Processed {segment_count} segments total")
            print(f"📋 Detailed log saved to: {log_file}")
            
            # Summary of emotions used
            if hasattr(self.ssml_processor, 'detailed_logging') and self.ssml_processor.detailed_logging:
                print(f"📝 Check log for detailed SSML processing information")
        
        return result
    
    def _preprocess_script(self, script):
        """Preprocess script to handle various formats and clean up"""
        lines = script.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines during preprocessing, but include them for processing
            # This allows the main loop to handle them appropriately
            processed_lines.append(line)
        
        return processed_lines
    
    def get_processing_stats(self):
        """Get statistics about the last processing run"""
        if not self.logger:
            return None
        
        # This could be enhanced to parse the log and return stats
        # For now, just return basic info
        return {
            "voices_used": list(self.voices.keys()),
            "voice_aliases": self.voice_aliases,
            "ssml_detailed_logging": hasattr(self.ssml_processor, 'detailed_logging')
        }