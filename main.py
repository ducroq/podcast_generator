#!/usr/bin/env python3
"""
Main script for Mondriaan de Denker podcast generator
"""

from src.podcast_generator import PodcastGenerator
from src.config_loader import load_config

def main():
    # Load configuration
    config = load_config()
    
    # Sample script with natural Dutch emotion markers
    script = """
[HOST A]: [vrolijk] Welkom bij Mondriaan de **Denker**! Ik ben Lucas.
[HOST B]: [super enthousiast] En ik ben Emma. (snel) Vandaag duiken we supersnel in Mondriaans *filosofie* (/snel)!
[PAUZE]
[HOST A]: [nieuwsgierig] Wist je dat Mondriaan ~eigenlijk~ meer dan honderd teksten heeft geschreven? (kort pauze) [verrast] (hoog) HONDERD (/hoog)!
[HOST B]: [geschokt] (laag) Echt waar? (/laag) [fluisterend] (fluister) Ik dacht dat hij alleen _schilderde_ (/fluister)!
[HOST A]: [oprecht geïnteresseerd] (langzaam) Nee, hij was een echte filosoof! (/langzaam) [trots] Hij wilde de wereld veranderen met zijn kunst.
"""
    
    generator = PodcastGenerator(
        api_key=config['api_key'],
        host_a_voice=config['host_a_voice'],
        host_b_voice=config['host_b_voice'],
        host_a_volume=config['host_a_volume'],
        host_b_volume=config['host_b_volume']
    )
    
    output_file = generator.create_podcast(script, "output/episode_01A")
    print(f"✓ Podcast created: {output_file}")

if __name__ == "__main__":
    main()