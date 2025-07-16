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