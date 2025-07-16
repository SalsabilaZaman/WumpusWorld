import pygame
from gui import *
from world import World
from agent import Agent

pygame.mixer.init()
init_assets()  # Initialize GUI assets

def main():
    play_bgm()  # Start background music
    screen = init_gui()  # Initialize GUI
    clock = pygame.time.Clock()
    running = True

    # world = World(map_file="src/maps/level1.txt")  # Load the map from a file
    world = World()  # Generate a random map
    
    agent = Agent()

    while running:
        screen.fill((255, 255, 235))  # White background
        
        draw_grid(screen)
        entities = world.get_entities()
        # Update entities with agent's knowledge
        entities["percepts"] = agent.kb.percepts_map
        draw_entities(screen, entities)

        # # --- BEFORE MOVE ---
        x, y = agent.position
        percepts = world.get_percepts(x, y)
        draw_percepts(screen, percepts)
        draw_agent_mind(screen, agent)
        agent.perceive(percepts)
        pygame.display.flip()

        # --- MOVE AGENT ---
        agent.step(world)

        # --- AFTER MOVE ---
        x, y = agent.position
        percepts = world.get_percepts(x, y)
        agent.perceive(percepts)
        draw_percepts(screen, percepts)
        draw_agent_mind(screen, agent)
        play_percept_sounds(percepts)  # Play sound for new cell
        pygame.display.flip()

        pygame.time.delay(100)  # Short pause to show new percepts

        if agent.found_gold:
            # print(f"\nGOLD FOUND at {agent.position}! GAME OVER.")
            show_game_over_popup(screen, agent.position)
            break

        clock.tick(30)

        # x, y = world.agent_pos
        # x, y = agent.position
        # percepts = world.get_percepts(x, y)
        # draw_percepts(screen, percepts)
        # draw_agent_mind(screen, agent)
        # # play sounds based on percepts
        # play_percept_sounds(percepts)
        # agent.perceive(percepts)
        # # print(f"Percepts: {percepts}")
        # if agent.found_gold:
        #     print(f"\n🎉 GOLD FOUND at {agent.position}! GAME OVER.")
        #     break
        # agent.step(world) 
        
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
        # pygame.time.delay(1500)
        # pygame.display.flip()
        # clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
# This is the main entry point for the Wumpus World game.
# It initializes the Pygame library, sets up the display, and runs the main game loop.