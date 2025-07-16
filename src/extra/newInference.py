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
    

    
    # def infer(self, pos,visited):
    #     print(f"Inferring at {pos} with percepts {self.percepts_map[pos]}")
    #     if "Breeze" in self.percepts_map[pos] :
    #         print(f"Breeze at {pos}")
    #         unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in self.unsafe]
    #         if len(unknowns) == 1:
    #             pit = unknowns[0]
    #             self.pits.add(pit)
    #             self.unsafe.add(pit)
    #         else:
    #             # for unknown in unknowns:
    #             #     self.risky.add(unknown)
    #             for diagonal in self.get_diagonal_neighbors(pos):
    #                 if self.percepts_map.get(diagonal, set()) == {"Breeze"} :
    #                     interacting_cells= self.get_interacting_cells(pos, diagonal)
    #                     count = len([cell for cell in interacting_cells if cell in self.safe])
    #                     if count == 1:
    #                         self.handle_interacting_cells(interacting_cells[0], interacting_cells[1])
                
    #                 for unknown in unknowns:
    #                     if unknown not in self.risky and unknown not in self.unsafe:
    #                         self.risky.append(unknown)

    #     if "Stench" in self.percepts_map[pos]:
    #         print(f"Stench at {pos}")
    #         unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in self.unsafe]
    #         if len(unknowns) == 1:
    #             wumpus = unknowns[0]
    #             print(f"Wumpus detected at {wumpus}.KILLED WUMPUS MUHAHAHAHA")
    #             self.wumpus.add(wumpus)
    #             self.unsafe.add(wumpus)
    #         else:
    #             # for unknown in unknowns:
    #             #     self.risky.add(unknown)
    #             for diagonal in self.get_diagonal_neighbors(pos):
    #                 if self.percepts_map.get(diagonal, set()) == {"Stench"}:
    #                     interacting_cells= self.get_interacting_cells(pos, diagonal)
    #                     count = len([cell for cell in interacting_cells if cell in self.safe])
    #                     if count == 1:
    #                         self.handle_interacting_cells(interacting_cells[0], interacting_cells[1])
            
    #                 for unknown in unknowns:
    #                     if unknown not in self.risky and unknown not in self.unsafe:
    #                         self.risky.append(unknown)
    #     self.resolve_risks()

    # def resolve_risks(self):
    #     # Try resolving risky cells using updated safe/unsafe sets
    #     for pos, percepts in self.percepts_map.items():
    #         if "Breeze" in percepts:
    #             unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in self.unsafe]
    #             if len(unknowns) == 1:
    #                 pit = unknowns[0]
    #                 print(f"[RESOLVED] Pit must be at {pit}")
    #                 self.pits.add(pit)
    #                 self.unsafe.add(pit)
    #                 if pit in self.risky:
    #                     self.risky.remove(pit)

    #         if "Stench" in percepts:
    #             unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in self.unsafe]
    #             if len(unknowns) == 1:
    #                 w = unknowns[0]
    #                 print(f"[RESOLVED] Wumpus must be at {w}")
    #                 self.wumpus.add(w)
    #                 self.unsafe.add(w)
    #                 if w in self.risky:
    #                     self.risky.remove(w)
    # def resolve_risks(self):
    #     for pos, percepts in self.percepts_map.items():
    #         neighbors = self.get_neighbors(pos)

    #         # Filter neighbors by current knowledge
    #         safe_or_unsafe = [n for n in neighbors if n in self.safe or n in self.unsafe]
    #         unknowns = [n for n in neighbors if n not in self.safe and n not in self.unsafe]

    #         # If there's only one unknown and all others are known (either safe or unsafe), we can infer
    #         if "Breeze" in percepts and len(unknowns) == 1 and len(safe_or_unsafe) == len(neighbors) - 1:
    #             pit = unknowns[0]
    #             if pit not in self.unsafe:
    #                 print(f"[RESOLVED] Breeze at {pos} → Pit must be at {pit}")
    #                 self.pits.add(pit)
    #                 self.unsafe.add(pit)
    #                 if pit in self.risky:
    #                     self.risky.remove(pit)

    #         if "Stench" in percepts and len(unknowns) == 1 and len(safe_or_unsafe) == len(neighbors) - 1:
    #             wumpus = unknowns[0]
    #             if wumpus not in self.unsafe:
    #                 print(f"[RESOLVED] Stench at {pos} → Wumpus must be at {wumpus}")
    #                 self.wumpus.add(wumpus)
    #                 self.unsafe.add(wumpus)
    #                 if wumpus in self.risky:
    #                     self.risky.remove(wumpus)