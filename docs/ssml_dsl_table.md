# SSML en DSL Referentie Tabel - Complete Guide

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

## Voice-Specific Emotie System

### Hoe het werkt
Het systeem gebruikt **voice-specific emotion settings** die geconfigureerd worden per stem:

```ini
[voice_settings_lucas]
default_stability = 0.8
default_style = 0.3
# Emotie-specifieke overrides
thoughtful_stability = 0.9
thoughtful_style = 0.2
passionate_stability = 0.6
passionate_style = 0.6
```

### Emotion Processing Flow
```
Script: [lucas]: [thoughtful] Dit is belangrijk...
↓
1. Detect emotion: "thoughtful"
2. Lookup voice: "lucas"
3. Get settings: lucas.thoughtful_stability/style
4. Apply to ElevenLabs API
5. Generate audio with custom settings
```

## Complete Nederlandse Emotie Markers (40+)

### Positieve Emoties
| Nederlandse DSL | Fallback Voice Settings | Beschrijving |
|-----------------|-------------------------|--------------|
| `[vrolijk]` | `{"stability": 0.3, "style": 0.7}` | Vrolijke stemming |
| `[blij]` | `{"stability": 0.3, "style": 0.6}` | Blijdschap |
| `[opgewonden]` | `{"stability": 0.2, "style": 0.8}` | Opwinding |
| `[enthousiast]` | `{"stability": 0.4, "style": 0.7}` | Enthousiasme |
| `[speels]` | `{"stability": 0.3, "style": 0.8}` | Speelse toon |
| `[trots]` | `{"stability": 0.6, "style": 0.5}` | Trots |
| `[zelfverzekerd]` | `{"stability": 0.7, "style": 0.4}` | Zelfvertrouwen |
| `[tevreden]` | `{"stability": 0.8, "style": 0.3}` | Tevredenheid |
| `[lachend]` | `{"stability": 0.2, "style": 0.9}` | Lachende toon |

### Nieuwsgierigheid & Interesse
| Nederlandse DSL | Fallback Voice Settings | Beschrijving |
|-----------------|-------------------------|--------------|
| `[nieuwsgierig]` | `{"stability": 0.4, "style": 0.6}` | Nieuwsgierigheid |
| `[geïnteresseerd]` | `{"stability": 0.5, "style": 0.5}` | Interesse |
| `[oprecht geïnteresseerd]` | `{"stability": 0.6, "style": 0.5}` | Oprechte interesse |
| `[fascinerend]` | `{"stability": 0.4, "style": 0.7}` | Fascinatie |
| `[verwonderd]` | `{"stability": 0.3, "style": 0.6}` | Verwondering |

### Verrassing & Ontdekking
| Nederlandse DSL | Fallback Voice Settings | Beschrijving |
|-----------------|-------------------------|--------------|
| `[verrast]` | `{"stability": 0.3, "style": 0.7}` | Verrassing |
| `[verbaasd]` | `{"stability": 0.4, "style": 0.6}` | Verbazing |
| `[geschokt]` | `{"stability": 0.2, "style": 0.8}` | Shock |
| `[onder de indruk]` | `{"stability": 0.5, "style": 0.6}` | Indruk |

### Rust & Bezonkenheid
| Nederlandse DSL | Fallback Voice Settings | Beschrijving |
|-----------------|-------------------------|--------------|
| `[rustig]` | `{"stability": 0.9, "style": 0.1}` | Rustige toon |
| `[kalm]` | `{"stability": 0.9, "style": 0.2}` | Kalmte |
| `[bedachtzaam]` | `{"stability": 0.8, "style": 0.2}` | Bedachtzaamheid |
| `[peinzend]` | `{"stability": 0.8, "style": 0.3}` | Peinzende toon |
| `[wijsheid]` | `{"stability": 0.9, "style": 0.2}` | Wijze toon |
| `[serieus]` | `{"stability": 0.8, "style": 0.3}` | Serieuze toon |

