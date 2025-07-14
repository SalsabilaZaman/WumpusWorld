class Agent:
    def __init__(self, grid_size=10):
        self.position = (0, 0)
        self.visited = set()
        self.safe = set([(0, 0)])
        self.frontier = set()
        self.kb = {}
        self.grid_size = grid_size
        self.path_history = [(0, 0)]  # Complete trail, never popped
        self.backtrack_stack = []     # Stack of places to backtrack

    def perceive(self, percepts):
        self.kb[self.position] = set(percepts)
        self.visited.add(self.position)

        x, y = self.position
        neighbors = self.get_neighbors((x, y))

        for nx, ny in neighbors:
            if (nx, ny) not in self.visited:
                self.frontier.add((nx, ny))

        if "Breeze" not in percepts and "Stench" not in percepts:
            for n in neighbors:
                self.safe.add(n)

    def get_neighbors(self, pos):
        x, y = pos
        return [(x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
                if 0 <= x+dx < self.grid_size and 0 <= y+dy < self.grid_size]

    def next_move(self):
        # Try safe, unvisited neighbors first
        for neighbor in self.get_neighbors(self.position):
            if neighbor in self.safe and neighbor not in self.visited:
                if neighbor in self.frontier:
                    self.frontier.remove(neighbor)
                self.backtrack_stack.append(self.position)  # Save current in backtrack
                return neighbor

        # If stuck: backtrack to previous position
        while self.backtrack_stack:
            back_pos = self.backtrack_stack.pop()
            for neighbor in self.get_neighbors(back_pos):
                if neighbor in self.safe and neighbor not in self.visited:
                    return back_pos  # Move to back_pos to continue from there

        return None  # No moves possible

    def move_to(self, cell):
        self.position = cell
        if cell not in self.path_history:
            self.path_history.append(cell)

    def step(self, world):
        x, y = self.position
        percepts = world.get_percepts(x, y)
        self.perceive(percepts)

        print(f"\nAgent is at: {self.position}")
        print(f"Percepts: {percepts}")
        print(f"Safe: {self.safe}")
        print(f"Visited: {self.visited}")
        print(f"Frontier: {self.frontier}")

        next_pos = self.next_move()
        if next_pos:
            self.move_to(next_pos)
            world.agent_pos = self.position
