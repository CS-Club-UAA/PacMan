import pygame
from core.scene import Scene


class PauseScene(Scene):
    """Pause menu drawn over the frozen game.

    GameScene pushes this on top of itself. Because only the top scene gets
    update(), the game underneath doesn't move until we pop() back to it.
    """

    is_overlay = True  # draw the game underneath first
    OPTIONS = ["Resume", "Settings", "Quit to Title"]

    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 80)
        self.font = pygame.font.Font(None, 50)
        self.selected = 0
        self.shade = None  # translucent layer, built to the window size in render()
        ctrl = self.settings.controls.keyboard
        self.resume_keys = {pygame.key.key_code(ctrl.pause), pygame.K_ESCAPE}

    def _choose(self, option):
        if option == "Resume":
            self.game.pop()
        elif option == "Settings":
            # Imported here because the scenes import each other in a circle
            from scenes.settings_scene import SettingsScene  # pylint: disable=import-outside-toplevel
            self.game.push(SettingsScene(self.game))
        elif option == "Quit to Title":
            from scenes.title_scene import TitleScene  # pylint: disable=import-outside-toplevel
            self.game.reset(TitleScene(self.game))  # throws away the paused game too

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in self.resume_keys:
            self.game.pop()
        elif event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.OPTIONS)
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.OPTIONS)
        elif event.key == pygame.K_RETURN:
            self._choose(self.OPTIONS[self.selected])

    def render(self, screen):
        width, height = screen.get_size()
        if self.shade is None or self.shade.get_size() != (width, height):
            self.shade = pygame.Surface((width, height), pygame.SRCALPHA)
            self.shade.fill((0, 0, 0, 170))
        screen.blit(self.shade, (0, 0))

        title = self.title_font.render("PAUSED", True, (255, 255, 0))
        screen.blit(title, title.get_rect(center=(width // 2, height // 2 - 100)))
        for index, option in enumerate(self.OPTIONS):
            color = (255, 255, 255) if index == self.selected else (100, 100, 100)
            text = self.font.render(option, True, color)
            screen.blit(text, text.get_rect(center=(width // 2, height // 2 + index * 50)))
