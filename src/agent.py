class Agent:
    def __init__(self, grid_size=10):
        self.position = (0, 0)
        self.visited = set()
        self.safe = set([(0, 0)])
        self.frontier = set()
        self.kb = {}  # Knowledge base: maps (x,y) to percepts like {"Breeze", "Stench"}
        self.grid_size = grid_size

    def perceive(self, percepts):
        self.kb[self.position] = set(percepts)
        self.visited.add(self.position)

        x, y = self.position
        neighbors = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]

        for nx, ny in neighbors:
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                if (nx, ny) not in self.visited:
                    self.frontier.add((nx, ny))

        if "Breeze" not in percepts and "Stench" not in percepts:
            for nx, ny in neighbors:
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    self.safe.add((nx, ny))

    def next_move(self):
        for cell in self.frontier:
            if cell not in self.visited and cell in self.safe:
                print(f"Returned Cell: {cell}")
                return cell
        return None  # No safe move known

    def move_to(self, cell):
        self.position = cell
    def step(self, world):
        x, y = self.position
        percepts = world.get_percepts(x, y)
        self.perceive(percepts)
        print(f"Agent is at: {self.position}")
        print(f"Percepts: {percepts}")
        print(f"Safe: {self.safe}")
        print(f"Frontier: {self.frontier}")
        print(f"Visited: {self.visited}")

        next_pos = self.next_move()
        if next_pos:
            self.move_to(next_pos)
            world.agent_pos = self.position
