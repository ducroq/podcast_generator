# Project Documentation

# Project Structure
```
podcast_generator/
├── config/
│   ├── config_template.ini
├── docs/
│   ├── ssml_dsl_table.md
├── src/
│   ├── __init__.py
│   ├── audio_processor.py
│   ├── config_loader.py
│   ├── elevenlabs_client.py
│   ├── logging_utils.py
│   ├── podcast_generator.py
│   ├── project_utils.py
│   ├── ssml_processor.py
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
```

# config\config_template.ini
```text
# config.ini - Generic Podcast Configuration Template

[voices]
# Add your voice names and ElevenLabs Voice IDs here
# Examples:
# narrator = ABC123DEF456
# character1 = GHI789JKL012
# character2 = MNO345PQR678
# host = STU901VWX234

[voice_aliases]
# Create aliases for easier script writing
# Examples:
# expert = narrator
# guest = character1
# host_a = host
# host_b = character1

# Voice settings sections - create one for each voice
# Template for voice settings:
# [voice_settings_VOICE_NAME]
# default_volume = 0              # -10 to +10 dB adjustment
# default_stability = 0.7         # 0.0-1.0, higher = more consistent
# default_style = 0.4             # 0.0-1.0, higher = more expressive
# 
# Emotion-specific settings (optional):
# excited_stability = 0.5
# excited_style = 0.7
# calm_stability = 0.8
# calm_style = 0.2
# thoughtful_stability = 0.8
# thoughtful_style = 0.3
# surprised_stability = 0.3
# surprised_style = 0.8

[audio]
model = eleven_multilingual_v2
optimize_streaming_latency = 0
output_format = mp3_44100_128

[podcast]
default_pause_duration = 0.5      # Short pause duration in seconds
long_pause_duration = 1.0         # Long pause duration in seconds
episode_intro_music = true
episode_outro_music = true
```


