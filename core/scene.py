class Scene:
    """Base class for every screen in the game (title, game, pause, settings, ...).

    Override only the methods you need; the defaults do nothing.
    A scene never switches scenes or quits by itself. It asks the Game:
        self.game.push(OtherScene(self.game))     # open on top, keep this one
        self.game.pop()                           # close this one, go back
        self.game.replace(OtherScene(self.game))  # swap this one out
        self.game.reset(OtherScene(self.game))    # clear everything, start fresh
        self.game.quit()                          # end the game loop
    """

    # True = the scene underneath is drawn first, so this one appears on top of it
    # (e.g. the pause menu over the frozen maze).
    is_overlay = False

    def __init__(self, game):
        self.game = game

    @property
    def settings(self):
        return self.game.settings

    def on_enter(self):
        """Became the top scene: the first time, or when returned to with pop()."""

    def on_exit(self):
        """Removed from the stack."""

    def on_pause(self):
        """Another scene was pushed on top of this one."""

    def handle_event(self, event):
        """Called once per pygame event, only while this is the top scene."""

    def update(self, dt):
        """Advance the scene by dt seconds. Only called while this is the top scene."""

    def render(self, screen):
        """Draw the scene. Never call pygame.display.flip() here; Game does it."""
