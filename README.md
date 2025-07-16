# Podcast Generator

AI-powered podcast generator with advanced Dutch markup language and voice-specific emotional settings for professional podcast production.

## ✨ Features

- **Advanced Dutch Markup Language**: 40+ Nederlandse emotie markers
- **Voice-Specific Emotional Settings**: Gepersonaliseerde emotie-instellingen per stem
- **Project Management System**: Georganiseerde multi-project structuur
- **Complete SSML Support**: Volledige Speech Synthesis Markup Language ondersteuning
- **Audio Processing**: Automatische volume balancing en normalisatie
- **Professional Post-Processing**: SoX mastering chain voor broadcast-quality audio
- **Detailed Logging**: Uitgebreide logs voor debugging en optimalisatie
- **Privacy & Compliance**: GDPR-compliant met ElevenLabs enterprise features

## 🚀 Quick Start

### 1. Dependencies installeren
```bash
pip install -r requirements.txt
```

### 2. FFmpeg installeren
**Windows (aanbevolen):**
1. Download van https://www.gyan.dev/ffmpeg/builds/
2. Pak uit naar `C:\ffmpeg\bin\`
3. Script detecteert automatisch deze locatie

**Linux/macOS:**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### 3. SoX installeren (optioneel voor mastering)
**Windows:**
1. Download van https://sourceforge.net/projects/sox/
2. Installeer naar `C:\Program Files (x86)\sox-14-4-2\`

**Linux/macOS:**
```bash
# Ubuntu/Debian
sudo apt install sox

# macOS
brew install sox
```

### 4. Project aanmaken
```python
from src.project_utils import quick_start_project

# Maak een nieuw project
quick_start_project("mijn_podcast", {
    'lucas': 'jouw_voice_id_1',
    'emma': 'jouw_voice_id_2'
})
```

### 5. Configuratie
1. **API Key instellen:**
```ini
# projects/mijn_podcast/config/credentials/secrets.ini
[elevenlabs]
api_key = jouw_echte_api_key_hier
```

2. **Voice IDs en instellingen:**
```ini
# projects/mijn_podcast/config/config.ini
[voices]
lucas = jouw_voice_id_1
emma = jouw_voice_id_2

[voice_settings_lucas]
default_volume = 0
default_stability = 0.8
default_style = 0.3
thoughtful_stability = 0.9
thoughtful_style = 0.2

[voice_settings_emma]
default_volume = 2
default_stability = 0.6
default_style = 0.5
excited_stability = 0.3
excited_style = 0.8
```

## 🎭 Voice System

### Stem-Specifieke Emotie Instellingen
Het systeem ondersteunt unieke emotie-instellingen per stem:

```ini
[voice_settings_lucas]
default_volume = 0              # Volume adjustment (-10 to +10 dB)
default_stability = 0.8         # Consistentie (0.0-1.0)
default_style = 0.3             # Expressiviteit (0.0-1.0)