# docs\ssml_dsl_table.md
```markdown
# SSML en DSL Referentie Tabel

## DSL naar SSML Conversie Tabel

| Nederlandse DSL | SSML Output | Beschrijving |
|-----------------|-------------|--------------|
| `**tekst**` | `<emphasis level="strong">tekst</emphasis>` | Sterke nadruk |
| `*tekst*` | `<emphasis level="moderate">tekst</emphasis>` | Gematigde nadruk |
| `_tekst_` | `<emphasis level="reduced">tekst</emphasis>` | Zachte nadruk |
| `~tekst~` | `<prosody volume="soft">tekst</prosody>` | Zachte spraak |
| `TEKST` | `<emphasis level="strong">TEKST</emphasis>` | Hoofdletters → nadruk |
| `(pauze)` | `<break time="0.5s"/>` | Korte pauze |
| `(lange pauze)` | `<break time="1.0s"/>` | Lange pauze |
| `(kort pauze)` | `<break time="0.3s"/>` | Heel korte pauze |
| `(stilte)` | `<break time="1.5s"/>` | Langere stilte |
| `(lange stilte)` | `<break time="2.0s"/>` | Extra lange stilte |
| `(fluister)...(/fluister)` | `<prosody volume="x-soft">...</prosody>` | Fluisteren |
| `(snel)...(/snel)` | `<prosody rate="fast">...</prosody>` | Snel spreken |
| `(langzaam)...(/langzaam)` | `<prosody rate="slow">...</prosody>` | Langzaam spreken |
| `(supersnel)...(/supersnel)` | `<prosody rate="x-fast">...</prosody>` | Extra snel |
| `(hoog)...(/hoog)` | `<prosody pitch="high">...</prosody>` | Hoge toon |
| `(laag)...(/laag)` | `<prosody pitch="low">...</prosody>` | Lage toon |
| `(superhoog)...(/superhoog)` | `<prosody pitch="x-high">...</prosody>` | Extra hoge toon |
| `(superlaag)...(/superlaag)` | `<prosody pitch="x-low">...</prosody>` | Extra lage toon |

## Emotie Markers (Voice Settings)

### Legacy Markers (Backwards Compatible)
| Nederlandse DSL | Voice Settings | Beschrijving |
|-----------------|----------------|--------------|
| `[EXCITED]` | `{"stability": 0.2, "style": 0.8}` | Levendig, enthousiast |
| `[THOUGHTFUL]` | `{"stability": 0.8, "style": 0.2}` | Bedachtzaam, rustig |
| `[SURPRISED]` | `{"stability": 0.3, "style": 0.7}` | Verrast, geanimeerd |
| `[CALM]` | `{"stability": 0.9, "style": 0.1}` | Kalm, stabiel |
| `[ENTHUSIASTIC]` | `{"stability": 0.4, "style": 0.7}` | Vol energie |

### Nieuwe Nederlandse Emotie Markers
| Nederlandse DSL | Voice Settings | Beschrijving |
|-----------------|----------------|--------------|
| **Positieve Emoties** |
| `[vrolijk]` | `{"stability": 0.3, "style": 0.7}` | Vrolijke stemming |
| `[blij]` | `{"stability": 0.3, "style": 0.6}` | Blijdschap |
| `[opgewonden]` | `{"stability": 0.2, "style": 0.8}` | Opwinding |
| `[enthousiast]` | `{"stability": 0.4, "style": 0.7}` | Enthousiasme |
| `[speels]` | `{"stability": 0.3, "style": 0.8}` | Speelse toon |
| `[trots]` | `{"stability": 0.6, "style": 0.5}` | Trots |
| `[zelfverzekerd]` | `{"stability": 0.7, "style": 0.4}` | Zelfvertrouwen |
| `[tevreden]` | `{"stability": 0.8, "style": 0.3}` | Tevredenheid |
| `[lachend]` | `{"stability": 0.2, "style": 0.9}` | Lachende toon |
| **Nieuwsgierigheid & Interesse** |
| `[nieuwsgierig]` | `{"stability": 0.4, "style": 0.6}` | Nieuwsgierigheid |
| `[geïnteresseerd]` | `{"stability": 0.5, "style": 0.5}` | Interesse |
| `[oprecht geïnteresseerd]` | `{"stability": 0.6, "style": 0.5}` | Oprechte interesse |
| `[fascinerend]` | `{"stability": 0.4, "style": 0.7}` | Fascinatie |
| `[verwonderd]` | `{"stability": 0.3, "style": 0.6}` | Verwondering |
| **Verrassing & Ontdekking** |
| `[verrast]` | `{"stability": 0.3, "style": 0.7}` | Verrassing |
| `[verbaasd]` | `{"stability": 0.4, "style": 0.6}` | Verbazing |
| `[geschokt]` | `{"stability": 0.2, "style": 0.8}` | Shock |
| `[onder de indruk]` | `{"stability": 0.5, "style": 0.6}` | Indruk |
| **Rust & Bezonkenheid** |
| `[rustig]` | `{"stability": 0.9, "style": 0.1}` | Rustige toon |
| `[kalm]` | `{"stability": 0.9, "style": 0.2}` | Kalmte |
| `[bedachtzaam]` | `{"stability": 0.8, "style": 0.2}` | Bedachtzaamheid |
| `[peinzend]` | `{"stability": 0.8, "style": 0.3}` | Peinzende toon |
| `[wijsheid]` | `{"stability": 0.9, "style": 0.2}` | Wijze toon |
| `[serieus]` | `{"stability": 0.8, "style": 0.3}` | Serieuze toon |
| **Twijfel & Onzekerheid** |
| `[aarzelend]` | `{"stability": 0.6, "style": 0.4}` | Aarzeling |
| `[onzeker]` | `{"stability": 0.5, "style": 0.4}` | Onzekerheid |
| `[twijfelend]` | `{"stability": 0.6, "style": 0.3}` | Twijfel |
| `[voorzichtig]` | `{"stability": 0.7, "style": 0.3}` | Voorzichtigheid |
| **Emotionele Tonen** |
| `[bezorgd]` | `{"stability": 0.5, "style": 0.5}` | Bezorgdheid |
| `[teleurgesteld]` | `{"stability": 0.6, "style": 0.4}` | Teleurstelling |
| `[verdrietig]` | `{"stability": 0.7, "style": 0.3}` | Verdriet |
| `[melancholisch]` | `{"stability": 0.8, "style": 0.3}` | Melancholie |
| **Speciale Tonen** |
| `[ironisch]` | `{"stability": 0.4, "style": 0.6}` | Ironie |
| `[sarcastisch]` | `{"stability": 0.5, "style": 0.7}` | Sarcasme |
| `[dromerig]` | `{"stability": 0.7, "style": 0.4}` | Dromerige toon |
| `[mysterieus]` | `{"stability": 0.6, "style": 0.5}` | Mysterie |
| `[fluisterend]` | `{"stability": 0.8, "style": 0.2}` | Fluisterend |
| **Intensiteit Variaties** |
| `[heel rustig]` | `{"stability": 0.95, "style": 0.1}` | Extra rustig |
| `[super enthousiast]` | `{"stability": 0.1, "style": 0.9}` | Extra enthousiast |
| `[licht geamuseerd]` | `{"stability": 0.6, "style": 0.4}` | Lichte amusement |
| `[diep geraakt]` | `{"stability": 0.7, "style": 0.5}` | Diep geraakt |

## Ontbrekende SSML Features

De volgende SSML features worden door ElevenLabs ondersteund maar zijn nog niet geïmplementeerd in onze DSL:

| SSML Feature | Functie | Voorbeeld | Status |
|--------------|---------|-----------|---------|
| `<phoneme>` | Uitspraak override | `<phoneme alphabet="ipa" ph="huːs">house</phoneme>` | ❌ Niet geïmplementeerd |
| `<say-as>` | Interpretatie type | `<say-as interpret-as="spell-out">hello</say-as>` | ❌ Niet geïmplementeerd |
| `<voice>` | Stem wisselen | `<voice name="Amy">Hello</voice>` | ❌ Niet geïmplementeerd |
| `<sub>` | Substitutie | `<sub alias="World Wide Web">WWW</sub>` | ❌ Niet geïmplementeerd |
| `<prosody volume>` | Extra volume levels | `<prosody volume="x-loud">tekst</prosody>` | ⚠️ Gedeeltelijk |
| `<prosody rate>` | Extra snelheden | `<prosody rate="x-slow">tekst</prosody>` | ⚠️ Gedeeltelijk |
| `<prosody pitch>` | Percentage pitch | `<prosody pitch="+20%">tekst</prosody>` | ❌ Niet geïmplementeerd |
| `<break strength>` | Pauze sterkte | `<break strength="weak"/>` | ❌ Niet geïmplementeerd |

## Mogelijke DSL Uitbreidingen

Deze features zouden toegevoegd kunnen worden aan onze Nederlandse markup:

| Voorgestelde DSL | Zou worden | SSML Output |
|------------------|------------|-------------|
| `(spel) W-W-W (/spel)` | Letter voor letter | `<say-as interpret-as="spell-out">WWW</say-as>` |
| `(datum) 01-01-2024 (/datum)` | Als datum uitspreken | `<say-as interpret-as="date">01-01-2024</say-as>` |
| `(getal) 123 (/getal)` | Als getal uitspreken | `<say-as interpret-as="number">123</say-as>` |
| `(vervang: dubbelyou) WWW` | Vervang uitspraak | `<sub alias="dubbelyou">WWW</sub>` |
| `(uitspraak: huːs) huis` | Fonetische uitspraak | `<phoneme alphabet="ipa" ph="huːs">huis</phoneme>` |
| `(stem: Rachel) tekst (/stem)` | Andere stem | `<voice name="Rachel">tekst</voice>` |
| `(pitch: +20%) tekst (/pitch)` | Relatieve toonhoogte | `<prosody pitch="+20%">tekst</prosody>` |
| `(extra hard) tekst (/extra hard)` | Extra hard volume | `<prosody volume="x-loud">tekst</prosody>` |
| `(zwakke pauze)` | Zwakke pauze | `<break strength="weak"/>` |
| `(sterke pauze)` | Sterke pauze | `<break strength="strong"/>` |

## Implementatie Status

### ✅ Volledig Geïmplementeerd (20 features)
- Klemtonen (emphasis)
- Volume aanpassingen (prosody volume)
- Spreeksnelheid (prosody rate)
- Toonhoogte (prosody pitch)
- Pauzes (break time) - uitgebreid met 5 variaties
- 40+ Nederlandse emotie markers via voice settings
- Backwards compatibility met legacy markers

### ⚠️ Gedeeltelijk Geïmplementeerd (2 features)
- Volume: alleen `soft` en `x-soft`, mist `loud`, `x-loud`
- Snelheid: alleen `fast`, `slow`, `x-fast`, mist `x-slow`

### ❌ Nog Niet Geïmplementeerd (8 features)
- Fonetische uitspraak (`<phoneme>`)
- Interpretatie types (`<say-as>`)
- Stem wisseling (`<voice>`)
- Tekst substitutie (`<sub>`)
- Percentage pitch (`<prosody pitch="+20%">`)
- Pauze sterkte (`<break strength="">`)
- Extra volume levels
- Extra snelheid levels

## Prioriteiten voor Toekomstige Implementatie

1. **Hoge Prioriteit**: `<say-as>` voor datum/getal uitspraak
2. **Medium Prioriteit**: `<sub>` voor afkortingen zoals "WWW", "AI", etc.
3. **Lage Prioriteit**: `<phoneme>` voor specifieke uitspraak correcties
```


