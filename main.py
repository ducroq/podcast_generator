#!/usr/bin/env python3
"""
Main script for Mondriaan de Denker podcast generator
"""

from src.podcast_generator import PodcastGenerator
from src.config_loader import load_config

def main():
    # Load configuration
    config = load_config()
    
    # Sample script with emotion markers and emphasis
    script = """
[HOST A]: Welkom bij Mondriaan de **Denker**! Ik ben Alex.
[HOST B]: [ENTHUSIASTIC] En ik ben Sam. (snel) Vandaag duiken we supersnel in Mondriaans *filosofie* (/snel)!
[PAUZE]
[HOST A]: [THOUGHTFUL] Wist je dat Mondriaan ~eigenlijk~ meer dan honderd teksten heeft geschreven? (pauze) (hoog) HONDERD (/hoog)!
[HOST B]: [SURPRISED] (laag) Echt waar? (/laag) (fluister) Ik dacht dat hij alleen maar *schilderde* (/fluister)!
[HOST A]: [EXCITED] (langzaam) Nee, hij was een echte filosoof! (/langzaam) Hij wilde de wereld veranderen met zijn kunst.
"""
    
    generator = PodcastGenerator(
        api_key=config['api_key'],
        host_a_voice=config['host_a_voice'],
        host_b_voice=config['host_b_voice'],
        host_a_volume=config['host_a_volume'],
        host_b_volume=config['host_b_volume']
    )
    
    output_file = generator.create_podcast(script, "output/episode_01")
    print(f"✓ Podcast created: {output_file}")

if __name__ == "__main__":
    main()