# This is the main gameloop file that initializes Pygame and runs the game.
import pygame
import json
from pathlib import Path
from core.sceneManager import sceneHandler
# TODO: Import all the scenes at once

# The rest is code where you implement your game using the Scenes model
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "data" / "usrSettings.json"

with SETTINGS_PATH.open("r") as f:
    settings = json.load(f)

pygame.init()

flags = pygame.FULLSCREEN if settings["fullscreen"] else pygame.RESIZABLE
width = settings["width"]
height = settings["height"]
screen = pygame.display.set_mode((width, height), flags)
clock = pygame.time.Clock()
fps = settings["fps"]

# TODO: Put into settings file
key_map = {
    "up": (pygame.K_UP, pygame.K_w),
    "down": (pygame.K_DOWN, pygame.K_s),
    "left": (pygame.K_LEFT, pygame.K_a),
    "right": (pygame.K_RIGHT, pygame.K_d)
}

class TitleScene(sceneHandler):
    def __init__(self):
        sceneHandler.__init__(self)

    def processInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.changeScene(GameScene())

    def gameUpdate(self):
        pass

    def sceneRender(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((255, 0, 0))

# TODO: Move into its own file
class GameScene(sceneHandler):
    grid = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,0,1,0,0,0,0,0,1],
            [1,0,1,0,0,0,1,0,1,1,1,0,1],
            [1,0,0,0,1,1,1,0,0,0,0,0,1],
            [1,0,1,0,0,0,0,0,1,1,1,0,1],
            [1,0,1,0,1,1,1,0,1,0,0,0,1],
            [1,0,1,0,1,0,0,0,1,1,1,0,1],
            [1,0,1,0,1,1,1,0,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

    GRID_WIDTH = len(grid[0])
    GRID_HEIGHT = len(grid)

    tiles = {}
    try:
        for i in range(16):
            tiles[i] = pygame.image.load(f"C:\\Users\\obsidian\\Repos\\School\\pacman\\assets/tile_{i:02}.png")
        tiles["blue"] = pygame.image.load(f"C:\\Users\\obsidian\\Repos\\School\\pacman\\assets/blue.png")
        tiles["pacman"] = pygame.image.load(f"C:\\Users\\obsidian\\Repos\\School\\pacman\\assets/pacman.png")
    except Exception as e:
        print(f"Error loading image: {e}")
        pygame.quit()
    
    image_grid = []
    for y in range(GRID_HEIGHT):
        image_grid.append([])
        for x in range(GRID_WIDTH):
            if (grid[y][x] == 1):
                index = (grid[y-1][x] == 0)*8 + (grid[y][(x+1) % GRID_WIDTH] == 0)*4 + (grid[(y+1) % GRID_HEIGHT][x] == 0)*2 + (grid[y][x-1] == 0)
                image_grid[y].append(tiles[index])
            else:
                image_grid[y].append(tiles[0])

    image_scale = min(width//GRID_WIDTH, height//GRID_HEIGHT)

    x_pos = 1
    y_pos = 1
    direction = -45

    def isValidMove(self, new_x, new_y):
        return self.grid[new_y][new_x] == 0

    def __init__(self):
        sceneHandler.__init__(self)

    def processInput(self, events, pressed_keys):
        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:
                        # Move to the next scene when the user pressed Delete
                        self.changeScene(TitleScene())
        
        new_x = self.x_pos
        new_y = self.y_pos
        new_dir = self.direction
        if any(pressed_keys[key] for key in key_map["up"]): # +90 - 45 = 45
            new_dir = 45
        elif any(pressed_keys[key] for key in key_map["down"]): # -90 - 45 = -135/225
            new_dir = 225
        elif any(pressed_keys[key] for key in key_map["left"]): # +180 - 45 = 135/-225
            new_dir = -225
        elif any(pressed_keys[key] for key in key_map["right"]): # -45
            new_dir = -45

        if new_dir == 45:
            new_y -= 0.1
        elif new_dir == 225:
            new_y += 0.1
        elif new_dir == -225:
            new_x -= 0.1
        elif new_dir == -45:
            new_x += 0.1

        self.direction = new_dir
        if self.isValidMove(round(new_x), round(new_y)):
            self.x_pos = new_x
            self.y_pos = new_y

    def gameUpdate(self):
        pass

    def sceneRender(self, screen):
        screen.fill((10, 10, 10))
        
        for y, row in enumerate(self.image_grid):
            for x, image in enumerate(row):
                screen.blit(pygame.transform.scale(image, (self.image_scale, self.image_scale)), (self.image_scale * x, self.image_scale * y))

        pacman = pygame.transform.rotate(pygame.transform.scale(self.tiles["pacman"], (self.image_scale, self.image_scale)), self.direction)
        rect = pacman.get_rect()
        rect.center = (self.image_scale * (self.x_pos + 0.5), self.image_scale * (self.y_pos + 0.5))# tiles["pacman"].get_rect().center
        screen.blit(pacman, rect)

active_scene = TitleScene()

while active_scene != None:
    pressed_keys = pygame.key.get_pressed()

    # Event filtering
    filtered_events = []
    for event in pygame.event.get():
        quit_attempt = False
        match event.type:
            case pygame.QUIT:
                quit_attempt = True
            case pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                # elif event.key == pygame.K_F4 and alt_pressed:
                #     quit_attempt = True
            case pygame.VIDEORESIZE:
                width = event.size[0]
                height = event.size[1]

        if quit_attempt:
            active_scene.endGame() # Also should exit here I think? since it causes an error when the scene tries to render # There are some things maybe we want to do when it quits like saving and stuff
        else:
            filtered_events.append(event)

    # TODO: Pass argument containing game data (e.g. screen dimensions, key map, etc.)
    active_scene.processInput(filtered_events, pressed_keys)
    active_scene.gameUpdate()
    active_scene.sceneRender(screen)

    active_scene = active_scene.next_scene
    pygame.display.flip()
    clock.tick(fps)
