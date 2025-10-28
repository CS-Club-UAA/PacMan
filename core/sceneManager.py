# This file manages different creates a sceneHandler class to manage different scenes in the game.
import pygame
import importlib
import pkgutil
import os


class sceneHandler:
    def __init__(self, screen, settings):
    	self.screen = screen
    	self.settings = settings
        self.next_scene = self
        self.current_scene = None

    def getCurrentScene(self):
        return self.current_scene

    def processInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def gameUpdate(self):
        print("uh-oh, you didn't override this in the child class")

    def sceneRender(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def changeScene(self, new_scene):
        self.next_scene = new_scene
        print(f"Scene changed to: {new_scene}")

    def endGame(self):
        self.current_scene = None
        print("Game Ended")
        pygame.quit()
        
class SceneManager:
    scenes = {}  # holds all scene classes by name

    @classmethod
    def register_scene(cls, name, scene_class):
        cls.scenes[name] = scene_class

    @classmethod
    def get_scene(cls, name):
        return cls.scenes.get(name)

    @classmethod
    def load_all_scenes(cls, package="scenes"):
        """Automatically import all files in the scenes/ folder."""
        package_path = os.path.join(os.path.dirname(__file__), package)
        for _, module_name, _ in pkgutil.iter_modules([package_path]):
            importlib.import_module(f"{package}.{module_name}")
