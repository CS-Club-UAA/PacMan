from core.sceneManager import sceneHandler, sceneManager
import pygame


class SettingsMenu(sceneHandler):
    def __init__(self, screen, settings):
        super().__init__(screen, settings)

        width, height = self.settings.video.resolution

    def handleEvent(self, event):
        pass

    def gameUpdate(self, dt, pressed_keys):
        pass

    def sceneRender(self, screen):
        pass

    def selector(self, event):
        return self.mouse_otion_selector(event) or self.keyboard_option_selector(event)


# Register correct class
sceneManager.register_scene("settings", SettingsMenu)