# src\__init__.py
```python
"""
Podcast Generator

A sophisticated text-to-speech podcast generator with custom markup language
for creating engaging audio content.
"""

from .podcast_generator import PodcastGenerator
from .config_loader import load_config

__version__ = "1.0.0"
__author__ = "Podcast Generator Team"
```


# src\audio_processor.py
```python
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
```


# src\config_loader.py
```python
"""
Configuration loader for podcast generator with advanced voice settings
"""

import configparser
import os

def load_config(config_dir="config"):
    """Load configuration from config files with advanced voice settings
    
    Args:
        config_dir: Path to config directory (default: "config")
    """
    # Load secrets
    secrets = configparser.ConfigParser()
    secrets_path = os.path.join(config_dir, 'credentials', 'secrets.ini')
    
    if not os.path.exists(secrets_path):
        raise FileNotFoundError(f"Secrets file not found: {secrets_path}")
    
    secrets.read(secrets_path)
    
    # Load public config
    config = configparser.ConfigParser()
    config_path = os.path.join(config_dir, 'config.ini')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    config.read(config_path)
    
    # Get all voices from [voices] section dynamically
    voice_names = list(config['voices'].keys()) if 'voices' in config else []
    
    # Parse voice settings for each voice dynamically
    voice_settings = {}
    for voice_name in voice_names:
        section_name = f'voice_settings_{voice_name}'
        if section_name in config:
            voice_settings[voice_name] = {
                'default_volume': config.getint(section_name, 'default_volume', fallback=0),
                'default_stability': config.getfloat(section_name, 'default_stability', fallback=0.7),
                'default_style': config.getfloat(section_name, 'default_style', fallback=0.4),
                'emotions': {}
            }
            
            # Load emotional variants
            for key, value in config.items(section_name):
                if key.endswith('_stability'):
                    emotion = key.replace('_stability', '')
                    if emotion != 'default':
                        if emotion not in voice_settings[voice_name]['emotions']:
                            voice_settings[voice_name]['emotions'][emotion] = {}
                        voice_settings[voice_name]['emotions'][emotion]['stability'] = float(value)
                elif key.endswith('_style'):
                    emotion = key.replace('_style', '')
                    if emotion != 'default':
                        if emotion not in voice_settings[voice_name]['emotions']:
                            voice_settings[voice_name]['emotions'][emotion] = {}
                        voice_settings[voice_name]['emotions'][emotion]['style'] = float(value)
    
    # Build voices dict dynamically
    voices = {}
    if 'voices' in config:
        voices = dict(config['voices'])
    
    return {
        'api_key': secrets['elevenlabs']['api_key'],
        'voices': voices,
        'voice_aliases': dict(config['voice_aliases']) if 'voice_aliases' in config else {},
        'voice_settings': voice_settings,
        'audio': {
            'model': config.get('audio', 'model', fallback='eleven_multilingual_v2'),
            'optimize_streaming_latency': config.getint('audio', 'optimize_streaming_latency', fallback=0),
            'output_format': config.get('audio', 'output_format', fallback='mp3_44100_128'),
        },
        'podcast': {
            'default_pause_duration': config.getfloat('podcast', 'default_pause_duration', fallback=0.5),
            'long_pause_duration': config.getfloat('podcast', 'long_pause_duration', fallback=1.0),
            'episode_intro_music': config.getboolean('podcast', 'episode_intro_music', fallback=True),
            'episode_outro_music': config.getboolean('podcast', 'episode_outro_music', fallback=True),
        }
    }
```


# src\elevenlabs_client.py
```python
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
```