# Emotie-specifieke overrides
thoughtful_stability = 0.9
thoughtful_style = 0.2
passionate_stability = 0.6
passionate_style = 0.6
confident_stability = 0.8
confident_style = 0.4
```

### Voice Aliases
```ini
[voice_aliases]
expert = lucas
curious = emma
host_a = lucas
host_b = emma
```

## 📝 Script Format & Markup

### Basis Script Structuur
```python
script = """
[lucas]: [thoughtful] Welkom bij Mondriaan de **Denker**!
[emma]: [enthusiastic] En ik ben Emma!
[PAUZE]
[lucas]: [calm] Wist je dat Mondriaan *filosoof* was? (pauze) ECHT waar!
[emma]: [surprised] Echt waar? Ik dacht dat hij alleen _schilderde_!
"""
```

### Complete Nederlandse Emotie Markers (40+)

#### Positieve Emoties
```
[vrolijk]        - vrolijke stemming
[blij]           - blijdschap  
[enthousiast]    - enthousiasme
[opgewonden]     - opwinding
[speels]         - speelse toon
[trots]          - trots
[zelfverzekerd]  - zelfvertrouwen
[tevreden]       - tevredenheid
[lachend]        - lachende toon
```

#### Nieuwsgierigheid & Interesse
```
[nieuwsgierig]            - nieuwsgierigheid
[geïnteresseerd]          - interesse
[oprecht geïnteresseerd]  - oprechte interesse
[fascinerend]             - fascinatie
[verwonderd]              - verwondering
```

#### Verrassing & Ontdekking
```
[verrast]         - verrassing
[verbaasd]        - verbazing
[geschokt]        - shock
[onder de indruk] - indruk
```

#### Rust & Bezonkenheid
```
[rustig]      - rustige toon
[kalm]        - kalmte
[bedachtzaam] - bedachtzaamheid
[peinzend]    - peinzende toon
[wijsheid]    - wijze toon
[serieus]     - serieuze toon
```

#### Twijfel & Onzekerheid
```
[aarzelend]   - aarzeling
[onzeker]     - onzekerheid
[twijfelend]  - twijfel
[voorzichtig] - voorzichtigheid
```

#### Emotionele Tonen
```
[bezorgd]        - bezorgdheid
[teleurgesteld]  - teleurstelling
[verdrietig]     - verdriet
[melancholisch]  - melancholie
```

#### Speciale Tonen
```
[ironisch]    - ironie
[sarcastisch] - sarcasme
[dromerig]    - dromerige toon
[mysterieus]  - mysterie
[fluisterend] - fluisterend
```

#### Intensiteit Variaties
```
[heel rustig]        - extra rustig
[super enthousiast]  - extra enthousiast
[licht geamuseerd]   - lichte amusement
[diep geraakt]       - diep geraakt
```

### Backwards Compatibility
Legacy markers blijven volledig ondersteund:
```
[EXCITED]      → [opgewonden]
[THOUGHTFUL]   → [bedachtzaam]
[SURPRISED]    → [verrast]
[CALM]         → [kalm]
[ENTHUSIASTIC] → [enthousiast]
```

## 🔧 SSML Markup Language

### Klemtonen (Emphasis)
```
**woord**  → sterke nadruk
*woord*    → gematigde nadruk  
_woord_    → zachte nadruk
~woord~    → zachte spraak (volume omlaag)
WOORD      → hoofdletters worden automatisch benadrukt
```

### Pauzes (Uitgebreid Systeem)
```
(pauze)         → korte pauze (0.5s)
(lange pauze)   → lange pauze (1.0s)
(kort pauze)    → heel korte pauze (0.3s)
(stilte)        → langere stilte (1.5s)
(lange stilte)  → extra lange stilte (2.0s)
```

### Volume Controle
```
(fluister) tekst hier (/fluister)  → hele zin fluisteren
```

### Spreeksnelheid
```
(snel) tekst hier (/snel)          → snel spreken
(langzaam) tekst hier (/langzaam)  → langzaam spreken
(supersnel) tekst hier (/supersnel) → extra snel
```

### Toonhoogte
```
(hoog) tekst hier (/hoog)          → hoge toon
(laag) tekst hier (/laag)          → lage toon
(superhoog) tekst hier (/superhoog) → extra hoge toon
(superlaag) tekst hier (/superlaag) → extra lage toon
```

### Complete Markup Voorbeeld
```python
script = """
[lucas]: [thoughtful] Dit is **heel belangrijk**! 
[emma]: [surprised] (hoog) ECHT? (/hoog) [fascinerend] (snel) Dat wist ik niet! (/snel)
[PAUZE]
[lucas]: [calm] (langzaam) Laten we dieper ingaan op zijn filosofie... (/langzaam)
[emma]: [excited] (fluister) Wow, dat is ongelofelijk... (/fluister) [enthusiastic] Vertel meer!
"""
```

## 🎵 Audio Processing

### Geavanceerde Audio Features
- **Voice-Specific Volume Balancing**: Automatische volume aanpassingen per stem
- **Smart Pause Detection**: Intelligente pauze plaatsing na `[PAUZE]` markers
- **Audio Normalization**: Automatische normalisatie van eindproduct
- **Quality Export**: High-quality MP3 export (128kbps, 44.1kHz)
- **Gap Management**: Configureerbare pauzes tussen sprekers

### Volume Instellingen
```ini
[voice_settings_lucas]
default_volume = 0    # Baseline volume
[voice_settings_emma]
default_volume = 2    # +2dB luider dan baseline
```

### Audio Configuratie
```ini
[audio]
model = eleven_multilingual_v2
optimize_streaming_latency = 0
output_format = mp3_44100_128

