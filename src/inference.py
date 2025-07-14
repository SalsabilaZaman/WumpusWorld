class KnowledgeBase:
    def __init__(self, grid_size=10):
        self.facts = set()
        self.safe = set()
        self.unsafe = set()
        self.pits = set()
        self.wumpus = set()
        self.grid_size = grid_size
        self.percepts_map = {}  # (x, y): set(percepts)

    def update(self, pos, percepts):
        self.percepts_map[pos] = set(percepts)
        for p in percepts:
            self.facts.add((pos, p))

    def get_neighbors(self, pos):
        x, y = pos
        return [(x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
                if 0 <= x+dx < self.grid_size and 0 <= y+dy < self.grid_size]

    def infer(self, visited):
        # Rule 1: If a cell has no Breeze or Stench, all neighbors are safe
        for pos, percepts in self.percepts_map.items():
            neighbors = self.get_neighbors(pos)
            if "Breeze" not in percepts and "Stench" not in percepts:
                for n in neighbors:
                    self.safe.add(n)

        # Rule 2: If a cell has Breeze, at least one neighbor has a pit
        for pos, percepts in self.percepts_map.items():
            neighbors = self.get_neighbors(pos)
            if "Breeze" in percepts:
                possible_pits = [n for n in neighbors if n not in self.safe and n not in visited]
                if len(possible_pits) == 1:
                    self.pits.add(possible_pits[0])
                    self.unsafe.add(possible_pits[0])

        # Rule 3: If a cell has Stench, at least one neighbor has a Wumpus
        for pos, percepts in self.percepts_map.items():
            neighbors = self.get_neighbors(pos)
            if "Stench" in percepts:
                possible_wumpus = [n for n in neighbors if n not in self.safe and n not in visited]
                if len(possible_wumpus) == 1:
                    self.wumpus.add(possible_wumpus[0])
                    self.unsafe.add(possible_wumpus[0])

        # Rule 4: If a neighbor is the only unexplored tile adjacent to a Breezy tile, it must be a pit
        for pos, percepts in self.percepts_map.items():
            if "Breeze" in percepts:
                neighbors = self.get_neighbors(pos)
                unexplored = [n for n in neighbors if n not in visited and n not in self.safe]
                if len(unexplored) == 1:
                    self.pits.add(unexplored[0])
                    self.unsafe.add(unexplored[0])

    def query(self, proposition):
        return proposition in self.facts

    def is_safe(self, pos):
        return pos in self.safe

    def is_unsafe(self, pos):
        return pos in self.unsafe
