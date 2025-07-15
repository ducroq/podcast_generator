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