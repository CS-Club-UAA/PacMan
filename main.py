from pathlib import Path
from core.settingsManager import SettingsManager
from core.game import Game
from scenes.title_scene import TitleScene

BASE_DIR = Path(__file__).resolve().parent


def main():
    print("Starting Pac-Man...")

    data_dir = BASE_DIR / "data"
    # usrSettings.json holds the defaults and is committed. A player's own
    # changes are saved to usrSettings.local.json, which is gitignored.
    settings = SettingsManager(
        data_dir / "usrSettings.json", data_dir / "usrSettings.local.json"
    )

    game = Game(settings)
    game.run(TitleScene(game))


if __name__ == "__main__":
    main()
