"""
Configuration loader for podcast generator
"""

import configparser
import os

def load_config():
    """Load configuration from config files"""
    # Load secrets
    secrets = configparser.ConfigParser()
    secrets_path = 'config/credentials/secrets.ini'
    
    if not os.path.exists(secrets_path):
        raise FileNotFoundError(f"Secrets file not found: {secrets_path}")
    
    secrets.read(secrets_path)
    
    # Load public config
    config = configparser.ConfigParser()
    config_path = 'config/config.ini'
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    config.read(config_path)
    
    return {
        'api_key': secrets['elevenlabs']['api_key'],
        'host_a_voice': config['voices']['host_a'],
        'host_b_voice': config['voices']['host_b'],
        'pause_duration': config.getint('audio', 'pause_duration', fallback=1000),
        'host_a_volume': config.getint('audio', 'host_a_volume', fallback=0),
        'host_b_volume': config.getint('audio', 'host_b_volume', fallback=0)
    }