[podcast]
default_pause_duration = 0.5    # Normale pauze tussen sprekers
long_pause_duration = 1.0       # Pauze na [PAUZE] markers
episode_intro_music = true
episode_outro_music = true
```

## 🎛️ Professional Post-Processing

### SoX Mastering Chain
```python
from src.podcast_postprocessor import PodcastPostProcessor

# Basis gebruik
processor = PodcastPostProcessor()
processor.apply_mastering_chain("raw_podcast.mp3", "mastered_podcast.mp3")

# Met preset
processor.apply_mastering_chain("input.mp3", "output.mp3", preset="broadcast")
```

### Beschikbare Presets
- **podcast**: Standaard voor spraak content
- **audiobook**: Geoptimaliseerd voor lang luisteren
- **broadcast**: Radio/TV broadcast ready
- **voice_only**: Maximum intelligibiliteit

### Mastering Chain Stappen
1. **Noise Gate**: Compand-based silence removal
2. **High-pass Filter**: Rumble/DC offset removal
3. **Compression**: Dynamic range control
4. **EQ**: Frequency balancing
5. **De-esser**: Sibilant reduction voor Nederlands
6. **Limiting**: Clip prevention
7. **Normalization**: Optimal loudness

### Batch Processing
```python
# Alle bestanden in directory verwerken
processor.batch_process("./output/", "./mastered/", preset="podcast")
```

## 📊 Project Management

### Project Directory Structuur
```
projects/
├── mijn_podcast/
│   ├── config/
│   │   ├── config.ini
│   │   └── credentials/
│   │       └── secrets.ini
│   ├── scripts/
│   │   └── episode_001.py
│   ├── output/
│   │   └── episode_001.mp3
│   ├── logs/
│   │   └── episode_001_20241216_143022.log
│   └── mastered/
│       └── episode_001_mastered.mp3
```

### ProjectManager Gebruik
```python
from src.project_utils import ProjectManager

# Project manager initialiseren
pm = ProjectManager(base_dir="projects")

# Nieuw project aanmaken
pm.create_project_structure("mijn_podcast")

# Project laden
generator = pm.create_generator("mijn_podcast")

# Podcast genereren
output_file = generator.create_podcast(script, "episode_001")

# Post-processing
from src.podcast_postprocessor import PodcastPostProcessor
processor = PodcastPostProcessor()
mastered_file = processor.apply_mastering_chain(output_file, "episode_001_mastered.mp3")
```

## 📋 Logging & Debugging

### Gedetailleerde Logs
Elke podcast generatie creëert uitgebreide logs:

```
logs/episode_001_20241216_143022.log
```

**Log Inhoud:**
- **Script Processing**: Originele tekst → emotie detectie → SSML conversie
- **API Calls**: Exacte parameters naar ElevenLabs
- **Voice Settings**: Toegepaste emotie-instellingen per stem
- **Audio Processing**: Volume adjustments en combinatie stappen
- **Error Tracking**: Debugging informatie

### Console Output
```
🎭 lucas: emotions={'stability': 0.9, 'style': 0.2}
📝 Processed: '<emphasis level="strong">heel belangrijk</emphasis>...'
🔊 Converting with stability=0.9, style=0.2: 'Dit is heel belangrijk...'
✓ Created temp_lucas_1.mp3 (15,234 bytes)
📊 Voice volumes: {'lucas': 0, 'emma': 2}
🎵 Combining 8 audio segments...
✅ Combined podcast: episode_001.mp3 (3.2 minutes)
📋 Detailed log saved to: logs/episode_001_20241216_143022.log
```

## 🛡️ Privacy & Compliance

### GDPR Compliance
- **ElevenLabs**: Volledig GDPR-compliant met EU data residency opties
- **No Training Use**: Consumer conversations niet gebruikt voor model training
- **Data Control**: Volledige gebruikerscontrole over data retention
- **Dutch Context**: Optimaal voor Nederlandse culturele projecten

### Enterprise Features
- **Zero Data Retention**: Immediate deletion na processing
- **EU Data Residency**: Data processing binnen EU grenzen
- **SOC2 Type II**: Enterprise-grade security certificering
- **Volume Discounts**: Beschikbaar voor grootschalige projecten

## 💰 Kosten Optimalisatie

### Character Efficiency
- **SSML Optimalisatie**: Minimale markup voor kostenbesparingen
- **Emotion Caching**: Hergebruik van voice settings
- **Batch Processing**: Efficiente API calls

### Kostenschatting
```
Gemiddelde 15-min podcast episode:
- Script lengte: ~8000 characters
- ElevenLabs kosten: €2-5 per episode
- Afhankelijk van subscription tier
```

### Best Practices
1. **Voice Consistency**: Gebruik zelfde voice IDs voor character continuity
2. **Emotion Efficiency**: Optimaliseer emotie gebruik voor kosten
3. **Batch Generation**: Genereer meerdere episodes in één sessie
4. **Script Optimization**: Minimaliseer onnodige markup

## 🔧 Advanced Configuration

### Custom Model Selection
```ini
[audio]
model = eleven_multilingual_v2    # Beste kwaliteit voor Nederlands
# model = eleven_turbo_v2         # Snellere/goedkopere optie
optimize_streaming_latency = 0
output_format = mp3_44100_128
```

### Voice Model Configuratie
```ini
[voice_settings_lucas]
default_volume = 0
default_stability = 0.8           # Hoger = consistenter
default_style = 0.3               # Hoger = expressiever
# ElevenLabs specifiek
similarity_boost = 0.8            # Voice similarity
use_speaker_boost = true          # Extra voice enhancement
```

## 🔍 Troubleshooting

### Common Issues

**FFmpeg Not Found:**
```bash
# Windows: Check C:\ffmpeg\bin\ffmpeg.exe exists
# Linux/macOS: Install via package manager
which ffmpeg
```

**API Errors:**
```python
# Check API key
print(config['api_key'])

