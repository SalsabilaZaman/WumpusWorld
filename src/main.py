import pygame
from gui import draw_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Wumpus World")
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((255, 255, 255))  # White background
        
        draw_grid(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
# This is the main entry point for the Wumpus World game.
# It initializes the Pygame library, sets up the display, and runs the main game loop.