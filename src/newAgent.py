from inference import KnowledgeBase

class Agent:
    def __init__(self, grid_size=10):
        self.position = (0, 0)
        self.grid_size = grid_size
        self.visited = set()
        self.kb = KnowledgeBase(grid_size)

        self.path_history = [(0, 0)]     # all places visited
        self.backtrack_stack = []        # decision points to revisit

    def get_neighbors(self, pos):
        x, y = pos
        return [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= x + dx < self.grid_size and 0 <= y + dy < self.grid_size]

    def perceive(self, percepts):
        self.kb.update(self.position, percepts)
        self.visited.add(self.position)
        self.kb.infer(self.visited)

    def next_move(self):
        # Priority 1: Safe and unvisited neighbors
        for neighbor in self.get_neighbors(self.position):
            if self.kb.is_safe(neighbor) and neighbor not in self.visited:
                self.backtrack_stack.append(self.position)
                return neighbor

        # Priority 2: Backtrack to earlier safe position and try its neighbors
        while self.backtrack_stack:
            back_pos = self.backtrack_stack.pop()
            for neighbor in self.get_neighbors(back_pos):
                if self.kb.is_safe(neighbor) and neighbor not in self.visited:
                    return back_pos

        # Priority 3: Risky frontier cell (if any known possible move)
        for cell in self.kb.get_frontier():
            if cell not in self.visited and cell not in self.kb.unsafe:
                return cell

        return None

    def move_to(self, cell):
        self.position = cell
        if cell not in self.path_history:
            self.path_history.append(cell)

    def step(self, world):
        percepts = world.get_percepts(*self.position)
        self.perceive(percepts)

        print(f"\nAgent is at: {self.position}")
        print(f"Percepts: {percepts}")
        print(f"Safe cells: {self.kb.safe}")
        print(f"Visited: {self.visited}")
        print(f"Pits: {self.kb.pits}")
        print(f"Wumpus: {self.kb.wumpus}")
        print(f"Unsafe: {self.kb.unsafe}")
        print(f"Frontier: {self.kb.get_frontier()}")

        next_pos = self.next_move()
        if next_pos:
            self.move_to(next_pos)
            world.agent_pos = self.position