# src\logging_utils.py
```python
"""
Logging utilities for podcast generator
"""

import os
import logging
from datetime import datetime
from pathlib import Path

class PodcastLogger:
    """Centralized logging for podcast generation"""
    
    def __init__(self, project_dir=None, episode_name="podcast"):
        self.project_dir = project_dir
        self.episode_name = episode_name
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging with both console and file output"""
        # Create logs directory
        if self.project_dir:
            self.log_dir = Path(self.project_dir) / "logs"
        else:
            self.log_dir = Path("logs")
        
        self.log_dir.mkdir(exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{self.episode_name}_{timestamp}.log"
        self.log_file = self.log_dir / log_filename
        
        # Setup detailed file logger
        self.file_logger = logging.getLogger(f"podcast_file_{timestamp}")
        self.file_logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.file_logger.handlers.clear()
        
        # File handler with detailed format
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.file_logger.addHandler(file_handler)
        
        print(f"📋 Logging to: {self.log_file}")
    
    def log_processing_step(self, speaker, original_text, emotions, voice_settings, processed_text):
        """Log detailed processing step"""
        step_info = f"""
=== PROCESSING STEP: {speaker} ===
Original text: {original_text}
Detected emotions: {emotions}
Voice settings: {voice_settings}
Processed text: {processed_text}
=====================================
"""
        self.file_logger.info(step_info)
        
        # Also print summary to console
        print(f"🎭 {speaker}: emotions={emotions}")
        print(f"📝 Processed: '{processed_text[:60]}...'")
    
    def log_api_call(self, text, voice_id, voice_settings, model_id, output_file):
        """Log ElevenLabs API call details"""
        api_info = f"""
=== ELEVENLABS API CALL ===
Text sent to API: {text}
Voice ID: {voice_id}
Model: {model_id}
Voice settings: {voice_settings}
Output file: {output_file}
===========================
"""
        self.file_logger.info(api_info)
        
        # Print summary to console
        settings_summary = f"stability={voice_settings.get('stability', 'N/A'):.1f}, style={voice_settings.get('style', 'N/A'):.1f}"
        print(f"🔊 API call: {settings_summary} → {output_file}")
    
    def log_audio_combination(self, audio_files, voice_volumes, output_file):
        """Log audio combination details"""
        audio_info = f"""
=== AUDIO COMBINATION ===
Audio files: {audio_files}
Voice volumes: {voice_volumes}
Final output: {output_file}
=========================
"""
        self.file_logger.info(audio_info)
        print(f"🎵 Combining {len(audio_files)} segments → {output_file}")
    
    def log_error(self, error_message, context=""):
        """Log error with context"""
        error_info = f"ERROR in {context}: {error_message}"
        self.file_logger.error(error_info)
        print(f"❌ {error_info}")
    
    def log_success(self, output_file, duration_info=""):
        """Log successful completion"""
        success_info = f"SUCCESS: Generated {output_file} {duration_info}"
        self.file_logger.info(success_info)
        print(f"✅ {success_info}")
    
    def get_log_summary(self):
        """Get summary of current session"""
        return {
            'log_file': str(self.log_file),
            'log_dir': str(self.log_dir),
            'episode_name': self.episode_name
        }
```


# src\podcast_generator.py
```python
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
    
    def create_podcast(self, script, output_name):
        """Create complete podcast from script with voice-specific settings"""
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
                
                # ===== PROCESSING DEBUG =====
                print(f"\n🔍 === PROCESSING DEBUG for {speaker_name} ===")
                print(f"📝 Original line: '{line}'")
                print(f"🎭 Detected emotions: {emotion_settings}")
                print(f"🎚️ Final voice settings: {final_settings}")
                
                # Process SSML markup
                processed_text = self.ssml_processor.process_text(text)
                print(f"📄 After SSML processing: '{processed_text}'")
                print(f"==========================================\n")
                
                if processed_text:
                    file = f"temp_{actual_voice_name}_{i}.mp3"
                    print(f"🎙️ {speaker_name} ({actual_voice_name}): {processed_text[:50]}...")
                    
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
                    else:
                        print(f"✗ Failed conversion: {processed_text}")
            
            elif '[PAUZE]' in line:
                # Mark this position for a longer pause
                pause_indices.append(segment_count - 1)
        
        if not audio_files:
            print("✗ No audio files generated!")
            return None
        
        # Get voice-specific volume adjustments
        voice_volumes = {}
        for voice_name in self.voices.keys():
            voice_volumes[voice_name] = self.ssml_processor.get_voice_volume_adjustment(voice_name)
        
        # Combine all audio files with smart gaps
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
            print("⚠️ Using legacy audio processor without voice volume support")
            result = self.audio_processor.combine_audio_segments(
                audio_files, 
                output_file, 
                pause_indices=pause_indices,
                normal_gap=int(self.config['podcast']['default_pause_duration'] * 1000),
                pause_gap=int(self.config['podcast']['long_pause_duration'] * 1000)
            )
        
        # Cleanup temp files
        self.audio_processor.cleanup_temp_files(temp_files)
        
        return result
```


