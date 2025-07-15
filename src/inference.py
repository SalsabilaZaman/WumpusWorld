class KnowledgeBase:
    def __init__(self, grid_size=10):
        # self.facts = set()
        self.safe = set()
        self.unsafe = set()
        self.risky = list()  # Changed to list for ordered processing
        self.pits = set()
        self.wumpus = set()
        self.frontier = set()
        self.grid_size = grid_size
        self.percepts_map = {}  # (x, y): set(percepts)
        self.found_gold = False

    def update(self, pos, percepts, visited=None):
        self.percepts_map[pos] = set(percepts)
        
        # for p in percepts:
        #     self.facts.add((pos, p))

        # If no danger, mark neighbors as safe and add to frontier
        if "Breeze" not in percepts and "Stench" not in percepts:
            for neighbor in self.get_neighbors(pos):
                self.safe.add(neighbor)
                if neighbor not in visited:
                     self.frontier.add(neighbor)
        if "Glitter" in percepts :
            self.found_gold = True
        else:    
            self.infer(pos,visited)
            print(f"Unsafe: {self.unsafe}")
            print(f"Pits: {self.pits}")
            print(f"Risky: {self.risky}")
            print(f"Wumpus: {self.wumpus}")
            # Otherwise, neighbors are risky until further inference
            # for neighbor in self.get_neighbors(pos):
            #     if neighbor not in self.safe and neighbor not in self.unsafe:
            #         self.risky.add(neighbor)

    def get_neighbors(self, pos):
        x, y = pos
        return [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= x + dx < self.grid_size and 0 <= y + dy < self.grid_size]
    def get_diagonal_neighbors(self, pos):
        x, y = pos
        return [(x + dx, y + dy) for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                if 0 <= x + dx < self.grid_size and 0 <= y + dy < self.grid_size]
    def get_interacting_cells(self, a, b):
        x1, y1 = a
        x2, y2 = b

        # Ensure they are diagonal (both x and y differ by 1)
        if abs(x1 - x2) == 1 and abs(y1 - y2) == 1:
            candidates = [(x1, y2), (x2, y1)]
            # Return only those within grid bounds
            return [(x, y) for x, y in candidates
                    if 0 <= x < self.grid_size and 0 <= y < self.grid_size]
        else:
            return []
    def handle_interacting_cells(self, cell1, cell2):
        is_cell1_safe = cell1 in self.safe
        is_cell2_safe = cell2 in self.safe

        if is_cell1_safe and not is_cell2_safe:
            if cell2 not in self.risky and cell2 not in self.unsafe:
                self.risky.append(cell2)  # Add to risky list
            # self.pits.add(cell2)
            # self.unsafe.add(cell2)
        elif not is_cell1_safe and is_cell2_safe:
            if cell1 not in self.risky and cell1 not in self.unsafe:
                self.risky.append(cell1)  # Add to risky list
            # self.pits.add(cell1)
            # self.unsafe.add(cell1)
        

    def infer(self, pos,visited):
        if "Breeze" in self.percepts_map[pos] :
            unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in self.unsafe]
            if len(unknowns) == 1:
                pit = unknowns[0]
                self.pits.add(pit)
                self.unsafe.add(pit)
            else:
                # for unknown in unknowns:
                #     self.risky.add(unknown)
                for diagonal in self.get_diagonal_neighbors(pos):
                    if self.percepts_map.get(diagonal, set()) == {"Breeze"} :
                        interacting_cells= self.get_interacting_cells(pos, diagonal)
                        count = len([cell for cell in interacting_cells if cell in self.safe])
                        if count == 1:
                            self.handle_interacting_cells(interacting_cells[0], interacting_cells[1])
                        if count == 0:
                            for unknown in unknowns:
                                if unknown not in self.risky and unknown not in self.unsafe:
                                    self.risky.append(unknown)

        if "Stench" in self.percepts_map[pos]:
            unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in self.unsafe]
            if len(unknowns) == 1:
                wumpus = unknowns[0]
                self.wumpus.add(wumpus)
                self.unsafe.add(wumpus)
            else:
                # for unknown in unknowns:
                #     self.risky.add(unknown)
                for diagonal in self.get_diagonal_neighbors(pos):
                    if self.percepts_map.get(diagonal, set()) == {"Stench"}:
                        interacting_cells= self.get_interacting_cells(pos, diagonal)
                        count = len([cell for cell in interacting_cells if cell in self.safe])
                        if count == 1:
                            self.handle_interacting_cells(interacting_cells[0], interacting_cells[1])
                        if count == 0:
                            for unknown in unknowns:
                                if unknown not in self.risky and unknown not in self.unsafe:
                                    self.risky.append(unknown)
        


                # self.pits.add(diagonal)
                # self.unsafe.add(diagonal) 
                # self.risky.add(unknowns)   
        # Rule 1: No Breeze or Stench => neighbors are safe
        # for pos, percepts in self.percepts_map.items():
        #     if "Breeze" not in percepts and "Stench" not in percepts:
        #         for neighbor in self.get_neighbors(pos):
        #             self.safe.add(neighbor)
        #             self.risky.discard(neighbor)

        # # Rule 2: Breeze => at least one neighbor has pit
        # for pos, percepts in self.percepts_map.items():
        #     if "Breeze" in percepts:
        #         unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in visited]
        #         if len(unknowns) == 1:
        #             pit = unknowns[0]
        #             self.pits.add(pit)
        #             self.unsafe.add(pit)
        #             self.risky.discard(pit)

        # # Rule 3: Stench => at least one neighbor has Wumpus
        # for pos, percepts in self.percepts_map.items():
        #     if "Stench" in percepts:
        #         unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in visited]
        #         if len(unknowns) == 1:
        #             w = unknowns[0]
        #             self.wumpus.add(w)
        #             self.unsafe.add(w)
        #             self.risky.discard(w)

        # # Rule 4: Breezy tile with 1 unknown neighbor => pit
        # for pos, percepts in self.percepts_map.items():
        #     if "Breeze" in percepts:
        #         unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in visited]
        #         if len(unknowns) == 1:
        #             pit = unknowns[0]
        #             self.pits.add(pit)
        #             self.unsafe.add(pit)
        #             self.risky.discard(pit)

    def get_frontier(self):
        return list(self.frontier)

    # def query(self, proposition):
    #     return proposition in self.facts

    def is_safe(self, pos):
        return pos in self.safe

    def is_unsafe(self, pos):
        return pos in self.unsafe

    def is_risky(self, pos):
        return pos in self.risky
