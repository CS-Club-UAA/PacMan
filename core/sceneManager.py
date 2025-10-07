# This file manages different creates a sceneHandler class to manage different scenes in the game.
import pygame


class sceneHandler:
    def __init__(self):
        self.next_scene = self

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
