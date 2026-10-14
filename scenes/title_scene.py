import pygame
from core.scene import Scene


class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        # Build fonts and text once, not every frame
        big_font = pygame.font.SysFont("Arial", 80)
        small_font = pygame.font.SysFont("Arial", 30)
        self.title_text = big_font.render("Pac-man", True, (255, 165, 0))
        self.start_text = big_font.render("Start", True, (255, 255, 255))
        self.settings_text = small_font.render("Settings", True, (0, 0, 0))
        self._layout()

    def _layout(self):
        """Position everything from the current window size."""
        width, height = self.game.screen.get_size()
        self.title_rect = self.title_text.get_rect(center=(width // 2, 180))
        self.start_rect = self.start_text.get_rect(center=(width // 2, height // 2))
        self.settings_rect = pygame.Rect(width - 140, 20, 110, 40)

    def on_enter(self):
        # The resolution may have changed in Settings
        self._layout()

    def _start_game(self):
        # Scenes import each other in a circle (Title -> Game -> Pause -> Title).
        # Importing inside the method avoids a circular-import error at startup.
        from scenes.game_scene import GameScene  # pylint: disable=import-outside-toplevel
        self.game.replace(GameScene(self.game))

    def _open_settings(self):
        from scenes.settings_scene import SettingsScene  # pylint: disable=import-outside-toplevel
        self.game.push(SettingsScene(self.game))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._start_game()
            elif event.key == pygame.K_s:
                self._open_settings()
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_rect.collidepoint(event.pos):
                self._start_game()
            elif self.settings_rect.collidepoint(event.pos):
                self._open_settings()

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.start_text, self.start_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.settings_rect)
        screen.blit(
            self.settings_text,
            self.settings_text.get_rect(center=self.settings_rect.center),
        )
