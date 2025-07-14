class KnowledgeBase:
    def __init__(self, grid_size=10):
        self.facts = set()
        self.safe = set()
        self.unsafe = set()
        self.risky = set()
        self.pits = set()
        self.wumpus = set()
        self.frontier = set()
        self.grid_size = grid_size
        self.percepts_map = {}  # (x, y): set(percepts)

    def update(self, pos, percepts):
        self.percepts_map[pos] = set(percepts)
        for p in percepts:
            self.facts.add((pos, p))

        # If no danger, mark neighbors as safe and add to frontier
        if "Breeze" not in percepts and "Stench" not in percepts:
            for neighbor in self.get_neighbors(pos):
                self.safe.add(neighbor)
                self.frontier.add(neighbor)
        else:
            # Otherwise, neighbors are risky until further inference
            for neighbor in self.get_neighbors(pos):
                if neighbor not in self.safe and neighbor not in self.unsafe:
                    self.risky.add(neighbor)
                    self.frontier.add(neighbor)

    def get_neighbors(self, pos):
        x, y = pos
        return [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= x + dx < self.grid_size and 0 <= y + dy < self.grid_size]

    def infer(self, visited):
        # Rule 1: No Breeze or Stench => neighbors are safe
        for pos, percepts in self.percepts_map.items():
            if "Breeze" not in percepts and "Stench" not in percepts:
                for neighbor in self.get_neighbors(pos):
                    self.safe.add(neighbor)
                    self.risky.discard(neighbor)

        # Rule 2: Breeze => at least one neighbor has pit
        for pos, percepts in self.percepts_map.items():
            if "Breeze" in percepts:
                unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in visited]
                if len(unknowns) == 1:
                    pit = unknowns[0]
                    self.pits.add(pit)
                    self.unsafe.add(pit)
                    self.risky.discard(pit)

        # Rule 3: Stench => at least one neighbor has Wumpus
        for pos, percepts in self.percepts_map.items():
            if "Stench" in percepts:
                unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in visited]
                if len(unknowns) == 1:
                    w = unknowns[0]
                    self.wumpus.add(w)
                    self.unsafe.add(w)
                    self.risky.discard(w)

        # Rule 4: Breezy tile with 1 unknown neighbor => pit
        for pos, percepts in self.percepts_map.items():
            if "Breeze" in percepts:
                unknowns = [n for n in self.get_neighbors(pos) if n not in self.safe and n not in visited]
                if len(unknowns) == 1:
                    pit = unknowns[0]
                    self.pits.add(pit)
                    self.unsafe.add(pit)
                    self.risky.discard(pit)

    def get_frontier(self):
        return list(self.frontier)

    def query(self, proposition):
        return proposition in self.facts

    def is_safe(self, pos):
        return pos in self.safe

    def is_unsafe(self, pos):
        return pos in self.unsafe

    def is_risky(self, pos):
        return pos in self.risky
