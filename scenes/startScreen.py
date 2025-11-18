from core.sceneManager import sceneHandler, sceneManager
import pygame


class StartScreen(sceneHandler):
    def __init__(self, screen, settings):
        super().__init__(screen, settings)
        print("Start screen has started")

    def processInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.changeScene("level1")

    def gameUpdate(self):
        pass

    def sceneRender(self, screen):
        pygame.display.set_caption("PacMan")

        width = self.settings["width"]
        height = self.settings["height"]

        screen.fill((0, 0, 0))

        # Title
        font = pygame.font.SysFont("Arial", 80)
        text2 = font.render("Pac-man", True, (255, 165, 0))
        text2_rect = text2.get_rect(center=(width // 2, 180))

        # Start button
        text = font.render("Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height // 2))

        screen.blit(text2, text2_rect)
        screen.blit(text, text_rect)


# Register correct class
sceneManager.register_scene("title", StartScreen)
