class KnowledgeBase:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.percepts_map = {}  # (x, y): set(percepts)

    def update(self, pos, percepts, visited, world):
        self.percepts_map[pos] = set(percepts)
        neighbors = self.get_neighbors(pos)
        
        # Current cell is safe ('-'), mark unvisited neighbors as safe (0) unless risky
        if percepts == set(['-']):
            for nx, ny in neighbors:
                if world.playing_grid[nx][ny] in [-1, -2, -5]:
                    world.playing_grid[nx][ny] = 0  # Correct incorrect risky deductions
                if (nx, ny) not in visited:
                    world.playing_grid[nx][ny] = 0

        # Handle Stench ('S') - possible Wumpus
        elif 'Stench' in percepts:
            unknowns = [n for n in neighbors if world.playing_grid[n[0]][n[1]] == 0]
            has_minus_one = any(world.playing_grid[n[0]][n[1]] == -1 for n in neighbors)
            
            if has_minus_one:
                for nx, ny in neighbors:
                    if world.playing_grid[nx][ny] == -1:
                        world.playing_grid[nx][ny] = -3  # Confirm Wumpus
            elif len(unknowns) == 1:
                nx, ny = unknowns[0]
                world.playing_grid[nx][ny] = -3  # Only one unknown, it's Wumpus
            elif unknowns:
                for nx, ny in unknowns:
                    world.playing_grid[nx][ny] = -1  # Multiple unknowns, mark as possible Wumpus

        # Handle Breeze ('B') - possible Pit
        elif 'Breeze' in percepts:
            unknowns = [n for n in neighbors if world.playing_grid[n[0]][n[1]] == 0]
            has_minus_two = any(world.playing_grid[n[0]][n[1]] == -2 for n in neighbors)
            
            if has_minus_two:
                for nx, ny in neighbors:
                    if world.playing_grid[nx][ny] == -2:
                        world.playing_grid[nx][ny] = -4  # Confirm Pit
            elif len(unknowns) == 1:
                nx, ny = unknowns[0]
                world.playing_grid[nx][ny] = -4  # Only one unknown, it's Pit
            elif unknowns:
                for nx, ny in unknowns:
                    world.playing_grid[nx][ny] = -2  # Multiple unknowns, mark as possible Pit

        # Handle T (Wumpus or Pit)
        elif 'T' in percepts:
            unknowns = [n for n in neighbors if world.playing_grid[n[0]][n[1]] == 0]
            has_wumpus = any(world.playing_grid[n[0]][n[1]] in [-1, -3] for n in neighbors)
            has_pit = any(world.playing_grid[n[0]][n[1]] in [-2, -4] for n in neighbors)
            
            if has_wumpus:
                for nx, ny in neighbors:
                    if world.playing_grid[nx][ny] in [-1, -3]:
                        world.playing_grid[nx][ny] = -3  # Confirm Wumpus
                    elif world.playing_grid[nx][ny] == 0:
                        world.playing_grid[nx][ny] = -4 if len(unknowns) == 1 else -2
            elif has_pit:
                for nx, ny in neighbors:
                    if world.playing_grid[nx][ny] in [-2, -4]:
                        world.playing_grid[nx][ny] = -4  # Confirm Pit
                    elif world.playing_grid[nx][ny] == 0:
                        world.playing_grid[nx][ny] = -3 if len(unknowns) == 1 else -1
            else:
                for nx, ny in unknowns:
                    world.playing_grid[nx][ny] = -5  # Possible Wumpus or Pit

    def get_neighbors(self, pos):
        x, y = pos
        return [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= x + dx < self.grid_size and 0 <= y + dy < self.grid_size]