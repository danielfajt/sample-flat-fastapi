"""

Python >= 3.11


Get project metadata to compose Docker image name:tag. Output is printed as JSON to STDOUT as the
script is meant to be run within ./devcontainer/docker-compose -> APP environment.

1) Read pyproject.toml from project root and get APP_NAME, APP_VERSION.
1) Get latest TAG, SHORT_HASH and COMMITS_AHEAD from the Git repository.
2) Get currently checkouted BRANCH_NAME from the Git repository.
3) Create TIME_TAG with timezone.

WARNING: Currently, the TIME_TAG doesn't contain timezone.
It is used for docker image TAG which doesn't support + character.
"""

if __name__ == "__main__":

    import json
    import subprocess
    from datetime import datetime
    from pathlib import Path
    from zoneinfo import ZoneInfo

    import tomllib

    # Read data from pyproject.toml
    toml_path = f"{Path(__name__).parent.absolute()}/pyproject.toml"

    with open(toml_path, 'rb') as f:
        toml_dict = tomllib.load(f)

    APP_NAME = toml_dict["tool"]["poetry"]["name"]
    APP_VERSION = toml_dict["tool"]["poetry"]["version"]

    # Get Git info: <version>-<commits ahead>-<short hash>
    # Example: 1.0.9-2-ga0f2562
    git_info_cmd = subprocess.run(['git', 'describe', '--long'], stdout=subprocess.PIPE, text=True)

    TAG, COMMITS_AHEAD, SHORT_HASH = [item.strip() for item in git_info_cmd.stdout.split('-')]
    COMMITS_AHEAD = int(COMMITS_AHEAD)
    SHORT_HASH = SHORT_HASH[1:]  # Cut "g" from the short hash value. ex.: ga0f2562

    # Get current branch name
    branch_name_cmd = subprocess.run(['git', 'branch', '--show-current'], stdout=subprocess.PIPE, text=True)
    BRANCH_NAME = branch_name_cmd.stdout.strip().replace('/', '_')

    # Time tag [YY-MM-DD-HH:MM:SS-Tz -> 221012145303T+0200]
    # TIME_TAG = datetime.now(ZoneInfo('Europe/Prague')).strftime("%y%m%d%H%M%ST%z")

    # No timezone as docker tag doesn't support + character
    TIME_TAG = datetime.now(ZoneInfo('Europe/Prague')).strftime("%y%m%d%H%M%S")

    # Full image 'name:tag'
    IMAGE_NAME = f'{APP_NAME}:{BRANCH_NAME}-{APP_VERSION}-{SHORT_HASH}'

    out = {
        "app_version": APP_VERSION,
        "commits_ahead": COMMITS_AHEAD,
        "short_hash": SHORT_HASH,
        "branch_name": BRANCH_NAME,
        "time_tag": TIME_TAG,
        "image_name": IMAGE_NAME,
    }

    print(json.dumps(out, ensure_ascii=True, default=str))
