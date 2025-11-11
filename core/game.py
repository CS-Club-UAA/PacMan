from core.sceneManager import SceneManager
from pathlib import Path
import pygame
import json


def gameLoop(settings):

    if settings is None:
        SETTINGS_PATH = (
            Path(__file__).resolve().parent.parent / "data" / "usrSettings.json"
        )

        with SETTINGS_PATH.open("r") as f:
            settings = json.load(f)

    pygame.init()

    flags = pygame.FULLSCREEN if settings["fullscreen"] else 0
    screen = pygame.display.set_mode((settings["width"], settings["height"]), flags)
    clock = pygame.time.Clock()
    fps = settings["fps"]

    running = True

    SceneManager.load_all_scenes()
    current_scene = SceneManager.get_scene("title")(screen, settings)

    while running:
        events = pygame.event.get()
        pressed_keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

            current_scene.processInput(events, pressed_keys)
            current_scene.gameUpdate()
            current_scene.sceneRender(screen)

            # Scene transitions
            if current_scene.next_scene != current_scene:
                next_scene_name = current_scene.next_scene
                next_scene_class = SceneManager.get_scene(next_scene_name)
                if next_scene_class:
                    current_scene = next_scene_class(screen, settings)
                else:
                    print(f"Scene '{next_scene_name}' not found!")

            pygame.display.flip()
            clock.tick(settings.get("fps", 60))

    pygame.quit()
