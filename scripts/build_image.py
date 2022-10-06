#!/usr/bin/env python3

"""
1) Get latest TAG and short SHA from Git as well as how many commits exist prior that tag.
2) Create full image name with tags.
3) Build image and show warnings if some prior commits exist.
"""

import subprocess


APP_NAME = None
if APP_NAME is None:
    raise ValueError("Application name is not set in build script.")

# Get Git info: <version>-<commits ahead>-<short hash>
# Example: 1.0.9-2-ga0f2562
git_info_cmd = subprocess.run(['git', 'describe', '--long'], stdout=subprocess.PIPE, text=True)
if git_info_cmd.returncode != 0:
    raise ValueError("Couldn't get tags from the Git.")

tag, commits_ahead, short_hash = [item.strip() for item in git_info_cmd.stdout.split('-')]
commits_ahead = int(commits_ahead)
short_hash = short_hash[1:] # Cut "g" from short hash: ex.: ga0f2562

# Get current branch name
branch_name_cmd = subprocess.run(['git', 'branch', '--show-current'], stdout=subprocess.PIPE, text=True)
branch_name = branch_name_cmd.stdout.strip().replace('/', '_')

print(f'''\n
tag: {tag}
commits ahead: {commits_ahead}
short hash: {short_hash}
branch name: {branch_name}
\n''')

# Build image
image_name = f'{APP_NAME}:{branch_name}-{tag}-{short_hash}'
subprocess.run(['docker', 'build', '-t', image_name, '..'])
print('\nIMAGE:\n', 'name:', image_name, '\n')

# Warnings
if commits_ahead > 0:
    print('WARNING:\n', f'There is/are {commits_ahead} commit(s) ahead prior to the last tag in git.\n')