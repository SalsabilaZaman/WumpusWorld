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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    world.move_agent(0, 1)
                elif event.key == pygame.K_DOWN:
                    world.move_agent(0, -1)
                elif event.key == pygame.K_LEFT:
                    world.move_agent(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    world.move_agent(1, 0)
                    
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
# This is the main entry point for the Wumpus World game.
# It initializes the Pygame library, sets up the display, and runs the main game loop.