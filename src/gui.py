import pygame
import math

CELL_SIZE = 60
GRID_SIZE = 10
AGENT_IMAGE_PATH = "src/images/new_agent.jpg"
BREEZE_IMAGE_PATH = "src/images/breeze.png"
STENCH_IMAGE_PATH = "src/images/stench.png"
GLITTER_IMAGE_PATH = "src/images/glitter.png"

# Enhanced color scheme
COLORS = {
    'background': (20, 25, 40),           # Dark blue-gray background
    'grid_line': (70, 80, 95),            # Subtle grid lines
    'unvisited': (45, 50, 65),            # Dark cells for unvisited
    'visited': (85, 120, 140),            # Light blue for visited
    'safe': (70, 130, 80),                # Green for safe cells
    'risky': (180, 140, 60),              # Orange for risky cells
    'unsafe': (160, 70, 70),              # Red for unsafe cells
    'frontier': (120, 90, 160),           # Purple for frontier
    'agent_path': (100, 100, 140),        # Path trail color
    'text_primary': (220, 220, 240),      # Light text
    'text_secondary': (180, 180, 200),    # Secondary text
    'text_accent': (255, 200, 100),       # Accent text
    'panel_bg': (30, 35, 50),             # Panel background
    'panel_border': (80, 90, 110),        # Panel border
}

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

    # Load and enhance agent image
    agent_img = pygame.image.load(AGENT_IMAGE_PATH)
    agent_img = pygame.transform.scale(agent_img, (CELL_SIZE - 4, CELL_SIZE - 4))
    
    # Load and enhance percept images with better blending
    breeze_img = pygame.image.load(BREEZE_IMAGE_PATH)
    breeze_img = pygame.transform.scale(breeze_img, (CELL_SIZE - 10, CELL_SIZE - 10))
    breeze_img.set_alpha(180)  # Semi-transparent
    
    stench_img = pygame.image.load(STENCH_IMAGE_PATH)
    stench_img = pygame.transform.scale(stench_img, (CELL_SIZE - 10, CELL_SIZE - 10))
    stench_img.set_alpha(180)
    
    glitter_img = pygame.image.load(GLITTER_IMAGE_PATH)
    glitter_img = pygame.transform.scale(glitter_img, (CELL_SIZE - 10, CELL_SIZE - 10))
    glitter_img.set_alpha(200)

    breeze_sound = pygame.mixer.Sound("src/sounds/breeze.mp3")
    stench_sound = pygame.mixer.Sound("src/sounds/stench.mp3")
    glitter_sound = pygame.mixer.Sound("src/sounds/glitter.mp3")


def init_gui():
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 700, GRID_SIZE * CELL_SIZE + 50))
    pygame.display.set_caption("Wumpus World AI - Enhanced Edition")    
    # Set default font to Orbitron if available
    try:
        pygame.font.SysFont("Orbitron", 40)
    except:
        pass  # If Orbitron is not available, fallback to default
    return screen

