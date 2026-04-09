from core.sceneManager import sceneHandler, sceneManager
from pathlib import Path
import pygame


STEPS = 10  # Ticks per tile (controls movement speed)


class XYPair:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "XYPair") -> "XYPair":
        return XYPair(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "XYPair") -> "XYPair":
        return XYPair(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier: float) -> "XYPair":
        return XYPair(self.x * multiplier, self.y * multiplier)

    def __mod__(self, modulus: "XYPair") -> "XYPair":
        return XYPair(self.x % modulus.x, self.y % modulus.y)

    def __repr__(self):
        return f"(x:{self.x:>5.2f}, y:{self.y:>5.2f})"


class GameScene(sceneHandler):
    grid = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
        [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,0,0,0,0,0],
        [0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0],
        [0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0],
        [1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0],
        [0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0],
        [0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,0,0,0,0,0],
        [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
        [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
        [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
        [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
        [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]

    GRID_WIDTH = len(grid[0])   # 28
    GRID_HEIGHT = len(grid)     # 31

    def __init__(self, screen, settings):
        # FIX 1: __init__ must accept (screen, settings) to match sceneHandler signature
        super().__init__(screen, settings)

        # FIX 2: Build tiles and image_grid inside __init__, not at class level.
        # Class-level pygame.image.load() runs at import time — before pygame.init() —
        # so surfaces are never created and the game crashes immediately.
        self.tiles = {}
        self._load_tiles()
        self.image_grid = self._build_image_grid()

        # FIX 3: Movement state lives on the instance, not the class.
        self.step = 0
        self.curr_dir = XYPair(1, 0)
        self.desired_dir = XYPair(1, 0)
        self.angle = 0

        # Grid position (integer tile coords)
        self.coord = XYPair(1, 1)

        # Build key map from settings controls
        ctrl = settings.controls.keyboard
        self.key_map = self._build_key_map(ctrl)

    # ------------------------------------------------------------------
    # Asset loading
    # ------------------------------------------------------------------

    def _load_tiles(self):
        assets = Path(__file__).resolve().parent.parent / "assets"
        try:
            for i in range(16):
                self.tiles[i] = pygame.image.load(assets / "4x4" / f"tile_{i:02}.png")
            self.tiles["blue"] = pygame.image.load(assets / "blue.png")
            self.tiles["pacman"] = pygame.image.load(assets / "pacman.png")
        except Exception as e:
            print(f"Error loading image: {e}")
            # Fallback: create solid-color placeholder surfaces so the game
            # can still run without assets present
            placeholder = pygame.Surface((8, 8))
            placeholder.fill((0, 0, 255))
            for i in range(16):
                self.tiles[i] = placeholder.copy()
            self.tiles["blue"] = placeholder.copy()
            yellow = pygame.Surface((8, 8))
            yellow.fill((255, 255, 0))
            self.tiles["pacman"] = yellow

    def _build_image_grid(self):
        image_grid = []
        for y in range(self.GRID_HEIGHT):
            row = []
            for x in range(self.GRID_WIDTH):
                if self.grid[y][x] == 1:
                    # Bitmask: which of the 4 neighbours is open (0)?
                    # bit3=top, bit2=right, bit1=bottom, bit0=left
                    top    = (y == 0)              or (self.grid[y - 1][x] == 0)
                    right  = (x == self.GRID_WIDTH - 1) or (self.grid[y][(x + 1) % self.GRID_WIDTH] == 0)
                    bottom = (y == self.GRID_HEIGHT - 1) or (self.grid[(y + 1) % self.GRID_HEIGHT][x] == 0)
                    left   = (x == 0)              or (self.grid[y][x - 1] == 0)
                    index = top * 8 + right * 4 + bottom * 2 + left * 1
                    row.append(self.tiles[index])
                else:
                    row.append(self.tiles[0])
            image_grid.append(row)
        return image_grid

    def _build_key_map(self, ctrl):
        """Convert string key names from JSON into pygame key constants."""
        # TODO: Convert key codes in settingsManager
        return {
            "up":    [pygame.key.key_code(ctrl.move_up)],
            "down":  [pygame.key.key_code(ctrl.move_down)],
            "left":  [pygame.key.key_code(ctrl.move_left)],
            "right": [pygame.key.key_code(ctrl.move_right)],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def isValidMove(self, coord: XYPair) -> bool:
        gx = int(coord.x) % self.GRID_WIDTH
        gy = int(coord.y) % self.GRID_HEIGHT
        return self.grid[gy][gx] == 0

    # ------------------------------------------------------------------
    # Scene interface
    # ------------------------------------------------------------------

    def handleEvent(self, event):
        # FIX 4: handleEvent receives a single event (from game.py's loop),
        # not the full event list. Remove the inner "for event in events" loop.
        match event.type:
            case pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    self.changeScene("title")
            case pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed on joystick {event.instance_id}")
            case pygame.JOYBUTTONUP:
                print(f"Button {event.button} released on joystick {event.instance_id}")
            case pygame.JOYAXISMOTION:
                if event.value != 0:
                    if event.axis == 0:
                        self.desired_dir = XYPair(round(event.value), 0)
                    elif event.axis == 1:
                        self.desired_dir = XYPair(0, round(event.value))

    def gameUpdate(self, dt, pressed_keys):
        # FIX 5: Move all game logic here (it was incorrectly placed inside
        # handleEvent). pressed_keys is only available in gameUpdate.

        # --- Read keyboard input ---
        if any(pressed_keys[k] for k in self.key_map["up"]):
            self.desired_dir = XYPair(0, -1)
        elif any(pressed_keys[k] for k in self.key_map["down"]):
            self.desired_dir = XYPair(0, 1)
        elif any(pressed_keys[k] for k in self.key_map["left"]):
            self.desired_dir = XYPair(-1, 0)
        elif any(pressed_keys[k] for k in self.key_map["right"]):
            self.desired_dir = XYPair(1, 0)

        # --- Advance step counter ---
        self.step = (self.step + 1) % STEPS
        if self.step != 0:
            return  # Only move Pac-Man once per STEPS ticks

        # --- Try to turn ---
        if self.isValidMove(self.coord + self.desired_dir):
            self.curr_dir = self.desired_dir

        # --- Try to move forward ---
        if self.isValidMove(self.coord + self.curr_dir):
            self.coord.x = (self.coord.x + self.curr_dir.x) % self.GRID_WIDTH
            self.coord.y = (self.coord.y + self.curr_dir.y) % self.GRID_HEIGHT

        # --- Update sprite rotation angle ---
        # Right=0°, Down=270°, Left=180°, Up=90°
        if self.curr_dir.x == 1:
            self.angle = 0
        elif self.curr_dir.x == -1:
            self.angle = 180
        elif self.curr_dir.y == -1:
            self.angle = 90
        elif self.curr_dir.y == 1:
            self.angle = 270

    def sceneRender(self, screen):
        screen.fill((10, 10, 10))
        width, height = self.settings.video.resolution
        image_scale = min(width // self.GRID_WIDTH, height // self.GRID_HEIGHT)
        center_offset = (width - image_scale * self.GRID_WIDTH) // 2

        # --- Draw maze tiles ---
        for y, row in enumerate(self.image_grid):
            for x, image in enumerate(row):
                screen.blit(
                    pygame.transform.scale(image, (image_scale, image_scale)),
                    (image_scale * x + center_offset, image_scale * y),
                )

        # --- Draw Pac-Man with smooth sub-tile interpolation ---
        # FIX 6: Use self.coord.x / self.coord.y (not self.x_pos / self.y_pos,
        # which don't exist). Re-enable smooth movement using step fraction.
        progress = self.step / STEPS  # 0.0 → 1.0 between tiles

        # Interpolate position one step ahead in the current direction
        render_x = self.coord.x + progress * self.curr_dir.x
        render_y = self.coord.y + progress * self.curr_dir.y

        pacman_surf = pygame.transform.rotate(
            pygame.transform.scale(self.tiles["pacman"], (image_scale, image_scale)),
            self.angle - 45,
        )

        # FIX 7: Use pacman_surf.get_rect() (not pacman.get_rect()); the rotated
        # surface has a different variable name and potentially different size.
        rect = pacman_surf.get_rect()
        rect.center = (
            int(image_scale * (render_x + 0.5) + center_offset),
            int(image_scale * (render_y + 0.5)),
        )
        screen.blit(pacman_surf, rect)


# Register scene
sceneManager.register_scene("RGame", GameScene)