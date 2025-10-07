import pygame

pygame.init()
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

key_map = {
    "up": (pygame.K_UP, pygame.K_w),
    "down": (pygame.K_DOWN, pygame.K_s),
    "left": (pygame.K_LEFT, pygame.K_a),
    "right": (pygame.K_RIGHT, pygame.K_d)
}

GRID_WIDTH = len(grid[0])
GRID_HEIGHT = len(grid)
IMAGE_SCALE = 80
WIDTH = IMAGE_SCALE * GRID_WIDTH
HEIGHT = IMAGE_SCALE * GRID_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Test")
clock = pygame.time.Clock()

tiles = {}
try:
    for i in range(16):
        tiles[i] = pygame.transform.scale(pygame.image.load(f"./assets/tile_{i:02}.png"), (IMAGE_SCALE, IMAGE_SCALE))
    tiles["blue"] = pygame.transform.scale(pygame.image.load(f"./assets/blue.png"), (IMAGE_SCALE, IMAGE_SCALE))
    tiles["pacman"] = pygame.transform.scale(pygame.image.load(f"./assets/pacman.png"), (IMAGE_SCALE, IMAGE_SCALE))
except Exception as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()

image_grid = []

# Print grid in console
print()
for r in grid:
    for c in r:
        print(("  ", "██")[c], end="")
    print()

# Make image_grid
for y in range(GRID_HEIGHT):
    image_grid.append([])
    for x in range(GRID_WIDTH):
        if (grid[y][x] == 1):
            index = (grid[y-1][x] == 0)*8 + (grid[y][(x+1) % GRID_WIDTH] == 0)*4 + (grid[(y+1) % GRID_HEIGHT][x] == 0)*2 + (grid[y][x-1] == 0)
            image_grid[y].append(tiles[index])
        else:
            image_grid[y].append(tiles[0])
# Alternative approach using just solid colors
# for y in range(GRID_HEIGHT):
#     image_grid.append([])
#     for x in range(GRID_WIDTH):
#         if (grid[y][x] == 1):
#             image_grid[y].append(tiles["blue"])
#         else:
#             image_grid[y].append(tiles[0])

def isValidMove(new_x, new_y):
    return grid[new_y][new_x] == 0

x_pos = 1
y_pos = 1
direction = -45

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((255, 255, 255)) # White background

    # Display maze
    for y, row in enumerate(image_grid):
        for x, image in enumerate(row):
            screen.blit(image, (IMAGE_SCALE * x, IMAGE_SCALE * y))
    
    new_x = x_pos
    new_y = y_pos
    new_dir = direction
    keys = pygame.key.get_pressed()
    # any(keys[key] for key in

    # TODO: Do something to look at most recent keys first to make the movement feel better
    if any(keys[key] for key in key_map["up"]): # +90 - 45 = 45
        new_dir = 45
    elif any(keys[key] for key in key_map["down"]): # -90 - 45 = -135/225
        new_dir = 225
    elif any(keys[key] for key in key_map["left"]): # +180 - 45 = 135/-225
        new_dir = -225
    elif any(keys[key] for key in key_map["right"]): # -45
        new_dir = -45

    if new_dir == 45:
        new_y -= 1
    if new_dir == 225:
        new_y += 1
    if new_dir == -225:
        new_x -= 1
    if new_dir == -45:
        new_x += 1

    # new_x = x_pos + keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    # new_y = y_pos + keys[pygame.K_DOWN] - keys[pygame.K_UP] # Todo, this will allow going diagonally. Probably don't want
    direction = new_dir
    if isValidMove(new_x, new_y):
        # print("Current:", x_pos, y_pos, "New:", new_x, new_y, "up/down:", keys[pygame.K_UP], keys[pygame.K_DOWN])
        x_pos = new_x
        y_pos = new_y

    pacman = pygame.transform.rotate(tiles["pacman"], direction)
    rect = pacman.get_rect()
    rect.center = (IMAGE_SCALE * (x_pos + 0.5), IMAGE_SCALE * (y_pos + 0.5))# tiles["pacman"].get_rect().center
    screen.blit(pacman, rect)

    pygame.display.update() # flip updates entire screen update has arguments to only update part of it
    clock.tick(7)

pygame.quit()
