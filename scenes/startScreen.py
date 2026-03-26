from core.sceneManager import sceneHandler, sceneManager
import pygame


class StartScreen(sceneHandler):
    def __init__(self, screen, settings):
        super().__init__(screen, settings)

        width, height = self.settings.video.resolution
        font = pygame.font.SysFont("Arial", 80)

        # Start button
        text = font.render("Start", True, (255, 255, 255))
        self.start_text = text
        self.start_rect = text.get_rect(center=(width // 2, height // 2))

        # Settings button
        self.settings_rect = pygame.Rect(width - 140, 20, 110, 40)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.changeScene("RGame")

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if self.start_rect.collidepoint((mx, my)):
                self.changeScene("RGame")
            elif self.settings_rect.collidepoint((mx, my)):
                self.changeScene("settings")

    def gameUpdate(self, dt, pressed_keys):
        pass

    def sceneRender(self, screen):
        pygame.display.set_caption("PacMan")

        width, height = self.settings.video.resolution
        screen.fill((0, 0, 0))

        font = pygame.font.SysFont("Arial", 80)

        # Title
        text2 = font.render("Pac-man", True, (255, 165, 0))
        text2_rect = text2.get_rect(center=(width // 2, 180))

        # Start button
        text = font.render("Start", True, (255, 255, 255))
        self.text_rect = text.get_rect(center=(width // 2, height // 2))

        # Settings button
        self.settings_rect = pygame.Rect(width - 140, 20, 110, 40)
        pygame.draw.rect(screen, (255, 255, 255), self.settings_rect)

        small_font = pygame.font.SysFont("Arial", 30)
        settings_button = small_font.render("Settings", True, (0, 0, 0))
        settings_button_rect = settings_button.get_rect(
            center=self.settings_rect.center
        )

        screen.blit(text2, text2_rect)
        screen.blit(text, self.text_rect)
        screen.blit(settings_button, settings_button_rect)


# Register correct class
sceneManager.register_scene("title", StartScreen)
