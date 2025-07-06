class World:
    def __init__(self):
        self.grid_size = 10
        self.pits = {(1, 3), (3, 2), (4, 6)}  # example pits
        self.wumpus = (2, 2)
        self.gold = (6, 6)
        self.agent_pos = (0, 0)

    def get_entities(self):
        return {
            "pits": self.pits,
            "wumpus": self.wumpus,
            "gold": self.gold,
            "agent": self.agent_pos
        }
    def move_agent(self, dx, dy):
        new_x = self.agent_pos[0] + dx
        new_y = self.agent_pos[1] + dy
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            self.agent_pos = (new_x, new_y)
    
    def get_percepts(self, x, y):
        percepts = []
        adj = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]

        for ax, ay in adj:
            if (ax, ay) in self.pits:
                percepts.append("Breeze")
            if (ax, ay) == self.wumpus:
                percepts.append("Stench")
        if (x, y) == self.gold:
            percepts.append("Glitter")
        return percepts