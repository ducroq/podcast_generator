"""
Project utilities for managing different podcast projects
"""

import os
from src.config_loader import load_config
from src.podcast_generator import PodcastGenerator

class ProjectManager:
    """Manages different podcast projects with their own configs"""
    
    def __init__(self, base_dir="projects"):
        self.base_dir = base_dir
    
    def create_project_structure(self, project_name):
        """Create directory structure for a new project"""
        project_dir = os.path.join(self.base_dir, project_name)
        config_dir = os.path.join(project_dir, "config")
        credentials_dir = os.path.join(config_dir, "credentials")
        scripts_dir = os.path.join(project_dir, "scripts")
        output_dir = os.path.join(project_dir, "output")
        
        # Create directories
        for directory in [project_dir, config_dir, credentials_dir, scripts_dir, output_dir]:
            os.makedirs(directory, exist_ok=True)
        
        print(f"✓ Created project structure for '{project_name}'")
        print(f"📁 Project directory: {project_dir}")
        print(f"⚙️ Config directory: {config_dir}")
        print(f"📝 Scripts directory: {scripts_dir}")
        print(f"🎵 Output directory: {output_dir}")
        
        return {
            'project_dir': project_dir,
            'config_dir': config_dir,
            'scripts_dir': scripts_dir,
            'output_dir': output_dir
        }
    
    def load_project(self, project_name):
        """Load a specific project's configuration"""
        project_dir = os.path.join(self.base_dir, project_name)
        config_dir = os.path.join(project_dir, "config")
        
        if not os.path.exists(config_dir):
            raise FileNotFoundError(f"Project '{project_name}' not found at {project_dir}")
        
        # Load config from project directory
        config = load_config(config_dir)
        
        print(f"🎙️ Loaded project: {project_name}")
        print(f"✓ Voices: {list(config['voices'].keys())}")
        print(f"✓ Aliases: {config['voice_aliases']}")
        
        return config, project_dir
    
    def create_generator(self, project_name):
        """Create a podcast generator for a specific project"""
        config, project_dir = self.load_project(project_name)
        generator = PodcastGenerator(config)
        
        # Add project-specific output path
        generator.project_dir = project_dir
        generator.output_dir = os.path.join(project_dir, "output")
        
        return generator
    
    def list_projects(self):
        """List all available projects"""
        if not os.path.exists(self.base_dir):
            print(f"No projects directory found at: {self.base_dir}")
            return []
        
        projects = []
        for item in os.listdir(self.base_dir):
            project_path = os.path.join(self.base_dir, item)
            config_path = os.path.join(project_path, "config", "config.ini")
            
            if os.path.isdir(project_path) and os.path.exists(config_path):
                projects.append(item)
        
        if projects:
            print("📚 Available projects:")
            for i, project in enumerate(projects, 1):
                print(f"  {i}. {project}")
        else:
            print("No projects found.")
        
        return projects

def create_sample_config(project_dir, voices_config=None):
    """Create sample config files for a new project"""
    config_dir = os.path.join(project_dir, "config")
    
    # Default voices if none provided
    if not voices_config:
        voices_config = {
            'host_a': 'your_voice_id_1',
            'host_b': 'your_voice_id_2'
        }
    
    # Create config.ini
    config_content = f"""# config.ini - Podcast Configuration

[voices]
"""
    
    for voice_name, voice_id in voices_config.items():
        config_content += f"{voice_name} = {voice_id}\n"
    
    config_content += """
[voice_aliases]
# Add aliases for easier scripting
# expert = host_a
# curious = host_b

"""
    
    # Add voice settings sections
    for voice_name in voices_config.keys():
        config_content += f"""[voice_settings_{voice_name}]
# {voice_name} voice settings
default_volume = 0
default_stability = 0.7
default_style = 0.4
# Add emotional variants:
# thoughtful_stability = 0.8
# thoughtful_style = 0.2
# excited_stability = 0.5
# excited_style = 0.6

"""
    
    config_content += """[audio]
model = eleven_multilingual_v2
optimize_streaming_latency = 0
output_format = mp3_44100_128

[podcast]
default_pause_duration = 0.5
long_pause_duration = 1.0
episode_intro_music = true
episode_outro_music = true"""
    
    # Write config.ini
    with open(os.path.join(config_dir, "config.ini"), "w") as f:
        f.write(config_content)
    
    # Create secrets.ini template
    secrets_content = """[elevenlabs]
api_key = your_elevenlabs_api_key_here"""
    
    with open(os.path.join(config_dir, "credentials", "secrets.ini"), "w") as f:
        f.write(secrets_content)
    
    print(f"✓ Created sample config files in {config_dir}")
    print(f"📝 Please edit config/credentials/secrets.ini with your API key")
    print(f"📝 Please edit config/config.ini with your voice IDs")

# Example usage functions
def quick_start_project(project_name, voices=None):
    """Quick start a new project with sample configs"""
    pm = ProjectManager()
    
    # Create project structure
    dirs = pm.create_project_structure(project_name)
    
    # Create sample config
    create_sample_config(dirs['project_dir'], voices)
    
    print(f"\n🚀 Project '{project_name}' is ready!")
    print(f"📋 Next steps:")
    print(f"   1. Edit {dirs['config_dir']}/credentials/secrets.ini")
    print(f"   2. Edit {dirs['config_dir']}/config.ini")
    print(f"   3. Put your scripts in {dirs['scripts_dir']}")
    print(f"   4. Run: python generate_podcast.py {project_name}")
    
    return dirs