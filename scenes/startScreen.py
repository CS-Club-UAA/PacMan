import pygame

pygame.init()

# Screen resolution
res = (800, 600)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("PacMan")

# "Pacman" text at the top
font = pygame.font.SysFont("Arial", 80)
text2 = font.render("Pac-man", True, (255, 165, 0))  # Orange color
text2_rect = text2.get_rect(center=(res[0] // 2, 180))  # Adjust Y to be at the top

# "Start" text in the center
font = pygame.font.SysFont("Arial", 80)
text = font.render("Start", True, (255, 255, 255))
text_rect = text.get_rect(center=(res[0] // 2, res[1] // 2))  # Center of the screen

button_padding = 20  # Padding around the text
button_color = (255, 165, 0)  # Orange color
button_rect = text_rect.inflate(
    button_padding * 2, button_padding * 2
)  # Inflate to add padding

running = True
while running:
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Draw the text
    screen.blit(text2, text2_rect)  # Draw "Pacman" at the top
    screen.blit(text, text_rect)  # Draw "Start" button

    # Check for mouse events
    mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
    mouse_click = pygame.mouse.get_pressed()  # Check if the mouse is clicked

    if mouse_click[0] == 1:  # Left mouse button clicked
        if button_rect.collidepoint(
            mouse_pos
        ):  # Check if the click is inside the button
            print("Start button clicked!")
            # Perform any action, e.g., start the game or transition to another screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()  # Update the screen

pygame.quit()
