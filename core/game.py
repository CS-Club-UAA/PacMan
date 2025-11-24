from core.sceneManager import sceneManager
from pathlib import Path
import pygame
import json


def gameLoop(settings):

    # Load settings if none passed
    if settings is None:
        SETTINGS_PATH = (
            Path(__file__).resolve().parent.parent / "data" / "usrSettings.json"
        )

        with SETTINGS_PATH.open("r") as f:
            settings = json.load(f)

    pygame.init()

    # Window setup
    flags = pygame.FULLSCREEN if settings["fullscreen"] else 0
    screen = pygame.display.set_mode((settings["width"], settings["height"]), flags)
    pygame.display.set_caption("Pac-Man")

    clock = pygame.time.Clock()
    fps = settings.get("fps", 60)

    running = True

    # Load scenes dynamically
    sceneManager.load_all_scenes()
    current_scene = sceneManager.get_scene("title")(screen, settings)

    # ---------------------------
    #     MAIN GAME LOOP
    # ---------------------------
    while running:

        # 1. Gather ALL events this frame
        events = pygame.event.get()
        pressed_keys = pygame.key.get_pressed()

        # 2. Handle only quit here
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # 3. Pass input to scene (ONCE per frame, NOT per event)
        current_scene.processInput(events, pressed_keys)

        # 4. Update logic (ONCE per frame)
        current_scene.gameUpdate()

        # 5. Render the frame (ONCE per frame)
        current_scene.sceneRender(screen)

        # 6. Handle scene transitions
        if current_scene.next_scene != current_scene:
            next_scene_name = current_scene.next_scene
            next_scene_class = sceneManager.get_scene(next_scene_name)

            if next_scene_class:
                current_scene = next_scene_class(screen, settings)
            else:
                print(f"Scene '{next_scene_name}' not found!")

        # 7. Update display
        pygame.display.flip()
        clock.tick(fps)

    # Exit cleanly
    pygame.quit()
