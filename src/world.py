class World:
    def __init__(self):
        self.grid_size = 10
        self.pits = {(1, 3), (3, 2), (4, 6)}  # example pits
        self.wumpus = (2, 2)
        self.gold = (6, 6)
        self.agent_pos = (0, 9)

    def get_entities(self):
        return {
            "pits": self.pits,
            "wumpus": self.wumpus,
            "gold": self.gold,
            "agent": self.agent_pos
        }