# src\project_utils.py
```python
"""
Project utilities for managing different podcast projects
"""

import os
from src.config_loader import load_config
from src.podcast_generator import PodcastGenerator

class ProjectManager:
    """Manages different podcast projects with their own configs"""
    
    def __init__(self, base_dir="projects"):
        self.base_dir = base_dir
    
    def create_project_structure(self, project_name):
        """Create directory structure for a new project"""
        project_dir = os.path.join(self.base_dir, project_name)
        config_dir = os.path.join(project_dir, "config")
        credentials_dir = os.path.join(config_dir, "credentials")
        scripts_dir = os.path.join(project_dir, "scripts")
        output_dir = os.path.join(project_dir, "output")
        
        # Create directories
        for directory in [project_dir, config_dir, credentials_dir, scripts_dir, output_dir]:
            os.makedirs(directory, exist_ok=True)
        
        print(f"✓ Created project structure for '{project_name}'")
        print(f"📁 Project directory: {project_dir}")
        print(f"⚙️ Config directory: {config_dir}")
        print(f"📝 Scripts directory: {scripts_dir}")
        print(f"🎵 Output directory: {output_dir}")
        
        return {
            'project_dir': project_dir,
            'config_dir': config_dir,
            'scripts_dir': scripts_dir,
            'output_dir': output_dir
        }
    
    def load_project(self, project_name):
        """Load a specific project's configuration"""
        project_dir = os.path.join(self.base_dir, project_name)
        config_dir = os.path.join(project_dir, "config")
        
        if not os.path.exists(config_dir):
            raise FileNotFoundError(f"Project '{project_name}' not found at {project_dir}")
        
        # Load config from project directory
        config = load_config(config_dir)
        
        print(f"🎙️ Loaded project: {project_name}")
        print(f"✓ Voices: {list(config['voices'].keys())}")
        print(f"✓ Aliases: {config['voice_aliases']}")
        
        return config, project_dir
    
    def create_generator(self, project_name):
        """Create a podcast generator for a specific project"""
        config, project_dir = self.load_project(project_name)
        generator = PodcastGenerator(config)
        
        # Add project-specific output path
        generator.project_dir = project_dir
        generator.output_dir = os.path.join(project_dir, "output")
        
        return generator
    
    def list_projects(self):
        """List all available projects"""
        if not os.path.exists(self.base_dir):
            print(f"No projects directory found at: {self.base_dir}")
            return []
        
        projects = []
        for item in os.listdir(self.base_dir):
            project_path = os.path.join(self.base_dir, item)
            config_path = os.path.join(project_path, "config", "config.ini")
            
            if os.path.isdir(project_path) and os.path.exists(config_path):
                projects.append(item)
        
        if projects:
            print("📚 Available projects:")
            for i, project in enumerate(projects, 1):
                print(f"  {i}. {project}")
        else:
            print("No projects found.")
        
        return projects

def create_sample_config(project_dir, voices_config=None):
    """Create sample config files for a new project"""
    config_dir = os.path.join(project_dir, "config")
    
    # Default voices if none provided
    if not voices_config:
        voices_config = {
            'host_a': 'your_voice_id_1',
            'host_b': 'your_voice_id_2'
        }
    
    # Create config.ini
    config_content = f"""# config.ini - Podcast Configuration

[voices]
"""
    
    for voice_name, voice_id in voices_config.items():
        config_content += f"{voice_name} = {voice_id}\n"
    
    config_content += """
[voice_aliases]
# Add aliases for easier scripting
# expert = host_a
# curious = host_b

"""
    
    # Add voice settings sections
    for voice_name in voices_config.keys():
        config_content += f"""[voice_settings_{voice_name}]
# {voice_name} voice settings
default_volume = 0
default_stability = 0.7
default_style = 0.4
# Add emotional variants:
# thoughtful_stability = 0.8
# thoughtful_style = 0.2
# excited_stability = 0.5
# excited_style = 0.6

"""
    
    config_content += """[audio]
model = eleven_multilingual_v2
optimize_streaming_latency = 0
output_format = mp3_44100_128

[podcast]
default_pause_duration = 0.5
long_pause_duration = 1.0
episode_intro_music = true
episode_outro_music = true"""
    
    # Write config.ini
    with open(os.path.join(config_dir, "config.ini"), "w") as f:
        f.write(config_content)
    
    # Create secrets.ini template
    secrets_content = """[elevenlabs]
api_key = your_elevenlabs_api_key_here"""
    
    with open(os.path.join(config_dir, "credentials", "secrets.ini"), "w") as f:
        f.write(secrets_content)
    
    print(f"✓ Created sample config files in {config_dir}")
    print(f"📝 Please edit config/credentials/secrets.ini with your API key")
    print(f"📝 Please edit config/config.ini with your voice IDs")

# Example usage functions
def quick_start_project(project_name, voices=None):
    """Quick start a new project with sample configs"""
    pm = ProjectManager()
    
    # Create project structure
    dirs = pm.create_project_structure(project_name)
    
    # Create sample config
    create_sample_config(dirs['project_dir'], voices)
    
    print(f"\n🚀 Project '{project_name}' is ready!")
    print(f"📋 Next steps:")
    print(f"   1. Edit {dirs['config_dir']}/credentials/secrets.ini")
    print(f"   2. Edit {dirs['config_dir']}/config.ini")
    print(f"   3. Put your scripts in {dirs['scripts_dir']}")
    print(f"   4. Run: python generate_podcast.py {project_name}")
    
    return dirs
```


