import json
from pathlib import Path
from core.game import gameLoop

BASE_DIR = Path(__file__).resolve().parent


def load_config():
    """Load the config JSON file."""
    config_path = BASE_DIR / "data" / "usrSettings.json"
    with open(config_path, "r") as f:
        return json.load(f)


def main():
    print("Starting Pac-Man...")
    settings = load_config()
    gameLoop(settings)


if __name__ == "__main__":
    main()
