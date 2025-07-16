import pygame

CELL_SIZE = 60
GRID_SIZE = 10
AGENT_IMAGE_PATH = "src/images/new_agent.jpg"
BREEZE_IMAGE_PATH = "src/images/breeze.png"
STENCH_IMAGE_PATH = "src/images/stench.png"
GLITTER_IMAGE_PATH = "src/images/glitter.png"

# Load percept images   
agent_img = None
breeze_img = None
stench_img = None
glitter_img = None

breeze_sound = None
stench_sound = None
glitter_sound = None
prev_breeze = False
prev_stench = False

def init_assets():
    global agent_img, breeze_img, stench_img, glitter_img
    global breeze_sound, stench_sound, glitter_sound

    agent_img = pygame.image.load(AGENT_IMAGE_PATH)
    agent_img = pygame.transform.scale(agent_img, (CELL_SIZE, CELL_SIZE))
    breeze_img = pygame.image.load(BREEZE_IMAGE_PATH)
    breeze_img = pygame.transform.scale(breeze_img, (CELL_SIZE, CELL_SIZE))
    stench_img = pygame.image.load(STENCH_IMAGE_PATH)
    stench_img = pygame.transform.scale(stench_img, (CELL_SIZE, CELL_SIZE))
    glitter_img = pygame.image.load(GLITTER_IMAGE_PATH)
    glitter_img = pygame.transform.scale(glitter_img, (CELL_SIZE, CELL_SIZE))

    breeze_sound = pygame.mixer.Sound("src/sounds/breeze.mp3")
    stench_sound = pygame.mixer.Sound("src/sounds/stench.mp3")
    glitter_sound = pygame.mixer.Sound("src/sounds/glitter.mp3")


def init_gui():
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 650, GRID_SIZE * CELL_SIZE))
    pygame.display.set_caption("Wumpus World AI")    
    # Set default font to Orbitron if available
    try:
        pygame.font.SysFont("Orbitron", 40)
    except:
        pass  # If Orbitron is not available, fallback to default
    return screen

def draw_grid(screen):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

def draw_entities(screen, entities):
    font = pygame.font.SysFont(None, 24)
    
    # Draw percepts in visited cells
    if "percepts" in entities:
        for (x, y), percepts in entities["percepts"].items():
            # print(f"Cell {(x, y)} percepts FROM GUI: {percepts}")  # Debug print
            flipped_y = GRID_SIZE - 1 - y
            if "Breeze" in percepts:
                screen.blit(breeze_img, (x * CELL_SIZE, flipped_y * CELL_SIZE))
            if "Stench" in percepts:
                screen.blit(stench_img, (x * CELL_SIZE, flipped_y * CELL_SIZE))
            if "Glitter" in percepts:
                screen.blit(glitter_img, (x * CELL_SIZE, flipped_y * CELL_SIZE))

    # Draw agent with agent image
    x, y = entities["agent"]
    flipped_y = GRID_SIZE - 1 - y  # Flip y-axis for correct orientation
    screen.blit(agent_img, (x * CELL_SIZE, flipped_y * CELL_SIZE))
    

