"""
Audio processing utilities for combining and normalizing audio files
"""

import os

# Setup FFmpeg BEFORE importing pydub to avoid warnings
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

from pydub import AudioSegment
from pydub.effects import normalize

class AudioProcessor:
    """Handles audio file operations and processing"""
    
    def __init__(self):
        self._setup_ffmpeg()
    
    def _setup_ffmpeg(self):
        """Setup FFmpeg paths"""
        # Explicitly set FFmpeg paths
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
    
    def combine_audio_segments(self, audio_files, output_file, pause_indices=None, normal_gap=150, pause_gap=800, host_a_volume=0, host_b_volume=0):
        """Combine multiple audio files into one podcast with smart gaps and volume balancing"""
        segments = []
        
        for file in audio_files:
            if file and os.path.exists(file):
                segment = AudioSegment.from_mp3(file)
                
                # Volume balancing based on voice type
                if 'temp_a_' in file:  # HOST A
                    segment = segment + host_a_volume  # Apply HOST A volume adjustment
                elif 'temp_b_' in file:  # HOST B
                    segment = segment + host_b_volume  # Apply HOST B volume adjustment
                
                segments.append(segment)
        
        if not segments:
            print("No valid audio segments to combine")
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
                    final_audio += AudioSegment.silent(duration=pause_gap)
                else:
                    # Short natural gap between speakers
                    final_audio += AudioSegment.silent(duration=normal_gap)
        
        # Final normalization of entire podcast
        final_audio = normalize(final_audio)
        final_audio.export(output_file, format="mp3")
        
        print(f"✓ Combined {len(segments)} segments with smart timing and volume balancing")
        return output_file
    
    def create_pause(self, duration_ms):
        """Create a silent audio segment"""
        return AudioSegment.silent(duration=duration_ms)
    
    def cleanup_temp_files(self, file_list):
        """Remove temporary audio files"""
        for file in file_list:
            if os.path.exists(file):
                os.remove(file)