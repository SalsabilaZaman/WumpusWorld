import random


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
        self.wumpus = set()
        self.gold = None
        self.agent_pos = (0, 0) 
        self.grid= [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        if map_file:
            self.load_map_from_file(map_file)
        else:
            self.generate_random_map(pit_prob=0.12, seed=42)  # Random map generation with fixed seed for reproducibility

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
                    self.wumpus.add((x,y))
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
            if (ax, ay) in self.wumpus:
                percepts.append("Stench")
        if (x, y) == self.gold:
            percepts.append("Glitter")
        return percepts
    
    def is_danger(self, pos):
        return pos in self.pits or pos in self.wumpus
    

    def generate_random_map(self, pit_prob=0.12, seed=None):
        
        if seed is not None:
            random.seed(seed)  # for reproducibility

        self.pits = set()
        self.wumpus = set()
        self.gold = None
        self.agent_pos = (0, 0)
        self.grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        total_cells = self.grid_size * self.grid_size
        available_cells = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)
                           if (x, y) != self.agent_pos]

        # Place pits randomly (based on probability)
        num_pits = int(pit_prob * total_cells)
        self.pits = set(random.sample(available_cells, num_pits))

        # Remove pits from available cells for wumpus/gold
        safe_cells = [cell for cell in available_cells if cell not in self.pits]

        # Place wumpus
        wumpus_pos = random.choice(safe_cells)
        self.wumpus = {wumpus_pos}
        safe_cells.remove(wumpus_pos)

        # Place gold
        self.gold = random.choice(safe_cells)

        print(f"[Map Generated] Pits: {len(self.pits)}, Wumpus: {self.wumpus}, Gold: {self.gold}")