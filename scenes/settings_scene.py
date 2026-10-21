import pygame
from core.scene import Scene


class SettingsScene(Scene):
    # (first index, last index + 1) in self.options for each menu section
    SECTIONS = {
        0: (0, 6),    # Graphics, Sound, Controls, Restart, Back, Exit Game
        1: (6, 9),    # Resolution, Fullscreen/Windowed, Back
        2: (9, 14),   # Master Volume, Music Volume, Sound Effects Volume, Mute/Unmute, Back
        3: (14, 16),  # Rebind Keys, Back
        4: (16, 23),  # Resolution options, Back
    }

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 50)  # created once, before any event arrives
        # TODO: Replace the flat list + SECTIONS with a nested structure (see TODO.md)
        self.options = [
            "Graphics",
            "Sound",
            "Controls",
            "Restart",
            "Back",
            "Exit Game",
            "Resolution",
            "Fullscreen/Windowed",
            "Back",
            "Master Volume",
            "Music Volume",
            "Sound Effects Volume",
            "Mute/Unmute",
            "Back",
            "Rebind Keys",
            "Back",
            "[3840,2160]",
            "[2560,1440]",
            "[1920,1080]",
            "[1280,780]",
            "[1080,480]",
            "[800,600]",
            "Back",
        ]
        self.selected_option = 0  # index into the options currently shown
        self.menu_section = 0

    def _visible_options(self):
        start, end = self.SECTIONS[self.menu_section]
        return self.options[start:end]

    def _open_section(self, section):
        self.menu_section = section
        self.selected_option = 0

    def _back(self):
        if self.menu_section == 0:
            self.game.pop()  # back to wherever Settings was opened from
        elif self.menu_section == 4:
            self._open_section(1)  # resolution list -> Graphics
        else:
            self._open_section(0)

    def _choose(self, option):
        if option == "Back":
            self._back()
        elif option == "Graphics":
            self._open_section(1)
        elif option == "Sound":
            self._open_section(2)
        elif option == "Controls":
            self._open_section(3)
        elif option == "Resolution":
            self._open_section(4)
        elif option == "Restart":
            from scenes.game_scene import GameScene  # pylint: disable=import-outside-toplevel
            self.game.reset(GameScene(self.game))
        elif option == "Exit Game":
            self.game.quit()
        # TODO: Fullscreen, volume, key rebinding and resolutions don't do anything yet

    def handle_event(self, event):
        visible = self._visible_options()

        # menu navigation via keyboard (up/down then press enter to select)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(visible)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(visible)
            elif event.key == pygame.K_RETURN:
                self._choose(visible[self.selected_option])
            elif event.key == pygame.K_ESCAPE:
                self._back()

        # menu navigation via mouse (hover then click to select)
        elif event.type == pygame.MOUSEMOTION:
            hovered = self._option_at(event.pos, visible)
            if hovered is not None:
                self.selected_option = hovered
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = self._option_at(event.pos, visible)
            if clicked is not None:
                self._choose(visible[clicked])

    def _option_at(self, pos, visible):
        """Index of the visible option under the mouse, or None."""
        mouse_x, mouse_y = pos
        # use the largest option to get a consistent width
        text_width, text_height = self.font.size("Sound Effects Volume")
        text_x = 100  # x position used in render()
        for index, _ in enumerate(visible):
            option_y = 100 + index * 40
            # vertical check, plus horizontal proximity: within 30 pixels of text bounds
            if (option_y <= mouse_y <= option_y + text_height
                    and text_x - 30 <= mouse_x <= text_x + text_width + 30):
                return index
        return None

    def render(self, screen):
        screen.fill((0, 0, 0))
        for index, option in enumerate(self._visible_options()):
            color = (
                (255, 255, 255) if index == self.selected_option else (100, 100, 100)
            )  # Highlight selected option
            text = self.font.render(option, True, color)
            screen.blit(text, (100, 100 + index * 40))