def draw_cell(screen, x, y, color, label, font):
    flipped_y = GRID_SIZE - 1 - y  # Flip y-axis for correct orientation
    rect = pygame.Rect(x * CELL_SIZE, flipped_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # border
    text = font.render(label, True, (255, 255, 255))
    screen.blit(text, (x * CELL_SIZE + 20, flipped_y * CELL_SIZE + 20))

def draw_percepts(screen, percepts):
    font = pygame.font.SysFont("Orbitron", 24)
    x_offset = GRID_SIZE * CELL_SIZE + 20
    base_y = 150  # Position above "What's on agent's Mind"
    pygame.draw.rect(screen, (255, 255, 255), (x_offset, base_y, 600, 40))  # clear previous text area
    label = font.render("Percepts: " + ", ".join(percepts), True, (0, 0, 128))
    screen.blit(label, (x_offset, base_y + 5))

def draw_agent_mind(screen, agent):
    font = pygame.font.SysFont("PressStart2P", 26)
    header_font = pygame.font.SysFont("Orbitron", 56, bold=True)
    # Start drawing at the right of the grid
    x_offset = GRID_SIZE * CELL_SIZE + 20
    base_y = 200  

    header_label = header_font.render("What's on agent's Mind", True, (204, 85, 0))
    header_x = x_offset + (600 - header_label.get_width()) // 2  # 600 is panel width, adjust if needed
    screen.blit(header_label, (header_x, base_y - 100))
    
    mind_lines = [
        f"I'm at: {agent.position}",
        f"Safe cells: {sorted(agent.safe)[-10:]}",        
        f"Risky cells: {sorted(agent.risky)[-10:]}",
        f"Cells to avoid: {sorted(agent.kb.unsafe)[-10:]}",
        f"Pits suspected at: {sorted(agent.kb.pits)}",
        f"Wumpus suspected at: {sorted(agent.kb.wumpus)}",
    ]

    # Action-specific reasoning
    # Show last action taken based on agent's state
    if hasattr(agent, "last_action") and agent.last_action:
        mind_lines.append(agent.last_action)
    else:
        # Decision summary
        if agent.safe:
            mind_lines.append("Safe frontier detected. Advancing to the next safe cell.")
        elif agent.risky:
            mind_lines.append("No safe moves left. Planning a path to the least risky cell.")
        elif len(agent.backtrack_stack) > 1:
            mind_lines.append(f"Backtracking from {agent.position} to {agent.backtrack_stack[-2]} due to lack of safe options.")
        else:
            mind_lines.append("No valid moves available. Agent is stuck.")

    for i, line in enumerate(mind_lines):
        label = font.render(line, True, (0, 0, 128))
        screen.blit(label, (x_offset, base_y + i * 22))

def play_bgm():
    pygame.mixer.music.load("src/sounds/bgm.mp3")
    pygame.mixer.music.play(-1)  # Loop forever
    pygame.mixer.music.set_volume(0.5)


# def play_percept_sounds(percepts):
#     global prev_breeze, prev_stench
#     if "Breeze" in percepts:
#         if prev_breeze:
#             breeze_sound.play(-1)
#         prev_breeze = True
#     else:
#         if prev_breeze:
#             breeze_sound.stop()
#         prev_breeze = False
    
#     if "Stench" in percepts:
#         if not prev_stench:
#             stench_sound.play(-1)
#         prev_stench = True
#     else:
#         if prev_stench:
#             stench_sound.stop()
#         prev_stench = False

#     if "Glitter" in percepts:
#         glitter_sound.play()

def play_percept_sounds(percepts):
    if "Breeze" in percepts:
        breeze_sound.stop()
        breeze_sound.play()
    if "Stench" in percepts:
        stench_sound.stop()
        stench_sound.play()
    if "Glitter" in percepts:
        glitter_sound.stop()
        glitter_sound.play()

def show_game_over_popup(screen, position):
    # Stop all sounds
    pygame.mixer.music.stop()
    if breeze_sound: breeze_sound.stop()
    if stench_sound: stench_sound.stop()
    if glitter_sound: glitter_sound.stop()

    # Popup styling
    popup_width, popup_height = 500, 220
    popup = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup.fill((255, 230, 120, 230))  # Warm gold with slight transparency

    # Draw border
    pygame.draw.rect(popup, (120, 80, 0), popup.get_rect(), 6, border_radius=20)

    # Fonts
    title_font = pygame.font.SysFont("PressStart2P", 38, bold=True)
    info_font = pygame.font.SysFont("arial", 24)
    button_font = pygame.font.SysFont("arial", 28, bold=True)

    # Main message
    msg = f"GOLD FOUND at {position}!"
    game_over = "GAME OVER."
    label1 = title_font.render(msg, True, (80, 40, 0))
    label2 = title_font.render(game_over, True, (180, 0, 0))

    # Center each line horizontally
    label1_x = (popup_width - label1.get_width()) // 2
    label2_x = (popup_width - label2.get_width()) // 2
    popup.blit(label1, (label1_x, 30))
    popup.blit(label2, (label2_x, 75))

    # Instructions
    info = "Click the Quit button to exit."
    info_label = info_font.render(info, True, (60, 60, 60))
    info_x = (popup_width - info_label.get_width()) // 2
    popup.blit(info_label, (info_x, 120))
    
    # Quit button
    button_rect = pygame.Rect(popup_width//2 - 70, 160, 140, 40)
    pygame.draw.rect(popup, (200, 60, 60), button_rect, border_radius=12)
    pygame.draw.rect(popup, (120, 0, 0), button_rect, 3, border_radius=12)
    button_label = button_font.render("Quit", True, (255, 255, 255))
    popup.blit(button_label, (button_rect.x + 32, button_rect.y + 5))

    # Center the popup
    screen_rect = screen.get_rect()
    popup_rect = popup.get_rect(center=screen_rect.center)
    screen.blit(popup, popup_rect)
    pygame.display.flip()

    # Wait for button click or quit event
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Translate mouse position to popup coordinates
                rel_x = mx - popup_rect.x
                rel_y = my - popup_rect.y
                if button_rect.collidepoint(rel_x, rel_y):
                    waiting = False
        pygame.time.delay(20)