# src\ssml_processor.py
```python
"""
SSML processor for converting markup to Speech Synthesis Markup Language
with voice-specific emotion handling
"""

import re

class SSMLProcessor:
    """Processes custom markup and converts to SSML with voice-specific settings"""
    
    def __init__(self, voice_settings=None):
        """Initialize SSML processor with optional voice settings"""
        self.voice_settings = voice_settings or {}
        
        # Core Nederlandse emotie mapping (fallback when voice-specific not available)
        self.default_emotions = {
            # Positieve emoties
            '[vrolijk]': {"stability": 0.3, "style": 0.7},
            '[blij]': {"stability": 0.3, "style": 0.6},
            '[opgewonden]': {"stability": 0.2, "style": 0.8},
            '[enthousiast]': {"stability": 0.4, "style": 0.7},
            '[speels]': {"stability": 0.3, "style": 0.8},
            '[trots]': {"stability": 0.6, "style": 0.5},
            '[zelfverzekerd]': {"stability": 0.7, "style": 0.4},
            '[tevreden]': {"stability": 0.8, "style": 0.3},
            '[lachend]': {"stability": 0.2, "style": 0.9},
            
            # Nieuwsgierigheid & interesse
            '[nieuwsgierig]': {"stability": 0.4, "style": 0.6},
            '[geïnteresseerd]': {"stability": 0.5, "style": 0.5},
            '[oprecht geïnteresseerd]': {"stability": 0.6, "style": 0.5},
            '[fascinerend]': {"stability": 0.4, "style": 0.7},
            '[verwonderd]': {"stability": 0.3, "style": 0.6},
            
            # Verrassing & ontdekking
            '[verrast]': {"stability": 0.3, "style": 0.7},
            '[verbaasd]': {"stability": 0.4, "style": 0.6},
            '[geschokt]': {"stability": 0.2, "style": 0.8},
            '[onder de indruk]': {"stability": 0.5, "style": 0.6},
            
            # Rust & bezonkenheid
            '[rustig]': {"stability": 0.9, "style": 0.1},
            '[kalm]': {"stability": 0.9, "style": 0.2},
            '[bedachtzaam]': {"stability": 0.8, "style": 0.2},
            '[peinzend]': {"stability": 0.8, "style": 0.3},
            '[wijsheid]': {"stability": 0.9, "style": 0.2},
            '[serieus]': {"stability": 0.8, "style": 0.3},
            
            # Twijfel & onzekerheid
            '[aarzelend]': {"stability": 0.6, "style": 0.4},
            '[onzeker]': {"stability": 0.5, "style": 0.4},
            '[twijfelend]': {"stability": 0.6, "style": 0.3},
            '[voorzichtig]': {"stability": 0.7, "style": 0.3},
            
            # Emotionele tonen
            '[bezorgd]': {"stability": 0.5, "style": 0.5},
            '[teleurgesteld]': {"stability": 0.6, "style": 0.4},
            '[verdrietig]': {"stability": 0.7, "style": 0.3},
            '[melancholisch]': {"stability": 0.8, "style": 0.3},
            
            # Speciale tonen
            '[ironisch]': {"stability": 0.4, "style": 0.6},
            '[sarcastisch]': {"stability": 0.5, "style": 0.7},
            '[dromerig]': {"stability": 0.7, "style": 0.4},
            '[mysterieus]': {"stability": 0.6, "style": 0.5},
            '[fluisterend]': {"stability": 0.8, "style": 0.2},
            
            # Intensiteit variaties
            '[heel rustig]': {"stability": 0.95, "style": 0.1},
            '[super enthousiast]': {"stability": 0.1, "style": 0.9},
            '[licht geamuseerd]': {"stability": 0.6, "style": 0.4},
            '[diep geraakt]': {"stability": 0.7, "style": 0.5},
        }
        
        # Backwards compatibility mapping
        self.legacy_mapping = {
            '[EXCITED]': '[opgewonden]',
            '[THOUGHTFUL]': '[bedachtzaam]',
            '[SURPRISED]': '[verrast]',
            '[CALM]': '[kalm]',
            '[ENTHUSIASTIC]': '[enthousiast]'
        }
        
        # Simplified emotion name mapping for config lookup
        self.emotion_name_mapping = {
            '[opgewonden]': 'excited',
            '[bedachtzaam]': 'thoughtful',
            '[verrast]': 'surprised',
            '[kalm]': 'calm',
            '[enthousiast]': 'enthusiastic',
            '[nieuwsgierig]': 'curious',
            '[geïnteresseerd]': 'interested',
            '[trots]': 'proud',
            '[aarzelend]': 'hesitant',
            '[zelfverzekerd]': 'confident',
            '[peinzend]': 'contemplative'
        }
    
    def process_text(self, text):
        """Main processing function"""
        text = self._clean_emotion_markers(text)
        text = self._process_emphasis_markers(text)
        return text
    
    def extract_emotion(self, line, voice_name=None):
        """Extract emotion markers and return voice settings for specific voice"""
        # Check for Dutch emotions first
        for emotion_marker in self.default_emotions.keys():
            if emotion_marker in line:
                return self._get_voice_specific_settings(emotion_marker, voice_name)
        
        # Check for legacy emotions (backwards compatibility)
        for legacy, dutch in self.legacy_mapping.items():
            if legacy in line:
                return self._get_voice_specific_settings(dutch, voice_name)
        
        # Return default settings for voice if no emotion found
        if voice_name and voice_name in self.voice_settings:
            voice_config = self.voice_settings[voice_name]
            return {
                "stability": voice_config.get('default_stability', 0.7),
                "style": voice_config.get('default_style', 0.4)
            }
        
        return {}
    
    def _get_voice_specific_settings(self, emotion_marker, voice_name=None):
        """Get emotion settings specific to a voice, fallback to defaults"""
        if not voice_name or voice_name not in self.voice_settings:
            # Use default emotion settings
            return self.default_emotions.get(emotion_marker, {})
        
        voice_config = self.voice_settings[voice_name]
        
        # Map emotion marker to simplified name for config lookup
        emotion_name = self.emotion_name_mapping.get(emotion_marker)
        
        # Check if voice has specific settings for this emotion
        if emotion_name and emotion_name in voice_config.get('emotions', {}):
            emotion_settings = voice_config['emotions'][emotion_name]
            return {
                "stability": emotion_settings.get('stability', voice_config.get('default_stability', 0.7)),
                "style": emotion_settings.get('style', voice_config.get('default_style', 0.4))
            }
        
        # Fallback to voice defaults
        return {
            "stability": voice_config.get('default_stability', 0.7),
            "style": voice_config.get('default_style', 0.4)
        }
    
    def get_default_voice_settings(self, voice_name):
        """Get default settings for a voice"""
        if voice_name not in self.voice_settings:
            return {
                "stability": 0.7,
                "similarity_boost": 0.8,
                "style": 0.4,
                "use_speaker_boost": True
            }
        
        voice_config = self.voice_settings[voice_name]
        return {
            "stability": voice_config.get('default_stability', 0.7),
            "similarity_boost": 0.8,  # Keep this consistent
            "style": voice_config.get('default_style', 0.4),
            "use_speaker_boost": True
        }
    
    def get_voice_volume_adjustment(self, voice_name):
        """Get volume adjustment for a voice"""
        if voice_name not in self.voice_settings:
            return 0
        return self.voice_settings[voice_name].get('default_volume', 0)
    
    def _clean_emotion_markers(self, text):
        """Remove emotion markers from text but keep SSML"""
        # Remove Dutch emotion markers
        for emotion in self.default_emotions.keys():
            text = text.replace(emotion, '')
        
        # Remove legacy markers
        for marker in self.legacy_mapping.keys():
            text = text.replace(marker, '')
        
        return text.strip()
    
    def _process_emphasis_markers(self, text):
        """Convert custom emphasis markers to SSML"""
        
        # KLEMTONEN
        # Convert **word** to <emphasis level="strong">word</emphasis>
        text = re.sub(r'\*\*([^*]+)\*\*', r'<emphasis level="strong">\1</emphasis>', text)
        
        # Convert *word* to <emphasis level="moderate">word</emphasis>  
        text = re.sub(r'\*([^*]+)\*', r'<emphasis level="moderate">\1</emphasis>', text)
        
        # Convert _word_ to <emphasis level="reduced">word</emphasis>
        text = re.sub(r'_([^_]+)_', r'<emphasis level="reduced">\1</emphasis>', text)
        
        # Convert ~word~ to <prosody volume="soft">word</prosody> (zachte spraak)
        text = re.sub(r'~([^~]+)~', r'<prosody volume="soft">\1</prosody>', text)
        
        # Convert WOORD to <emphasis level="strong">WOORD</emphasis>
        text = re.sub(r'\b([A-Z]{2,})\b', r'<emphasis level="strong">\1</emphasis>', text)
        
        # PAUZES (uitgebreid)
        text = re.sub(r'\(pauze\)', '<break time="0.5s"/>', text)
        text = re.sub(r'\(lange pauze\)', '<break time="1.0s"/>', text)
        text = re.sub(r'\(kort pauze\)', '<break time="0.3s"/>', text)
        text = re.sub(r'\(korte pauze\)', '<break time="0.3s"/>', text)
        text = re.sub(r'\(stilte\)', '<break time="1.5s"/>', text)
        text = re.sub(r'\(lange stilte\)', '<break time="2.0s"/>', text)
        
        # VOLUME
        text = re.sub(r'\(fluister\)', '<prosody volume="x-soft">', text)
        text = re.sub(r'\(/fluister\)', '</prosody>', text)
        
        # SPREEKSNELHEID
        text = re.sub(r'\(snel\)', '<prosody rate="fast">', text)
        text = re.sub(r'\(/snel\)', '</prosody>', text)
        text = re.sub(r'\(langzaam\)', '<prosody rate="slow">', text)
        text = re.sub(r'\(/langzaam\)', '</prosody>', text)
        text = re.sub(r'\(supersnel\)', '<prosody rate="x-fast">', text)
        text = re.sub(r'\(/supersnel\)', '</prosody>', text)
        
        # TOONHOOGTE  
        text = re.sub(r'\(hoog\)', '<prosody pitch="high">', text)
        text = re.sub(r'\(/hoog\)', '</prosody>', text)
        text = re.sub(r'\(laag\)', '<prosody pitch="low">', text)
        text = re.sub(r'\(/laag\)', '</prosody>', text)
        text = re.sub(r'\(superhoog\)', '<prosody pitch="x-high">', text)
        text = re.sub(r'\(/superhoog\)', '</prosody>', text)
        text = re.sub(r'\(superlaag\)', '<prosody pitch="x-low">', text)
        text = re.sub(r'\(/superlaag\)', '</prosody>', text)
        
        return text
```


