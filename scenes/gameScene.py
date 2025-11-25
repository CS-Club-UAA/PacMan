from core.sceneManager import sceneHandler, sceneManager
import pygame


class GameScene(sceneHandler):
    def __init__(self, screen, settings):
        super().__init__(screen, settings)

    def processInput(self, event):
        pass

    def gameUpdate(self, dt, pressed_keys):
        pass

    def sceneRender(self, screen):
        pass


# Registering Regular Game Scene
sceneManager.register_scene("RGame", GameScene)
