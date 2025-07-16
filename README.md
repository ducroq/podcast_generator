# Podcast Generator

AI-powered podcast generator with advanced Dutch markup language and voice-specific emotional settings.

Automatische podcast generatie met ElevenLabs AI voices voor professionele podcast series met geavanceerde emotie-ondersteuning.

## ✨ Features

- **Advanced Dutch Markup Language**: 40+ Nederlandse emotie markers
- **Voice-Specific Settings**: Gepersonaliseerde emotie-instellingen per stem
- **Project Management**: Georganiseerde project structuur
- **SSML Support**: Volledige Speech Synthesis Markup Language ondersteuning
- **Audio Processing**: Automatische volume balancing en normalisatie
- **Detailed Logging**: Uitgebreide logs voor debugging en optimalisatie

## 🚀 Quick Start

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

### 3. Project aanmaken
```python
from src.project_utils import quick_start_project

# Maak een nieuw project
quick_start_project("mijn_podcast", {
    'host_a': 'jouw_voice_id_1',
    'host_b': 'jouw_voice_id_2'
})
```

### 4. Config bestanden invullen
1. Edit `projects/mijn_podcast/config/credentials/secrets.ini`:
```ini
[elevenlabs]
api_key = jouw_echte_api_key_hier
```

2. Edit `projects/mijn_podcast/config/config.ini` met je voice IDs en instellingen

## 🎭 Voice System

### Voice Configuration
Het systeem ondersteunt stem-specifieke instellingen:

```ini
[voices]
lucas = jouw_voice_id_1
emma = jouw_voice_id_2

[voice_aliases]
expert = lucas
curious = emma

[voice_settings_lucas]
default_volume = 0
default_stability = 0.8
default_style = 0.3
# Emotie-specifieke instellingen
thoughtful_stability = 0.9
thoughtful_style = 0.2
passionate_stability = 0.6
passionate_style = 0.6

[voice_settings_emma]
default_volume = 2
default_stability = 0.6
default_style = 0.5
excited_stability = 0.3
excited_style = 0.8
```

## 📝 Script Format

### Basis Structuur
```python
script = """
[lucas]: [thoughtful] Welkom bij Mondriaan de **Denker**!
[emma]: [enthusiastic] En ik ben Emma!
[PAUZE]
[lucas]: [calm] Wist je dat Mondriaan *filosoof* was? (pauze) ECHT waar!
[emma]: [surprised] Echt waar? Ik dacht dat hij alleen _schilderde_!
"""
```

### Nederlandse Emotie Markers (40+ ondersteuning)

**Positieve Emoties:**
- `[vrolijk]` - vrolijke stemming
- `[blij]` - blijdschap
- `[enthousiast]` - enthousiasme
- `[opgewonden]` - opwinding
- `[speels]` - speelse toon
- `[trots]` - trots
- `[zelfverzekerd]` - zelfvertrouwen
- `[tevreden]` - tevredenheid
- `[lachend]` - lachende toon

**Nieuwsgierigheid & Interesse:**
- `[nieuwsgierig]` - nieuwsgierigheid
- `[geïnteresseerd]` - interesse
- `[oprecht geïnteresseerd]` - oprechte interesse
- `[fascinerend]` - fascinatie
- `[verwonderd]` - verwondering

**Verrassing & Ontdekking:**
- `[verrast]` - verrassing
- `[verbaasd]` - verbazing
- `[geschokt]` - shock
- `[onder de indruk]` - indruk

**Rust & Bezonkenheid:**
- `[rustig]` - rustige toon
- `[kalm]` - kalmte
- `[bedachtzaam]` - bedachtzaamheid
- `[peinzend]` - peinzende toon
- `[wijsheid]` - wijze toon
- `[serieus]` - serieuze toon

**Twijfel & Onzekerheid:**
- `[aarzelend]` - aarzeling
- `[onzeker]` - onzekerheid
- `[twijfelend]` - twijfel
- `[voorzichtig]` - voorzichtigheid

**Emotionele Tonen:**
- `[bezorgd]` - bezorgdheid
- `[teleurgesteld]` - teleurstelling
- `[verdrietig]` - verdriet
- `[melancholisch]` - melancholie

**Speciale Tonen:**
- `[ironisch]` - ironie
- `[sarcastisch]` - sarcasme
- `[dromerig]` - dromerige toon
- `[mysterieus]` - mysterie
- `[fluisterend]` - fluisterend

**Intensiteit Variaties:**
- `[heel rustig]` - extra rustig
- `[super enthousiast]` - extra enthousiast
- `[licht geamuseerd]` - lichte amusement
- `[diep geraakt]` - diep geraakt

### Backwards Compatibility
Legacy markers blijven ondersteund:
- `[EXCITED]` → `[opgewonden]`
- `[THOUGHTFUL]` → `[bedachtzaam]`
- `[SURPRISED]` → `[verrast]`
- `[CALM]` → `[kalm]`
- `[ENTHUSIASTIC]` → `[enthousiast]`

## 🔧 SSML Markup

