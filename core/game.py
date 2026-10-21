import pygame


class Game:
    """Owns the window, the clock and a stack of scenes, and runs the main loop.

    Only the top scene gets events and update(); the scenes below it are frozen,
    which is how pausing works. Scene changes are queued and applied at the end
    of the frame, so a scene is never swapped out halfway through its own code.
    """

    MAX_DT = 0.1  # seconds; stops things from jumping after the window is dragged

    def __init__(self, settings):
        pygame.init()
        self.settings = settings
        flags = pygame.FULLSCREEN if settings.video.fullscreen else 0
        self.screen = pygame.display.set_mode(settings.video.resolution, flags)
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.fps = getattr(settings.video, "fps", 60)
        self.running = False
        self._stack = []
        self._pending = []  # scene changes requested during this frame

    # ------------------------------------------------------------------
    # Scene changes (called by scenes; applied at the end of the frame)
    # ------------------------------------------------------------------

    def push(self, scene):
        """Put a scene on top. The current scene stays alive underneath."""
        self._pending.append(("push", scene))

    def pop(self):
        """Close the top scene and go back to the one below it."""
        self._pending.append(("pop", None))

    def replace(self, scene):
        """Swap the top scene for a new one."""
        self._pending.append(("replace", scene))

    def reset(self, scene):
        """Close every scene and start over with this one."""
        self._pending.append(("reset", scene))

    def quit(self):
        self.running = False

    @property
    def top_scene(self):
        return self._stack[-1] if self._stack else None

    def _apply_pending(self):
        while self._pending:
            action, scene = self._pending.pop(0)
            if action == "push":
                if self._stack:
                    self._stack[-1].on_pause()
            elif action in ("pop", "replace"):
                if self._stack:
                    self._stack.pop().on_exit()
            elif action == "reset":
                while self._stack:
                    self._stack.pop().on_exit()

            if scene is not None:
                self._stack.append(scene)
            if self._stack:
                self._stack[-1].on_enter()

        if not self._stack:
            self.running = False  # nothing left to show

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self, first_scene):
        self.push(first_scene)
        self._apply_pending()
        self.running = True
        try:
            while self.running:
                dt = min(self.clock.tick(self.fps) / 1000, self.MAX_DT)
                top = self._stack[-1]

                # 1. Input: only the top scene gets events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit()
                    else:
                        top.handle_event(event)

                # 2. Update: only the top scene runs; the ones below are frozen
                top.update(dt)

                # 3. Render: start at the highest scene that isn't an overlay,
                #    then draw every scene above it (overlays on top)
                first = len(self._stack) - 1
                while first > 0 and self._stack[first].is_overlay:
                    first -= 1
                for scene in self._stack[first:]:
                    scene.render(self.screen)
                pygame.display.flip()

                # 4. Scene changes requested this frame
                self._apply_pending()
        finally:
            pygame.quit()