### Twijfel & Onzekerheid
| Nederlandse DSL | Fallback Voice Settings | Beschrijving |
|-----------------|-------------------------|--------------|
| `[aarzelend]` | `{"stability": 0.6, "style": 0.4}` | Aarzeling |
| `[onzeker]` | `{"stability": 0.5, "style": 0.4}` | Onzekerheid |
| `[twijfelend]` | `{"stability": 0.6, "style": 0.3}` | Twijfel |
| `[voorzichtig]` | `{"stability": 0.7, "style": 0.3}` | Voorzichtigheid |

### Emotionele Tonen
| Nederlandse DSL | Fallback Voice Settings | Beschrijving |
|-----------------|-------------------------|--------------|
| `[bezorgd]` | `{"stability": 0.5, "style": 0.5}` | Bezorgdheid |
| `[teleurgesteld]` | `{"stability": 0.6, "style": 0.4}` | Teleurstelling |
| `[verdrietig]` | `{"stability": 0.7, "style": 0.3}` | Verdriet |
| `[melancholisch]` | `{"stability": 0.8, "style": 0.3}` | Melancholie |

### Speciale Tonen
| Nederlandse DSL | Fallback Voice Settings | Beschrijving |
|-----------------|-------------------------|--------------|
| `[ironisch]` | `{"stability": 0.4, "style": 0.6}` | Ironie |
| `[sarcastisch]` | `{"stability": 0.5, "style": 0.7}` | Sarcasme |
| `[dromerig]` | `{"stability": 0.7, "style": 0.4}` | Dromerige toon |
| `[mysterieus]` | `{"stability": 0.6, "style": 0.5}` | Mysterie |
| `[fluisterend]` | `{"stability": 0.8, "style": 0.2}` | Fluisterend |

### Intensiteit Variaties
| Nederlandse DSL | Fallback Voice Settings | Beschrijving |
|-----------------|-------------------------|--------------|
| `[heel rustig]` | `{"stability": 0.95, "style": 0.1}` | Extra rustig |
| `[super enthousiast]` | `{"stability": 0.1, "style": 0.9}` | Extra enthousiast |
| `[licht geamuseerd]` | `{"stability": 0.6, "style": 0.4}` | Lichte amusement |
| `[diep geraakt]` | `{"stability": 0.7, "style": 0.5}` | Diep geraakt |

## Backwards Compatibility

### Legacy Markers (Fully Supported)
| Legacy DSL | Nederlandse Equivalent | Beschrijving |
|------------|------------------------|--------------|
| `[EXCITED]` | `[opgewonden]` | Levendig, enthousiast |
| `[THOUGHTFUL]` | `[bedachtzaam]` | Bedachtzaam, rustig |
| `[SURPRISED]` | `[verrast]` | Verrast, geanimeerd |
| `[CALM]` | `[kalm]` | Kalm, stabiel |
| `[ENTHUSIASTIC]` | `[enthousiast]` | Vol energie |

### English Variants (Also Supported)
| English DSL | Nederlandse Equivalent | Beschrijving |
|-------------|------------------------|--------------|
| `[curious]` | `[nieuwsgierig]` | Nieuwsgierigheid |
| `[confident]` | `[zelfverzekerd]` | Zelfvertrouwen |
| `[passionate]` | `[hartstochtelijk]` | Passie |
| `[contemplative]` | `[bedachtzaam]` | Contemplatief |
| `[realization]` | `[onder de indruk]` | Besef |

## Configuration Examples

### Basic Voice Setup
```ini
[voices]
lucas = your_voice_id_1
emma = your_voice_id_2

[voice_aliases]
expert = lucas
curious = emma
```

### Advanced Voice Settings
```ini
[voice_settings_lucas]
default_volume = 0
default_stability = 0.8
default_style = 0.3
# Emotie-specifieke overrides
thoughtful_stability = 0.9
thoughtful_style = 0.2
passionate_stability = 0.6
passionate_style = 0.6
confident_stability = 0.8
confident_style = 0.4

[voice_settings_emma]
default_volume = 2
default_stability = 0.6
default_style = 0.5
excited_stability = 0.3
excited_style = 0.8
curious_stability = 0.4
curious_style = 0.6
surprised_stability = 0.2
surprised_style = 0.8
```

