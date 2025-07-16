#!/usr/bin/env python3
"""
Main script for Mondriaan de Denker podcast generator
Using ProjectManager for proper path management
"""

from pathlib import Path
from src.project_utils import ProjectManager

def main():
    # Setup project manager met je base directory
    pm = ProjectManager(base_dir=r"C:\local_dev")
    
    # Load het Mondriaan project
    try:
        generator = pm.create_generator("Mondriaan_podcast")
        
        print("🎙️ Mondriaan de Denker Podcast Generator")
        print(f"📁 Project loaded from: {generator.project_dir}")
        print(f"🎵 Output directory: {generator.output_dir}")
        
        # Sample script demonstrating the new voice system
        script = """
[lucas]: [thoughtful] Welkom bij Mondriaan de **Denker**! Ik ben Lucas, en vandaag duiken we diep in de filosofie van Piet Mondriaan.
[emma]: [enthusiastic] En ik ben Emma! [curious] Lucas, ik moet eerlijk zeggen... (kort pauze) ik dacht altijd dat Mondriaan gewoon een kunstenaar was?
[PAUZE]
[lucas]: [calm] Dat denken veel mensen, Emma. Maar Mondriaan heeft meer dan *honderd* teksten geschreven over zijn filosofie!
[emma]: [surprised] (hoog) HONDERD? (/hoog) [excited] Dat is ongelofelijk! Waar ging dat dan over?
[lucas]: [contemplative] (langzaam) Hij geloofde dat kunst de wereld kon veranderen... (/langzaam) [passionate] Door perfecte harmonie te vinden tussen tegenpolen.
[emma]: [fascinerend] ~Tegenpolen?~ Kun je daar een voorbeeld van geven?
[lucas]: [confident] Natuurlijk! Denk aan zijn beroemde schilderijen: (pauze) **verticale** en **horizontale** lijnen, *primaire* kleuren tegen wit...
[emma]: [verwonderd] Oh! [realization] Dus die simpele lijntjes waren eigenlijk heel diep filosofisch bedoeld?
[PAUZE]
[lucas]: [proud] Precies! Mondriaan zocht naar wat hij de 'nieuwe beelding' noemde. (lange pauze) Een universeeltaal die iedereen zou begrijpen.
[emma]: [thoughtful] (fluister) Dat is eigenlijk heel mooi... (/fluister) [enthusiastic] Vertel eens meer over die filosofie!
"""
        
        # Generate podcast - output gaat automatisch naar project/output/
        output_file = generator.create_podcast(script, "episode_test_advanced")
        
        if output_file:
            print(f"🎉 Podcast successfully created: {output_file}")
            print(f"📊 Using voice-specific emotion settings from config")
        else:
            print("❌ Failed to create podcast")
            
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print(f"💡 Make sure your project structure is:")
        print(f"   C:\\local_dev\\Mondriaan_podcast\\config\\config.ini")
        print(f"   C:\\local_dev\\Mondriaan_podcast\\config\\credentials\\secrets.ini")
        
        # Optionally create the project structure
        create_structure = input("\n🔧 Create project structure? (y/n): ")
        if create_structure.lower() == 'y':
            from project_utils import quick_start_project
            
            # Copy your existing config
            print("📋 Creating project structure...")
            quick_start_project("Mondriaan_podcast")
            print("📝 Please move your existing config files to the new structure")

if __name__ == "__main__":
    main()