### Klemtonen
- `**woord**` → sterke nadruk
- `*woord*` → gematigde nadruk  
- `_woord_` → zachte nadruk
- `~woord~` → zachte spraak (volume omlaag)
- `WOORD` → hoofdletters worden automatisch benadrukt

### Pauzes (Uitgebreid)
- `(pauze)` → korte pauze (0.5s)
- `(lange pauze)` → lange pauze (1.0s)
- `(kort pauze)` → heel korte pauze (0.3s)
- `(stilte)` → langere stilte (1.5s)
- `(lange stilte)` → extra lange stilte (2.0s)

### Volume Controle
- `(fluister) tekst hier (/fluister)` → hele zin fluisteren

### Spreeksnelheid
- `(snel) tekst hier (/snel)` → snel spreken
- `(langzaam) tekst hier (/langzaam)` → langzaam spreken
- `(supersnel) tekst hier (/supersnel)` → extra snel

### Toonhoogte
- `(hoog) tekst hier (/hoog)` → hoge toon
- `(laag) tekst hier (/laag)` → lage toon
- `(superhoog) tekst hier (/superhoog)` → extra hoge toon
- `(superlaag) tekst hier (/superlaag)` → extra lage toon

### Voorbeelden
```
[lucas]: Dit is **heel belangrijk**! (snel) Dit ging supersnel (/snel), maar (hoog) dit heel hoog (/hoog)!
[emma]: [verrast] (fluister) Wow, dat wist ik niet... (/fluister) [enthousiast] Vertel meer!
```

## 🎵 Audio Processing

### Geavanceerde Features
- **Voice-specific Volume Balancing**: Automatische volume aanpassingen per stem
- **Smart Pause Detection**: Intelligente pauze plaatsing na `[PAUZE]` markers
- **Audio Normalization**: Automatische normalisatie van eindproduct
- **Quality Export**: High-quality MP3 export (128kbps, 44.1kHz)

### Volume Instellingen
```ini
[voice_settings_lucas]
default_volume = 0    # Geen aanpassing
[voice_settings_emma]
default_volume = 2    # +2dB luider
```

## 📊 Project Management

### Project Structuur
```
projects/
├── mijn_podcast/
│   ├── config/
│   │   ├── config.ini
│   │   └── credentials/
│   │       └── secrets.ini
│   ├── scripts/
│   ├── output/
│   └── logs/
```

### Gebruik
```python
from src.project_utils import ProjectManager

pm = ProjectManager(base_dir="projects")
generator = pm.create_generator("mijn_podcast")
output_file = generator.create_podcast(script, "episode_001")
```

## 📋 Detailed Logging

Het systeem genereert uitgebreide logs voor elke episode:

```
logs/
├── episode_001_20241216_143022.log
```

Logs bevatten:
- **API calls**: Exacte parameters naar ElevenLabs
- **Voice settings**: Toegepaste emotie-instellingen
- **SSML processing**: Markup conversie details
- **Audio processing**: Volume adjustments en combinatie stappen
- **Error tracking**: Debugging informatie

## 💰 Kosten

ElevenLabs rekent per karakter:
- **Gemiddelde 15-min aflevering**: €2-5 afhankelijk van je plan
- **Character optimization**: Intelligent SSML gebruik voor kostenefficiëntie
- **Voice reuse**: Hergebruik van stemmen voor kostenbesparingen

## 🔍 Troubleshooting

### FFmpeg Issues
```bash
# Controleer FFmpeg installatie
ffmpeg -version

# Windows: zorg dat C:\ffmpeg\bin\ffmpeg.exe bestaat
# Script zoekt automatisch naar deze locatie
```

### API Errors
```python
# Controleer je API key
print(config['api_key'])

# Controleer voice IDs (geen quotes!)
print(config['voices'])
```

### Voice Settings Debug
```python
# Gebruik detailed logging voor debugging
generator = pm.create_generator("mijn_podcast")
output_file = generator.create_podcast(script, "debug_episode")
# Check logs/debug_episode_*.log voor details
```

## 🛠️ Advanced Configuration

### Custom Model Selection
```ini
[audio]
model = eleven_multilingual_v2
optimize_streaming_latency = 0
output_format = mp3_44100_128
```

### Episode Settings
```ini
[podcast]
default_pause_duration = 0.5
long_pause_duration = 1.0
episode_intro_music = true
episode_outro_music = true
```

## 🎯 Best Practices

1. **Voice Consistency**: Gebruik dezelfde voice IDs voor character continuity
2. **Emotion Gradation**: Varieer emotie-intensiteit voor natuurlijke conversaties
3. **Pause Strategy**: Gebruik `[PAUZE]` voor dramatische effecten
4. **Volume Balancing**: Test verschillende stemmen en pas volume aan in config
5. **Script Testing**: Test korte segmenten voordat je volledige episodes genereert

## 📚 More Information

- **SSML Reference**: Zie `docs/ssml_dsl_table.md` voor complete markup guide
- **Voice Configuration**: Uitgebreide voice settings in project config
- **Project Management**: Gebruik `src/project_utils.py` voor multi-project workflows

---

**Made with ❤️ for professional podcast production**