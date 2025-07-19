"""
SSML processor for converting markup to Speech Synthesis Markup Language
with voice-specific emotion handling - ENHANCED VERSION
"""

import re
import logging

class SSMLProcessor:
    """Processes custom markup and converts to SSML with voice-specific settings"""
    
    def __init__(self, voice_settings=None, enable_detailed_logging=False):
        """Initialize SSML processor with optional voice settings and logging"""
        self.voice_settings = voice_settings or {}
        self.detailed_logging = enable_detailed_logging
        
        if self.detailed_logging:
            self.logger = logging.getLogger('SSML_Processor')
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self.logger.setLevel(logging.INFO)
        
        # UITGEBREIDE Nederlandse emotie mapping
        self.default_emotions = {
            # Positieve emoties
            '[vrolijk]': {"stability": 0.3, "style": 0.7},
            '[blij]': {"stability": 0.3, "style": 0.6},
            '[opgewonden]': {"stability": 0.2, "style": 0.8},
            '[enthousiast]': {"stability": 0.35, "style": 0.7},  # Aangepast voor Lucas
            '[enthusiastic]': {"stability": 0.35, "style": 0.7},  # English variant
            '[excited]': {"stability": 0.2, "style": 0.8},      # English variant
            '[speels]': {"stability": 0.3, "style": 0.8},
            '[trots]': {"stability": 0.6, "style": 0.5},
            '[zelfverzekerd]': {"stability": 0.7, "style": 0.4},
            '[confident]': {"stability": 0.7, "style": 0.4},    # English variant
            '[tevreden]': {"stability": 0.8, "style": 0.3},
            '[lachend]': {"stability": 0.2, "style": 0.9},
            
            # Nieuwsgierigheid & interesse
            '[nieuwsgierig]': {"stability": 0.4, "style": 0.5},  # Voor Emma
            '[curious]': {"stability": 0.4, "style": 0.5},      # English variant
            '[geïnteresseerd]': {"stability": 0.5, "style": 0.5},
            '[oprecht geïnteresseerd]': {"stability": 0.6, "style": 0.5},
            '[fascinerend]': {"stability": 0.4, "style": 0.7},
            '[verwonderd]': {"stability": 0.3, "style": 0.6},
            
            # Verrassing & ontdekking
            '[verrast]': {"stability": 0.3, "style": 0.7},
            '[surprised]': {"stability": 0.3, "style": 0.7},    # English variant
            '[verbaasd]': {"stability": 0.4, "style": 0.5},     # Voor Emma - aangepast
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
            
            # NIEUWE EMOTIES - gevonden in je test script
            '[opbouwend]': {"stability": 0.3, "style": 0.8},       # Building excitement
            '[betekenisvol]': {"stability": 0.6, "style": 0.6},    # Meaningful, profound
            '[bevestigend]': {"stability": 0.35, "style": 0.5},    # Confirmative (voor Lucas)
            '[realiserend]': {"stability": 0.4, "style": 0.5},     # Realizing (voor Emma)
            '[ontroerd]': {"stability": 0.7, "style": 0.4},        # Touched, moved
            '[warm]': {"stability": 0.35, "style": 0.5},           # Warm, friendly (voor Lucas)
            '[filosofisch]': {"stability": 0.8, "style": 0.3},     # Philosophical (voor Piet)
            
            # Aanvullende nuttige emoties
            '[verbazingwekkend]': {"stability": 0.3, "style": 0.7}, # Amazing
            '[inspirerend]': {"stability": 0.5, "style": 0.6},     # Inspiring
            '[intrigerend]': {"stability": 0.4, "style": 0.6},     # Intriguing
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
            '[peinzend]': 'contemplative',
            '[opbouwend]': 'building',
            '[betekenisvol]': 'meaningful',
            '[bevestigend]': 'confirmative',
            '[realiserend]': 'realizing',
            '[ontroerd]': 'touched',
            '[warm]': 'warm',
            '[filosofisch]': 'philosophical'
        }
    
    def process_text(self, text, voice_name=None):
        """Main processing function with enhanced logging"""
        original_text = text
        
        if self.detailed_logging:
            self.logger.info(f"=== PROCESSING START ===")
            self.logger.info(f"Original text: {original_text}")
        
        # Step 1: Extract and log all emotions found
        emotions_found = self.extract_all_emotions(text)
        if self.detailed_logging and emotions_found:
            self.logger.info(f"Emotions found: {emotions_found}")
        
        # Step 2: Process emphasis markers and log transformations
        text_before_emphasis = text
        text = self._process_emphasis_markers(text)
        if self.detailed_logging and text != text_before_emphasis:
            self.logger.info(f"Emphasis transformations applied")
            self._log_transformations(text_before_emphasis, text)
        
        # Step 3: Clean emotion markers
        text = self._clean_emotion_markers(text)
        
        if self.detailed_logging:
            self.logger.info(f"Final processed text: {text}")
            self.logger.info(f"=== PROCESSING END ===")
        
        return text
    
    def extract_emotion(self, line, voice_name=None):
        """Extract emotion markers and return voice settings for specific voice"""
        emotions = self.extract_all_emotions(line)
        primary_emotion = emotions[0] if emotions else None
        
        if self.detailed_logging:
            if emotions:
                self.logger.info(f"Emotions in line: {emotions}")
                if len(emotions) > 1:
                    self.logger.warning(f"Multiple emotions found, using primary: {primary_emotion}")
            else:
                self.logger.info("No emotions found, using default settings")
        
        if primary_emotion:
            settings = self._get_voice_specific_settings(primary_emotion, voice_name)
            if self.detailed_logging:
                self.logger.info(f"Emotion settings for {primary_emotion}: {settings}")
            return settings
        
        # Return default settings for voice if no emotion found
        if voice_name and voice_name in self.voice_settings:
            voice_config = self.voice_settings[voice_name]
            return {
                "stability": voice_config.get('default_stability', 0.7),
                "style": voice_config.get('default_style', 0.4)
            }
        
        return {}
    
    def extract_all_emotions(self, text):
        """Extract ALL emotion markers from text, including inline ones"""
        emotions_found = []
        
        # Find all emotion markers in the text
        emotion_pattern = r'\[([a-zA-ZÀ-ÿ\s]+)\]'
        matches = re.findall(emotion_pattern, text)
        
        for match in matches:
            emotion_marker = f'[{match}]'
            if emotion_marker in self.default_emotions:
                emotions_found.append(emotion_marker)
            elif emotion_marker in self.legacy_mapping:
                emotions_found.append(self.legacy_mapping[emotion_marker])
        
        return emotions_found
    
    def process_text_with_emotion_splits(self, text, voice_name=None):
        """
        Process text that may contain multiple emotion markers
        Returns list of (text_segment, emotion_settings) tuples
        """
        segments = []
        
        # Split on emotion markers while keeping them
        emotion_pattern = r'(\[[a-zA-ZÀ-ÿ\s]+\])'
        parts = re.split(emotion_pattern, text)
        
        current_emotion = None
        
        for part in parts:
            if not part.strip():
                continue
                
            # Check if this part is an emotion marker
            if part.startswith('[') and part.endswith(']'):
                if part in self.default_emotions or part in self.legacy_mapping:
                    current_emotion = part
                continue
            
            # This is actual text content
            if current_emotion:
                settings = self._get_voice_specific_settings(current_emotion, voice_name)
            else:
                settings = self.get_default_voice_settings(voice_name)
                
            # Process the text segment
            processed_text = self._clean_emotion_markers(part)
            processed_text = self._process_emphasis_markers(processed_text)
            
            segments.append((processed_text, settings))
        
        return segments
    
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
        text = re.sub(r'\[([a-zA-ZÀ-ÿ\s]+)\]', '', text)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _process_emphasis_markers(self, text):
        """Convert custom emphasis markers to SSML with detailed logging"""
        original_text = text
        transformations_applied = []
        
        # KLEMTONEN
        # Convert **word** to <emphasis level="strong">word</emphasis>
        if '**' in text:
            text = re.sub(r'\*\*([^*]+)\*\*', r'<emphasis level="strong">\1</emphasis>', text)
            transformations_applied.append('** -> <emphasis level="strong">')
        
        # Convert *word* to <emphasis level="moderate">word</emphasis>  
        if '*' in text and '**' not in original_text:  # Avoid double processing
            text = re.sub(r'\*([^*]+)\*', r'<emphasis level="moderate">\1</emphasis>', text)
            transformations_applied.append('* -> <emphasis level="moderate">')
        
        # Convert _word_ to <emphasis level="reduced">word</emphasis>
        if '_' in text:
            text = re.sub(r'_([^_]+)_', r'<emphasis level="reduced">\1</emphasis>', text)
            transformations_applied.append('_ -> <emphasis level="reduced">')
        
        # Convert ~word~ to <prosody volume="soft">word</prosody> (zachte spraak)
        if '~' in text:
            text = re.sub(r'~([^~]+)~', r'<prosody volume="soft">\1</prosody>', text)
            transformations_applied.append('~ -> <prosody volume="soft">')
        
        # Convert WOORD to <emphasis level="strong">WOORD</emphasis>
        caps_words = re.findall(r'\b([A-Z]{2,})\b', text)
        if caps_words:
            text = re.sub(r'\b([A-Z]{2,})\b', r'<emphasis level="strong">\1</emphasis>', text)
            transformations_applied.append('CAPS -> <emphasis level="strong">')
        
        # PAUZES (uitgebreid)
        pause_mappings = [
            (r'\(pauze\)', '<break time="0.5s"/>', '(pauze)'),
            (r'\(lange pauze\)', '<break time="1.0s"/>', '(lange pauze)'),
            (r'\(kort pauze\)', '<break time="0.3s"/>', '(kort pauze)'),
            (r'\(korte pauze\)', '<break time="0.3s"/>', '(korte pauze)'),
            (r'\(stilte\)', '<break time="1.5s"/>', '(stilte)'),
            (r'\(lange stilte\)', '<break time="2.0s"/>', '(lange stilte)')
        ]
        
        for pattern, replacement, name in pause_mappings:
            if re.search(pattern, text):
                text = re.sub(pattern, replacement, text)
                transformations_applied.append(f'{name} -> {replacement}')
        
        # VOLUME
        volume_mappings = [
            (r'\(fluister\)', '<prosody volume="x-soft">', '(fluister)'),
            (r'\(/fluister\)', '</prosody>', '(/fluister)')
        ]
        
        for pattern, replacement, name in volume_mappings:
            if re.search(pattern, text):
                text = re.sub(pattern, replacement, text)
                transformations_applied.append(f'{name} -> {replacement}')
        
        # SPREEKSNELHEID
        rate_mappings = [
            (r'\(snel\)', '<prosody rate="fast">', '(snel)'),
            (r'\(/snel\)', '</prosody>', '(/snel)'),
            (r'\(langzaam\)', '<prosody rate="slow">', '(langzaam)'),
            (r'\(/langzaam\)', '</prosody>', '(/langzaam)'),
            (r'\(supersnel\)', '<prosody rate="x-fast">', '(supersnel)'),
            (r'\(/supersnel\)', '</prosody>', '(/supersnel)')
        ]
        
        for pattern, replacement, name in rate_mappings:
            if re.search(pattern, text):
                text = re.sub(pattern, replacement, text)
                transformations_applied.append(f'{name} -> {replacement}')
        
        # TOONHOOGTE  
        pitch_mappings = [
            (r'\(hoog\)', '<prosody pitch="high">', '(hoog)'),
            (r'\(/hoog\)', '</prosody>', '(/hoog)'),
            (r'\(laag\)', '<prosody pitch="low">', '(laag)'),
            (r'\(/laag\)', '</prosody>', '(/laag)'),
            (r'\(superhoog\)', '<prosody pitch="x-high">', '(superhoog)'),
            (r'\(/superhoog\)', '</prosody>', '(/superhoog)'),
            (r'\(superlaag\)', '<prosody pitch="x-low">', '(superlaag)'),
            (r'\(/superlaag\)', '</prosody>', '(/superlaag)')
        ]
        
        for pattern, replacement, name in pitch_mappings:
            if re.search(pattern, text):
                text = re.sub(pattern, replacement, text)
                transformations_applied.append(f'{name} -> {replacement}')
        
        # Log transformations if detailed logging is enabled
        if self.detailed_logging and transformations_applied:
            self.logger.info(f"Applied transformations: {', '.join(transformations_applied)}")
        
        return text
    
    def _log_transformations(self, before, after):
        """Log specific transformations that were applied (legacy method for compatibility)"""
        if not self.detailed_logging:
            return
        # This method is now handled within _process_emphasis_markers
        pass