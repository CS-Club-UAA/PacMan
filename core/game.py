# This is the main gameloop file that initializes Pygame and runs the game.
import pygame
import json
from pathlib import Path
from core.sceneManager import sceneHandler

# The rest is code where you implement your game using the Scenes model


class TitleScene(sceneHandler):
    def __init__(self):
        sceneHandler.__init__(self)

    def processInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.changeScene(GameScene())

    def gameUpdate(self):
        pass

    def sceneRender(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((255, 0, 0))


class GameScene(sceneHandler):
    def __init__(self):
        sceneHandler.__init__(self)

    def processInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                # Move to the next scene when the user pressed Enter
                self.changeScene(TitleScene())

    def gameUpdate(self):
        pass

    def sceneRender(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0, 0, 255))


SETTINGS_PATH = Path(__file__).resolve().parent.parent / "data" / "usrSettings.json"

with SETTINGS_PATH.open("r") as f:
    settings = json.load(f)

pygame.init()

flags = pygame.FULLSCREEN if settings["fullscreen"] else 0
screen = screen = pygame.display.set_mode(
    (settings["width"], settings["height"]), flags
)
clock = pygame.time.Clock()
fps = settings["fps"]

active_scene = TitleScene()

while active_scene != None:
    pressed_keys = pygame.key.get_pressed()

    # Event filtering
    filtered_events = []
    for event in pygame.event.get():
        quit_attempt = False
        if event.type == pygame.QUIT:
            quit_attempt = True
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_ESCAPE:
                quit_attempt = True
            elif event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True

        if quit_attempt:
            active_scene.endGame()
        else:
            filtered_events.append(event)

    active_scene.processInput(filtered_events, pressed_keys)
    active_scene.gameUpdate()
    active_scene.sceneRender(screen)

    active_scene = active_scene.next_scene
    pygame.display.flip()
    clock.tick(fps)
