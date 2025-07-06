import pygame
from gui import draw_grid,draw_entities
from world import World

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Wumpus World")
    clock = pygame.time.Clock()
    running = True

    world = World()

    while running:
        screen.fill((255, 255, 255))  # White background
        
        draw_grid(screen)
        entities = world.get_entities()
        draw_entities(screen, entities)
        
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