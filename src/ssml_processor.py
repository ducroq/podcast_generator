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
            '[enthusiastic]': {"stability": 0.4, "style": 0.7},  # English variant
            '[excited]': {"stability": 0.2, "style": 0.8},      # English variant
            '[speels]': {"stability": 0.3, "style": 0.8},
            '[trots]': {"stability": 0.6, "style": 0.5},
            '[zelfverzekerd]': {"stability": 0.7, "style": 0.4},
            '[confident]': {"stability": 0.7, "style": 0.4},    # English variant
            '[tevreden]': {"stability": 0.8, "style": 0.3},
            '[lachend]': {"stability": 0.2, "style": 0.9},
            
            # Nieuwsgierigheid & interesse
            '[nieuwsgierig]': {"stability": 0.4, "style": 0.6},
            '[curious]': {"stability": 0.4, "style": 0.6},      # English variant
            '[geïnteresseerd]': {"stability": 0.5, "style": 0.5},
            '[oprecht geïnteresseerd]': {"stability": 0.6, "style": 0.5},
            '[fascinerend]': {"stability": 0.4, "style": 0.7},
            '[verwonderd]': {"stability": 0.3, "style": 0.6},
            
            # Verrassing & ontdekking
            '[verrast]': {"stability": 0.3, "style": 0.7},
            '[surprised]': {"stability": 0.3, "style": 0.7},    # English variant
            '[verbaasd]': {"stability": 0.4, "style": 0.6},
            '[geschokt]': {"stability": 0.2, "style": 0.8},
            '[onder de indruk]': {"stability": 0.5, "style": 0.6},
            '[realization]': {"stability": 0.5, "style": 0.6},  # English variant
            
            # Rust & bezonkenheid
            '[rustig]': {"stability": 0.9, "style": 0.1},
            '[kalm]': {"stability": 0.9, "style": 0.2},
            '[calm]': {"stability": 0.9, "style": 0.2},         # English variant
            '[bedachtzaam]': {"stability": 0.8, "style": 0.2},
            '[thoughtful]': {"stability": 0.8, "style": 0.2},   # English variant
            '[contemplative]': {"stability": 0.8, "style": 0.2}, # English variant
            '[peinzend]': {"stability": 0.8, "style": 0.3},
            '[wijsheid]': {"stability": 0.9, "style": 0.2},
            '[serieus]': {"stability": 0.8, "style": 0.3},
            '[passionate]': {"stability": 0.6, "style": 0.6},   # English variant
            '[proud]': {"stability": 0.6, "style": 0.5},        # English variant
            
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
        # Remove ALL Dutch emotion markers from our comprehensive list
        for emotion in self.default_emotions.keys():
            text = text.replace(emotion, '')
        
        # Remove legacy markers
        for marker in self.legacy_mapping.keys():
            text = text.replace(marker, '')
        
        # Remove any remaining emotion markers in the pattern [word] 
        # This catches any markers we missed in our lists
        import re
        text = re.sub(r'\[([a-zA-ZÀ-ÿ\s]+)\]', '', text)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        
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