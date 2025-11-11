import json
from pathlib import Path
from core.game import gameloop


def load_config():
    """Load the config JSON file."""
    with open("config.json") as f:
        return json.load(f)


def main():
    print("Starting Pac-Man...")
    settings = load_config()
    gameloop(settings)


if __name__ == "__main__":
    main()
