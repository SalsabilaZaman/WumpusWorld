import sys
from inference import KnowledgeBase


class Agent:
    def __init__(self, grid_size=10):
        self.position = (0, 0)
        self.visited = set()
        self.safe = set([(0, 0)])   
        self.frontier = set()
        self.risky = set()
        self.kb = KnowledgeBase(grid_size)
        self.grid_size = grid_size
        self.path_history = [(0, 0)]  # Complete trail, never popped
        self.backtrack_stack = [(0, 0)]     # Stack of places to backtrack

    def perceive(self, percepts):
        print(f"\nAgent is at: {self.position}")
        print(f"Safe: {self.safe}")
        print(f"Visited: {self.visited}")
        print(f"Frontier: {self.frontier}")
        print(f"Neighbors: {self.get_neighbors(self.position)}")
        print(f"Path History: {self.path_history}")
        print(f"Backtrack Stack: {self.backtrack_stack}")

        self.visited.add(self.position)
        self.kb.update(self.position, percepts,self.visited)
        self.safe=self.kb.safe
        self.frontier = self.kb.frontier
        self.risky = self.kb.risky


        # x, y = self.position
        # neighbors = self.get_neighbors((x, y))

        # if "Breeze" not in percepts and "Stench" not in percepts:   #might be overlapping with previous logic
        #     for nx, ny in neighbors:
        #         self.safe.add((nx, ny))
        #         if (nx, ny) not in self.visited:
        #             self.frontier.add((nx, ny))
                    

    def get_neighbors(self, pos):
        x, y = pos
        return [(x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
                if 0 <= x+dx < self.grid_size and 0 <= y+dy < self.grid_size]

    def next_move(self):
        # Try safe, unvisited neighbors(frontier) first
        for frontier_cell in self.frontier:
            if frontier_cell in self.get_neighbors(self.position):
                print(f"Moving to safe frontier cell: {frontier_cell}")
                self.frontier.remove(frontier_cell)
                return frontier_cell
            
        if self.frontier:
            # If stuck: backtrack to previous position
            if len(self.backtrack_stack)>1:
                print(f"Backtracking from {self.position} to {self.backtrack_stack[-2]}")
                self.backtrack_stack.pop()
                back_pos = self.backtrack_stack.pop()
                return back_pos
        
        for risky_cell in self.risky:
            for neighbor in self.get_neighbors(risky_cell):
                if neighbor in self.path_history:
                    # Extract subpath from current position to that neighbor
                    try:
                        current_index = self.path_history.index(self.position)
                        target_index = self.path_history.index(neighbor)
                        if current_index < target_index:
                            subpath = self.path_history[current_index:target_index + 1]
                        else:
                            subpath = self.path_history[target_index:current_index + 1][::-1]
                        if len(subpath) > 1:
                            print(f"Navigating to {neighbor} to attempt risky cell {risky_cell}")
                            return subpath[1]  # Next step toward neighbor
                    except ValueError:
                        continue  # In case something's off
        return None

        
    def move_to(self, cell):
        self.position = cell
        self.path_history.append(cell)
        self.backtrack_stack.append(cell)

    def step(self, world):
        x, y = self.position
        # percepts = world.get_percepts(x, y)
        # self.perceive(percepts)

        

        next_pos = self.next_move()
        if next_pos:
            self.move_to(next_pos)
            world.agent_pos = self.position
        else:
            print("No valid moves available. Agent is stuck.")
            sys.exit(0)  # Exit if no moves are possible
