from pathlib import Path
from core.settingsManager import SettingsManager
from core.game import gameLoop

BASE_DIR = Path(__file__).resolve().parent


def main():
    print("Starting Pac-Man...")

    config_path = BASE_DIR / "data" / "usrSettings.json"
    settings = SettingsManager(config_path)

    gameLoop(settings)


if __name__ == "__main__":
    main()
