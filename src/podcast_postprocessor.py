#!/usr/bin/env python3
"""
Standalone Podcast Post-Processor

Professional mastering chain for podcast audio using SoX and FFmpeg.
Inspired by Elliot Williams' Hackaday Podcast workflow.

Usage:
    python podcast_postprocessor.py input.mp3 [output.mp3]
    python podcast_postprocessor.py --analyze input.mp3
    python podcast_postprocessor.py --batch directory/
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse
import json
from datetime import datetime

class PodcastPostProcessor:
    """Professional podcast post-processing with SoX mastering chain"""

    def __init__(self, enable_mastering=True, quality_preset="podcast", debug=False):
        self.enable_mastering = enable_mastering
        self.quality_preset = quality_preset
        self.debug = debug
        
        self.temp_dir = Path("temp_mastering")
        self.temp_dir.mkdir(exist_ok=True)

        self.presets = {
            "podcast": {
                "name": "Podcast Standard",
                "description": "Optimized for speech, broadcast-ready",
                "mp3_bitrate": "192k",
                "normalization": "-3", # dB value, gives -3dB peak level
                "compression": "medium"
            },
            "audiobook": {
                "name": "Audiobook Quality",
                "description": "High quality for long listening with balanced dynamics",
                "mp3_bitrate": "128k",
                "normalization": "-3", # Conservative for long listening
                "compression": "heavy"
            },
            "broadcast": {
                "name": "Broadcast Standard",
                "description": "Radio/TV broadcast ready with higher loudness",
                "mp3_bitrate": "320k",
                "normalization": "-1", # Louder for broadcast
                "compression": "light"
            },
            "voice_only": {
                "name": "Voice Only",
                "description": "Maximum intelligibility with strong compression",
                "mp3_bitrate": "128k",
                "normalization": "-1", # Can be louder since it's heavily compressed
                "compression": "heavy"
            }
        }

        self._setup_sox()
        self._setup_ffmpeg() # FFmpeg setup is crucial now for analysis and MP3 output

    def _setup_sox(self):
        """Setup SoX for mastering by finding its executable and checking its version."""
        self.sox_available = False
        self.sox_path = None

        if not self.enable_mastering:
            print("🚫 Mastering disabled by user request. Skipping SoX setup.")
            return

        sox_locations = [
            'sox',  # Check if in system PATH first
            r'C:\Program Files (x86)\sox-14-4-2\sox.exe', # Your specific path
            r'C:\Program Files\sox-14-4-2\sox.exe',
            r'C:\sox\sox.exe',
            r'C:\Program Files\SoX\sox.exe',
            '/usr/bin/sox',  # Linux
            '/usr/local/bin/sox',  # macOS
        ]

        print("🔍 Searching for SoX...")
        for sox_candidate_path in sox_locations:
            try:
                result = subprocess.run([sox_candidate_path, '--version'],
                                        capture_output=True, text=True, check=True, timeout=5, encoding='utf-8')
                
                self.sox_available = True
                self.sox_path = sox_candidate_path
                
                version_line = result.stdout.strip()
                if "SoX v" in version_line:
                    version_info = version_line.split("SoX v")[-1].splitlines()[0].strip()
                    print(f"✓ SoX found at: {self.sox_path}")
                    print(f"✓ SoX version: v{version_info}")
                else:
                    print(f"✓ SoX found at: {self.sox_path}, but version output was unexpected.")
                    print(f"   Output: {version_line[:50]}...")
                
                break
            except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                continue

        if not self.sox_available:
            print("⚠️ SoX not found - mastering will be disabled.")
            print("⚠️ Please install SoX from: https://sourceforge.net/projects/sox/")
            print("⚠️ Tried locations:")
            for loc in sox_locations:
                print(f"   - {loc}")
            self.enable_mastering = False

    def _setup_ffmpeg(self):
        """Setup FFmpeg (ffmpeg and ffprobe) for format conversion and analysis."""
        self.ffmpeg_available = False
        self.ffmpeg_path = None
        self.ffprobe_path = None

        ffmpeg_locations = [
            'ffmpeg',  # Check if in system PATH
            r'C:\ffmpeg\bin\ffmpeg.exe', # Common Windows path
            r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
            '/usr/bin/ffmpeg',  # Linux
            '/usr/local/bin/ffmpeg',  # macOS
        ]
        ffprobe_locations = [
            'ffprobe', # Check if in system PATH
            r'C:\ffmpeg\bin\ffprobe.exe',
            r'C:\Program Files\ffmpeg\bin\ffprobe.exe',
            '/usr/bin/ffprobe',
            '/usr/local/bin/ffprobe',
        ]

        print("🔍 Searching for FFmpeg...")
        for ffmpeg_candidate_path in ffmpeg_locations:
            try:
                subprocess.run([ffmpeg_candidate_path, '-version'],
                               capture_output=True, text=True, check=True, timeout=5, encoding='utf-8')
                self.ffmpeg_path = ffmpeg_candidate_path
                print(f"✓ FFmpeg found at: {self.ffmpeg_path}")
                break
            except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                continue

        print("🔍 Searching for FFprobe...")
        for ffprobe_candidate_path in ffprobe_locations:
            try:
                subprocess.run([ffprobe_candidate_path, '-version'],
                               capture_output=True, text=True, check=True, timeout=5, encoding='utf-8')
                self.ffprobe_path = ffprobe_candidate_path
                print(f"✓ FFprobe found at: {self.ffprobe_path}")
                break
            except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                continue
        
        if self.ffmpeg_path and self.ffprobe_path:
            self.ffmpeg_available = True
        else:
            print("⚠️ FFmpeg (or FFprobe) not fully found - format conversion or analysis may be limited.")
            print("⚠️ Please install FFmpeg from: https://ffmpeg.org/download.html and ensure both `ffmpeg.exe` and `ffprobe.exe` are in your PATH or accessible.")


    def get_preset_info(self, preset_name):
        """Get information about a preset. Defaults to 'podcast' if not found."""
        return self.presets.get(preset_name, self.presets["podcast"])

    def list_presets(self):
        """List all available presets."""
        print("\n---")
        print("📋 Available quality presets:")
        for name, info in self.presets.items():
            print(f"  ✨ {name}: {info['name']}")
            print(f"    ➡️ {info['description']}")
            print(f"    ➡️ Output Bitrate: {info['mp3_bitrate']}, Normalization: {info['normalization']}")
        print("---\n")

    def apply_mastering_chain(self, input_file_path, output_file_path, preset=None):
        """
        Apply professional mastering chain to an audio file.

        Args:
            input_file_path (str): Path to the input audio file.
            output_file_path (str): Path to the desired output audio file.
            preset (str, optional): Name of the quality preset to use. Defaults to self.quality_preset.
        """
        input_file = Path(input_file_path)
        output_file = Path(output_file_path)

        if not self.enable_mastering or not self.sox_available:
            print(f"⚠️ Mastering disabled or SoX not available - copying {input_file.name} directly to {output_file.name}")
            shutil.copy2(input_file, output_file)
            return output_file

        preset_info = self.get_preset_info(preset or self.quality_preset)
        print(f"🎚️ Applying mastering chain: {preset_info['name']}")
        print(f"📝 {preset_info['description']}")

        temp_wav_input = self.temp_dir / "audio_raw.wav"
        temp_mastered_output = self.temp_dir / "audio_mastered.wav"

        try:
            # Step 1: Convert input to WAV for SoX processing using FFmpeg primarily
            print("🔄 Converting input to WAV for processing...")
            if not input_file.suffix.lower() == '.wav':
                if self.ffmpeg_available:
                    ffmpeg_convert_cmd = [
                        self.ffmpeg_path, '-i', str(input_file), '-y', # -y to overwrite output file
                        '-acodec', 'pcm_s16le', '-ar', '44100', # 16-bit PCM, 44.1 kHz sample rate
                        str(temp_wav_input)
                    ]
                    subprocess.run(ffmpeg_convert_cmd, check=True, capture_output=True)
                elif self.sox_available: # Fallback to SoX for conversion if FFmpeg isn't there
                    print("⚠️ FFmpeg not available for conversion. Falling back to SoX (may be less robust for some formats).")
                    sox_convert_cmd = [self.sox_path, str(input_file), str(temp_wav_input)]
                    subprocess.run(sox_convert_cmd, check=True, capture_output=True)
                else:
                    raise RuntimeError("Neither FFmpeg nor SoX available for WAV conversion.")
            else:
                shutil.copy2(input_file, temp_wav_input)

            if not temp_wav_input.exists() or temp_wav_input.stat().st_size == 0:
                raise RuntimeError(f"Failed to create temporary WAV file: {temp_wav_input}. Conversion may have failed.")

            # Step 2: Apply mastering chain with SoX
            print("🎛️ Applying SoX mastering effects:")
            sox_effects_steps = [
                "→ Noise gate (compand-based silence/noise removal)",
                "→ High-pass filter (remove rumble/DC offset)",
                "→ Compression (dynamic range control)",
                "→ EQ (frequency balancing)",
                "→ De-esser (reduce harsh 's' sounds for Dutch speech)",
                "→ Limiting (prevent clipping)",
                "→ Safety limiter (final clip protection)",
                "→ Normalization (optimal loudness)"
            ]

            for step in sox_effects_steps:
                print(f"   {step}")

            # Build SoX command - use compand for noise gating instead of gate effect
            sox_cmd = [self.sox_path, str(temp_wav_input), str(temp_mastered_output)]

            # 1. Noise gate using compand - SoX doesn't have a separate gate effect
            # Format: compand attack,decay transfer_function gain initial_volume delay
            # This acts as a noise gate: signals below -40dB are heavily attenuated
            sox_cmd.extend(['compand', '0.1,0.2', '-inf,-40.1,-inf,-40,-40', '0', '-90', '0.1'])

            # 2. High-pass filter - remove low-frequency rumble
            sox_cmd.extend(['highpass', '80'])

            # 3. Compression with careful parameter handling
            if preset_info.get('compression') == 'heavy':
                # Attack,decay transfer_function gain initial_volume delay
                sox_cmd.extend(['compand', '0.05,0.2', '6:-40,-40,-25,-25,-15,-15', '0', '-90', '0.1'])
                sox_cmd.extend(['gain', '-8'])  # Apply -8dB gain reduction separately
            elif preset_info.get('compression') == 'light':
                sox_cmd.extend(['compand', '0.1,0.3', '6:-25,-25,-15,-15,-5,-5', '0', '-90', '0.2'])
                sox_cmd.extend(['gain', '-3'])  # Apply -3dB gain reduction separately
            else:  # medium
                sox_cmd.extend(['compand', '0.05,0.2', '6:-30,-30,-20,-20,-10,-10', '0', '-90', '0.1'])
                sox_cmd.extend(['gain', '-6'])  # Apply -6dB gain reduction separately

            # 4. EQ
            sox_cmd.extend(['equalizer', '200', '0.7', '2'])    # Warmth/body
            sox_cmd.extend(['equalizer', '3000', '0.5', '1.5']) # Presence/intelligibility
            sox_cmd.extend(['equalizer', '8000', '0.3', '-2'])  # Reduce harshness/sibilance more aggressively

            # 5. De-esser - reduce harsh 's' sounds (sibilants) for Dutch speech
            # Target the 6-8kHz range where sibilants are most prominent
            sox_cmd.extend(['compand', '0.01,0.05', '6:-15,-15,-10,-8,-5,-5', '0', '-90', '0.01'])
            sox_cmd.extend(['equalizer', '6500', '0.8', '-3'])  # Additional sibilant reduction

            # 6. Light limiting using compand
            sox_cmd.extend(['compand', '0.01,0.02', '6:-20,-20,-10,-10', '0', '-90', '0.01'])

            # 7. Safety limiter to prevent any clipping
            sox_cmd.extend(['compand', '0.001,0.001', '6:-6,-6,-3,-3,0,-3', '0', '-90', '0.001'])

            # 8. Final normalization
            sox_cmd.extend(['norm', preset_info['normalization']])

            print("Executing SoX command...")
            if self.debug:
                print(f"DEBUG: SoX command: {' '.join(sox_cmd)}")
            sox_process_result = subprocess.run(sox_cmd, check=True, capture_output=True, encoding='utf-8')
            
            # Step 3: Convert mastered WAV to final output format (MP3, WAV, etc.)
            if output_file.suffix.lower() == '.mp3':
                print("💿 Converting mastered WAV to final MP3...")
                if self.ffmpeg_available:
                    ffmpeg_output_cmd = [
                        self.ffmpeg_path, '-i', str(temp_mastered_output), '-y',
                        '-codec:a', 'libmp3lame',
                        '-b:a', preset_info['mp3_bitrate'],
                        '-ar', '44100',
                        str(output_file)
                    ]
                    subprocess.run(ffmpeg_output_cmd, check=True, capture_output=True)
                else:
                    print("❌ FFmpeg not available for MP3 encoding. Outputting to WAV instead.")
                    # Change output file extension to .wav if MP3 requested but cannot be encoded
                    output_file = output_file.with_suffix('.wav')
                    shutil.copy2(str(temp_mastered_output), output_file)
            else:
                # For other formats (e.g., WAV output), just copy the mastered WAV
                shutil.copy2(str(temp_mastered_output), output_file)

            file_size_bytes = Path(output_file).stat().st_size
            print(f"✅ Mastering complete: {output_file.name}")
            print(f"📊 Output size: {file_size_bytes / (1024*1024):.2f} MB")

            return str(output_file)

        except subprocess.CalledProcessError as e:
            print(f"❌ Mastering failed for {input_file.name}: SoX process error")
            if self.debug:
                print(f"   Command: {' '.join(e.cmd)}")
                if e.stdout:
                    print(f"   Stdout: {e.stdout.strip()[:200]}...")
                if e.stderr:
                    print(f"   Stderr: {e.stderr.strip()[:200]}...")
            elif e.stderr and len(e.stderr.strip()) < 200:
                print(f"   Error: {e.stderr.strip()}")
            
            print(f"   Using original file as fallback...")
            shutil.copy2(input_file, output_file)
            return str(output_file)
        except FileNotFoundError as e:
            print(f"❌ Mastering failed: Executable not found. Error: {e}")
            print(f"   Ensure SoX and FFmpeg are correctly installed and in your system's PATH, or their hardcoded paths are correct.")
            print(f"   Copying original file to {output_file.name} as fallback.")
            shutil.copy2(input_file, output_file)
            return str(output_file)
        except Exception as e:
            print(f"❌ An unexpected error occurred during mastering of {input_file.name}: {e}")
            print(f"   Copying original file to {output_file.name} as fallback.")
            shutil.copy2(input_file, output_file)
            return str(output_file)

    def analyze_audio_quality(self, audio_file_path):
        """Analyze audio quality using FFprobe (instead of SoX) for broader format support."""
        audio_file = Path(audio_file_path)

        if not self.ffmpeg_available or not self.ffprobe_path:
            print("⚠️ FFprobe not available - skipping quality analysis.")
            return None

        try:
            print(f"\n📊 Analyzing audio quality for: {audio_file.name} using FFprobe")

            # FFprobe command to get stream and format info in JSON format
            ffprobe_cmd = [
                self.ffprobe_path,
                '-v', 'quiet',  # Suppress verbose output
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                '-i', str(audio_file)
            ]
            
            result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True, encoding='utf-8')
            info = json.loads(result.stdout)

            metrics = {}
            audio_stream = None

            # Find the first audio stream
            for stream in info.get('streams', []):
                if stream.get('codec_type') == 'audio':
                    audio_stream = stream
                    break

            if audio_stream:
                metrics['codec_name'] = audio_stream.get('codec_name')
                metrics['sample_rate'] = audio_stream.get('sample_rate')
                metrics['channels'] = audio_stream.get('channels')
                metrics['bit_rate'] = audio_stream.get('bit_rate')
                metrics['duration_seconds'] = float(audio_stream.get('duration', 0)) if audio_stream.get('duration') else 'N/A'
                metrics['loudness_integrated_lufs'] = 'N/A' # FFprobe doesn't directly give LUFS without a filter
                
                # Try to get peak and RMS level using FFmpeg's volumedetect filter
                # This is a separate FFmpeg call, as ffprobe itself doesn't do this easily.
                # Only if ffmpeg is available
                if self.ffmpeg_path:
                    try:
                        volumedetect_cmd = [
                            self.ffmpeg_path,
                            '-i', str(audio_file),
                            '-af', 'volumedetect',
                            '-vn', '-sn', '-dn', # Disable video, subtitle, data streams
                            '-f', 'null',
                            '-' # Output to stdout
                        ]
                        vol_result = subprocess.run(volumedetect_cmd, capture_output=True, text=True, check=False, encoding='utf-8') # check=False because volumedetect often returns non-zero for verbose output
                        
                        # Parse volumedetect output (usually in stderr)
                        vol_lines = vol_result.stderr.splitlines()
                        for line in vol_lines:
                            if 'max_volume:' in line:
                                metrics['peak_level_db'] = line.split('max_volume:')[1].strip().split(' ')[0]
                            elif 'mean_volume:' in line:
                                metrics['rms_level_db'] = line.split('mean_volume:')[1].strip().split(' ')[0]

                    except Exception as ve:
                        print(f"  ⚠️  Could not run volumedetect with FFmpeg: {ve}")

            print(f"\n📊 Audio Quality Metrics for {audio_file.name}:")
            print(f"  🎵 Codec: {metrics.get('codec_name', 'N/A')}")
            print(f"  🎵 Duration: {metrics.get('duration_seconds', 'N/A'):.2f} seconds")
            print(f"  🔊 Peak Level: {metrics.get('peak_level_db', 'N/A')} dB")
            print(f"  📈 RMS Level (Mean Volume): {metrics.get('rms_level_db', 'N/A')} dB")
            print(f"  📊 Sample Rate: {metrics.get('sample_rate', 'N/A')} Hz")
            print(f"  ➡️ Channels: {metrics.get('channels', 'N/A')}")
            print(f"  ➡️ Bit Rate: {float(metrics.get('bit_rate', 0)) / 1000:.0f} kbps" if metrics.get('bit_rate') != 'N/A' else '  ➡️ Bit Rate: N/A')
            
            # Quality assessment (using FFprobe data)
            print(f"\n🎯 Quality Assessment:")
            try:
                peak_db = float(metrics.get('peak_level_db', '0').replace('dB', '').strip())
                rms_db = float(metrics.get('rms_level_db', '-30').replace('dB', '').strip())
                
                if peak_db > -0.5:
                    print(f"  ⚠️  Peak level is very high ({peak_db:.1f} dB) - potential clipping.")
                elif peak_db > -3.0:
                    print(f"  ✅ Peak level good ({peak_db:.1f} dB).")
                else:
                    print(f"  ℹ️  Peak level is low ({peak_db:.1f} dB) - could be louder.")

                if rms_db > -10.0:
                    print(f"  ⚠️  RMS level is very high ({rms_db:.1f} dB) - likely over-compressed.")
                elif rms_db < -20.0:
                    print(f"  ℹ️  RMS level is low ({rms_db:.1f} dB) - may sound too quiet.")
                else:
                    print(f"  ✅ RMS level good ({rms_db:.1f} dB).")
                                    
            except (ValueError, TypeError):
                print(f"  ⚠️  Could not perform numerical quality assessment due to missing or invalid metrics.")

            return metrics
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to analyze {audio_file.name}: FFprobe command failed.")
            if e.stdout:
                print(f"   Stdout:\n{e.stdout.strip()}")
            if e.stderr:
                print(f"   Stderr:\n{e.stderr.strip()}")
            print(f"   Command that failed: {' '.join(e.cmd)}")
            return None
        except FileNotFoundError as e:
            print(f"❌ Failed to analyze {audio_file.name}: FFprobe executable not found. Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse FFprobe JSON output for {audio_file.name}: {e}")
            print(f"   FFprobe raw output (if any):\n{result.stdout if 'result' in locals() else 'N/A'}")
            return None
        except Exception as e:
            print(f"❌ An unexpected error occurred during analysis of {audio_file.name}: {e}")
            return None

    def batch_process(self, input_directory_path, output_directory_path=None, preset=None):
        """Process all audio files in a directory."""
        input_path = Path(input_directory_path)

        if not input_path.exists():
            print(f"❌ Input directory not found: {input_directory_path}")
            return

        if output_directory_path is None:
            output_path = input_path / "mastered"
        else:
            output_path = Path(output_directory_path)
            
        output_path.mkdir(parents=True, exist_ok=True)

        audio_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac']
        audio_files = []
        
        for ext in audio_extensions:
            audio_files.extend(input_path.rglob(f"*{ext.lower()}"))
        
        audio_files = list(set(audio_files)) 
        audio_files.sort()

        if not audio_files:
            print(f"❌ No supported audio files found in {input_directory_path}")
            return

        print(f"\n---")
        print(f"📁 Processing {len(audio_files)} files from {input_directory_path}")
        print(f"📁 Output directory: {output_path}")
        print(f"---\n")

        for i, audio_file in enumerate(audio_files, 1):
            print(f"\n--- File {i}/{len(audio_files)} ---")
            print(f"🎵 Processing: {audio_file.name}")

            output_file_name = f"{audio_file.stem}_mastered.mp3"
            output_file = output_path / output_file_name

            processed_file_path = self.apply_mastering_chain(str(audio_file), str(output_file), preset)

            if processed_file_path and self.ffmpeg_available: # Use FFmpeg for analysis now
                print(f"\n📊 Quality analysis for output file:")
                self.analyze_audio_quality(processed_file_path)
            print("---\n")

        print(f"\n🎉 Batch processing complete!")
        print(f"📁 Check output directory: {output_path}")

    def cleanup(self):
        """Clean up temporary files and directories."""
        if self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir)
                print(f"🧹 Cleaned up temporary directory: {self.temp_dir}")
            except Exception as e:
                print(f"⚠️ Could not clean up temporary directory {self.temp_dir}: {e}")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Professional podcast post-processing with SoX mastering chain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python podcast_postprocessor.py input.mp3 output.mp3
  python podcast_postprocessor.py --analyze input.mp3
  python podcast_postprocessor.py --batch ./audio_files/
  python podcast_postprocessor.py --preset audiobook input.mp3 output.mp3
  python podcast_postprocessor.py --list-presets
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input audio file or directory')
    parser.add_argument('output', nargs='?', help='Output audio file (optional)')
    parser.add_argument('--analyze', action='store_true', help='Analyze audio quality only')
    parser.add_argument('--batch', action='store_true', help='Process all files in directory')
    parser.add_argument('--preset', choices=['podcast', 'audiobook', 'broadcast', 'voice_only'], 
                        default='podcast', help='Quality preset to use')
    parser.add_argument('--list-presets', action='store_true', help='List available presets')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--no-mastering', action='store_true', help='Disable mastering chain')
    
    args = parser.parse_args()
    
    processor = PodcastPostProcessor(
        enable_mastering=not args.no_mastering,
        quality_preset=args.preset,
        debug=args.debug
    )
    
    try:
        if args.list_presets:
            processor.list_presets()
            return
        
        if not args.input:
            parser.print_help()
            return
        
        if args.analyze:
            processor.analyze_audio_quality(args.input)
        elif args.batch:
            processor.batch_process(args.input, args.output, args.preset)
        else:
            input_path = Path(args.input)
            if not input_path.exists():
                print(f"❌ Input file not found: {args.input}")
                return
                
            if not args.output:
                args.output = f"{input_path.stem}_mastered.mp3"
            
            print(f"🎵 Processing single file: {input_path.name}")
            processed_output_path = processor.apply_mastering_chain(args.input, args.output, args.preset)
            
            if processed_output_path and processor.ffmpeg_available:
                print(f"\n📊 Quality analysis for output file:")
                processor.analyze_audio_quality(processed_output_path)
    
    finally:
        processor.cleanup()

if __name__ == "__main__":
    # --- How to circumvent arguments in an IDE for testing ---
    # Uncomment one of the following lines to simulate command-line arguments

    # Example 1: Simulate single file processing
    # sys.argv = ['podcast_postprocessor.py', 'input_audio.mp3', 'output_mastered.mp3']

    # Example 2: Simulate batch processing
    sys.argv = ['podcast_postprocessor.py', '--batch', r"C:\local_dev\Mondriaan_podcast\output\episode_00", r"C:\local_dev\Mondriaan_podcast\output_mastered", '--preset', 'podcast']
    
    # Example 3: Simulate analysis
    # sys.argv = ['podcast_postprocessor.py', '--analyze', r"C:\local_dev\Mondriaan_podcast\output\some_audio.mp3"]

    # Example 4: Simulate listing presets
    # sys.argv = ['podcast_postprocessor.py', '--list-presets']

    # Example 5: Simulate single file with specific preset and no output specified
    # sys.argv = ['podcast_postprocessor.py', '--preset', 'audiobook', r"C:\local_dev\Mondriaan_podcast\output\some_podcast.mp3"]

    main()