# Verify voice IDs (without quotes)
print(config['voices'])
```

**Voice Settings Not Applied:**
```python
# Check config file syntax
[voice_settings_voicename]  # Must match voice name exactly
```

**Audio Quality Issues:**
```python
# Use post-processor for professional quality
from src.podcast_postprocessor import PodcastPostProcessor
processor = PodcastPostProcessor()
processor.apply_mastering_chain("input.mp3", "output.mp3", preset="podcast")
```

### Debug Mode
```python
# Enable detailed logging
processor = PodcastPostProcessor(debug=True)
```

## 🎯 Best Practices

### Script Writing
1. **Natural Flow**: Schrijf zoals mensen echt praten
2. **Emotion Progression**: Varieer emotie-intensiteit natuurlijk
3. **Pause Strategy**: Gebruik `[PAUZE]` voor dramatische effecten
4. **Voice Balance**: Test verschillende stemmen en volume instellingen

### Production Workflow
1. **Script Development**: Schrijf en test in kleine segmenten
2. **Voice Testing**: Test emotie-instellingen per stem
3. **Batch Generation**: Genereer meerdere episodes tegelijk
4. **Post-Processing**: Gebruik SoX mastering voor professional quality
5. **Quality Control**: Analyseer audio metrics voor consistency

### Performance Optimization
1. **Config Caching**: Hergebruik configuraties tussen episodes
2. **Batch API Calls**: Minimaliseer API roundtrips
3. **Local Processing**: Gebruik lokale audio processing waar mogelijk
4. **Memory Management**: Cleanup temporary files automatisch

## 📚 Documentation

### Complete References
- **SSML Guide**: `docs/ssml_dsl_table.md` - Complete markup reference
- **Voice Config**: Uitgebreide voice configuration voorbeelden
- **Project Utils**: Multi-project management workflows
- **Post-Processing**: Professional audio mastering guide

### Code Examples
```python
# Basis gebruik
from src.project_utils import ProjectManager

pm = ProjectManager()
generator = pm.create_generator("mijn_podcast")
output = generator.create_podcast(script, "episode_001")

# Met post-processing
from src.podcast_postprocessor import PodcastPostProcessor
processor = PodcastPostProcessor()
mastered = processor.apply_mastering_chain(output, "episode_001_mastered.mp3")
```

## 🚀 Future Roadmap

### Planned Features
- **Multi-Language Support**: Uitbreiding naar Engels en Duits
- **Voice Cloning**: Custom voice training voor unieke karakters
- **Advanced SSML**: Phonetic pronunciation overrides
- **Cloud Integration**: Direct upload naar podcast platforms
- **Analytics Dashboard**: Usage en quality metrics

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests voor nieuwe functionaliteit
4. Submit pull request

---

**Made with ❤️ for professional Dutch podcast production**

*For support, issues, or feature requests, please check the documentation or create an issue on GitHub.*