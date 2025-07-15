"""
SSML processor for converting markup to Speech Synthesis Markup Language
"""

import re

class SSMLProcessor:
    """Processes custom markup and converts to SSML"""
    
    def __init__(self):
        self.emotion_markers = ['[EXCITED]', '[THOUGHTFUL]', '[SURPRISED]', '[CALM]', '[ENTHUSIASTIC]']
    
    def process_text(self, text):
        """Main processing function"""
        text = self._clean_emotion_markers(text)
        text = self._process_emphasis_markers(text)
        return text
    
    def extract_emotion(self, line):
        """Extract emotion markers and return voice settings"""
        emotions = {
            '[EXCITED]': {"stability": 0.2, "style": 0.8},
            '[THOUGHTFUL]': {"stability": 0.8, "style": 0.2},
            '[SURPRISED]': {"stability": 0.3, "style": 0.7},
            '[CALM]': {"stability": 0.9, "style": 0.1},
            '[ENTHUSIASTIC]': {"stability": 0.4, "style": 0.7}
        }
        
        for marker, settings in emotions.items():
            if marker in line:
                return settings
        return {}
    
    def _clean_emotion_markers(self, text):
        """Remove emotion markers from text but keep SSML"""
        for marker in self.emotion_markers:
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
        
        # PAUZES
        text = re.sub(r'\(pauze\)', '<break time="0.5s"/>', text)
        text = re.sub(r'\(lange pauze\)', '<break time="1.0s"/>', text)
        
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