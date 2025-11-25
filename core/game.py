from core.sceneManager import sceneManager
from pathlib import Path
import pygame
from core.settingsManager import SettingsManager  # import helper


def gameLoop(settings=None):

    pygame.init()

    # Video setup
    width, height = settings.video.resolution
    flags = pygame.FULLSCREEN if settings.video.fullscreen else 0
    screen = pygame.display.set_mode((width, height), flags)
    pygame.display.set_caption("Pac-Man")

    clock = pygame.time.Clock()
    fps = getattr(settings.video, "fps", 60)

    # Load all scenes
    sceneManager.load_all_scenes()
    current_scene = sceneManager.get_scene("title")(screen, settings)

    running = True
    while running:
        dt = clock.get_time() / 1000  # delta time in seconds
        events = pygame.event.get()
        pressed_keys = pygame.key.get_pressed()

        # 1. Handle quit and pass events to scene
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            current_scene.handleEvent(event)

        # 2. Update scene logic
        current_scene.gameUpdate(dt, pressed_keys)

        # 3. Render scene
        current_scene.sceneRender(screen)

        # 4. Handle scene transitions
        if current_scene.next_scene:
            next_scene_name = current_scene.next_scene
            next_scene_class = sceneManager.get_scene(next_scene_name)
            if next_scene_class:
                current_scene = next_scene_class(screen, settings)
            else:
                print(f"Scene '{next_scene_name}' not found!")

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
