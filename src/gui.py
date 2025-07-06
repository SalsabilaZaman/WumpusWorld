import pygame

CELL_SIZE = 60
GRID_SIZE = 10

def draw_grid(screen):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

def draw_entities(screen, entities):
    font = pygame.font.SysFont(None, 24)
    
    # Draw pits
    for (x, y) in entities["pits"]:
        draw_cell(screen, x, y, (50, 50, 50), "P", font)

    # Draw Wumpus
    x, y = entities["wumpus"]
    draw_cell(screen, x, y, (139, 0, 0), "W", font)

    # Draw gold
    x, y = entities["gold"]
    draw_cell(screen, x, y, (255, 223, 0), "G", font)

    # Draw agent
    x, y = entities["agent"]
    draw_cell(screen, x, y, (0, 128, 255), "A", font)

def draw_cell(screen, x, y, color, label, font):
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # border
    text = font.render(label, True, (255, 255, 255))
    screen.blit(text, (x * CELL_SIZE + 20, y * CELL_SIZE + 20))
