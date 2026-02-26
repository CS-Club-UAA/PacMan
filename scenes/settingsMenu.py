from core.sceneManager import sceneHandler, sceneManager
from core.settingsManager import SettingsMenu
import pygame


class SubMenu(sceneHandler):
    def __init__(self, screen, settings):
        super().__init__(screen, settings)
        width, height = self.settings.video.resolution
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
        ]  # Number of things in each section (6,3,5,2,7)
        self.selected_option = 0

    def handleEvent(self, event):
        # menu navigation via keyboard (up/down then press enter to select)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        # menu navigation via mouse (hover then click to select)
        if event.type == pygame.MOUSEMOTION:
            mouse_y = event.pos[1]
            mouse_x = event.pos[0]
            for index in range(len(self.options)):
                option_y = 100 + index * 40
                # determine the rendered text width so we can check horizontal proximity
                text = self.options[index]
                text_width, text_height = self.font.size(
                    "Sound Effects Volume"
                )  # use the largest option to get consistent width
                text_x = 100  # x position used in draw()

                # vertical check (approx height of text)
                if option_y <= mouse_y <= option_y + text_height:
                    # horizontal proximity: within 30 pixels of text bounds
                    if (mouse_x >= text_x - 30) and (
                        mouse_x <= text_x + text_width + 30
                    ):
                        self.selected_option = index
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                return self.options[self.selected_option]
        return None

    def gameUpdate(self, dt, pressed_keys):
        pass

    def sceneRender(self, screen, settings_state=0):
        screen.fill((0, 0, 0))
        self.font = pygame.font.Font(None, 50)  # sets the font in menu
        temperary_options = []  # Placeholder for future use
        start = 0

        # Graphics, Sound, Controls, Restart, Back, Exit Game
        if settings_state == 0:
            for index, option in enumerate(self.options[0:6], start):
                temperary_options.append(option)

        # Resolution, Fullscreen/Windowed, Back
        elif settings_state == 1:
            start = 6
            for index, option in enumerate(self.options[6:9], start):
                temperary_options.append(option)

        # Master Volume, Music Volume, Sound Effects Volume, Mute/Unmute, Back
        elif settings_state == 2:
            start = 9
            for index, option in enumerate(self.options[9:14], start):
                temperary_options.append(option)

        # Rebind Keys, Back
        elif settings_state == 3:
            start = 14
            for index, option in enumerate(self.options[14:15], start):
                temperary_options.append(option)

        # Resolution options
        elif settings_state == 4:
            start = 16
            for index, option in enumerate(
                self.options[16:23], start=16
            ):  # Resolution options
                temperary_options.append(option)

        for index, option in enumerate(temperary_options):
            color = (
                (255, 255, 255) if index == self.selected_option else (100, 100, 100)
            )  # Highlight selected option
            text = self.font.render(option, True, color)
            screen.blit(text, (100, 100 + index * 40))
        pygame.display.flip()

    def selector(self, event):
        pass


# Register correct class
sceneManager.register_scene("settings", SubMenu)