# LICENSE
```text
MIT License

Copyright (c) 2025 Jeroen Veen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```


# README.md
```markdown
# Podcast Generator

AI-powered podcast generator with Dutch markup language

Automatische podcast generatie met ElevenLabs AI voices voor een podcast serie.

## Setup

### 1. Dependencies installeren
```bash
pip install -r requirements.txt
```

### 2. FFmpeg installeren
**Windows (aanbevolen):**
1. Ga naar https://www.gyan.dev/ffmpeg/builds/
2. Download "release builds" → "ffmpeg-release-essentials.zip"
3. Pak uit naar `C:\ffmpeg`
4. Script zoekt automatisch naar `C:\ffmpeg\bin\ffmpeg.exe`

### 3. Config bestanden aanmaken
1. Maak `config/credentials/secrets.ini`
2. Vul je ElevenLabs API key in:
```ini
[elevenlabs]
api_key = jouw_echte_api_key_hier
```

### 4. Voice IDs kiezen
1. Log in op [ElevenLabs dashboard](https://elevenlabs.io)
2. Ga naar Voice Library
3. Kies 2 stemmen voor je hosts
4. Kopieer de Voice IDs (zonder quotes!)
5. Update `config/config.ini`:
```ini
[voices]
host_a = jouw_voice_id_1
host_b = jouw_voice_id_2
```

## Gebruik

```python
python simple_podcast_generator.py
```

Het script gebruikt automatisch je config bestanden en genereert de podcast.

## Script Format

```python
script = """
[HOST A]: Welkom bij Mondriaan de **Denker**!
[HOST B]: [ENTHUSIASTIC] En ik ben Sam!
[PAUZE]
[HOST A]: [THOUGHTFUL] Wist je dat Mondriaan *filosoof* was? (pauze) ECHT waar!
[HOST B]: [SURPRISED] Echt waar? Ik dacht dat hij alleen _schilderde_!
"""
```

## Emotie Markers

Voeg deze toe aan je script voor expressie:

- `[EXCITED]` - levendig, enthousiast
- `[THOUGHTFUL]` - bedachtzaam, rustig
- `[SURPRISED]` - verrast, geanimeerd
- `[CALM]` - kalm, stabiel
- `[ENTHUSIASTIC]` - vol energie
- `[PAUZE]` - 1 seconde stilte

## Klemtonen & Pauzes

**Klemtonen:**
- `**woord**` → sterke nadruk
- `*woord*` → gematigde nadruk  
- `_woord_` → zachte nadruk
- `~woord~` → zachte spraak (volume omlaag)
- `WOORD` → hoofdletters worden automatisch benadrukt

**Pauzes:**
- `(pauze)` → korte pauze (0.5s)
- `(lange pauze)` → lange pauze (1.0s)

**Volume:**
- `(fluister) tekst hier (/fluister)` → hele zin fluisteren

**Spreeksnelheid:**
- `(snel) tekst hier (/snel)` → snel spreken
- `(langzaam) tekst hier (/langzaam)` → langzaam spreken
- `(supersnel) tekst hier (/supersnel)` → extra snel

**Toonhoogte:**
- `(hoog) tekst hier (/hoog)` → hoge toon
- `(laag) tekst hier (/laag)` → lage toon
- `(superhoog) tekst hier (/superhoog)` → extra hoge toon
- `(superlaag) tekst hier (/superlaag)` → extra lage toon

**Voorbeeld:**
```
[HOST A]: Dit is **heel belangrijk**! (snel) Dit ging supersnel (/snel), maar (hoog) dit heel hoog (/hoog)!
```

## Output

Script genereert een MP3 bestand klaar voor upload naar Spotify, Apple Podcasts, etc.

## Host Persoonlijkheden

- **HOST A**: Meer stabiel/professioneel (expert rol)
- **HOST B**: Meer expressief/nieuwsgierig (leek rol)

## Kosten

ElevenLabs rekent per karakter. Gemiddelde 15-min aflevering ≈ €2-5 afhankelijk van je plan.

## Troubleshooting

**FFmpeg errors**: Script zoekt automatisch naar FFmpeg in `C:\ffmpeg\bin\`. Als je het ergens anders hebt geïnstalleerd, pas het pad aan in het script.

**API errors**: Check je API key en zorg dat je voice IDs correct zijn (geen quotes).
```


