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