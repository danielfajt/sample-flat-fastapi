"""
1) Get latest TAG and short SHA from Git as well as how many commits exist prior that tag.
2) Create full image name with tags.
3) Build image and show warnings if some prior commits exist.
"""

import json
import subprocess
from pathlib import Path

project_root = Path(__name__).parent.parent.absolute()
print(project_root)

subprocess.run(['docker-compose', '-f', f'{project_root}/.devcontainer/docker-compose.yml', 'build', '--quiet', 'app'])

# Build dev image with project's Python version
cmd = ['python', 'scripts/.build_image.py']
result = subprocess.run(
    ['docker-compose', '-f', f'{project_root}/.devcontainer/docker-compose.yml', 'run', '--rm', 'app', *cmd],
    stdout=subprocess.PIPE,
    text=True,
)

project_meta = json.loads(result.stdout)


# # Build image
subprocess.run(['docker', 'build', '-t', project_meta["image_name"], f'{project_root}'])
print('\nIMAGE:\n', 'name:', project_meta["image_name"], '\n')

# Warnings
if int(project_meta["commits_ahead"]) > 0:
    print('WARNING:\n', f'There is/are {project_meta["commits_ahead"]} commit(s) ahead prior to the last tag in git.\n')