## Usage Examples

### Basic Conversation
```
[lucas]: [thoughtful] Welkom bij de podcast.
[emma]: [enthusiastic] Hallo iedereen!
```

### Advanced Emotional Progression
```
[lucas]: [calm] Laten we beginnen met een simpele vraag...
[emma]: [curious] Oké, ik luister.
[lucas]: [passionate] Mondriaan geloofde dat kunst de wereld kon veranderen!
[emma]: [surprised] Echt waar? [fascinerend] Dat is ongelofelijk!
[lucas]: [proud] Precies! [thoughtful] En dat is nog maar het begin...
```

### Mixed Markup
```
[lucas]: [thoughtful] Dit is **heel belangrijk**! (pauze) Mondriaan schreef *meer dan honderd* teksten.
[emma]: [surprised] (hoog) HONDERD? (/hoog) [excited] (snel) Dat wist ik niet! (/snel)
[PAUZE]
[lucas]: [calm] (langzaam) Laten we dieper ingaan op zijn filosofie... (/langzaam)
```

## Audio Processing Integration

### Volume Balancing
```ini
[voice_settings_lucas]
default_volume = 0      # Baseline
[voice_settings_emma]
default_volume = 2      # +2dB luider
```

### Pause Detection
```
[PAUZE]  # Creates longer pause in audio processing
```

### Smart Gap Management
- **Normal gaps**: 150ms between speakers
- **Pause gaps**: 800ms after `[PAUZE]` markers
- **Configurable**: Via `config.ini` podcast settings

## Error Handling

### Missing Voice Settings
```python
# Fallback to default emotions if voice not configured
if voice_name not in self.voice_settings:
    return self.default_emotions.get(emotion_marker, {})
```

### Emotion Not Found
```python
# Uses voice defaults if emotion not configured
if emotion not in voice_config['emotions']:
    return voice_config['default_stability/style']
```

## Performance Considerations

### Character Optimization
- **SSML efficiency**: Minimal markup for cost control
- **Emotion processing**: Cached settings per voice
- **Audio processing**: Efficient segment combination

### Voice Reuse
- **Consistent character voices**: Lower learning curve
- **Bulk processing**: Batch API calls when possible
- **Memory management**: Cleanup temporary files

## Debugging & Logging

### Console Output
```
🎭 lucas: emotions={'stability': 0.9, 'style': 0.2}
📝 Processed: '<emphasis level="strong">belangrijk</emphasis>...'
🔊 Converting with stability=0.9, style=0.2: 'Dit is heel belangrijk...'
```

### Detailed Logs
```
=== PROCESSING: lucas (lucas) ===
Original text: [thoughtful] Dit is **heel belangrijk**!
Detected emotions: {'stability': 0.9, 'style': 0.2}
Voice settings: {'stability': 0.9, 'style': 0.2, 'similarity_boost': 0.8}
Processed text: <emphasis level="strong">heel belangrijk</emphasis>!
```

## Advanced Features

### Multi-Language Support
```python
# English emotions also supported
'[excited]': {"stability": 0.2, "style": 0.8},
'[confident]': {"stability": 0.7, "style": 0.4},
```

### Custom Emotion Mapping
```python
# Add custom emotions in config
self.emotion_name_mapping = {
    '[jouw_emotie]': 'custom_emotion_name'
}
```

### Future Extensions
- **Phonetic overrides**: `(uitspraak: huːs) huis`
- **Voice switching**: `(stem: Rachel) tekst (/stem)`
- **Percentage pitch**: `(pitch: +20%) tekst (/pitch)`

---

**This system provides the most advanced Dutch podcast markup language with voice-specific emotional intelligence for professional audio production.**