# main.py
```python
#!/usr/bin/env python3
"""
Main script for Mondriaan de Denker podcast generator
Using ProjectManager for proper path management
"""

from pathlib import Path
from src.project_utils import ProjectManager

def main():
    # Setup project manager met je base directory
    pm = ProjectManager(base_dir=r"C:\local_dev")
    
    # Load het Mondriaan project
    try:
        generator = pm.create_generator("Mondriaan_podcast")
        
        print("🎙️ Mondriaan de Denker Podcast Generator")
        print(f"📁 Project loaded from: {generator.project_dir}")
        print(f"🎵 Output directory: {generator.output_dir}")
        
        # Sample script demonstrating the new voice system
        script = """
[lucas]: [thoughtful] Welkom bij Mondriaan de **Denker**! Ik ben Lucas, en vandaag duiken we diep in de filosofie van Piet Mondriaan.
[emma]: [enthusiastic] En ik ben Emma! [curious] Lucas, ik moet eerlijk zeggen... (kort pauze) ik dacht altijd dat Mondriaan gewoon een kunstenaar was?
[PAUZE]
[lucas]: [calm] Dat denken veel mensen, Emma. Maar Mondriaan heeft meer dan *honderd* teksten geschreven over zijn filosofie!
[emma]: [surprised] (hoog) HONDERD? (/hoog) [excited] Dat is ongelofelijk! Waar ging dat dan over?
[lucas]: [contemplative] (langzaam) Hij geloofde dat kunst de wereld kon veranderen... (/langzaam) [passionate] Door perfecte harmonie te vinden tussen tegenpolen.
[emma]: [fascinerend] ~Tegenpolen?~ Kun je daar een voorbeeld van geven?
[lucas]: [confident] Natuurlijk! Denk aan zijn beroemde schilderijen: (pauze) **verticale** en **horizontale** lijnen, *primaire* kleuren tegen wit...
[emma]: [verwonderd] Oh! [realization] Dus die simpele lijntjes waren eigenlijk heel diep filosofisch bedoeld?
[PAUZE]
[lucas]: [proud] Precies! Mondriaan zocht naar wat hij de 'nieuwe beelding' noemde. (lange pauze) Een universeeltaal die iedereen zou begrijpen.
[emma]: [thoughtful] (fluister) Dat is eigenlijk heel mooi... (/fluister) [enthusiastic] Vertel eens meer over die filosofie!
"""
        
        # Generate podcast - output gaat automatisch naar project/output/
        output_file = generator.create_podcast(script, "episode_test_advanced")
        
        if output_file:
            print(f"🎉 Podcast successfully created: {output_file}")
            print(f"📊 Using voice-specific emotion settings from config")
        else:
            print("❌ Failed to create podcast")
            
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print(f"💡 Make sure your project structure is:")
        print(f"   C:\\local_dev\\Mondriaan_podcast\\config\\config.ini")
        print(f"   C:\\local_dev\\Mondriaan_podcast\\config\\credentials\\secrets.ini")
        
        # Optionally create the project structure
        create_structure = input("\n🔧 Create project structure? (y/n): ")
        if create_structure.lower() == 'y':
            from project_utils import quick_start_project
            
            # Copy your existing config
            print("📋 Creating project structure...")
            quick_start_project("Mondriaan_podcast")
            print("📝 Please move your existing config files to the new structure")

if __name__ == "__main__":
    main()
```


# requirements.txt
```cmake
requests>=2.31.0
pydub>=0.25.1
ffmpeg-python>=0.2.0
```

