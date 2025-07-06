class World:
    def __init__(self):
        self.grid_size = 10
        self.pits = set()
        self.wumpus = (2, 2)
        self.gold = (4, 4)
        self.agent_pos = (0, 0)

    def get_percepts(self, pos):
        # Return simulated percepts based on surroundings
        return ["Breeze"] if any((x, y) in self.pits for (x, y) in self.adjacent(pos)) else []

    def adjacent(self, pos):
        x, y = pos
        return [(x+dx, y+dy) for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]
                if 0 <= x+dx < self.grid_size and 0 <= y+dy < self.grid_size]
