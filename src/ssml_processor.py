"""
SSML processor for converting markup to Speech Synthesis Markup Language
"""

import re

class SSMLProcessor:
    """Processes custom markup and converts to SSML"""
    
    def __init__(self):
        # Oude emotie markers (backwards compatibility)
        self.legacy_emotions = ['[EXCITED]', '[THOUGHTFUL]', '[SURPRISED]', '[CALM]', '[ENTHUSIASTIC]']
        
        # Nieuwe Nederlandse emotie mapping
        self.dutch_emotions = {
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
    
    def process_text(self, text):
        """Main processing function"""
        text = self._clean_emotion_markers(text)
        text = self._process_emphasis_markers(text)
        return text
    
    def extract_emotion(self, line):
        """Extract emotion markers and return voice settings"""
        # Check for new Dutch emotions first
        for emotion, settings in self.dutch_emotions.items():
            if emotion in line:
                return settings
        
        # Check for legacy emotions (backwards compatibility)
        for legacy, dutch in self.legacy_mapping.items():
            if legacy in line:
                return self.dutch_emotions.get(dutch, {})
        
        return {}
    
    def _clean_emotion_markers(self, text):
        """Remove emotion markers from text but keep SSML"""
        # Remove Dutch emotion markers
        for emotion in self.dutch_emotions.keys():
            text = text.replace(emotion, '')
        
        # Remove legacy markers
        for marker in self.legacy_emotions:
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