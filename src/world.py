class World:
    # def __init__(self):
    #     self.grid_size = 10
    #     self.pits = {(1, 3), (3, 2), (4, 6)}  # example pits
    #     self.wumpus = (2, 2)
    #     self.gold = (6, 6)
    #     self.agent_pos = (0, 0)
    def __init__(self, map_file=None):
        self.grid_size = 10
        self.pits = set()
        self.wumpus = None
        self.gold = None
        self.agent_pos = (0, 0) 
        self.grid= [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        if map_file:
            self.load_map_from_file(map_file)

    def load_map_from_file(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.read().strip().split('\n')

        lines = lines[:self.grid_size]  

        for row_index, line in enumerate(lines):
            y = self.grid_size - 1 - row_index  # flip Y to match bottom-left origin
            for x, char in enumerate(line.strip()):
                if char == 'P':
                    self.pits.add((x, y))
                elif char == 'W':
                    self.wumpus = (x, y)
                elif char == 'G':
                    self.gold = (x, y)

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

    # def get_percepts(self, x, y):
    #     percepts = set()
    #     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down

    #     for dx, dy in directions:
    #         nx, ny = x + dx, y + dy
    #         if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
    #             symbol = self.grid[ny][nx]
    #             if symbol == 'P':
    #                 percepts.add("Breeze")
    #             elif symbol == 'W':
    #                 percepts.add("Stench")

    #     if self.grid[y][x] == 'G':
    #         percepts.add("Glitter")

    #     return list(percepts)
