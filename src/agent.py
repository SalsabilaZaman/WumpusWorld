import sys
from inference import KnowledgeBase


class Agent:
    def __init__(self, grid_size=10):
        self.position = (0, 0)
        self.visited = set()
        self.safe = set([(0, 0)])   
        self.frontier = set()
        self.risky = list()  # Changed to list for ordered processing
        self.kb = KnowledgeBase(grid_size)
        self.grid_size = grid_size
        self.path_history = [(0, 0)]  # Complete trail, never popped
        self.backtrack_stack = [(0, 0)]     # Stack of places to backtrack
        self.planned_path = []  # Stores the full safe path to a risky neighbor
        self.found_gold = False
        self.points = 0
        self.arrow_used = False


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
        self.found_gold = self.kb.found_gold
        if self.found_gold:
            self.add_points(+1000, reason="Agent escaped with gold")
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
        if len(self.planned_path)>0:
            return self.planned_path.pop(0)  # Return next planned step if available
        for risky_cell in self.risky:
            for neighbor in self.get_neighbors(risky_cell):
                if neighbor in self.path_history:
                    try:
                        current_index = self.path_history.index(self.position)
                        target_index = self.path_history.index(neighbor)
                        if current_index < target_index:
                            self.planned_path = self.path_history[current_index + 1:target_index + 1]
                        else:
                            self.planned_path = self.path_history[target_index:current_index][::-1]
                        self.planned_path.append(risky_cell)
                        print(f"Planning path to risky cell via neighbor {neighbor}")
                        print(f"Planned path: {self.planned_path}")
                        return self.planned_path.pop(0) 
                    except ValueError:
                        continue        
        return None

        
    def move_to(self, cell):
        self.position = cell
        self.path_history.append(cell)
        self.backtrack_stack.append(cell)
        

    def step(self, world):
        x, y = self.position
        # percepts = world.get_percepts(x, y)
        # self.perceive(percepts)
        if world.is_danger(self.position):
            print(f"💀 Agent moved into danger at {self.position}! GAME OVER.")
            self.add_points(-1000, reason="Agent died")
            sys.exit(0)
             
        next_pos = self.next_move()         
        if next_pos:
            self.move_to(next_pos)
            self.add_points(-1, reason=f"Moved to {next_pos}")
            world.agent_pos = self.position
        else:
            print("No valid moves available. Agent is stuck.")
            sys.exit(0)  # Exit if no moves are possible
   
    def add_points(self, amount, reason=""):
        self.points += amount
        print(f"[Points] {reason}: {amount:+} → Total: {self.points}")


    def use_arrow(self):
        if not self.arrow_used:
            self.arrow_used = True
            self.add_points(-10, reason="Used Arrow")
        else:
            print("Arrow already used.")

    def collect_gold(self):
        self.found_gold = True
        print("Gold collected!")

    def get_score(self):
        return self.points