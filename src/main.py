import pygame
from gui import draw_grid,draw_entities,draw_percepts
from world import World
from agent import Agent


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Wumpus World")
    clock = pygame.time.Clock()
    running = True

    world = World(map_file="src/maps/level1.txt")  # Load the map from a file
    agent = Agent()

    while running:
        screen.fill((255, 255, 255))  # White background
        
        draw_grid(screen)
        entities = world.get_entities()
        draw_entities(screen, entities)

        # x, y = world.agent_pos
        x, y = agent.position
        percepts = world.get_percepts(x, y)
        draw_percepts(screen, percepts)
        agent.perceive(percepts)
        # print(f"Percepts: {percepts}")
        if agent.found_gold:
            print(f"\n🎉 GOLD FOUND at {agent.position}! GAME OVER.")
            break
        agent.step(world) 
        
        # next_pos = agent.next_move()          #just for reference for single step
        # if next_pos:
        #     agent.move_to(next_pos)
        #     world.agent_pos = agent.position

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_UP:
        #             world.move_agent(0, 1)
        #         elif event.key == pygame.K_DOWN:
        #             world.move_agent(0, -1)
        #         elif event.key == pygame.K_LEFT:
        #             world.move_agent(-1, 0)
        #         elif event.key == pygame.K_RIGHT:
        #             world.move_agent(1, 0)
        pygame.time.delay(1500)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
# This is the main entry point for the Wumpus World game.
# It initializes the Pygame library, sets up the display, and runs the main game loop.