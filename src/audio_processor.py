"""
Audio processing utilities for combining and normalizing audio files
with voice-specific volume adjustments
"""

import os

# Setup FFmpeg BEFORE importing pydub to avoid warnings
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

from pydub import AudioSegment
from pydub.effects import normalize

class AudioProcessor:
    """Handles audio file operations and processing with advanced voice balancing"""
    
    def __init__(self):
        self._setup_ffmpeg()
    
    def _setup_ffmpeg(self):
        """Setup FFmpeg paths"""
        ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
        ffprobe_path = r"C:\ffmpeg\bin\ffprobe.exe"
        
        if os.path.exists(ffmpeg_path):
            AudioSegment.converter = ffmpeg_path
            AudioSegment.ffmpeg = ffmpeg_path
            AudioSegment.ffprobe = ffprobe_path
            print(f"✓ Using FFmpeg at: {ffmpeg_path}")
        else:
            print(f"✗ FFmpeg not found at {ffmpeg_path}")
            exit(1)
    
    def combine_audio_segments(self, audio_files, output_file, pause_indices=None, voice_volumes=None, normal_gap=150, pause_gap=800):
        """Combine multiple audio files with voice-specific volume balancing"""
        segments = []
        voice_volumes = voice_volumes or {}
        
        print(f"🎵 Combining {len(audio_files)} audio segments...")
        print(f"📊 Voice volumes: {voice_volumes}")
        
        for file in audio_files:
            if file and os.path.exists(file):
                segment = AudioSegment.from_mp3(file)
                
                # Apply voice-specific volume adjustment
                volume_adjustment = 0
                for voice_name, volume in voice_volumes.items():
                    if f'temp_{voice_name}_' in file:
                        volume_adjustment = volume
                        print(f"🔊 Applying {volume:+d}dB to {voice_name}")
                        break
                
                if volume_adjustment != 0:
                    segment = segment + volume_adjustment
                
                segments.append(segment)
                print(f"✓ Loaded {file} ({len(segment)}ms, {volume_adjustment:+d}dB)")
        
        if not segments:
            print("✗ No valid audio segments to combine")
            return None
        
        # Combine all segments with smart gaps
        final_audio = AudioSegment.empty()
        pause_indices = pause_indices or []
        
        for i, segment in enumerate(segments):
            final_audio += segment
            
            # Add gap only if not the last segment
            if i < len(segments) - 1:
                if i in pause_indices:
                    # Longer pause after [PAUZE] markers
                    gap_duration = pause_gap
                    final_audio += AudioSegment.silent(duration=gap_duration)
                    print(f"🔇 Added {gap_duration}ms pause after segment {i}")
                else:
                    # Short natural gap between speakers
                    final_audio += AudioSegment.silent(duration=normal_gap)
        
        # Final normalization of entire podcast
        print("🎚️ Normalizing final audio...")
        final_audio = normalize(final_audio)
        
        # Export with quality settings
        final_audio.export(output_file, format="mp3", bitrate="128k")
        
        duration_minutes = len(final_audio) / 1000 / 60
        print(f"✓ Combined podcast: {output_file} ({duration_minutes:.1f} minutes)")
        
        return output_file
    
    def create_pause(self, duration_ms):
        """Create a silent audio segment"""
        return AudioSegment.silent(duration=duration_ms)
    
    def cleanup_temp_files(self, file_list):
        """Remove temporary audio files"""
        cleaned_count = 0
        for file in file_list:
            if os.path.exists(file):
                os.remove(file)
                cleaned_count += 1
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned up {cleaned_count} temporary files")