def draw_grid(screen, agent):
    """Draw enhanced grid with cell coloring based on agent's knowledge"""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            flipped_y = GRID_SIZE - 1 - y
            rect = pygame.Rect(x * CELL_SIZE, flipped_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            # Determine cell color based on agent's knowledge
            cell_color = COLORS['unvisited']  # Default
            
            if (x, y) in agent.visited:
                cell_color = COLORS['visited']
            elif (x, y) in agent.safe:
                cell_color = COLORS['safe']
            elif (x, y) in agent.risky:
                cell_color = COLORS['risky']
            elif (x, y) in agent.kb.unsafe:
                cell_color = COLORS['unsafe']
            elif (x, y) in agent.frontier:
                cell_color = COLORS['frontier']
            
            # Add subtle gradient effect
            if (x, y) in agent.path_history:
                # Create a trail effect with fading intensity
                trail_index = len(agent.path_history) - agent.path_history.index((x, y))
                alpha = max(30, 100 - trail_index * 10)
                trail_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                trail_surface.fill((*COLORS['agent_path'], alpha))
                screen.blit(trail_surface, (x * CELL_SIZE, flipped_y * CELL_SIZE))
            
            # Fill cell with determined color
            pygame.draw.rect(screen, cell_color, rect)
            
            # Add subtle inner border for depth
            inner_rect = pygame.Rect(x * CELL_SIZE + 1, flipped_y * CELL_SIZE + 1, 
                                   CELL_SIZE - 2, CELL_SIZE - 2)
            pygame.draw.rect(screen, tuple(min(255, c + 20) for c in cell_color), inner_rect, 1)
            
            # Draw main border
            pygame.draw.rect(screen, COLORS['grid_line'], rect, 1)

def draw_entities(screen, entities):
    """Draw entities with enhanced visual effects"""
    
    # Draw percepts in visited cells with better positioning
    if "percepts" in entities:
        for (x, y), percepts in entities["percepts"].items():
            flipped_y = GRID_SIZE - 1 - y
            
            # Center the percept images in the cell
            percept_x = x * CELL_SIZE + 5
            percept_y = flipped_y * CELL_SIZE + 5
            
            # Add glow effect for percepts
            if "Breeze" in percepts:
                # Create a subtle glow effect
                glow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (100, 200, 255, 50), 
                                 (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2)
                screen.blit(glow_surface, (x * CELL_SIZE, flipped_y * CELL_SIZE))
                screen.blit(breeze_img, (percept_x, percept_y))
                
            if "Stench" in percepts:
                # Create a subtle glow effect
                glow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 100, 100, 50), 
                                 (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2)
                screen.blit(glow_surface, (x * CELL_SIZE, flipped_y * CELL_SIZE))
                screen.blit(stench_img, (percept_x, percept_y))
                
            if "Glitter" in percepts:
                # Create a golden glow effect
                glow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 215, 0, 80), 
                                 (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2)
                screen.blit(glow_surface, (x * CELL_SIZE, flipped_y * CELL_SIZE))
                screen.blit(glitter_img, (percept_x, percept_y))

    # Draw agent with enhanced visual effects
    x, y = entities["agent"]
    flipped_y = GRID_SIZE - 1 - y
    
    # Add agent glow effect
    agent_glow = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(agent_glow, (255, 255, 100, 100), 
                      (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2)
    screen.blit(agent_glow, (x * CELL_SIZE, flipped_y * CELL_SIZE))
    
    # Draw agent with slight offset for better centering
    screen.blit(agent_img, (x * CELL_SIZE + 2, flipped_y * CELL_SIZE + 2))
    

def draw_cell(screen, x, y, color, label, font):
    flipped_y = GRID_SIZE - 1 - y  # Flip y-axis for correct orientation
    rect = pygame.Rect(x * CELL_SIZE, flipped_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # border
    text = font.render(label, True, (255, 255, 255))
    screen.blit(text, (x * CELL_SIZE + 20, flipped_y * CELL_SIZE + 20))

def draw_percepts(screen, percepts):
    """Draw current percepts with enhanced styling"""
    font = pygame.font.SysFont("Consolas", 22, bold=True)
    x_offset = GRID_SIZE * CELL_SIZE + 30
    base_y = 20
    
    # Draw panel background
    panel_rect = pygame.Rect(x_offset - 10, base_y - 10, 650, 60)
    pygame.draw.rect(screen, COLORS['panel_bg'], panel_rect)
    pygame.draw.rect(screen, COLORS['panel_border'], panel_rect, 2)
    
    # Title
    title_font = pygame.font.SysFont("Orbitron", 24, bold=True)
    title_label = title_font.render("CURRENT PERCEPTS", True, COLORS['text_accent'])
    screen.blit(title_label, (x_offset, base_y))
    
    # Percepts with icons
    percept_text = ", ".join(percepts) if percepts else "None"
    percept_color = COLORS['text_primary'] if percepts else COLORS['text_secondary']
    
    # Add colored indicators for each percept
    y_pos = base_y + 35
    if "Breeze" in percepts:
        pygame.draw.circle(screen, (100, 200, 255), (x_offset, y_pos), 8)
        screen.blit(font.render("Breeze", True, (100, 200, 255)), (x_offset + 20, y_pos - 10))
        x_offset += 100
    if "Stench" in percepts:
        pygame.draw.circle(screen, (255, 100, 100), (x_offset, y_pos), 8)
        screen.blit(font.render("Stench", True, (255, 100, 100)), (x_offset + 20, y_pos - 10))
        x_offset += 100
    if "Glitter" in percepts:
        pygame.draw.circle(screen, (255, 215, 0), (x_offset, y_pos), 8)
        screen.blit(font.render("Glitter", True, (255, 215, 0)), (x_offset + 20, y_pos - 10))
    
    if not percepts:
        screen.blit(font.render("No percepts detected", True, COLORS['text_secondary']), 
                   (GRID_SIZE * CELL_SIZE + 30, y_pos - 10))

def draw_agent_mind(screen, agent):
    """Draw enhanced agent mind panel with better organization and styling"""
    x_offset = GRID_SIZE * CELL_SIZE + 30
    base_y = 100
    panel_width = 650
    panel_height = 500
    
    # Draw main panel background
    panel_rect = pygame.Rect(x_offset - 10, base_y - 10, panel_width, panel_height)
    pygame.draw.rect(screen, COLORS['panel_bg'], panel_rect)
    pygame.draw.rect(screen, COLORS['panel_border'], panel_rect, 3)
    
    # Header
    header_font = pygame.font.SysFont("Orbitron", 32, bold=True)
    header_label = header_font.render("AGENT INTELLIGENCE", True, COLORS['text_accent'])
    header_x = x_offset + (panel_width - header_label.get_width()) // 2 - 10
    screen.blit(header_label, (header_x, base_y))
    
    # Sub-header
    sub_font = pygame.font.SysFont("Consolas", 16, italic=True)
    sub_label = sub_font.render("Real-time decision making process", True, COLORS['text_secondary'])
    sub_x = x_offset + (panel_width - sub_label.get_width()) // 2 - 10
    screen.blit(sub_label, (sub_x, base_y + 40))
    
    # Status section
    status_y = base_y + 80
    status_font = pygame.font.SysFont("Consolas", 20, bold=True)
    info_font = pygame.font.SysFont("Consolas", 18)
    
    # Current position with highlight
    pos_label = status_font.render("CURRENT POSITION:", True, COLORS['text_accent'])
    screen.blit(pos_label, (x_offset, status_y))
    pos_value = info_font.render(f"{agent.position}", True, COLORS['text_primary'])
    screen.blit(pos_value, (x_offset + 200, status_y))
    
    # Score
    score_label = status_font.render("SCORE:", True, COLORS['text_accent'])
    screen.blit(score_label, (x_offset + 350, status_y))
    score_value = info_font.render(f"{agent.get_score()}", True, COLORS['text_primary'])
    screen.blit(score_value, (x_offset + 420, status_y))
    
    # Knowledge sections
    sections = [
        ("EXPLORED CELLS", sorted(agent.visited)[-7:], (70, 200, 70)),
        ("SAFE FRONTIER", sorted(agent.safe)[-7:], (70, 170, 70)),
        ("RISKY CELLS", sorted(agent.risky)[-7:], (200, 140, 70)),
        ("DANGEROUS CELLS", sorted(agent.kb.unsafe)[-7:], (200, 70, 70)),
        ("SUSPECTED PITS", sorted(agent.kb.pits)[-7:], (180, 80, 80)),
        ("WUMPUS LOCATIONS", sorted(agent.kb.wumpus)[-7:], (150, 60, 60)),
    ]
    
    section_y = status_y + 40
    for i, (title, data, color) in enumerate(sections):
        y_pos = section_y + (i * 55)
        
        # Section title
        title_label = status_font.render(title + ":", True, color)
        screen.blit(title_label, (x_offset, y_pos))
        
        # Data (show only recent items to prevent overflow)
        if data:
            display_data = data[-7:] if len(data) > 8 else data
            if len(data) > 8:
                data_text = f"{display_data} ...({len(data)} total)"
            else:
                data_text = str(display_data)
        else:
            data_text = "None detected"
        
        data_label = info_font.render(data_text, True, COLORS['text_primary'])
        screen.blit(data_label, (x_offset + 20, y_pos + 20))
    
    # Decision making section
    decision_y = section_y + 350
    decision_font = pygame.font.SysFont("Consolas", 18, bold=True)
    
    # Decision background
    decision_rect = pygame.Rect(x_offset - 5, decision_y - 5, panel_width - 20, 80)
    pygame.draw.rect(screen, tuple(max(0, c - 10) for c in COLORS['panel_bg']), decision_rect)
    pygame.draw.rect(screen, COLORS['text_accent'], decision_rect, 2)
    
    decision_label = decision_font.render("CURRENT STRATEGY:", True, COLORS['text_accent'])
    screen.blit(decision_label, (x_offset, decision_y))
    
    # Strategy text based on agent state
    if hasattr(agent, "last_action") and agent.last_action:
        strategy = agent.last_action
    else:
        frontier_list = list(agent.frontier)
        if len(frontier_list) > 1 and frontier_list[0] in agent.get_neighbors(agent.position):
           strategy = "Advancing to safe frontier cells"
        elif len(agent.backtrack_stack) > 1 and len(agent.frontier) > 1:
            strategy = f"Backtracking to safer position"
        elif agent.risky:
            strategy = f"Calculating risk for frontier exploration"
        else:
            strategy = f"No valid moves - reassessing situation"
    
    strategy_lines = []
    words = strategy.split()
    current_line = ""
    for word in words:
        if len(current_line + word) < 50:
            current_line += word + " "
        else:
            strategy_lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        strategy_lines.append(current_line.strip())
    
    for i, line in enumerate(strategy_lines):
        strategy_label = info_font.render(line, True, COLORS['text_primary'])
        screen.blit(strategy_label, (x_offset + 10, decision_y + 25 + i * 20))

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

def show_game_over_popup(screen, position, died=False):
    """Enhanced game over popup with modern styling. If died=True, show death message."""
    # Stop all sounds
    pygame.mixer.music.stop()
    if breeze_sound: breeze_sound.stop()
    if stench_sound: stench_sound.stop()
    if glitter_sound: glitter_sound.stop()

    # Enhanced popup styling
    popup_width, popup_height = 600, 300
    popup = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    
    # Gradient background effect
    for i in range(popup_height):
        alpha = int(220 - (i * 0.3))
        color = (40, 45, 60, alpha)
        pygame.draw.rect(popup, color, (0, i, popup_width, 1))
    
    # Draw border with glow effect
    pygame.draw.rect(popup, (255, 215, 0), popup.get_rect(), 8, border_radius=25)
    pygame.draw.rect(popup, (200, 160, 0), popup.get_rect(), 4, border_radius=25)

    # Fonts
    title_font = pygame.font.SysFont("Orbitron", 42, bold=True)
    subtitle_font = pygame.font.SysFont("Orbitron", 32, bold=True)
    info_font = pygame.font.SysFont("Consolas", 22)
    button_font = pygame.font.SysFont("Orbitron", 24, bold=True)

    # Title with golden glow
    if died:
        title_msg = "GAME OVER!"
        subtitle_msg = f"Agent Died at {position}"
        game_over_msg = "MISSION FAILED"
        info_msg = "Agent fell into a pit \n OR \n was eaten by the Wumpus!"
        game_over_color = (255, 100, 100)
    else:
        title_msg = "MISSION ACCOMPLISHED!"
        subtitle_msg = f"Gold Retrieved at {position}"
        game_over_msg = "GAME COMPLETED SUCCESSFULLY"
        info_msg = "Agent successfully navigated Wumpus World!"
        game_over_color = (100, 255, 100)

    title_label = title_font.render(title_msg, True, (255, 215, 0))
    subtitle_label = subtitle_font.render(subtitle_msg, True, (255, 200, 100))
    # Center titles
    title_x = (popup_width - title_label.get_width()) // 2
    subtitle_x = (popup_width - subtitle_label.get_width()) // 2
    popup.blit(title_label, (title_x, 40))
    popup.blit(subtitle_label, (subtitle_x, 90))
    # Game over/accomplished message
    game_over_label = title_font.render(game_over_msg, True, game_over_color)
    game_over_x = (popup_width - game_over_label.get_width()) // 2
    popup.blit(game_over_label, (game_over_x, 130))
    # Info
    info_label = info_font.render(info_msg, True, COLORS['text_primary'])
    info_x = (popup_width - info_label.get_width()) // 2
    popup.blit(info_label, (info_x, 180))
    
    # Enhanced quit button
    button_rect = pygame.Rect(popup_width//2 - 80, 220, 160, 50)
    
    # Button gradient
    for i in range(button_rect.height):
        color_intensity = int(200 - (i * 2))
        button_color = (color_intensity, 60, 60)
        pygame.draw.rect(popup, button_color, 
                        (button_rect.x, button_rect.y + i, button_rect.width, 1))
    
    # Button border
    pygame.draw.rect(popup, (255, 100, 100), button_rect, 3, border_radius=15)
    pygame.draw.rect(popup, (200, 0, 0), button_rect, 1, border_radius=15)
    
    # Button text
    button_label = button_font.render("EXIT GAME", True, (255, 255, 255))
    button_text_x = button_rect.x + (button_rect.width - button_label.get_width()) // 2
    button_text_y = button_rect.y + (button_rect.height - button_label.get_height()) // 2
    popup.blit(button_label, (button_text_x, button_text_y))

    # Center the popup on screen
    screen_rect = screen.get_rect()
    popup_rect = popup.get_rect(center=screen_rect.center)
    
    # Add shadow effect
    shadow_surface = pygame.Surface((popup_width + 20, popup_height + 20), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 100))
    shadow_rect = shadow_surface.get_rect(center=(popup_rect.centerx + 10, popup_rect.centery + 10))
    screen.blit(shadow_surface, shadow_rect)
    
    # Draw the popup
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