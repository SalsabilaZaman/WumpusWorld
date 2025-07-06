class Agent:
    def __init__(self, world, kb):
        self.pos = (0, 0)
        self.kb = kb
        self.world = world

    def step(self):
        percepts = self.world.get_percepts(self.pos)
        self.kb.update(percepts)
        # Add logic to decide next move
        print(f"Agent at {self.pos} perceives: {percepts}")
