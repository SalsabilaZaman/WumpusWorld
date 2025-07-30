import sys
import random
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
        self.loop_history = []
        self.loop_window = 8
        self.loop_threshold = 3


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
        # if self.kb.wumpus:
        #     self.use_arrow()
        
        # Track position for loop detection
        self.loop_history.append(self.position)
        if len(self.loop_history) > self.loop_window:
            self.loop_history.pop(0)
                    

    def get_neighbors(self, pos):
        x, y = pos
        return [(x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
                if 0 <= x+dx < self.grid_size and 0 <= y+dy < self.grid_size]

    def is_in_loop(self):
        """Detect if agent is stuck in a local loop."""
        if len(self.loop_history) < self.loop_window:
            return False
        pos_counts = {}
        for pos in self.loop_history:
            pos_counts[pos] = pos_counts.get(pos, 0) + 1
        # If any position repeats more than threshold, consider it a loop
        return any(count >= self.loop_threshold for count in pos_counts.values())

    def next_move(self):
        # Try safe, unvisited neighbors(frontier) first
        for frontier_cell in self.frontier:
            if frontier_cell in self.get_neighbors(self.position):
                print(f"Moving to safe frontier cell: {frontier_cell}")
                self.frontier.remove(frontier_cell)
                return frontier_cell

        # If stuck: backtrack to previous position
        if self.frontier:
            if len(self.backtrack_stack) > 1:
                print(f"Backtracking from {self.position} to {self.backtrack_stack[-2]}")
                self.backtrack_stack.pop()
                back_pos = self.backtrack_stack.pop()
                return back_pos

        # If planned_path exists, follow it
        if len(self.planned_path) > 0:
            return self.planned_path.pop(0)

        # If in a loop, try a risky cell probabilistically
        if self.is_in_loop():
            print("Loop detected! Trying risky cell to escape.")
            # Find risky neighbors
            risky_neighbors = [cell for cell in self.get_neighbors(self.position) if cell in self.risky and cell not in self.visited]
            if risky_neighbors:
                chosen = random.choice(risky_neighbors)
                print(f"Probabilistically moving to risky cell: {chosen}")
                return chosen

        # Try risky cells as last resort (original logic)
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
            try:
                import pygame
                from gui import show_game_over_popup
                screen = pygame.display.get_surface()
                if screen is not None:
                    show_game_over_popup(screen, self.position, died=True)
                    pygame.time.wait(2000)
                else:
                    print("Game Over: Agent Died")
            except Exception as e:
                print(f"Game Over popup failed: {e}")
            raise SystemExit(0)
        next_pos = self.next_move()         
        if next_pos:
            self.move_to(next_pos)
            self.add_points(-1, reason=f"Moved to {next_pos}")
            world.agent_pos = self.position
        else:
            print("No valid moves available. Agent is stuck.")
            try:
                import pygame
                from gui import show_game_over_popup
                screen = pygame.display.get_surface()
                if screen is not None:
                    show_game_over_popup(screen, self.position, died=True)
                    pygame.time.wait(2000)
                else:
                    print("Game Over: Agent Stuck")
            except Exception as e:
                print(f"Game Over popup failed: {e}")
            raise SystemExit(0)
   
    def add_points(self, amount, reason=""):
        self.points += amount
        print(f"[Points] {reason}: {amount:+} → Total: {self.points}")


    def use_arow(self):
        if not self.arrow_used:
            self.arrow_used = True
            self.add_points(-10, reason="Used Arrow")
            self.last_action = "Used Arrow"
        else:
            print("Arrow already used.")
            self.last_action = "Tried to use arrow, but it was already used."

    def collect_gold(self):
        self.found_gold = True
        print("Gold collected!")

    def get_score(self):
        return self.points